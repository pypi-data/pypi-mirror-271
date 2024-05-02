# MotionLake Client

MotionLake Client is a Python client library for interacting with a storage server designed for a new mobility data lake
solution. It provides functionalities to create collections, store data, query data, and retrieve collections.

## Installation

You can install the library via pip:

```bash
pip install motion-lake-client
```

## Usage

Here's a brief overview of how to use the library:

```python
from motion_lake_client import BaseClient

# Initialize the client with the base URL of the storage server
client = BaseClient(lake_url="http://localhost:8000")

# Create a new collection
client.create_collection("my_collection")

# Store data in a collection
data = b"example_data"
timestamp = int(datetime.now().timestamp())
client.store("my_collection", data, timestamp)

# Query data from a collection
results = client.query(
    "my_collection", min_timestamp=0, max_timestamp=timestamp, ascending=True
)

# Retrieve last item from a collection
last_item = client.get_last_item("my_collection")

# Retrieve first item from a collection
first_item = client.get_first_item("my_collection")

# Get items between two timestamps
items_between = client.get_items_between(
    "my_collection", min_timestamp=0, max_timestamp=timestamp
)

# Get items before a timestamp
items_before = client.get_items_before("my_collection", timestamp, limit=10)

# Get items after a timestamp
items_after = client.get_items_after("my_collection", timestamp, limit=10)

# Get all collections
collections = client.get_collections()

```

## Documentation

The library provides a series of classes and methods for storing, querying, and managing collections of data items. Each
item is timestamped and can be stored in various formats. Below is a detailed usage guide for each component provided by
the API.

### Prerequisites

Before using the API, make sure you have the `requests` library installed:

```bash
pip install requests
```

### Initializing the Client

To start interacting with the data storage server, instantiate the `BaseClient` with the URL of the storage server:

```python
from datetime import datetime
from my_module import BaseClient, ContentType

# Initialize the client; replace 'http://localhost:8000' with your server's URL
client = BaseClient('http://localhost:8000')
```

### Creating a Data Collection

Create a new data collection by specifying its name:

```python
response = client.create_collection("weather_data")
print(response)
```

### Storing Data

Store data in a specified collection:

```python
data = b"Example data"
timestamp = datetime.now()

# Store data as raw bytes
response = client.store("weather_data", data, timestamp, ContentType.RAW)
print(response)
```

You can also specify whether to create the collection if it doesn't exist:

```python
response = client.store("weather_data", data, timestamp, ContentType.JSON, create_collection=True)
print(response)
```

### Querying Data

Retrieve items from a collection based on various criteria:

- **Query by Timestamp Range**:
  ```python
  from datetime import datetime, timedelta

  start_date = datetime.now() - timedelta(days=1)
  end_date = datetime.now()

  items = client.get_items_between("weather_data", start_date, end_date)
  for item in items:
      print("Timestamp:", item.timestamp, "Data:", item.data)
  ```

- **Get Last N Items**:
  ```python
  last_items = client.get_last_items("weather_data", 5)
  for item in last_items:
      print("Timestamp:", item.timestamp, "Data:", item.data)
  ```

- **Get First N Items**:
  ```python
  first_items = client.get_first_items("weather_data", 5)
  for item in first_items:
      print("Timestamp:", item.timestamp, "Data:", item.data)
  ```
  
- **Get Items but skip data (only load timestamps)**:
  ```python
  first_items = client.get_first_items("weather_data", 5, skip_data=True)
  for item in first_items:
      print("Timestamp:", item.timestamp)
      assert item.data is None, "Data should be None, otherwise developer made a mistake (aka me)" 
  ```

### Advanced Queries

Perform an advanced SQL-like query (make sure your query string contains the placeholder `[table]`):

```python
query = "SELECT * FROM [table] WHERE data LIKE '%sample%'"
min_timestamp = datetime(2023, 1, 1)
max_timestamp = datetime(2023, 1, 31)

response = client.advanced_query("weather_data", query, min_timestamp, max_timestamp)
print(response)
```

### Managing Collections

- **List All Collections**:
  ```python
  collections = client.get_collections()
  for collection in collections:
      print(f"Collection: {collection.name}, Items: {collection.count}")
  ```

- **Delete a Collection**:
  ```python
  response = client.delete_collection("weather_data")
  print(response)
  ```


## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.

## License

All rights reserved.