from chromadb import PersistentClient

# Initialize the client
client = PersistentClient(path="../backend\chroma_db")

# List all collections
collections = client.list_collections()

# Print collection names
for collection in collections:
    print(collection.name)
    print(collection.count())

