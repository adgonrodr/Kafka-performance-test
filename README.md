# Kafka Performance Test

This project is designed to test Kafka performance by generating dummy datasets and sending them to Kafka using Avro serialization.

## Project Structure

```
kafka-performance-test/
│
├── kafka_performance_test/                # Main project directory containing the scripts for generating data and sending to Kafka
│   ├── common/                            # Common directory containing shared resources like Avro schemas
│   │   └── schemas/                       # Folder containing Avro schemas used for Kafka key and value serialization
│   │       ├── kafka_key_schema.avsc      # Avro key schema for Kafka messages
│   │       └── kafka_value_schema.avsc    # Avro value schema for Kafka messages
│   │
│   ├── data_generator/                    # Directory containing the script to generate dummy datasets
│   │   └── dummy_data_generator.py        # Python script to generate dummy datasets based on the Avro schema
│   │
│   └── kafka_producer/                    # Directory containing the script to send datasets to Kafka
│       └── kafka_producer.py              # Python script to send the generated datasets to Kafka using Avro serialization
│
├── README.md                              # Project documentation with instructions on generating datasets, sending to Kafka, and deploying the Kafka cluster
└── requirements.txt                       # Python project dependencies for dataset generation and Kafka integration
```

## Requirements
The Python libraries listed in `requirements.txt` are required for both [generating dummy datasets](#generate-dummy-datasets) and [sending datasets to Kafka](#send-datasets-to-kafka). You can install them using:

```bash
pip install -r requirements.txt
```

However, the [deploy the Confluent Kafka cluster](#deploy-confluent-kafka-cluster) does not need these Python dependencies. You only need Docker installed. The Kafka cluster can be deployed using Docker Compose, as detailed in the Deploy Confluent Kafka cluster section.

## Deploy Confluent Kafka cluster
Follow [Confluent guide](https://github.com/confluentinc/cp-all-in-one/tree/7.5.0-post/cp-all-in-one)

```bash
git clone https://github.com/confluentinc/cp-all-in-one.git
cd cp-all-in-one/cp-all-in-one
docker compose up -d 
```

## Generate dummy datasets
Use the dummy_data_generator.py script to generate dummy datasets based on Avro schemas.

```bash
python kafka_performance_test/data_generator/dummy_data_generator.py -s path/to/kafka_value_schema.avsc -n 1000 -o target/
```
* -s or --schema-file: Path to the Avro schema file (e.g., kafka_performance_test/common/schemas/kafka_value_schema.avsc).
* -n or --num-records: Number of records to generate (e.g., 1000).
* -o or --output-folder: Directory where the generated file will be saved (e.g., target/).

## Send datasets to kafka
Use the kafka_producer.py script to send the generated datasets to a Kafka topic using Avro serialization.
```bash
python kafka_performance_test/kafka_producer/kafka_producer.py \
    -b localhost:9092 \
    -r http://localhost:8081 \
    -t test_topic \
    -k kafka_performance_test/common/schemas/kafka_key_schema.avsc \
    -v kafka_performance_test/common/schemas/kafka_value_schema.avsc \
    -d target/1000_kafka_value_schema.jsonl
```

* -b or --kafka-broker: Kafka broker address (e.g., localhost:9092).
* -r or --schema-registry-url: Schema Registry URL (e.g., http://localhost:8081).
* -t or --kafka-topic: Kafka topic to send messages to (e.g., test_topic).
* -k or --key-schema-file: Path to the Avro key schema file (e.g., kafka_performance_test/common/schemas/kafka_key_schema.avsc).
* -v or --value-schema-file: Path to the Avro value schema file (e.g., kafka_performance_test/common/schemas/kafka_value_schema.avsc).
* -d or --data-file: Path to the dataset file to send (e.g., target/1000_kafka_value_schema.jsonl).

