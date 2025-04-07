import streamlit as st
import requests

# API configuration
API_KEY = "CS2iq3kE5NTmtA97BjhkmprNEya6EuQH"
API_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"

# Static instruction prompt for SQL query generation
static_context = """
You are an expert SQL assistant. Convert the following natural language question into a syntactically correct SQL query. 
Use standard SQL (MySQL/PostgreSQL style), unless a specific dialect is mentioned.
Assume the database contains relevant columns and use best practices.
Only return the SQL query as output. Do not add explanations or notes.
"""

def call_mistral_api(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "open-mixtral-8x22b",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("choices", [])[0].get("message", {}).get("content", "")
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except (IndexError, KeyError) as e:
        return f"Unexpected response format: {e}"

def main():
    st.markdown(
        """
        <h1 style='text-align: center;'>SQL Query Builder</h1>
        <h3 style='text-align: center; font-weight: normal;'>Describe your query in English and get a working SQL statement!</h3>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.header("Enter your query description in English")
    query_description = st.text_area(
        "Describe what you want to do with the database:",
        placeholder="e.g., Get the names of all customers who placed more than 3 orders last month."
    )

    if st.button("Generate SQL Query"):
        if not query_description.strip():
            st.error("Please enter a query description.")
            return

        prompt = f"{static_context}\n\nNatural Language Input:\n{query_description}"
        sql_result = call_mistral_api(prompt)
        st.markdown("### Generated SQL Query")
        st.code(sql_result, language='sql')

if __name__ == "__main__":
    main()
