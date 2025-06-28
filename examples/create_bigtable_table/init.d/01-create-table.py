from google.cloud import bigtable
from google.cloud.bigtable import column_family

def get_bigtable_client(project_id):
    return bigtable.Client(project=project_id, admin=True)

def create_column_families():
    return {
        'user': column_family.MaxVersionsGCRule(2),
        'data': column_family.MaxVersionsGCRule(10)
    }

def create_table(client, instance_id, table_id, column_families=None):
    """Create a Bigtable table with column families.

    Note: In the emulator, instances are virtual and don't need to be created.
    You can use any instance name to create tables.
    """
    if column_families is None:
        column_families = create_column_families()

    # In the emulator, we can use any instance name without creating it
    instance = client.instance(instance_id)
    table = instance.table(table_id)

    try:
        table.create(column_families=column_families)
        print(f"Table created: {table_id} in instance: {instance_id}")
        return True
    except Exception as e:
        print(f"Error creating table {table_id}: {e}")
        return False

if __name__ == "__main__":
    try:
        # Initialize Bigtable client
        client = get_bigtable_client("test-project")

        # Define tables to create
        # Note: In emulator, instance names are arbitrary and don't need pre-creation
        tables_config = [
            {"instance_id": "test-instance", "table_id": "user-data"},
            {"instance_id": "test-instance", "table_id": "analytics"}
        ]

        # Create tables (instances are virtual in emulator)
        successful_tables = 0
        for config in tables_config:
            if create_table(client, **config):
                successful_tables += 1

        print(f"Bigtable initialization completed: {successful_tables}/{len(tables_config)} tables created successfully")

    except Exception as e:
        print(f"Error initializing Bigtable: {e}")
