# project : amazon recommender system

## Overview
B2B businesses use recommender systemst to recommend products to their customers. This project seeks to build a recommender system that can recommend products customers based on their history and/or based on similar users.

## 1. Project Objective:
Build a recommender systems of collabative-filtering, content-based filtering and hybrid filtering for amazon products.

### 2. Data Collection and ingestion:
Data for this project will be collected using web scraping using beautifulsoup and selenium. This data will include product name, price, description and rating.
We will ensure a steady flow of data into our pipeline.

### 3. ETL System
The data collected from amazon is raw and can be untidy. We shall perform data preprocessing and transformation. These pipelines shall clean, format, and aggregate data making it ready for the recommender system.

### 4. Data Lake
Efficient data storage and management are critical components of this project. We will deploy a robust database system to store and organize the processed data, using a centralized repo to store them. As the size of our data increases, we need to ensure that our system scales with it. We shall use AWS to process the vast amounts of data that we shall be getting.

### 5. Analystics and Machine Learning
Efficient data storage and management are critical components of this project. We will deploy a robust database system to store and organize the processed data, using a centralized repo to store them. As the size of our data increases, we need to ensure that our system scales with it. We shall use AWS to process the vast amounts of data that we shall be getting. We shall build recommender systems to recommend product to users.

### 6. Deployemnt
After developing the recommender system, we shall deploy the recommender system by using MLOps techniques. Containerization techniques like kubernetes and docker shall be used, together with flask framework.

