from setuptools import setup, find_packages

setup(
    name='chord_reviews',
    version='0.1.1',
    description="Process reviews data, apply text preprocessing, and generate a chord plot visualization showing word co-occurrence patterns and sentiment analysis.",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'nltk',
        'collections',
        'beautifulsoup4',
        'networkx',
        'matplotlib',
        'holoviews'
    ],
    keywords=['customer reviews', 'sentiment analysis', 'chord plot'],
)