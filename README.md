# 🛒 E-Commerce ETL Pipeline

A complete ETL pipeline built with Python to process e-commerce data and load it into a PostgreSQL database. This project demonstrates core data engineering skills including data extraction, transformation, loading, and pipeline automation.

---

## 🚀 Features

- Extracts raw e-commerce data from CSV files
- Cleans and transforms data using `pandas`
- Loads data into a normalized PostgreSQL schema
- Logs each ETL step for monitoring and debugging
- Modular structure for easy extension and maintenance

---

## 🧰 Tech Stack

- **Programming Language:** Python
- **Libraries:** pandas, psycopg2, os, logging
- **Database:** PostgreSQL
- **Environment:** Jupyter Notebook / Python scripts
- **Pipeline Scheduling:** Apache Airflow

---

## 📁 Project Structure

```
e-commerce-etl-pipline/
├── data/
│   ├── customers.csv
│   ├── orders.csv
│   └── products.json
├── etl/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── logs/
│   └── etl.log
├── config.py
├── main.py
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/ahmedwalid98/e-commerce-etl-pipline.git
cd e-commerce-etl-pipline
```

### 2. Set up a virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🧪 Sample Use Cases

- Analyze customer order behavior
- Build dashboards for top-selling products
- Integrate with BI tools (e.g. Tableau, Power BI)

---

## 📌 Future Improvements

- Add data validation and unit tests
- Integrate with cloud storage (e.g., AWS S3)
- Dockerize the project for deployment

---

## 📬 Contact

**Ahmed Walid Youssif**  
📧 ahmedwalid98.aw@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/ahmed-walid-262a111a4/)  
💻 [GitHub](https://github.com/ahmedwalid98)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
