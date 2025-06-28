from google.cloud import spanner

def create_instance_and_database(project_id, instance_id, database_id):
    """Create a Spanner instance and database with a sample table."""
    spanner_client = spanner.Client(project=project_id)
    
    # Create instance configuration
    config_name = f"projects/{project_id}/instanceConfigs/emulator-config"
    
    # Create instance
    instance = spanner_client.instance(instance_id)
    operation = instance.create()
    
    print(f"Waiting for operation to complete...")
    operation.result(120)  # Wait up to 120 seconds
    print(f"Instance {instance_id} created successfully.")
    
    # Create database with DDL
    database = instance.database(database_id, ddl_statements=[
        """CREATE TABLE Users (
            UserId INT64 NOT NULL,
            UserName STRING(100),
            Email STRING(255),
            CreatedAt TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp=true),
        ) PRIMARY KEY (UserId)""",
        """CREATE TABLE Orders (
            OrderId INT64 NOT NULL,
            UserId INT64 NOT NULL,
            ProductName STRING(255),
            Quantity INT64,
            Price NUMERIC,
            OrderDate TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp=true),
        ) PRIMARY KEY (OrderId)"""
    ])
    
    operation = database.create()
    print(f"Waiting for database creation to complete...")
    operation.result(120)  # Wait up to 120 seconds
    
    print(f"Database {database_id} created with sample tables.")
    
    # Insert sample data
    with database.batch() as batch:
        batch.insert(
            table="Users",
            columns=("UserId", "UserName", "Email", "CreatedAt"),
            values=[
                (1, "Alice Smith", "alice@example.com", spanner.COMMIT_TIMESTAMP),
                (2, "Bob Johnson", "bob@example.com", spanner.COMMIT_TIMESTAMP),
                (3, "Carol Williams", "carol@example.com", spanner.COMMIT_TIMESTAMP),
            ],
        )
        batch.insert(
            table="Orders", 
            columns=("OrderId", "UserId", "ProductName", "Quantity", "Price", "OrderDate"),
            values=[
                (1001, 1, "Laptop", 1, 999.99, spanner.COMMIT_TIMESTAMP),
                (1002, 2, "Mouse", 2, 25.50, spanner.COMMIT_TIMESTAMP),
                (1003, 1, "Keyboard", 1, 79.99, spanner.COMMIT_TIMESTAMP),
            ],
        )
    
    print("Sample data inserted successfully.")

try:
    create_instance_and_database("test-project", "test-instance", "test-database")
    print("Spanner setup completed successfully!")
except Exception as e:
    print(f"Error during Spanner setup: {e}")
    raise