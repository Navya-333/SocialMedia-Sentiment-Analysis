import streamlit as st
from textblob import TextBlob
import pickle
from os import path
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

def clean_Text(Text):
    Text = re.sub(r'https?://\S+|www\.\S+', '', Text)
    Text = re.sub(r'@[^\s]+', '', Text)
    Text = re.sub(r'#', '', Text)
    Text = re.sub(r'[^\w\s]', '', Text)
    Text = Text.lower()
    words = Text.split()
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    return " ".join(words)

def analyze_sentiment(Text):
    analysis = TextBlob(Text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

st.markdown("<h1 style='text-align: center; color:rgb(255, 0, 119);'>Social Media Sentiment Analysis App</h1>", unsafe_allow_html=True)

st.markdown("""
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
        }
        h1 {
            color:rgb(255, 0, 144);
        }
        .button {
            background-color:rgb(255, 0, 166);
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .button:hover {
            background-color:rgb(217, 0, 137);
        }
    </style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        if 'Text' not in data.columns:
            st.error("The CSV file must contain a column named 'Text'.")
        else:
            data['cleaned_Text'] = data['Text'].apply(clean_Text)
            data['Sentiment'] = data['cleaned_Text'].apply(analyze_sentiment)
            st.write(data.head(33))
            sentiment_counts = data['Sentiment'].value_counts()
            st.bar_chart(sentiment_counts)
            st.download_button(
                label="Download updated CSV",
                data=data.to_csv(index=False).encode('utf-8'),
                file_name='sentiment_analyzed_data.csv',
                mime='Text/csv',
            )
    except Exception as e:
        st.error(f"An error occurred: {e}")

message = st.text_input("Enter text to analyze:")
if st.button("Analyse the Sentiment"):
    blob = TextBlob(message)
    sentiment = blob.sentiment.polarity
    result = blob.sentiment
    st.write(result)
    polarity = result.polarity
    subjectivity = result.subjectivity
    if polarity < 0:
        st.image("c:/Users/navya/Downloads/WhatsApp Image 2025-03-01 at 19.57.00_0ac23897.jpg")
        st.warning("The entered text has negative sentiments associated with it"+str(polarity))
    elif polarity > 0:
        st.image("c:/Users/navya/Downloads/WhatsApp Image 2025-03-01 at 19.57.00_86607d84.jpg")
        st.success("The entered text has positive sentiments associated with it."+str(polarity))
    else:
        st.image("c:/Users/navya/Downloads/WhatsApp Image 2025-03-01 at 19.57.00_ef91791e.jpg")
        st.write("The entered text has neutral sentiments associated with it."+str(polarity))

