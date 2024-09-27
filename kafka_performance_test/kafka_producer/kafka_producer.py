import os
import json
import uuid
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import argparse


class KafkaAvroProducer:
    """
    A class to handle sending messages to Kafka using Avro serialization.
    """

    def __init__(self, kafka_broker, schema_registry_url, kafka_topic, key_schema_file, value_schema_file,
                 key_field=None):
        """
        Initialize the KafkaAvroProducer with Kafka and Schema Registry settings.

        Args:
            kafka_broker (str): The address of the Kafka broker.
            schema_registry_url (str): The URL of the Schema Registry.
            kafka_topic (str): The Kafka topic to send messages to.
            key_schema_file (str): Path to the Avro key schema file.
            value_schema_file (str): Path to the Avro value schema file.
            key_field (str, optional): The field name to use as the key. If not provided, a random UUID is used.
        """
        self.kafka_topic = kafka_topic
        self.key_field = key_field

        # Load key and value schemas from files
        self.key_schema = self.load_avro_schema(key_schema_file)
        self.value_schema = self.load_avro_schema(value_schema_file)

        # Kafka configuration with Schema Registry
        kafka_config = {
            'bootstrap.servers': kafka_broker,
            'schema.registry.url': schema_registry_url
        }

        # Initialize AvroProducer with Schema Registry
        self.avro_producer = AvroProducer(kafka_config, default_key_schema=self.key_schema,
                                          default_value_schema=self.value_schema)

    def load_avro_schema(self, schema_file):
        """
        Load an Avro schema from a file.

        Args:
            schema_file (str): The path to the Avro schema file.

        Returns:
            Avro schema: The loaded Avro schema.
        """
        with open(schema_file, 'r') as file:
            return avro.loads(file.read())

    def send_to_kafka_with_avro(self, data_file):
        """
        Send messages to Kafka with Avro serialization.

        Args:
            data_file (str): The path to the JSONL file containing the data.
        """
        # Open the file and read each line as a separate JSON object
        with open(data_file, 'r') as json_file:
            for line in json_file:
                record = json.loads(line.strip())  # Load each line as a JSON object

                # Use the field specified by key_field or generate a random UUID if not defined
                if self.key_field and self.key_field in record:
                    key = str(record[self.key_field])
                    print(f"Using provided key field '{self.key_field}': {key}")
                else:
                    key = str(uuid.uuid4())  # Generate a random UUID if key_field is not provided or not in record
                    print(f"Generated random key: {key}")

                self.avro_producer.produce(topic=self.kafka_topic, key={"id": key}, value=record)
                print(f"Sent record with key 'id': {key} and value: {record}")

        # Wait for all messages to be delivered
        self.avro_producer.flush()


def main(kafka_broker, schema_registry_url, kafka_topic, key_schema_file, value_schema_file, data_file, key_field=None):
    """
    Main function to send JSONL data to Kafka using Avro serialization.

    Args:
        kafka_broker (str): The address of the Kafka broker.
        schema_registry_url (str): The URL of the Schema Registry.
        kafka_topic (str): The Kafka topic to send messages to.
        key_schema_file (str): Path to the Avro key schema file.
        value_schema_file (str): Path to the Avro value schema file.
        data_file (str): The path to the JSONL data file.
        key_field (str, optional): The field name to use as the key.
    """
    producer = KafkaAvroProducer(kafka_broker, schema_registry_url, kafka_topic, key_schema_file, value_schema_file,
                                 key_field)
    producer.send_to_kafka_with_avro(data_file)


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Send JSONL data to Kafka using Avro serialization")
    parser.add_argument("-b", "--kafka-broker", type=str, required=True, help="Kafka broker address")
    parser.add_argument("-r", "--schema-registry-url", type=str, required=True, help="Schema Registry URL")
    parser.add_argument("-t", "--kafka-topic", type=str, required=True, help="Kafka topic to send messages to")
    parser.add_argument("-k", "--key-schema-file", type=str, required=True, help="Path to the Avro key schema file")
    parser.add_argument("-v", "--value-schema-file", type=str, required=True, help="Path to the Avro value schema file")
    parser.add_argument("-d", "--data-file", type=str, required=True, help="Path to the JSONL data file")
    parser.add_argument("-kf", "--key-field", type=str, help="Field name to use as key for Kafka messages")

    args = parser.parse_args()

    # Run the main function with parsed arguments
    main(args.kafka_broker, args.schema_registry_url, args.kafka_topic, args.key_schema_file, args.value_schema_file,
         args.data_file, args.key_field)