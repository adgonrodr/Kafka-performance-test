import os
import json
import random
import argparse
from faker import Faker
from datetime import datetime


class DataGenerator:
    """
    A class to generate dummy data based on a given schema using Faker.
    """

    def __init__(self):
        """
        Initialize the DataGenerator with a Faker instance.
        """
        self.fake = Faker()

    def load_schema_from_file(self, schema_file):
        """
        Load the schema from a JSON file.

        Args:
            schema_file (str): The path to the schema file.

        Returns:
            dict: The loaded schema as a dictionary.
        """
        with open(schema_file, 'r') as file:
            return json.load(file)

    def handle_complex_type(self, field):
        """
        Handle object-type fields with properties like maxLength.

        Args:
            field (dict): The field definition from the schema.

        Returns:
            str or None: The generated value for complex types or None if not applicable.
        """
        if isinstance(field['type'], dict):
            if field['type']['type'] == 'string' and 'maxLength' in field['type']:
                max_length = field['type']['maxLength']
                return self.fake.lexify(text='?' * max_length)
        return None

    def generate_dummy_data(self, schema, num_records=10, output_folder="output", schema_name="default_schema"):
        """
        Generate dummy data based on the provided schema.

        Args:
            schema (dict): The schema definition.
            num_records (int): The number of records to generate. Default is 10.
            output_folder (str): The folder to save the generated data. Default is 'output'.
            schema_name (str): The name of the schema used to generate the filename.

        Returns:
            None: Outputs the dataset to a file in the specified folder.
        """
        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Generate the output filename based on the pattern {num_records}_{schema_name}.jsonl
        output_file = os.path.join(output_folder, f"{num_records}_{schema_name}.jsonl")

        with open(output_file, 'w') as outfile:
            for _ in range(num_records):
                record = {}
                for field in schema['fields']:
                    field_name = field['name']
                    field_type = field['type']

                    # Handle complex types
                    complex_value = self.handle_complex_type(field)
                    if complex_value is not None:
                        record[field_name] = complex_value
                        continue

                    # Handle basic types
                    if field_type == 'int':
                        record[field_name] = random.randint(18, 99)
                    elif field_type == 'string':
                        if field_name == 'email':
                            record[field_name] = self.fake.email()
                        elif field_name == 'created_at':
                            record[field_name] = self.fake.date_time().isoformat()
                        elif field_name == 'join_date':
                            record[field_name] = self.fake.date()
                        elif field_name == 'timestamp_ntz':
                            record[field_name] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                        else:
                            record[field_name] = self.fake.word()[:5]
                    elif field_type == 'double':
                        record[field_name] = round(random.uniform(0, 99999999999999), 7)

                # Write each record as a JSON object in a new line
                outfile.write(json.dumps(record) + '\n')

        print(f"Dataset saved to {output_file}")


def main(schema_file, num_records, output_folder):
    """
    Main function to load schema and generate dummy data based on input arguments.

    Args:
        schema_file (str): The path to the schema file.
        num_records (int): The number of records to generate.
        output_folder (str): The folder to save the generated dataset.
    """
    # Create instance of DataGenerator
    generator = DataGenerator()

    # Load schema
    schema = generator.load_schema_from_file(schema_file)

    # Extract schema file name (without path and extension)
    schema_name = os.path.splitext(os.path.basename(schema_file))[0]

    # Generate dummy data
    generator.generate_dummy_data(schema, num_records=num_records, output_folder=output_folder, schema_name=schema_name)


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Generate dummy data from a schema")
    parser.add_argument("-s", "--schema-file", type=str, required=True, help="Path to the schema file")
    parser.add_argument("-n", "--num-records", type=int, required=True, help="Number of records to generate")
    parser.add_argument("-o", "--output-folder", type=str, default="target",
                        help="Folder to save the generated dataset")

    args = parser.parse_args()

    # Run the main function with parsed arguments
    main(args.schema_file, args.num_records, args.output_folder)