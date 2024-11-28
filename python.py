from spellchecker import SpellChecker
from textblob import TextBlob

# Initialize Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia('en')

# Fetch the article
page = wiki_wiki.page('Python (programming language)')

# Check if the page exists
if page.exists():
    # Print the title and summary of the article
    print("Title: ", page.title)
    print("Summary: ", page.summary[:60])  # Print first 60 characters of the summary
else:
    print("The page does not exist.")