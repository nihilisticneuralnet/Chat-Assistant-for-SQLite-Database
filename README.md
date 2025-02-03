# Chat Assistant for SQLite Database

This project is a Chat Assistant for SQLite Database built using Streamlit, SQLAlchemy, and SmolAgents. It allows users to interact with an in-memory SQLite database via natural language queries. The assistant translates user queries into SQL, executes them on the database, and returns the results.

## How It Works

- **Database Initialization**: The project uses an in-memory SQLite database, creating two tables: employees and departments.

- **Data Population**: Predefined sample data is inserted into both tables.

- **Natural Language Query Processing**:

   - Users enter questions about the database (e.g., "Who has the highest salary?").

   - A **CodeAgent** powered by **Qwen2.5-72B-Instruct** converts the question into an SQL query.

   - The query is executed using SQLAlchemy, and the results are displayed to the user.

- **Streamlit UI**: The frontend provides an interactive interface where users can input queries, get results, and explore database schemas and sample questions.


## Installation

Follow these steps to set up the project:

1. **Clone the Repository**: Run `git clone https://github.com/nihilisticneuralnet/Chat-Assistant-for-SQLite-Database.git` to clone the repository to your local machine.

2. **Install Dependencies**: Navigate to the project directory and install the required packages by running `cd <repository-directory>` followed by `pip install -r requirements.txt`. 

3. **Set Up Environment Variables**: In the `.env` file in the project root directory and insert your Gemini and Sarvam API keys as follows:
   ```plaintext
   HUGGINGFACE_TOKEN="your_huggingface_api"
   ```
   Replace `your_huggingface_api` with your actual API keys.

4. **Run the Application**: Finally, run the application using Streamlit by executing `python -m streamlit run app.py`.

Ensure you have all the necessary libraries installed before running these commands.


## Architecture Flow

<img src="img/workflow.png" /> 


## Output

<img src="img/1.png" /> 


## Known Limitations & Improvements

### Limitations

- The database is in-memory, meaning data is lost when the app is restarted.

- The assistant may misinterpret complex queries.

- It relies on Qwen2.5-72B-Instruct, which requires an internet connection.

### Suggested Improvements

- Use a persistent database (e.g., PostgreSQL, MySQL) for data retention.

- Improve query translation accuracy using additional fine-tuned LLMs.

- Enhance error handling for malformed queries.

- Add user authentication for security and access control.

- Use classic RAG Model instead of Multi-AI Agents using Faiss vector database to store database locally
