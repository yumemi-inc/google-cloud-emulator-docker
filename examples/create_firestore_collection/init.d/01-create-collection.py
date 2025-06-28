from google.cloud import firestore

def get_firestore_client(project_id):
    return firestore.Client(project=project_id)

def add_documents_to_collection(db, collection_name, documents):
    try:
        collection_ref = db.collection(collection_name)

        for doc in documents:
            collection_ref.add(doc)

        print(f"{collection_name} collection created with {len(documents)} documents")
        return True
    except Exception as e:
        print(f"Error adding documents to {collection_name}: {e}")
        return False

def create_users_collection(db):
    users_data = [
        {
            'name': 'Alice Johnson',
            'email': 'alice@example.com',
            'role': 'admin',
            'created_at': firestore.SERVER_TIMESTAMP
        },
        {
            'name': 'Bob Smith',
            'email': 'bob@example.com',
            'role': 'user',
            'created_at': firestore.SERVER_TIMESTAMP
        }
    ]

    return add_documents_to_collection(db, 'users', users_data)

def create_products_collection(db):
    products_data = [
        {
            'name': 'Laptop',
            'price': 999.99,
            'category': 'electronics',
            'in_stock': True
        },
        {
            'name': 'Coffee Mug',
            'price': 15.99,
            'category': 'home',
            'in_stock': True
        }
    ]

    return add_documents_to_collection(db, 'products', products_data)

if __name__ == "__main__":
    try:
        # Initialize Firestore client
        db = get_firestore_client("test-project")

        # Create collections with sample data
        users_success = create_users_collection(db)
        products_success = create_products_collection(db)

        if users_success and products_success:
            print("All collections initialized successfully!")
        else:
            print("Some collections failed to initialize")

    except Exception as e:
        print(f"Error initializing Firestore: {e}")