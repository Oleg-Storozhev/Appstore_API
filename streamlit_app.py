import streamlit as st
import requests
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8001"

st.title("App Store Review Analysis")

app_name = st.text_input("App Name:", placeholder="Enter the app name")
app_id = st.text_input("App ID:", placeholder="Enter the app ID")


def plot_pie_chart(data, title):
    labels = list(data.keys())
    sizes = list(data.values())
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    plt.title(title)
    st.pyplot(fig)


def plot_bar_chart(data, title):
    labels = list(data.keys())
    sizes = list(data.values())
    fig, ax = plt.subplots()
    ax.bar(labels, sizes, color="skyblue")
    plt.title(f"{title} Distribution")
    plt.xlabel(title)
    plt.ylabel("Count")
    st.pyplot(fig)


def call_api(endpoint, method="GET", data=None):
    url = f"{API_URL}{endpoint}"
    try:
        if method == "POST":
            response = requests.post(url, json=data)
        elif method == "GET":
            response = requests.get(url, params=data)
        else:
            return None
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Exception occurred: {e}")
        return None


if st.button("Fetch Reviews"):
    if app_name and app_id:
        result = call_api("/get_reviews", method="POST", data={"app_name": app_name, "app_id": app_id})
        if result:
            st.success("Reviews fetched successfully and saved to the database!")
    else:
        st.error("Please provide both App Name and App ID.")


if st.button("Get Review Metrics"):
    if app_name and app_id:
        result = call_api("/get_reviews_metrics", method="GET", data={"app_name": app_name, "app_id": app_id})
        if result:
            st.subheader("Metrics")
            metrics = result.get("metrics", {})
            st.json(metrics)

            st.subheader("Improvement Suggestions")
            improvement_suggestions = result.get("improvement_suggestions", "")
            st.markdown(improvement_suggestions)

            st.subheader("Ratings Distribution")
            ratings_distribution = metrics.get("ratings_distribution_count", {})
            if ratings_distribution:
                plot_bar_chart(ratings_distribution,"Ratings")

            st.subheader("Sentiment Distribution")
            sentiment_distribution = metrics.get("sentiment_distribution_count", {})
            if sentiment_distribution:
                plot_bar_chart(sentiment_distribution,"Sentiment")

            st.subheader("Ratings Distribution (Percentage)")
            ratings_count_percentage = metrics.get("ratings_count_percentage", {})
            if ratings_count_percentage:
                plot_pie_chart(ratings_count_percentage, "Ratings Distribution")

            st.subheader("Sentiment Distribution (Percentage)")
            sentiment_count_percentage = metrics.get("sentiment_count_percentage", {})
            if sentiment_count_percentage:
                plot_pie_chart(sentiment_count_percentage, "Sentiment Distribution")
    else:
        st.error("Please provide both App Name and App ID.")

if st.button("Download Reviews"):
    if app_name and app_id:
        result = requests.get(f"{API_URL}/download_reviews", params={"app_name": app_name, "app_id": app_id})
        if result.status_code == 200:
            st.download_button(
                label="Download Reviews JSON",
                data=result.content,
                file_name=f"{app_name}_reviews.json",
                mime="application/json",
            )
        else:
            st.error(f"Error: {result.status_code} - {result.text}")
    else:
        st.error("Please provide both App Name and App ID.")