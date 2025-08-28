# backend/extrinsic_detector.py
import requests
from bs4 import BeautifulSoup

def check_extrinsic_plagiarism(text):
    """
    Checks for extrinsic plagiarism by searching for the text on the web.
    :param text: The text to check for plagiarism
    :return: Boolean indicating if plagiarism is detected
    """
    # URL encode the text for search
    search_query = '+'.join(text.split())
    url = f"https://www.google.com/search?q={search_query}"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    # Send the request to Google search (or another engine/API)
    response = requests.get(url, headers=headers)
    
    # Parse the response (this is a basic web scraping method; could be improved with APIs)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    
    # Check if there are links in the search results matching the text
    for link in links:
        if link.get('href') and text.lower() in link.get('href').lower():
            return True  # Plagiarism detected
    
    return False