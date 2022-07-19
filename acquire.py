import pandas as pd
from requests import get
from bs4 import BeautifulSoup
import os

#Getting Codeup Blog Data:

def get_blog_articles(urls, refresh = False):
    
    codeup_articles = []
    
    #Checks whether there is already a CSV or if user wants to refresh data:
    if not os.path.isfile('blog_articles.csv') or refresh:
        
        for url in urls:
            #Creating an empty dataframe to store lists of article data components:
            #article_info = pd.DataFrame()
            headers = {'User-Agent': 'Codeup Data Science'}
            response = get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string
            contents = soup.select(".entry-content")
            #Creating a dictionary entry for current article:
            article_info = {
                'url' : url,
                'title' : title,
                'contents' : contents
            }
            #Converting article dictionary to DataFrame:
            article_info = pd.DataFrame(article_info)
            #Appending dictionary entry for current article onto list of blog info:
            codeup_articles.append(article_info)
            
        #Concatenating all of the DataFrames in the list to create one large DataFrame:
        codeup_articles = pd.concat(codeup_articles)
        #Writes the total DataFrame to a CSV for caching:
        codeup_articles.to_csv('blog_articles.csv', index = False)
        
    return codeup_articles


#Getting News Article Data:

def get_shorts_articles(categories, refresh = False):
        
    #Creating an empty list to contain DataFrames of scraped data components:
    inshorts_articles = []
    
    #Checks whether there is already a CSV or if user wants to refresh data:
    if not os.path.isfile('news_articles.csv') or refresh:

        #Establishing a for-loop to iterate through desired categories:
        for category in categories:
            #Creating an empty dataframe to store lists of article data components:
            article_info = pd.DataFrame()
            #Establishing baseline url and using format string to iterate through categories:
            url = f'https://inshorts.com/en/read/{category}'
            #Establishing header so it doesn't look like 'python-request':
            headers = {'User-Agent': 'Codeup Data Science'}
            #saving the response from the website:
            response = get(url, headers=headers)
            #Creating a beautiful soup object to contain the HTML information from the page:
            soup = BeautifulSoup(response.content, 'html.parser')
            # creating a list of all titles in the given category:
            titles = soup.find_all(itemprop = 'headline')
            #Creating a list of all article bodies in the given category
            contents = soup.find_all(itemprop = 'articleBody')
            #Adding 'title' column to DataFrame containing title text for each article:
            article_info['title'] = [title.text for title in titles]
            #Adding 'contents' column to DataFrame containing article body text for each article
            article_info['contents'] = [content.text for content in contents]
            #Adding 'category' column to list category for each article in the category:
            article_info['category'] = category
            #Appending DataFrame for each category to overall list of DataFrames:
            inshorts_articles.append(article_info)

        #Concatenating all of the DataFrames in the list to create one large DataFrame:
        inshorts_articles = pd.concat(inshorts_articles)
        #Writes the total DataFrame to a CSV for caching:
        inshorts_articles.to_csv('news_articles.csv', index = False)
        #Returning final DataFrame:
    return inshorts_articles