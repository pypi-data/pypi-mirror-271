extern crate hyper;
extern crate hyper_rustls;
extern crate google_sheets4 as sheets4;
extern crate google_drive3 as drive3;

use hyper::client::HttpConnector;
use hyper_rustls::HttpsConnector;
use futures::{stream, StreamExt};
use futures_retry::{RetryPolicy, StreamRetryExt};


use std::fs::File;
use std::io::Cursor;
use anyhow::{Context, Error, Result};
use aws_sdk_s3::config::Region;
use aws_sdk_s3::primitives::ByteStream;
use backoff::ExponentialBackoff;
use calamine::{DataType, open_workbook_from_rs, Reader, Xlsx};
use chrono::{DateTime, Duration, NaiveDate, Utc};
use drive3::{DriveHub, oauth2};
use sheets4::oauth2::read_service_account_key;

use serde::{Serialize, Deserialize};
use time_humanize::{Accuracy, HumanTime, Tense};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Sheet {
    pub name: String,
    pub values: Vec<Vec<String>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Workbook {
    pub id: String,
    pub name: String,
    pub sheets: Vec<Sheet>,
    pub kind: String,
    pub last_modified: Option<DateTime<Utc>>,
}

impl Workbook {
    pub fn new(id: String, name: String, sheets: Vec<Sheet>, kind: String, last_modified: Option<DateTime<Utc>>) -> Self {
        Self {
            id,
            name,
            sheets,
            kind,
            last_modified,
        }
    }
}

async fn list_all_sheets_in_folder(hub: &DriveHub<HttpsConnector<HttpConnector>>, drive_folder_id: &str) -> Result<Vec<(String, String)>> {

    let mut next_page_token: Option<String>= None;
    let mut sheet_ids = vec![];

    loop {
        if let Some(page_token) = next_page_token {
            let (_, file_listing) = hub
                .files()
                .list()
                .q(&format!("'{}' in parents", drive_folder_id))
                .supports_all_drives(true)
                .include_items_from_all_drives(true)
                .page_size(1000)
                .page_token(page_token.as_str())
                .doit()
                .await?;
            
            let resp_next_page_token = file_listing.next_page_token;
            if let Some(tok) = resp_next_page_token {
                next_page_token = Some(tok);
            } else {
                next_page_token = None;
            }

            let f = file_listing.files.ok_or(Error::msg("no files found"))?;
            let current_sheet_ids = f.into_iter().filter_map(|file| {
                if file.mime_type == Some("application/vnd.google-apps.spreadsheet".to_string()) {
                    Some((file.id.unwrap(), file.name.unwrap()))
                } else {
                    None
                }
            }).collect::<Vec<(String, String)>>();

            sheet_ids.extend(current_sheet_ids);
        } else {
            let (_, file_listing) = hub
                .files()
                .list()
                .q(&format!("'{}' in parents", drive_folder_id))
                .supports_all_drives(true)
                .include_items_from_all_drives(true)
                .page_size(1000)
                .doit()
                .await?;

            let resp_next_page_token = file_listing.next_page_token;
            if let Some(tok) = resp_next_page_token {
                next_page_token = Some(tok);
            } else {
                next_page_token = None;
            }

            let f = file_listing.files.ok_or(Error::msg("no files found"))?;
            let current_sheet_ids = f.into_iter().filter_map(|file| {
                if file.mime_type == Some("application/vnd.google-apps.spreadsheet".to_string()) {
                    Some((file.id.unwrap(), file.name.unwrap()))
                } else {
                    None
                }
            }).collect::<Vec<(String, String)>>();

            sheet_ids.extend(current_sheet_ids);
        }

        if next_page_token.is_none() {
            break;
        }
    }
    Ok(sheet_ids)
}

fn from_days_since_1900(days_since_1900: i64) -> NaiveDate {
    // Excel uses 1900-01-01 as day 1. Excel has a well-known bug where it treats 1900 as a leap year even though it is not.
    // https://docs.microsoft.com/en-us/office/troubleshoot/excel/wrongly-assumes-1900-is-leap-year
    let d1900 = NaiveDate::from_ymd_opt(1900, 1, 1).unwrap();
    // I'm assuming that the offset is 2 because of the leap year bug.
    d1900 + Duration::days(days_since_1900 - 2)
}

pub async fn get_sheet_via_export(drive_hub: &DriveHub<HttpsConnector<HttpConnector>>, item: ExportItem, existing_workbook_last_modified: Option<DateTime<Utc>>) -> Result<Option<Workbook>> {
    let workbook_id = item.workbook_id;
    let workbook_name = item.workbook_name;
    let resp = drive_hub.clone().files().export(workbook_id.as_str(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet").doit().await?;
    let data = Cursor::new(hyper::body::to_bytes(resp.into_body()).await?);

    let file_metadata = drive_hub.files().get(workbook_id.as_str()).supports_all_drives(true).param("fields", "id,name,modifiedTime").doit().await.map_err(|e| {
        Error::msg(format!("error getting file metadata: {:?}", e))
    })?.1;
    if let Some(current_last_modified) = file_metadata.modified_time {
        if let Some(existing_last_modified) = existing_workbook_last_modified {
            if current_last_modified <= existing_last_modified {
                let duration: std::time::Duration = (Utc::now() - current_last_modified).to_std().context("error converting to std::time::Duration")?;
                println!("Skipping {} -- no changes since {}", workbook_id, HumanTime::from(duration).to_text_en(Accuracy::Rough, Tense::Past));
                return Ok(None);
            }
        }
    }
    let last_modified = file_metadata.modified_time.map(|last_modified| Utc::now() - last_modified).map(|duration| HumanTime::from(duration.to_std().unwrap()).to_text_en(Accuracy::Rough, Tense::Past).to_string()).unwrap_or("".to_string());
    println!("Downloading {}({}) -- last modified: {:?} ({})", workbook_id, file_metadata.name.context("failed to access file metadata").unwrap(), file_metadata.modified_time, last_modified);

    let mut workbook: Xlsx<_> = open_workbook_from_rs(data).unwrap();
    let sheet_names = match item.sheet_names {
        Some(sheet_names) => sheet_names.iter().map(|sheet_name| sheet_name.to_string()).collect::<Vec<String>>(),
        None => workbook.sheet_names().to_vec(),
    };
    let sheets = sheet_names.iter().map(|sheet_name| {
        let s = workbook.worksheet_range(sheet_name).ok_or_else(|| Error::msg("no sheet"))??;
        let rows = s.rows().enumerate().map(|(_row_index, row)| {
            row.iter().enumerate().map(|(_cell_index, cell)| match cell {
                DataType::DateTimeIso(dt) => {
                    dt.to_string()
                },
                DataType::DateTime(dt) => {
                    // TODO: Given some kind of library-friendly logging mechanism, log this as a warning
                    from_days_since_1900(*dt as i64).format("%Y-%m-%d").to_string()
                },
                _ => cell.to_string(),
            }).collect::<Vec<String>>()
        }).collect::<Vec<Vec<String>>>();

        Ok(Sheet {
            name: sheet_name.to_string(),
            values: rows,
        })
    }).collect::<Result<Vec<Sheet>>>()?;
    Ok(Some(Workbook::new(workbook_id.to_string(), workbook_name.unwrap_or("".to_string()), sheets, item.kind, file_metadata.modified_time)))
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExportItem {
    pub workbook_id: String,
    pub workbook_name: Option<String>,
    pub sheet_names: Option<Vec<String>>,
    pub kind: String,
}


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DriveFolder {
    pub folder_id: String,
    pub kind: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SheetsConfiguration {
    pub sheets: Option<Vec<ExportItem>>,
    pub drive_folders: Option<Vec<DriveFolder>>,
}

impl ExportItem {
    pub fn new<T>(workbook_id: T, workbook_name: Option<T>, sheet_names: Option<Vec<T>>, kind: T) -> Self where T: Into<String> {
        Self {
            workbook_id: workbook_id.into(),
            workbook_name: workbook_name.map(|workbook_name| workbook_name.into()),
            sheet_names: sheet_names.map(|sheet_names| sheet_names.into_iter().map(|sheet_name| sheet_name.into()).collect::<Vec<String>>()),
            kind: kind.into(),
        }
    }
}

fn handle_get_sheet_error(err: Error) -> RetryPolicy<Error> {
    println!("[retry handler]: encountered error: {:?} -- retrying", err);
    RetryPolicy::WaitRetry(std::time::Duration::from_secs(5))
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct S3Configuration {
    pub url: String,
    pub key: String,
    pub secret: String,
    pub bucket_name: String,
    pub region: String,
}

fn get_s3_client(s3_configuration: S3Configuration) -> (aws_sdk_s3::Client, String) {
    let credentials_provider = aws_sdk_s3::config::Credentials::new(s3_configuration.key, s3_configuration.secret, None, None, "");
    let cfg = aws_sdk_s3::config::Config::builder()
        .credentials_provider(credentials_provider)
        .endpoint_url(s3_configuration.url)
        .region(Region::new(s3_configuration.region))
        .behavior_version_latest()
        .build();
    (aws_sdk_s3::Client::from_conf(cfg), s3_configuration.bucket_name)
}

async fn read_existing_file(s3_configuration: Option<S3Configuration>, archive_location: WorkbookArchiveFile) -> Result<Vec<Workbook>> {
    match archive_location {
        WorkbookArchiveFile::Local(existing_file) => {
            let file = File::open(existing_file)?;
            let workbooks: Vec<Workbook> = serde_json::from_reader(file)?;
            Ok(workbooks)
        },
        WorkbookArchiveFile::Remote(existing_file) => {
            let s3cfg = s3_configuration.context("s3 configuration required for remote file")?;
            let (s3, bucket_name) = get_s3_client(s3cfg);
            let obj = s3
                .get_object()
                .bucket(bucket_name)
                .key(existing_file)
                .send()
                .await?;

            let workbooks: Vec<Workbook> = serde_json::from_slice(obj.body.collect().await?.to_vec().as_slice())?;
            Ok(workbooks)
        },
    }
}

async fn upload_file_to_s3(s3_configuration: S3Configuration, filename: &str, body: ByteStream) -> Result<()> {
    let (s3, bucket_name) = get_s3_client(s3_configuration);
    println!("Uploading {} to s3://{} within bucket {}", filename, filename, bucket_name);
    let _ = s3
        .put_object()
        .bucket(bucket_name)
        .key(filename)
        .body(body)
        .send()
        .await?;

    Ok(())
}

pub enum WorkbookArchiveFile {
    Local(String),
    Remote(String),
}

pub async fn download_all_sheets(credentials_file_path: &str, output_file: WorkbookArchiveFile, max_download_concurrency: usize, configuration_filename: &str, existing_file: Option<WorkbookArchiveFile>, s3_configuration: Option<S3Configuration>) -> Result<()> {
    let service_account_key = read_service_account_key(credentials_file_path).await.context("failed to read service account key")?;
    let auth = oauth2::ServiceAccountAuthenticator::builder(service_account_key)
        .build()
        .await
        .context("failed to create authenticator")?;

    let drive_hub = DriveHub::new(hyper::Client::builder().build(hyper_rustls::HttpsConnectorBuilder::new().with_native_roots().https_or_http().enable_http2().build()), auth.clone());

    let sheets_configuration_contents = File::open(configuration_filename)?;
    let sheets_configuration: SheetsConfiguration = serde_yaml::from_reader(sheets_configuration_contents)?;

    let mut all_sheet_ids: Vec<ExportItem> = sheets_configuration.sheets.map(|sheets| sheets.into_iter().collect::<Vec<ExportItem>>()).unwrap_or_default().iter().map(|workbook: &ExportItem| {
        let workbook = workbook.clone();
        ExportItem::new(workbook.workbook_id, workbook.workbook_name, workbook.sheet_names, workbook.kind)
    }).collect::<Vec<ExportItem>>();

    for drive_folder in sheets_configuration.drive_folders.map(|drive_folders| drive_folders.into_iter().collect::<Vec<DriveFolder>>()).unwrap_or_default() {
        let cloned_drive_folder = drive_folder.clone();
        let cloned_drive_hub = drive_hub.clone();
        let folder_id = cloned_drive_folder.folder_id.clone();
        let sheet_list = list_all_sheets_in_folder(&cloned_drive_hub, folder_id.clone().as_str()).await?;
        let folder_kind = cloned_drive_folder.kind.clone();
        sheet_list.iter().for_each(|(workbook_id, sheet_name)| {
            all_sheet_ids.push(ExportItem::new(workbook_id.clone(), Some(sheet_name.clone()), None, folder_kind.clone()));
        });
    }

    let mut existing_workbooks = std::collections::BTreeMap::new();
    if let Some(existing_file) = existing_file {
        read_existing_file(s3_configuration.clone(), existing_file).await?.iter().for_each(|workbook| {
            let workbook_id = workbook.id.clone();
            existing_workbooks.insert(workbook_id, workbook.clone());
        });
    }

    let workbooks = stream::iter(all_sheet_ids.iter().map(|item| {
        let cloned_drive_hub = drive_hub.clone();
        let existing_workbook = existing_workbooks.get(&item.workbook_id);
        async move {
            backoff::future::retry(ExponentialBackoff::default(), || async {
                let existing_wb = existing_workbook.cloned();
                let last_modified = match existing_wb.clone() {
                    Some(existing_wb) => existing_wb.last_modified,
                    None => None,
                };
                let export_result = get_sheet_via_export(&cloned_drive_hub, item.clone(), last_modified).await.map_err(|e| {
                    println!("Encountered transient error for ({}): {:?} -- retrying in 5 seconds", item.workbook_id, e);
                    backoff::Error::Transient {
                        err: e,
                        retry_after: Some(core::time::Duration::from_secs(5)),
                    }
                });
                match export_result {
                    Ok(Some(wb)) => Ok(wb),
                    Ok(None) => Ok(existing_wb.context("no existing workbook found").unwrap().clone()),
                    Err(e) => Err(e),
                }
            }).await
        }
    })).buffer_unordered(max_download_concurrency).retry(handle_get_sheet_error).filter_map(|result| async move {
        match result {
            Ok((workbook, _)) => Some(workbook),
            Err(e) => {
                println!("error downloading sheet: {:?}", e);
                None
            }
        }
    }).collect::<Vec<Workbook>>().await;

    if workbooks.is_empty() {
        return Err(Error::msg("no workbooks downloaded"));
    }
    if workbooks.len() != all_sheet_ids.len() {
        return Err(Error::msg("not all workbooks downloaded"));
    }

    match output_file {
        WorkbookArchiveFile::Local(output_filename) => {
            let mut file = File::create(output_filename)?;
            serde_json::to_writer_pretty(&mut file, &workbooks)?;
        },
        WorkbookArchiveFile::Remote(output_filename) => {
            let s3_configuration = s3_configuration.context("s3 configuration required for remote file")?;
            let body = ByteStream::from(serde_json::to_vec_pretty(&workbooks)?);
            upload_file_to_s3(s3_configuration, output_filename.as_str(), body).await?;
        },
    }

    Ok(())
}

// not dead! this is actually consumed by Maturin/PyO3
#[allow(dead_code)]
pub (crate) fn load_sheets_sync(
    credentials_file_path: &str,
    output_filename: &str,
    max_download_concurrency: usize,
    configuration_filename: &str,
    existing_file: Option<String>,
    s3_configuration: Option<S3Configuration>,
) -> Result<()> {
    let runtime = tokio::runtime::Runtime::new().context("failed to create tokio runtime")?;
    let output_filename = if output_filename.starts_with("s3://") {
        WorkbookArchiveFile::Remote(output_filename.replace("s3://", ""))
    } else {
        WorkbookArchiveFile::Local(output_filename.to_string())
    };
    let existing_file = existing_file.map(|existing_file| if existing_file.starts_with("s3://") {
        WorkbookArchiveFile::Remote(existing_file.replace("s3://", ""))
    } else {
        WorkbookArchiveFile::Local(existing_file)
    });
    runtime.block_on(download_all_sheets(credentials_file_path, output_filename, max_download_concurrency, configuration_filename, existing_file, s3_configuration))
}
