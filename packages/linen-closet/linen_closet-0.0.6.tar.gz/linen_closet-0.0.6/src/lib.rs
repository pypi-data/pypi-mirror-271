#![cfg(feature = "python")]

mod loader;

use pyo3::prelude::*;


#[pyfunction]
fn load_sheets(
    credentials_file: &str,
    output_filename: &str,
    max_download_concurrency: usize,
    configuration_filename: &str,
    existing_file: Option<String>,
    s3_configuration: Option<S3Configuration>,
) -> PyResult<()> {
    loader::load_sheets_sync(
        credentials_file,
        output_filename,
        max_download_concurrency,
        configuration_filename,
        existing_file,
        s3_configuration.map(|s3_configuration| loader::S3Configuration {
            url: s3_configuration.url,
            key: s3_configuration.key,
            secret: s3_configuration.secret,
            bucket_name: s3_configuration.bucket_name,
            region: s3_configuration.region,
        }),
    ).map_err(|err| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(err.to_string()))
}

#[derive(Clone)]
#[pyclass]
#[pyo3(name="S3Configuration")]
pub struct S3Configuration {
    #[pyo3(get, set)]
    pub url: String,
    #[pyo3(get, set)]
    pub key: String,
    #[pyo3(get, set)]
    pub secret: String,
    #[pyo3(get, set)]
    pub bucket_name: String,
    #[pyo3(get, set)]
    pub region: String,
}


#[pymethods]
impl S3Configuration {
    #[new]
    fn new(
        url: String,
        key: String,
        secret: String,
        bucket_name: String,
        region: String,
    ) -> Self {
        Self {
            url,
            key,
            secret,
            bucket_name,
            region,
        }
    }

    fn __repr__(slf: &PyCell<Self>) -> PyResult<String> {
        Ok(format!(
            "S3Configuration(url={}, key={}, secret={}, bucket_name={}, region={})",
            slf.borrow().url,
            slf.borrow().key,
            slf.borrow().secret,
            slf.borrow().bucket_name,
            slf.borrow().region,
        ))
    }
}

#[pymodule]
#[pyo3(name="linen_closet")]
fn b(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load_sheets, m)?)?;
    m.add_class::<S3Configuration>()?;
    Ok(())
}
