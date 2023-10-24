# project : Amazon Products Recommender Engine
## project structure:
* [tasks](/tasks)
* [analytics/](./tasks/analytics)
* [etl_system/](./tasks/etl_system)
  * [.ipynb_checkpoints/](./tasks/etl_system/.ipynb_checkpoints)
    * [scrape_amazon-checkpoint.ipynb](./tasks/etl_system/.ipynb_checkpoints/scrape_amazon-checkpoint.ipynb)
  * [.jovianrc](./tasks/etl_system/.jovianrc)
  * [scrape_amazon.ipynb](./tasks/etl_system/scrape_amazon.ipynb)
* [ml/](./tasks/ml)

## Overview
B2B businesses use recommender systems to recommend products to their customers. This project seeks to build a recommender system that can recommend products to customers based on their history and/or based on similar users.

### 1. Project Objective:
Build recommender systems of collaborative filtering, content-based filtering and hybrid filtering for Amazon products.

### 2. Data Collection and Ingestion:
Data for this project will be collected using web scraping using BeautifulSoup and Selenium. This data will include product name, price, mean rating and the number of ratings for each product.
We will ensure a steady flow of data into our pipeline.

### 3. ETL System
The data collected from Amazon is raw and can be untidy. We shall perform data preprocessing and transformation. These pipelines shall clean, format, and aggregate data, making them ready for the recommender system.

### 4. Data Lake
Efficient data storage and management are critical components of this project. We will deploy a robust database system to store and organize the processed data, using Amazon S3. As the size of our data increases, we need to ensure that our system scales with it. We shall use AWS to process the vast amounts of data that we shall be getting.

### 5. Analytics and Machine Learning
With clean data at our proposal, we shall perform some basic analytics and build recommender systems to recommend product to users.

### 6. Deployment
After developing the recommender system, we shall deploy the recommender system using appropriate MLOps techniques.
