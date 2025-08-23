use tonic::{Request, Response, Status, Streaming};
use tonic::transport::Server;

use tokio::sync::{mpsc, Semaphore};
use tokio::time::{sleep, Duration};

use futures::stream::StreamExt;

use std::any::Any;
use std::f64;
use std::sync::Arc;
use std::time::UNIX_EPOCH;
use std::time::SystemTime;

use log::{info, error};
use reqwest::Client;
use serde_json::Value;

// PROMETHEUS
const PROMETHEUS_URL: &str = "http://prometheus-operated.default.svc.cluster.local:9090";

// VICTORIA
// const PROMETHEUS_URL: &str = "http://vmsingle-vmks-victoria-metrics-k8s-stack.default.svc.cluster.local:8428";
const INTERVAL: u64 = 10;

pub mod prom_query_proto {
    tonic::include_proto!("prom_query");
}

use prom_query_proto::{MonitoringRequest, MonitoringResponse};
use prom_query_proto::prom_query_server::{PromQuery, PromQueryServer};


#[derive(Debug, Default)]
pub struct PromQueryService {}


async fn query_prometheus(query: &str) -> Result<Value, reqwest::Error> {
    let client = Client::builder().build()?;
    let url = format!("{}/api/v1/query", PROMETHEUS_URL);

    let response = client.get(&url)
        .query(&[("query", query)])
        .send()
        .await?
        .json::<Value>()
        .await?;

    Ok(response["data"]["result"].clone())
}

fn get_value_for_instance(data: &[Value], target_instance: &str) -> Option<f64> {
    data.iter()
        .find(|obj| obj["metric"]["pod"] == target_instance)
        .and_then(|obj| obj["value"][1].as_str())
        .and_then(|s| s.parse::<f64>().ok())
}

#[tonic::async_trait]
impl PromQuery for PromQueryService {
    type PromQueryStream = tokio_stream::wrappers::ReceiverStream<Result<MonitoringResponse, Status>>;

    async fn prom_query(&self, request: Request<Streaming<MonitoringRequest>>) -> Result<Response<Self::PromQueryStream>, Status> {
        error!("started");
        error!("{:?}", SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_millis());

        let mut stream = request.into_inner();
        let (tx, rx) = mpsc::channel(10);

        let semaphore = Arc::new(Semaphore::new(100));

        tokio::spawn(async move {
            while let Some(req) = stream.next().await {
                let permit = match semaphore.clone().acquire_owned().await {
                    Ok(p) => p,
                    Err(_) => {
                        error!("Semaphore acquisition failed");
                        continue;
                    }
                };

                match req {
                    Ok(req) => {
                        let request_id = req.request_id.clone();
                        let query = req.query.clone();
                        let instance = req.instance.clone();
                        let threshold: f64 = req.threshold.clone().into();

                        let tx: mpsc::Sender<Result<MonitoringResponse, Status>> = tx.clone();

                        tokio::spawn(async move {
                            let _permit = permit;

                            let mut i = 0;
                            loop {
                                error!("iteration {}", i);
                                error!("{:?}", SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_millis());
                                i += 1;

                                match query_prometheus(&query).await {
                                    Ok(cpu_usage) => {
                                        error!("CPU Usage {:#?} {:?}", cpu_usage, cpu_usage.type_id());
                                        error!("instance: {}", instance);
                                        error!("{:?}", SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_millis());

                                        let value = match get_value_for_instance(cpu_usage.as_array().unwrap(), &instance) {
                                            Some(x) => {
                                                error!("x = {}", x);
                                                x
                                            },
                                            None => {
                                                error!("None");
                                                0 as f64
                                            },
                                        };

                                        if value > threshold {
                                            error!("{} is higher than {}", value, threshold);
                                            error!("{:?}", SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_millis());
                                            let _ = tx.send(Ok(MonitoringResponse {
                                                request_id: request_id.clone(),
                                                value: value.clone() as i32,
                                            })).await;
                                            break;
                                        }
                                    }
                                    Err(e) => error!("Error: {}", e),
                                }

                                sleep(Duration::from_millis(INTERVAL)).await;
                            }
                        });
                    }
                    Err(_) => break,
                }
            }
        });

       Ok(Response::new(tokio_stream::wrappers::ReceiverStream::new(rx)))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    env_logger::init();

    let addr = "[::]:50051".parse()?;
    let prom_query_service = PromQueryService::default();

    Server::builder()
        .add_service(PromQueryServer::new(prom_query_service))
        .serve(addr)
        .await?;

    Ok(())
}
