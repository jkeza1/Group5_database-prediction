# Group5_database-prediction

# Teen Phone Addiction and Lifestyle Survey Analysis

## Project Overview

This project addresses the design and implementation of a database system and API integration to support predictive analytics on teen phone addiction. Utilizing a comprehensive dataset, the team developed both relational (SQL) and NoSQL (MongoDB) databases, implemented FastAPI CRUD endpoints, and created a script for fetching, preprocessing data, and making machine learning predictions.

The goal is to provide accurate predictions of addiction levels to aid intervention strategies.

---

## Features and Deliverables

### Database Design and Implementation

- Developed a relational database schema with three tables, including primary and foreign keys.
- Created an Entity-Relationship Diagram (ERD) to illustrate database relationships.
- Implemented the schema in MongoDB collections to support NoSQL storage.
- Developed stored procedures and triggers in the relational database to automate validation and logging.

### API Endpoints

- Implemented FastAPI endpoints supporting full CRUD operations on the relational database.
- Input validation and error handling to ensure robust and secure API interactions.
- Integrated the API with MongoDB to manage data effectively.

### Machine Learning Pipeline

- Developed a RandomForestRegressor model to predict addiction levels based on teen phone usage and lifestyle features.
- Created a script that:
  - Fetches the latest data entry via the API.
  - Preprocesses and prepares the data for prediction.
  - Loads the trained model and generates predictions.
  - Logs prediction results back into the database.

---

## Dataset

- Dataset: Teen Phone Addiction Dataset  
- Records: 3000  
- Features: 25, including demographic data, phone usage patterns, and psychological factors.  
- Source: [Dataset CSV on GitHub](https://raw.githubusercontent.com/jkeza1/Group5_database-prediction/refs/heads/main/data/teen_phone_addiction_dataset.csv)

---

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
