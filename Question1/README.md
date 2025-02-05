# Question 1: Real-Time Data Processing and Visualization

## Project Overview

This project involves streaming real-time data from Reddit, processing it using Apache Spark and Kafka, and visualizing the processed data using Kibana.

## How to Run the Project

### Step 1: Download and Extract the Project Archive

Download and extract `BDA3.zip` to your desired location.

### Step 2: Navigate to the `Question1` Directory

Use the following command to navigate into the project directory:

```bash
cd path/to/Question1
```

### Step 3: Make sure you have Docker Desktop

Ensure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is installed and running on your machine, as it is required to run the project containers.

### Step 4: Build and Run the Docker Containers

Run the following command to build and start all Docker containers:

```bash
docker-compose up --build
```

This command will:

- Build images for the `reddit_to_kafka` and `kafka_to_spark services`.
- Start all containers, including Logstash, which forwards processed data to Elasticsearch.

### Step 5: Verify the Services

Confirm that the services are running correctly:

- `reddit_to_kafka` should be streaming data from Reddit into Kafka topics.
- `kafka_to_spark` should be reading data from Kafka, processing it, and sending the output to another Kafka topic.
- `Logstash` should be forwarding the processed data to Elasticsearch.

### Step 6: Access Kibana for Data Visualization

- Open your web browser and go to: http://localhost:5601

## How to Visualize Data in Kibana

### Step 1: Access Kibana

1. **Open your web browser** and navigate to `http://localhost:5601` to access the Kibana dashboard.

### Step 2: Create or Select an Index Pattern

- Navigate to **Management** > **Stack Management** > **Index Patterns**.
- **If you need to create an index pattern**:
  - Click **"Create index pattern"**.
  - Enter the index pattern that matches your data (e.g., `entities-*`).
  - Select a time field (if applicable) and complete the creation by following the prompts.
- **If you already have an index pattern**, ensure it matches the data you wish to visualize.

### Step 3: Navigate to Visualizations

- From the left sidebar, click on **"Visualize Library"**.
- Click **"Create visualization"** and select **"Bar chart"** as the visualization type.

### Step 4: Configure the Bar Chart Visualization

#### 1. **Choose Data Source**

- Select the appropriate index pattern you created (e.g., `entities-*`).

#### 2. **Add Metrics**

- Under **"Metrics"**, verify that the aggregation is set to **"Count"** (default) to count the number of documents.

#### 3. **Configure Buckets**

- Click **"Add"** under **"Buckets"** and choose **"X-axis"**.
- Configure the following:
  - **Aggregation**: Select **"Terms"**.
  - **Field**: Choose the field representing the entities (e.g., `entity.keyword`).
  - **Order by**: Select **"Metric: Count"**.
  - **Order**: Choose **Descending**.
  - **Size**: Set the number of top entities to display (e.g., 10).
  - **Advanced Options**: Disable the **"Group other values in separate bucket"** option to exclude grouped results.

#### 4. **Y-axis Configuration**

- Ensure the Y-axis is configured to display the **"Count"** of documents.

### Step 5: Apply and Preview

- Click **"Update"** to apply the changes and preview the bar chart. Ensure the visualization accurately reflects the top entities and their counts.

### Step 6: Save the Visualization

1. Click **"Save"** at the top right of the screen.
2. Enter a descriptive name for your visualization (e.g., **"Top Entities by Count"**).
3. Click **"Save"** to store the visualization for future use.

### Optional: Add the Visualization to a Dashboard

1. Navigate to **"Dashboard"** from the sidebar.
2. Click **"Create new dashboard"** or open an existing one.
3. Click **"Add"** and select your saved bar chart visualization.
4. Rearrange and resize the chart as needed.
5. Click **"Save"** to save the updated dashboard.
