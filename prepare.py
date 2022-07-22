import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import acquire

def basic_clean(string):
    '''
    Takes in a string, and returns a normalized
    version of the string for use in NLP.
    '''
    #lowercases all letters in the string:
    string = string.lower()
    #Removes any special characters and normalizes them into their regular forms:
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    #Replaces anything that is not a letter, number, whitespace, or single quote:
    string = re.sub(r"[^\da-z\'\s]", '', string)
    return string

def tokenize(string):
    '''
    Takes ina string and tokenizes all of
    the words in the string (breaking them
    into discrete units). 
    '''
    #Creating the tokenizer object:
    tokenizer = nltk.tokenize.ToktokTokenizer()
    #Usign the tokenizer on the string:
    string = tokenizer.tokenize(string, return_str=True)
    #returning tokenized string:
    return string

def stem(string):
    '''
    Takes in a string, returns the string with 
    all words reduced to their root forms.
    '''
    #Creating the stemmer object:
    ps = nltk.porter.PorterStemmer()
    #Creating a list of stemmed words:
    stems = [ps.stem(word) for word in string.split()]
    #Joining stemmed words into list into one contiguous string:
    string_stemmed = ' '.join(stems)
    #returning string of stemmed words:
    return string_stemmed

def lemmatize(string):
    '''
    Takes in a string, returns a LIST with
    all words reduced to their root *words*.
    '''
    #Creating the lemmatizer object:
    wnl = nltk.stem.WordNetLemmatizer()
    #Applying the lemmatizer to every word in the string:
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    #Returning list of lemmatized words:
    return lemmas

def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    Takes in a string, removes stopwords, and returns
    a string that does not contain those stopwords. 
    Optional arguments to add extra stopwords or to 
    add words that should not be considered stopwords.
    '''
    #Creating a list of stopwords from NLTK's standard list:
    stopword_list = stopwords.words('english')
    #Creating a list of words by splitting the string:
    words = string.split()
    #Saving words to list if they are not in stopword list:
    filtered_words = [w for w in words if w not in stopword_list]
    #Joining all words in list of non-stopwords:
    string_without_stopwords = ' '.join(filtered_words)
    #Returning string with stopwords removed:
    return string_without_stopwords

def prep_text_data(df, column, extra_words = [], exclude_words = []):
    '''
    Takes in a DataFrame and a column name in string format, optionally 
    including lists of extra_words and exclude_words. Returns
    a DataFrame with columns listing the title, body of text, 
    stemmed text, lemmatized text, and the cleaned, tokenized, 
    and lemmatized text with stopwords removed. 
    '''
    
    #Creating a column named 'cleaned' that has the following cleaning functions applied to the text:
    df['cleaned'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords,
                                  extra_words=extra_words,
                                  exclude_words=exclude_words)
    
    #Creating a separate column that has the stemmed version of the cleaned text:
    df['stemmed'] = df['cleaned'].apply(stem)
    
    #Creating a separate column that has the lemmatized version of the cleaned text:
    df['lemmatized'] = df['cleaned'].apply(lemmatize)
    
    #returning the DataFrame's new columns:
    return df[['id', column, 'cleaned', 'stemmed', 'lemmatized']]

