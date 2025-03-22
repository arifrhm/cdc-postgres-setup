# PostgreSQL CDC (Change Data Capture) with Debezium

This project demonstrates the implementation of Change Data Capture (CDC) using PostgreSQL, Debezium, Apache Kafka, and a Python consumer.

## Prerequisites

- Docker and Docker Compose
- Python 3.x
- curl (for HTTP requests)
- pip (Python package manager)

## Project Structure

```
cdc-postgres-setup/
├── docker-compose.yml
├── connector.json
├── kafka_cdc_consumer.py
└── README.md
```

## Installation

1. Clone this repository:
```bash
git clone [<repository-url>](https://github.com/arifrhm/cdc-postgres-setup.git)
cd cdc-postgres-setup
```

2. Install Python dependencies:
```bash
pip install kafka-python
```

3. Start services using Docker Compose:
```bash
docker compose up -d
```

4. Verify all services are running:
```bash
docker compose ps
```

## CDC Configuration

1. Create customers table in PostgreSQL:
```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
```

2. Register Debezium connector:
```bash
curl -X POST -H "Content-Type: application/json" --data @connector.json http://localhost:8083/connectors
```

3. Run the Python consumer:
```bash
python kafka_cdc_consumer.py
```

## Usage

1. Access Kafka UI for monitoring:
```
http://localhost:8080
```

2. Example database operations for testing:
```sql
-- Insert data
INSERT INTO customers (name, email) VALUES ('Test User', 'test@example.com');

-- Update data
UPDATE customers SET email = 'new@example.com' WHERE id = 1;

-- Delete data
DELETE FROM customers WHERE id = 1;
```

## Ports Used

- PostgreSQL: 5432
- Kafka: 9092
- Zookeeper: 2181
- Kafka Connect: 8083
- Kafka UI: 8080

## Monitoring and Troubleshooting

### Check Connector Status
```bash
curl -X GET http://localhost:8083/connectors/inventory-connector/status
```

### View Logs
```bash
# All services
docker compose logs -f

# Service specific
docker compose logs connect
docker compose logs kafka
docker compose logs postgres
```

### Delete Connector
```bash
curl -X DELETE http://localhost:8083/connectors/inventory-connector
```

## Stopping Services

```bash
docker compose down
```

To remove data volumes:
```bash
docker compose down -v
```

## Core Components

- **PostgreSQL**: Source database with logical replication enabled
- **Apache Kafka**: Message broker for stream processing
- **Debezium**: CDC platform that captures database changes
- **Kafka Connect**: Framework for connecting Kafka with external systems
- **Kafka UI**: Web UI for monitoring Kafka cluster
- **Python Consumer**: Script to process CDC events

## Note for M1/M2 Mac Users

If you're using a Mac with Apple Silicon (M1/M2), ensure you use the appropriate platform configuration in `docker-compose.yml`:

```yaml
platform: linux/arm64  # For ARM64 supported services
platform: linux/amd64  # For services requiring emulation
```

## Common Troubleshooting

1. **Connector Error**: Check connector logs and status
2. **Consumer Not Receiving Events**: Verify Kafka topics and consumer configuration
3. **Database Connection Issues**: Verify credentials and database accessibility

## References

- [Debezium Documentation](https://debezium.io/documentation/)
- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
