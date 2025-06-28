from google.cloud import datastore

def get_datastore_client(project_id):
    return datastore.Client(project=project_id)

def create_entity(client, kind, entity_id, properties):
    try:
        key = client.key(kind, entity_id)
        entity = datastore.Entity(key=key)
        entity.update(properties)
        return entity
    except Exception as e:
        print(f"Error creating {kind} entity: {e}")
        return None

def create_user_entities(client):
    user_data = [
        {
            'id': 'user1',
            'properties': {
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'age': 30
            }
        },
        {
            'id': 'user2',
            'properties': {
                'name': 'Jane Smith',
                'email': 'jane.smith@example.com',
                'age': 25
            }
        }
    ]

    entities = []
    for user in user_data:
        entity = create_entity(client, 'User', user['id'], user['properties'])
        if entity:
            entities.append(entity)

    return entities

def create_product_entities(client):
    product_data = [
        {
            'id': 'product1',
            'properties': {
                'name': 'Laptop',
                'price': 999.99,
                'category': 'Electronics'
            }
        },
        {
            'id': 'product2',
            'properties': {
                'name': 'Coffee Mug',
                'price': 15.99,
                'category': 'Home'
            }
        }
    ]

    entities = []
    for product in product_data:
        entity = create_entity(client, 'Product', product['id'], product['properties'])
        if entity:
            entities.append(entity)

    return entities

def create_order_entities(client):
    order_data = [
        {
            'id': 'order1',
            'properties': {
                'user_id': 'user1',
                'product_id': 'product1',
                'quantity': 1,
                'status': 'pending'
            }
        },
        {
            'id': 'order2',
            'properties': {
                'user_id': 'user2',
                'product_id': 'product2',
                'quantity': 2,
                'status': 'completed'
            }
        }
    ]

    entities = []
    for order in order_data:
        entity = create_entity(client, 'Order', order['id'], order['properties'])
        if entity:
            entities.append(entity)

    return entities

def save_entities(client, entities):
    try:
        client.put_multi(entities)
        return True
    except Exception as e:
        print(f"Error saving entities: {e}")
        return False

if __name__ == "__main__":
    try:
        # Initialize Datastore client
        client = get_datastore_client("test-project")

        # Create entities
        user_entities = create_user_entities(client)
        product_entities = create_product_entities(client)
        order_entities = create_order_entities(client)

        # Combine all entities
        all_entities = user_entities + product_entities + order_entities

        # Save all entities
        if save_entities(client, all_entities):
            print(f"All entities created successfully in project: test-project")
            print(f"- Users: {len(user_entities)} entities")
            print(f"- Products: {len(product_entities)} entities")
            print(f"- Orders: {len(order_entities)} entities")
        else:
            print("Failed to save some entities")

    except Exception as e:
        print(f"Error initializing Datastore: {e}")
