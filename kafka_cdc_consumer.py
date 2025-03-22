from kafka import KafkaConsumer
import json
from datetime import datetime

def process_cdc_event(event):
    """Process a CDC event from Debezium."""
    operation = None
    if 'op' in event:
        if event['op'] == 'c':
            operation = 'CREATE'
        elif event['op'] == 'u':
            operation = 'UPDATE'
        elif event['op'] == 'd':
            operation = 'DELETE'
    
    table = event.get('source', {}).get('table')
    timestamp = event.get('source', {}).get('ts_ms')
    if timestamp:
        timestamp = datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
    
    data = None
    if 'after' in event:
        data = event['after']
    elif 'before' in event:  # For deletes
        data = event['before']
    
    print(f"Operation: {operation}, Table: {table}, Timestamp: {timestamp}")
    print(f"Data: {json.dumps(data, indent=2)}")
    print("-" * 50)
    
    # Here you can add your custom logic to process the CDC event
    # Examples:
    # - Forward to another system
    # - Update a data warehouse
    # - Trigger business logic
    # - etc.

def main():
    # Configure the Kafka consumer
    consumer = KafkaConsumer(
        'dbserver1.public.customers',  # Topic name follows pattern: <server>.<schema>.<table>
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='cdc-consumer-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        key_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None
    )
    
    print("CDC Consumer started. Waiting for messages...")
    
    # Process messages
    for message in consumer:
        try:
            process_cdc_event(message.value)
        except Exception as e:
            print(f"Error processing message: {e}")

if __name__ == "__main__":
    main()
