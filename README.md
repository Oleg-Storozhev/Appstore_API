# Appstore_API

# Appstore_API

## Instructions for Running Locally

To set up and run the API locally on your machine, follow these steps:

### Prerequisites
1. **Install Python**: Ensure you have Python 3.10.16 or higher installed. You can download Python [here](https://www.python.org/downloads/).
2. **Install MongoDB**: Set up a MongoDB instance, as this API uses MongoDB for data storage.
3. **Setup Environment Variables**: Create a `.env` file and populate it with your configuration:
    - `MONGO_CLIENT`, `MONGO_DB_NAME`, `MONGO_COLLECTION_NAME`
    - `HF_KEY` (HuggingFace API key for summarization)
    - Other required information specific to your MongoDB setup.

### Steps to Run
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

## Project Approach and Key Design Decisions

### Approach
The purpose of the project is to develop an API for app reviews management, including tasks like fetching reviews, analyzing metrics, extracting meaningful insights, and generating actionable improvement suggestions. Here's the breakdown of key features:
1. **Fetching Reviews**: The `ReviewFetcher` component retrieves app reviews from the App Store.
2. **Storage**: All reviews are stored or updated in a MongoDB database via `MongoConnector`, ensuring data persistence.
3. **Preprocessing and Sentiment Analysis**: Reviews are pre-cleaned, and their sentiment is calculated using `TextBlob`.
4. **Metrics Calculation**: Using `MetricsCalculator`, insights such as average ratings and distribution of ratings are generated.
5. **Keyword Extraction**: For negative reviews, the `KeywordExtractor` identifies common issues using the KeyBERT library.
6. **Summarization with LLMs**: Issues are compiled and summarized into actionable suggestions by leveraging a Hugging Face-hosted LLM (`ImprovementSuggestionsSummarizer`).
7. **Usability**: The API provides endpoints for downloading reviews, generating metrics, and retrieving actionable insights.

### Key Design Decisions
1. **Modularity**: The application is broken into logical modules (`review_fetcher`, `mongodb_connector`, `metrics_calculator`, etc.) for simplicity, reusability, and ease of testing or further extension.
2. **FastAPI Framework**: FastAPI was chosen for its speed, support for asynchronous operations, and automatic generation of API documentation.
3. **MongoDB for Storage**: MongoDB’s flexibility with schema-free documents was ideal for storing nested review structures.
4. **LLM for Summarization**: Hugging Face’s hosted endpoint was chosen for its reliability in generating professional and human-like improvement suggestions.
5. **Logs and Monitoring**: Using custom logging (`logger_file`) to track resource usage and errors ensures transparency during runtime.
6. **Error Handling**: Graceful error handling minimizes API crashes (e.g., during data fetching or storage).
7. **Environment Configuration**: Storing sensitive configurations (API keys, database credentials) in `.env` ensures security and flexibility for different operating environments.
