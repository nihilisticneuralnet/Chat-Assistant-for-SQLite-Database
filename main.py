import streamlit as st
import sqlalchemy
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, Float, Date, MetaData, create_engine, insert, text, inspect
from smolagents import tool, CodeAgent, HfApiModel
from dotenv import load_dotenv
import os
from huggingface_hub import login

login(token="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")

# load_dotenv()
# hf_token = os.getenv("HUGGINGFACE_TOKEN")
# login(token=hf_token)

engine = create_engine("sqlite:///:memory:")
metadata_obj = MetaData()

employees = Table(
    "employees", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("department", String(50), nullable=False),
    Column("salary", Float, nullable=False),
    Column("hire_date", Date, nullable=False)
)

departments = Table(
    "departments", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False, unique=True),
    Column("manager", String(50), nullable=False)
)

metadata_obj.create_all(engine)

employee_rows = [
    {"id": 1, "name": "Alice", "department": "Sales", "salary": 50000, "hire_date": datetime.strptime("2021-01-15", "%Y-%m-%d").date()},
    {"id": 2, "name": "Bob", "department": "Engineering", "salary": 70000, "hire_date": datetime.strptime("2020-06-10", "%Y-%m-%d").date()},
    {"id": 3, "name": "Charlie", "department": "Marketing", "salary": 60000, "hire_date": datetime.strptime("2022-03-20", "%Y-%m-%d").date()}
]

department_rows = [
    {"id": 1, "name": "Sales", "manager": "Alice"},
    {"id": 2, "name": "Engineering", "manager": "Bob"},
    {"id": 3, "name": "Marketing", "manager": "Charlie"}
]

with engine.begin() as connection:
    connection.execute(insert(employees), employee_rows)
    connection.execute(insert(departments), department_rows)

@tool
def sql_engine(query: str) -> str:
    """
    Executes an SQL query and returns the result as a string.

    Args:
        query (str): The SQL query to execute.

    Returns:
        str: The result of the query.
    """
    output = ""
    with engine.connect() as con:
        rows = con.execute(text(query))
        for row in rows:
            output += "\n" + str(row)
    return output

def get_table_description():
    description = """Allows you to perform SQL queries on the table. Beware that this tool's output is a string representation of the execution output.
It can use the following tables:"""
    inspector = inspect(engine)
    for table in ["employees", "departments"]:
        columns_info = [(col["name"], col["type"]) for col in inspector.get_columns(table)]
        table_description = f"\n\nTable '{table}':\n"
        table_description += "Columns:\n" + "\n".join([f"  - {name}: {col_type}" for name, col_type in columns_info])
        description += table_description
    return description

sql_engine.description = get_table_description()

agent = CodeAgent(
    tools=[sql_engine],
    model=HfApiModel("Qwen/Qwen2.5-72B-Instruct"),
)

st.title("Chat Assistant for SQLite Database")

user_query = st.text_input("Enter your question:", placeholder="e.g., Which employee got more total salary?")

if st.button("🔍 Get Answer"):
    if user_query:
        with st.spinner("🤔 Thinking..."):
            try:
                result = agent.run(user_query)
                st.write("Answer:", result)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a question.")
    
    # Sample questions
with st.expander("💡 Sample Questions", expanded=False):
    st.markdown("""
    Try these example questions:
    - Which employee got more total salary?
    - How many employees are there in each department?
    - Who are the department managers?
    - What is the average salary by department?
    - Who was hired most recently?
    """)

with st.expander("View Database Schema"):
    st.code(get_table_description())
