from google.cloud import pubsub_v1

def create_topic(project_id, topic_name):
    """Create a new Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    try:
        topic = publisher.create_topic(request={"name": topic_path})
        print(f"Topic created: {topic.name}")
    except Exception as e:
        print(f"Error creating topic: {e}")

create_topic("test-project", "email-notifications")
create_topic("test-project", "push-notifications")
