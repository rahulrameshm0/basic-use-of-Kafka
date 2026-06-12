# Kafka Order Tracker

A simple Kafka project built with Python using a Producer and Consumer.

## Features

* Kafka broker running with Docker Compose
* Producer sends order messages to Kafka
* Consumer receives and tracks order messages
* JSON-based message format

## Project Structure

```text
.
├── docker-compose.yaml
├── producer.py
├── tracker.py
└── README.md
```

## Requirements

* Python 3.x
* Docker
* confluent-kafka

## Installation

Install the Kafka client:

```bash
pip install confluent-kafka
```

Start Kafka:

```bash
docker compose up -d
```

## Running the Consumer

```bash
python tracker.py
```

## Running the Producer

```bash
python producer.py
```

## Example Output

Consumer:

```text
🟢 Consumer is running and subscribed to order topic
📦 Received order: 1 x Frozen Chicken from James
```

Producer:

```text
✅ Delivered message successfully
```

## Technologies Used

* Python
* Apache Kafka
* Docker Compose
