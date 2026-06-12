from confluent_kafka import Producer
import uuid
import json
producer_config = {
    'bootstrap.servers': 'localhost:9092'
}
producer = Producer(producer_config)

def delivery_report(err, msg):
    if err:
        print(f"❌ Delivery Failed: {err}")
    else:
        print(f"✅ Delivered {msg.value().decode('utf-8')}")
        print(f"✅ Delivered to {msg.topic()}: Partition {msg.partition()}: at offset {msg.offset()}")

order = {
    "order_id": str(uuid.uuid4()),
    "user":"James",
    "item":"Frozen Chicken",
    "quantity": 1
}


value = json.dumps(order).encode("utf-8")
producer.produce(topic="orders",
                 value=value,
                 callback=delivery_report
                 )

producer.flush()



