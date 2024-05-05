from setuptools import setup, find_packages
# Import packages
import csv
import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')
import re
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.probability import FreqDist
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
import holoviews as hv
from holoviews import opts, dim

setup(
    name='chord_reviews',
    version='0.1',
    description="Process reviews data, apply text preprocessing, and generate a chord plot visualization showing word co-occurrence patterns and sentiment analysis.",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'nltk',
        're',
        'collections',
        'beautifulsoup4',
        'networkx',
        'matplotlib',
        'holoviews'
    ],
    keywords=['reviews', 'sentiment analysis', 'chord plot'],
)