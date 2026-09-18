# 🤖 Intelligent Text-to-SQL Assistant

<p align="center">
  <b>Ask questions in natural language. Get SQL results instantly.</b>
</p>

<p align="center">
  An AI-powered Text-to-SQL application that converts natural language questions into SQL queries and executes them on a MySQL database.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white">
  <img src="https://img.shields.io/badge/Google%20Gemini-AI-blue?logo=google">
  <img src="https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white">
  <img src="https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=white">
</p>

---

## 📌 Overview

**Intelligent Text-to-SQL Assistant** allows users to interact with databases using natural language instead of manually writing SQL queries.

The application uses **Google Gemini** to understand the user's question, generate an appropriate SQL query, execute it on **MySQL**, and display the results through an interactive **Streamlit** interface.

The application supports two modes:

- 🗄️ **Demo Database** — Explore a ready-to-use sample database
- 📁 **Upload Your Data** — Upload your own CSV and query it using natural language

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 AI SQL Generation | Converts natural-language questions into SQL |
| 🗄️ Demo Database | Query sample customers, products and orders |
| 📁 CSV Upload | Upload your own dataset |
| 🔍 Schema Detection | Automatically detects uploaded table columns |
| 💬 Clarification | Handles ambiguous questions before generating SQL |
| 🔐 SQL Validation | Allows only read-only SQL queries |
| 📊 Query Results | Displays results in an interactive table |
| 🎨 Streamlit UI | Clean and interactive web interface |

---

## 🖥️ Application Preview

### 🏠 Home Screen

<p align="center">
  <img src="screenshots/home.png" width="850">
</p>

The home screen provides two options:

### 🗄️ Try Demo Database

<p align="center">
  <img src="image/demo.png" width="850">
</p>

Explore the built-in sample database without uploading any files.

### 📁 Upload Your Data

Upload a CSV file and ask questions about your own dataset.

---

## 📁 Upload Your Own Dataset

<p align="center">
  <img src="image/database.png" width="850">
</p>

The application:

1. Accepts a CSV file
2. Displays a data preview
3. Loads the dataset into MySQL
4. Detects the uploaded schema
5. Allows natural-language queries on the dataset

---

## 🤖 Natural Language → SQL

Example question:

```text
How many customers are from France?
```

The AI generates a SQL query such as:

```sql
SELECT COUNT(*)
FROM uploaded_data
WHERE country = 'France';
```

The generated query is then executed on MySQL and the result is displayed in the application.

---

## 💬 Intelligent Clarification

The application can detect when a question is ambiguous.

For example:

```text
User:
Show customers
```

Instead of blindly generating SQL, the application can ask:

```text
Could you clarify?

Do you want to see all customers
or customers from a specific city?
```

The user's clarification is then combined with the original question before generating the final SQL query.

---

## 🔐 SQL Safety

The application includes SQL validation to prevent accidental modification of database data.

Only read-only queries are allowed:

```text
SELECT
WITH ... SELECT
```

Queries involving operations such as:

```text
INSERT
UPDATE
DELETE
DROP
```

are rejected.

---

## 🏗️ How It Works

```text
             User Question
                   │
                   ▼
        ┌─────────────────────┐
        │ Clarification Check │
        └──────────┬──────────┘
                   │
                   ▼
          Google Gemini API
                   │
                   ▼
          SQL Query Generation
                   │
                   ▼
          SQL Safety Validation
                   │
                   ▼
             MySQL Database
                   │
                   ▼
            Query Execution
                   │
                   ▼
             Query Results
                   │
                   ▼
           Streamlit Interface
```

---

## 🛠️ Tech Stack

### Frontend / UI

- Streamlit

### Programming Language

- Python

### Database

- MySQL
- `mysql-connector-python`

### AI / LLM

- Google Gemini API

### Data Processing

- Pandas
  
### Prompt Engineering 

- Custom prompts for SQL generation and clarification detection

### Validation

- Pydantic

### Configuration

- python-dotenv

---

## 📂 Project Structure

```text
text-to-sql-clarification-engine/
│
├── app/
│   ├── main.py
│   ├── llm.py
│   ├── database.py
│   └── clarification.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

```bash
cd text-to-sql-clarification-engine
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project directory:

```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
GEMINI_API_KEY=your_gemini_api_key
```

⚠️ **Never upload your `.env` file to GitHub.**

Add this to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Run the Application

Start the Streamlit application with:

```bash
streamlit run app/main.py
```

The application will open in your browser.

---

## 🧪 Example Dataset

You can test the application using a CSV containing columns such as:

```text
customer_id
credit_score
country
gender
age
tenure
balance
products_number
credit_card
active_member
estimated_salary
churn
```

Example questions:

```text
How many customers are from France?
```

```text
Show customers with a balance greater than 50000.
```

```text
How many customers have churned?
```

```text
Which country has the most customers?
```

```text
Show customers older than 40.
```

```text
What is the average balance?
```

---

## 🚀 Future Improvements

- 📈 Automatic data visualizations
- 🕘 Query history
- 🧠 Improved schema understanding
- 🗃️ Support for additional databases
- ⚡ Better SQL error handling
- 📊 Automatic chart generation
- 🔎 More advanced query clarification
- 🔐 More robust SQL validation

---

## 🎯 Project Highlights

This project demonstrates practical implementation of:

- Natural Language Processing
- Generative AI
- LLM-based SQL generation
- Prompt engineering
- Database connectivity
- SQL validation
- Schema handling
- CSV-to-MySQL data loading
- Streamlit application development
- Pydantic structured outputs

---

## 👩‍💻 Author

### Somya Nema

**B.Tech — Artificial Intelligence & Machine Learning**

---

## ⭐ If You Like This Project

If you find this project useful, consider giving the repository a ⭐ on GitHub!

```text
Made with Python + Streamlit + MySQL + Gemini 🤖
```
