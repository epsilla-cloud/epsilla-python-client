import sys
import json

try:
    from pyepsilla import cloud
except ImportError as e:
    print("Failed to import pyepsilla. Ensure the library is installed.")
    sys.exit(1)

try:
    # Connect to Epsilla Cloud
    client = cloud.Client(
        project_id="project-id",
        api_key="epsilla-cloud-api-key",
    )

    # Connect to Vectordb
    db = client.vectordb(db_id="6accafb1-476d-43b0-aa64-12ebfbf7442d")

    # Data for creating table
    table_fields = [
        {"name": "ID", "dataType": "INT", "primaryKey": True},
        {"name": "Doc", "dataType": "STRING"},
        {"name": "Embedding", "dataType": "VECTOR_FLOAT", "dimensions": 4},
    ]
    print("Table fields:", table_fields)

    # Create a table with schema
    status_code, response = db.create_table(
        table_name="MyTable",
        table_fields=table_fields,
    )
    print(status_code, response)

    # Data for inserting records
    records = [
        {"ID": 1, "Doc": "Berlin", "Embedding": [0.05, 0.61, 0.76, 0.74]},
        {"ID": 2, "Doc": "London", "Embedding": [0.19, 0.81, 0.75, 0.11]},
        {"ID": 3, "Doc": "Moscow", "Embedding": [0.36, 0.55, 0.47, 0.94]},
        {"ID": 4, "Doc": "San Francisco", "Embedding": [0.18, 0.01, 0.85, 0.80]},
        {"ID": 5, "Doc": "Shanghai", "Embedding": [0.24, 0.18, 0.22, 0.44]},
    ]
    print("Records:", records)

    # Insert new vector records into table
    status_code, response = db.insert(
        table_name="MyTable",
        records=records,
    )
    print(status_code, response)

    # Query parameters
    query_vector = [0.35, 0.55, 0.47, 0.94]
    print("Query vector:", query_vector)

    # Query Vectors with specific response field, otherwise it will return all fields
    status_code, response = db.query(
        table_name="MyTable",
        query_field="Embedding",
        query_vector=query_vector,
        response_fields=["Doc"],
        limit=2,
    )
    print(status_code, response)

    # Delete specific records from table
    primary_keys_to_delete = [4, 5]
    print("Primary keys to delete:", primary_keys_to_delete)
    status_code, response = db.delete(table_name="MyTable", primary_keys=primary_keys_to_delete)
    print(status_code, response)
    status_code, response = db.delete(table_name="MyTable", filter="Doc <> 'San Francisco'")
    print(status_code, response)

    # Drop table
    status_code, response = db.drop_table(table_name="MyTable")
    print(status_code, response)
except Exception as e:
    print(f"An error occurred: {e}")

