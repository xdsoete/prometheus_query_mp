FROM rust:1.74 AS builder

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y protobuf-compiler && rm -rf /var/lib/apt/lists/*

RUN rustup default nightly
RUN cargo build --release

FROM ubuntu:22.04

RUN apt-get update && apt-get install -y libssl3 ca-certificates && apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /app/target/release/prom_query /app/prom_query

ENTRYPOINT ["/app/prom_query"]
