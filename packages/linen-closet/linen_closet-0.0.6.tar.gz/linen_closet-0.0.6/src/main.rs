mod loader;

use anyhow::Result;
use clap::Parser;
use crate::loader::WorkbookArchiveFile;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Output file name
    #[arg(short, long, default_value = "workbooks.json")]
    output_filename: String,

    /// Max download concurrency
    #[arg(short, long, default_value = "50")]
    max_download_concurrency: usize,

    /// Sheet configuration
    #[arg(short, long, default_value = "sheets.yaml")]
    sheet_configuration: String,

    /// Credentials file path
    #[arg(short, long, default_value = "credentials.json")]
    credentials_file_path: String,

    /// Existing file to read from
    #[arg(short, long)]
    existing_file: Option<String>,
}


#[tokio::main]
async fn main() -> Result<()> {

    let args = Args::parse();

    let credentials_file_path = std::env::var("GOOGLE_APPLICATION_CREDENTIALS").unwrap_or(args.credentials_file_path);

    let output_filename = std::env::var("OUTPUT_FILENAME").unwrap_or(args.output_filename);
    let output_filename = if output_filename.starts_with("s3://") {
        WorkbookArchiveFile::Remote(output_filename.replace("s3://", ""))
    } else {
        WorkbookArchiveFile::Local(output_filename)
    };

    let max_download_concurrency = match std::env::var("MAX_DOWNLOAD_CONCURRENCY") {
        Ok(max_download_concurrency) => max_download_concurrency.parse::<usize>().unwrap(),
        Err(_) => args.max_download_concurrency,
    };

    let sheet_configuration = std::env::var("SHEET_CONFIGURATION").unwrap_or(args.sheet_configuration);

    let existing_file: Option<WorkbookArchiveFile> = match std::env::var("EXISTING_FILE") {
        Ok(existing_file) => Some(existing_file),
        Err(_) => args.existing_file,
    }.map(|existing_file| if existing_file.starts_with("s3://") {
        WorkbookArchiveFile::Remote(existing_file.replace("s3://", ""))
    } else {
        WorkbookArchiveFile::Local(existing_file)
    });

    let s3_configuration = if std::env::var("S3_URL").is_ok() {
        Some(loader::S3Configuration {
            url: std::env::var("S3_URL").unwrap(),
            key: std::env::var("S3_KEY").unwrap(),
            secret: std::env::var("S3_SECRET").unwrap(),
            bucket_name: std::env::var("S3_BUCKET_NAME").unwrap(),
            region: std::env::var("S3_REGION").unwrap(),
        })
    } else {
        None
    };

    loader::download_all_sheets(
        credentials_file_path.as_str(),
        output_filename,
        max_download_concurrency,
        sheet_configuration.as_str(),
        existing_file,
        s3_configuration,
    ).await
}