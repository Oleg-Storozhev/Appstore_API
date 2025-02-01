# Appstore_API

## Instructions for Running Locally

To set up and run the API and its associated Streamlit app locally on your machine, follow these steps:

### Prerequisites
1. **Install Python**: Ensure you have Python 3.10.16 or higher installed. You can download Python [here](https://www.python.org/downloads/).
2. **Install MongoDB**: Set up a MongoDB instance, as this API uses MongoDB for data storage.
3. **Setup Environment Variables**: Create a `.env` file and populate it with your configuration:
   - `MONGO_CLIENT`, `MONGO_DB_NAME`, `MONGO_COLLECTION_NAME`
   - `HF_KEY` (HuggingFace API key for summarization)
   - Other required information specific to your MongoDB setup.

### Steps to Run the API
1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Install Dependencies**:  
   Install all required Python packages listed in `requirements.txt` using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run MongoDB**:  
   Ensure your MongoDB service is running and the database is properly configured.

4. **Run the API**:  
   Start the API using Uvicorn:
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8001
   ```

5. **Access the API**:
   - Go to: [http://127.0.0.1:8001/healthcheck](http://127.0.0.1:8001/healthcheck) to confirm it's running.

---

### Steps to Run the Streamlit App
1. Ensure that the API is already running (`uvicorn` process as mentioned above).
2. Navigate to the project directory and start Streamlit:
   ```bash
   streamlit run streamlit_app.py
   ```
3. Access the Streamlit app in your browser at [http://localhost:8501](http://localhost:8501).  
   Use the available text inputs to interact with the API:
   - Enter the "App Name" and "App ID".
   - Perform tasks like fetching reviews, extracting metrics, or downloading reviews.

---

## Project Approach and Key Design Decisions

### Approach
The purpose of the project is to develop an API for app reviews management and a Streamlit-based front-end for visualization and interaction. The project includes tasks like fetching reviews, analyzing metrics, extracting meaningful insights, and generating actionable improvement suggestions. Here's the breakdown of key features:

1. **Fetching Reviews**: The `ReviewFetcher` component retrieves app reviews from the App Store.
2. **Storage**: All reviews are stored or updated in a MongoDB database via `MongoConnector`, ensuring data persistence.
3. **Preprocessing and Sentiment Analysis**: Reviews are pre-cleaned, and their sentiment is calculated using `TextBlob`.
4. **Metrics Calculation**: Using `MetricsCalculator`, insights such as average ratings and distribution of ratings are generated.
5. **Keyword Extraction**: For negative reviews, the `KeywordExtractor` identifies common issues using the KeyBERT library.
6. **Summarization with LLMs**: Issues are compiled and summarized into actionable suggestions by leveraging a Hugging Face-hosted LLM (`ImprovementSuggestionsSummarizer`).
7. **Usability**: The API provides endpoints for downloading reviews, generating metrics, and retrieving actionable insights.
8. **Streamlit Frontend**: The Streamlit UI allows users to interact with the API for app analysis, visualization of insights (e.g., pie charts, bar charts), and downloading results.

### Key Design Decisions
1. **Modularity**: The application is broken into logical modules (`review_fetcher`, `mongodb_connector`, `metrics_calculator`, etc.) for simplicity, reusability, and ease of testing or further extension.
2. **FastAPI Framework**: FastAPI was chosen for its speed, support for asynchronous operations, and automatic generation of API documentation.
3. **MongoDB for Storage**: MongoDB’s flexibility with schema-free documents was ideal for storing nested review structures.
4. **Streamlit for Frontend**: Streamlit was chosen for its simplicity and ability to quickly create user-friendly dashboards and interfaces.
5. **LLM for Summarization**: Hugging Face’s hosted endpoint was chosen for its reliability in generating professional and human-like improvement suggestions.
6. **Logs and Monitoring**: Using custom logging (`logger_file`) to track resource usage and errors ensures transparency during runtime.
7. **Error Handling**: Graceful error handling minimizes API crashes (e.g., during data fetching or storage).
8. **Environment Configuration**: Storing sensitive configurations (API keys, database credentials) in `.env` ensures security and flexibility for different operating environments.