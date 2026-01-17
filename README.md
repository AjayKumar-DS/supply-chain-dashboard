# Supply Chain Analytics Dashboard

## Overview
This project is an interactive **Supply Chain Analytics Dashboard** developed using **Python, Dash, Pandas, and Plotly**.  
It analyzes a real-world supply chain dataset to generate insights into **forecast accuracy, promotions, supplier performance, inventory behavior, and sales trends**.

The dashboard is designed to support **data-driven decision-making** by transforming raw operational data into clear, interactive visualizations.

---

## Objectives
The main objectives of this project are:
- To analyze supply chain performance across multiple dimensions
- To identify patterns and inefficiencies in demand forecasting and supplier reliability
- To understand the impact of promotions on sales and profitability
- To present insights in an interactive and user-friendly dashboard

---

## Dashboard Structure
The dashboard is organized into multiple research questions (RQs):

### RQ1 – Demand Forecast Analysis
- Comparison of forecasted demand vs actual sales
- Identification of under- and over-forecasted products and regions
- Impact of promotions on forecast accuracy

### RQ2 – Promotion Impact Analysis
- Effect of promotions on sales volume
- Effect of promotions on profitability
- Regional distribution of promotional activity

### RQ3 – Supplier Lead Time Analysis
- Comparison of average lead times across suppliers
- Identification of the most consistent and reliable suppliers
- Analysis of the relationship between supplier lead times and inventory levels
- Includes bar charts, box plots, scatter plots, and summary tables

### RQ4 – Inventory & Replenishment Analysis
- Alignment of inventory levels with sales demand
- Analysis of reorder points and inventory cover

### RQ5 – Sales Performance Analysis
- Identification of top-selling products
- Comparison of sales performance across regions
- Analysis of sales trends over time

---

## Technologies Used
- **Python**
- **Pandas** – Data cleaning, transformation, and aggregation
- **Dash** – Interactive web application framework
- **Dash Bootstrap Components** – Layout and styling
- **Plotly Express** – Interactive charts and visualizations

---

## Project Structure
```text
.
├── data/
│   └── supply_chain_dataset1.csv
├── analysis/
│   ├── data_modelling.py
│   ├── analysis_rq1.py
│   ├── analysis_rq2.py
│   ├── analysis_rq3.py
│   ├── analysis_rq4.py
│   └── analysis_rq5.py
├── main.py
├── requirements.txt
└── README.md
