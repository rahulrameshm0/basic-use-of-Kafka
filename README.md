# Kafka Orders Demo

A minimal Kafka setup for learning event streaming. It runs a single-node Kafka broker in KRaft mode (no ZooKeeper), publishes fake orders to an `orders` topic, and consumes them in a separate process.

## Project Structure

```
.
├── docker-compose.yaml   # Single-node Kafka broker (KRaft)
├── producer.py           # Publishes one order message to the "orders" topic
└── tracker.py            # Consumer that listens to "orders" and prints them
```

## Requirements

- [Docker](https://docs.docker.com/get-docker/) (with Docker Compose)
- Python 3.8+
- Python packages:

  ```bash
  pip install confluent-kafka
  ```

## Getting Started

### 1. Start Kafka

```bash
docker compose up -d
```

Wait a few seconds for the broker to become ready. You can check the logs with:

```bash
docker compose logs -f kafka
```

Kafka is exposed on `localhost:9092`.

### 2. Start the consumer

In a terminal, run:

```bash
python tracker.py
```

You should see:

```
🟢 Consumer is running and subscribed to order topic
```

### 3. Produce a message

In another terminal, run:

```bash
python producer.py
```

The producer prints delivery details, and the consumer prints the received order:

```
✅ Delivered {"order_id": "...", "user": "James", "item": "Frozen Chicken", "quantity": 1}
✅ Delivered to orders: Partition 0: at offset 0

📦 Received order: 1 x Frozen Chicken from James
```

Stop the consumer with `Ctrl+C`.

## How It Works

### Broker (`docker-compose.yaml`)

- Uses the `confluentinc/cp-kafka:8.1.3` image.
- Runs a single node that acts as both **broker** and **controller** (`KAFKA_PROCESS_ROLES: broker,controller`), so no ZooKeeper is needed.
- Listens on port `9092` for clients and `9093` for the controller quorum.
- The topic `orders` is created automatically on first produce (default auto-topic creation).

### Producer (`producer.py`)

- Connects to `localhost:9092`.
- Builds an order with a random UUID, user, item, and quantity.
- Serializes it as JSON and publishes it to the `orders` topic.
- Uses a delivery callback to report success or failure, then calls `flush()` to ensure the message is sent before exiting.

### Consumer (`tracker.py`)

- Connects with consumer group `order-tracker`.
- Subscribes to the `orders` topic.
- `auto.offset.reset: earliest` means it reads from the beginning of the topic if no committed offset exists for the group.
- Polls continuously, deserializes each message from JSON, and prints it.
- Closes the consumer cleanly on `Ctrl+C`.

## Useful Commands

List topics:

```bash
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list
```

Read messages directly from the topic:

```bash
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic orders \
  --from-beginning
```

Stop and remove the broker (data is kept in the `kafka_kraft` volume):

```bash
docker compose down
```

Remove the broker including its data:

```bash
docker compose down -v
```

## Ideas to Extend

- Send multiple orders with a loop instead of a single message.
- Add message keys (e.g. `order_id`) to control partitioning.
- Use Avro or Protobuf with Schema Registry instead of raw JSON.
- Add a second consumer group to practice parallel consumption.
