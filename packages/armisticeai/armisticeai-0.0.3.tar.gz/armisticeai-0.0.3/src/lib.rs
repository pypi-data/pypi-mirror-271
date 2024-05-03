use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine};
use janus_messages::{codec::Decode, Duration, TaskId};
use prio::vdaf::prio3::Prio3;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use serde::{de::Visitor, Deserialize, Serialize};
use serde_json::json;
use std::env;
use std::io::Cursor;
use std::{fmt::Display, marker::PhantomData, str::FromStr};
use url::Url;

static CLIENT_USER_AGENT: &str = concat!(
    env!("CARGO_PKG_NAME"),
    "/",
    env!("CARGO_PKG_VERSION"),
    "/",
    "client"
);

/// Helper type to serialize/deserialize a large number as a string.
#[derive(Debug, Clone)]
pub struct NumberAsString<T>(pub T);

impl<T> Serialize for NumberAsString<T>
where
    T: Display,
{
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        serializer.serialize_str(&self.0.to_string())
    }
}

impl<'de, T> Deserialize<'de> for NumberAsString<T>
where
    T: FromStr,
    <T as FromStr>::Err: Display,
{
    fn deserialize<D>(deserializer: D) -> Result<NumberAsString<T>, D::Error>
    where
        D: serde::Deserializer<'de>,
    {
        deserializer.deserialize_str(NumberAsStringVisitor::new())
    }
}

struct NumberAsStringVisitor<T>(PhantomData<T>);

impl<T> NumberAsStringVisitor<T> {
    fn new() -> NumberAsStringVisitor<T> {
        NumberAsStringVisitor(PhantomData)
    }
}

impl<'de, T> Visitor<'de> for NumberAsStringVisitor<T>
where
    T: FromStr,
    <T as FromStr>::Err: Display,
{
    type Value = NumberAsString<T>;

    fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result {
        formatter.write_str("a string with a number in base 10")
    }

    fn visit_str<E>(self, value: &str) -> Result<NumberAsString<T>, E>
    where
        E: serde::de::Error,
    {
        let number = value
            .parse()
            .map_err(|err| E::custom(format!("string could not be parsed into number: {err}")))?;
        Ok(NumberAsString(number))
    }
}

/// Parse a vector measurement from its intermediate JSON representation.
fn parse_vector_measurement<T>(value: serde_json::Value) -> anyhow::Result<Vec<T>>
where
    T: FromStr,
    T::Err: Display,
{
    Ok(
        serde_json::value::from_value::<Vec<NumberAsString<T>>>(value)?
            .into_iter()
            .map(|elem| elem.0)
            .collect(),
    )
}

#[pyclass]
struct UploadRequest {
    task_id: TaskId,
    leader_url: Url,
    helper_url: Url,
    time_precision: Duration,
    bits: usize,
    length: usize,
    chunk_length: usize,
    measurement: Vec<u128>,
}

fn tokio() -> &'static tokio::runtime::Runtime {
    use std::sync::OnceLock;
    static RT: OnceLock<tokio::runtime::Runtime> = OnceLock::new();
    RT.get_or_init(|| tokio::runtime::Runtime::new().unwrap())
}

#[pymethods]
impl UploadRequest {
    #[new]
    fn new(task_config: &PyDict, measurement: Vec<String>) -> Self {
        let json_measurement = json!(measurement);
        let parsed_measurement =
            parse_vector_measurement::<u128>(json_measurement.clone()).unwrap();
        let bits = task_config.get_item("bits").unwrap().unwrap();
        let length = task_config.get_item("length").unwrap().unwrap();
        let chunk_length = task_config.get_item("chunk_length").unwrap().unwrap();
        let task_id_str = task_config.get_item("task_id").unwrap().unwrap();
        let task_id_bytes = URL_SAFE_NO_PAD
            .decode(task_id_str.extract::<String>().unwrap())
            .unwrap();
        let mut cursor = Cursor::new(task_id_bytes.as_slice());
        let task_id = TaskId::decode(&mut cursor).unwrap();
        let time_precision_raw = task_config.get_item("time_precision").unwrap().unwrap();
        let time_precision = Duration::from_seconds(time_precision_raw.extract::<u64>().unwrap());
        let leader = task_config.get_item("leader").unwrap().unwrap();
        let leader_url = Url::parse(&leader.extract::<String>().unwrap()).unwrap();
        let helper = task_config.get_item("helper").unwrap().unwrap();
        let helper_url = Url::parse(&helper.extract::<String>().unwrap()).unwrap();
        UploadRequest {
            task_id: task_id,
            leader_url: leader_url,
            helper_url: helper_url,
            time_precision: time_precision,
            bits: bits.extract::<usize>().unwrap(),
            length: length.extract::<usize>().unwrap(),
            chunk_length: chunk_length.extract::<usize>().unwrap(),
            measurement: parsed_measurement,
        }
    }

    fn run(&self, py: Python) -> PyResult<()> {
        py.allow_threads(|| {
            let app = {
                let vdaf =
                    Prio3::new_sum_vec_multithreaded(2, self.bits, self.length, self.chunk_length)
                        .unwrap();
                let http_client = reqwest::Client::builder()
                    .user_agent(CLIENT_USER_AGENT)
                    .build()
                    .unwrap();
                let client = janus_client::Client::builder(
                    self.task_id,
                    self.leader_url.clone(),
                    self.helper_url.clone(),
                    self.time_precision,
                    vdaf,
                )
                .with_http_client(http_client.clone());
                client
            };
            let rt = tokio();
            let _ = rt.block_on(async {
                let client = app.build().await.unwrap();
                println!("started upload");
                client.upload(&self.measurement).await.unwrap()
            });
            println!("done uploading");
            Ok(())
        })
    }
}

#[pymodule]
fn armisticeai(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<UploadRequest>()?;
    Ok(())
}
