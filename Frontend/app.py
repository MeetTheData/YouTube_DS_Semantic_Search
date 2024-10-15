import streamlit as st
import requests
import json

# Apply custom styles
st.markdown("""
    <style>
        h1 {
            color: #FF6347;  /* Tomato color */
            font-family: 'Arial', sans-serif;
            text-align: center;
        }
        .stTextInput > div > div > input {
            background-color: #F0F8FF;  /* Light cyan */
            border: 2px solid #FF6347;  /* Tomato border */
            padding: 5px;
            font-family: 'Courier New', monospace;
        }
        .stButton > button {
            background-color: #FF6347;  /* Tomato */
            color: white;
            font-weight: bold;
            cursor: pointer;
            border: 1px solid #F0F8FF;  /* Light cyan border */
        }
        .stMarkdown {
            color: #2F4F4F;  /* Dark slate gray */
            font-family: 'Georgia', serif;
        }
    </style>
""", unsafe_allow_html=True)

headers = {
    "authorization": st.secrets["GCR_API_URL_KEY"],
    "content-type": "application/json"
}

def callSearchAPI(query: str) -> dict:
    """
    Call search API hosted on AWS
    """
    url = st.secrets["GCR_API_URL_KEY"]
    params = {"query": query}
    response = requests.get(url + "/search", params=params, headers=headers)
    return json.loads(response.text)

def formatResultText(title: str, video_id: str):
    """
    Function to format video title and id as markdown
    """
    return f"### {title}\n🔗 [Video Link](https://youtu.be/{video_id})"

def formatVideoEmbed(video_id: str):
    """
    Function to generate video embed from video_id
    """
    return f'<iframe width="576" height="324" src="https://www.youtube.com/embed/{video_id}"></iframe>'

def searchResults(query):
    """
    Function to perform search and display results
    """
    response = callSearchAPI(query)
    
    if not response.get('title'):
        st.write("No results. Try rephrasing your query.")
    else:
        for i in range(len(response['title'])):
            video_id = response['video_id'][i]
            title = response['title'][i]
            
            st.markdown(formatResultText(title, video_id), unsafe_allow_html=True)
            st.components.v1.html(formatVideoEmbed(video_id), height=324)
            st.markdown("---")

# Streamlit app
st.title("YouTube Search")

query = st.text_input("What are you looking for?", key="search_query")
search_button = st.button("Search")

if search_button or query:
    searchResults(query)