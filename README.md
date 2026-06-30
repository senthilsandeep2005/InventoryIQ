# 📦 InventoryIQ

## Enterprise Inventory Optimization Platform

InventoryIQ is an end-to-end cloud inventory analytics platform built to demonstrate how modern organizations can centralize operational data, analyze inventory performance, and generate business insights using AWS cloud services.

The application simulates a single distribution center and provides executive dashboards for inventory optimization, sales performance, supplier analytics, and inventory risk management.

Developed by **Sandeep Senthil**

---

# Project Overview

InventoryIQ demonstrates a modern cloud analytics workflow:

Warehouse Data
→ Amazon S3 Data Lake
→ Amazon Athena Serverless SQL
→ Python Data Processing
→ Interactive Streamlit Dashboard
→ Executive Decision Support

The platform transforms operational warehouse data into interactive business intelligence dashboards suitable for executives, operations managers, supply chain analysts, and inventory planners.

---

## Enterprise Architecture

The diagram below illustrates the overall cloud architecture of InventoryIQ, from the source dataset through AWS services to the interactive analytics dashboard.

<p align="center">
  <img src="docs/Architecture/Enterprise_Architecture.jpeg" width="100%">
</p>

---

# Features

## Executive Dashboard

- Executive KPI scorecards
- Total inventory value
- Inventory health score
- High-risk SKU monitoring
- Reorder recommendations
- Inventory value by category
- Sales revenue by category
- Monthly sales trends
- Warehouse transaction activity

---

## Inventory Analytics

- Inventory value analysis
- SKU inventory health
- Stock level analysis
- Days of inventory
- ABC classification
- Stockout risk distribution
- Inventory value by category
- Highest-value inventory
- Inventory filtering by:
  - Category
  - Supplier
  - Stockout Risk

---

## Sales Analytics

- Revenue dashboard
- Revenue by category
- Monthly revenue trends
- Top revenue SKUs
- Sales filters
- Units sold
- Average order value
- Order analytics

---

## Supplier Analytics

- Supplier performance dashboard
- Supplier reliability
- Inventory supplied
- Supplier contribution
- Supplier risk analysis
- Supplier level filtering

---

## Risk Center

- High-risk inventory monitoring
- Stockout risk analysis
- Slow-moving inventory
- Excess inventory detection
- Reorder priority recommendations
- Inventory risk dashboard

---

# Cloud Architecture

```
Kaggle Dataset
       │
       ▼
Amazon S3 Data Lake
       │
       ▼
Amazon Athena
(Serverless SQL)
       │
       ▼
Python + Pandas
Business Logic
       │
       ▼
Streamlit Dashboard
       │
       ▼
Interactive Analytics
```

---

# Technology Stack

### Cloud

- Amazon S3
- Amazon Athena

### Programming

- Python
- SQL

### Data Processing

- Pandas
- NumPy

### Visualization

- Plotly
- Streamlit

### Development

- Git
- GitHub
- VS Code

---

## End-to-End Data Flow

InventoryIQ follows a modern analytics pipeline that transforms raw warehouse data into actionable business insights.

<p align="center">
  <img src="docs/Architecture/Data_Flow_Diagram.png" width="100%">
</p>

--- 

## AWS Cloud Architecture

InventoryIQ leverages a serverless AWS analytics stack consisting of Amazon S3, Amazon Athena, Python, and Streamlit.

<p align="center">
  <img src="docs/Architecture/AWS_Cloud_Architecture.jpeg" width="100%">
</p>

---

# Dataset

This project is built using the Logistics Warehouse Dataset from Kaggle and has been adapted into a production-style inventory optimization platform.

Dataset:

https://www.kaggle.com/datasets/ziya07/logistics-warehouse-dataset

---

# Repository Structure

```
InventoryIQ/
│
├── dashboard/
│   ├── app.py
│   ├── pages/
│   │   ├── Executive_Dashboard.py
│   │   ├── Inventory_Analytics.py
│   │   ├── Sales_Analytics.py
│   │   ├── Supplier_Analytics.py
│   │   └── Risk_Center.py
│   │
│   ├── sql/
│   ├── utils/
│   └── assets/
│
├── data/
│
├── docs/
│
├── screenshots/
│
└── README.md
```

---

# Skills Demonstrated

- Cloud Data Engineering
- Business Intelligence
- Inventory Optimization
- SQL Analytics
- Data Visualization
- KPI Development
- Supply Chain Analytics
- Dashboard Design
- AWS Analytics Services
- Python Data Processing
- Interactive Business Applications

---

# Future Enhancements

- User authentication
- Role-based access control
- Live database connectivity
- Automated data refresh
- Forecasting models
- Machine learning demand prediction
- Executive PDF reporting
- Cloud deployment
- CI/CD pipeline
- Custom alerting and notifications

---

# Screenshots

(Add dashboard screenshots here)

- Executive Dashboard
- Inventory Analytics
- Sales Analytics
- Supplier Analytics
- Risk Center

---

# Author

**Sandeep Senthil**

InventoryIQ was developed as a portfolio project to demonstrate cloud analytics, business intelligence, inventory optimization, and full-stack dashboard development using AWS, SQL, Python, and Streamlit.