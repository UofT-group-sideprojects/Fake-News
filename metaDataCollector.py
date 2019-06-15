from newspaper import Article
import newspaper
from nltk.corpus import stopwords
import re
import datetime
from pymongo import MongoClient

#Select Database


"""
Collect meta information from a given url, add it to the database

Step 1: identify if the url is of a news source or an article
information to collect example

url:
news_source: "the economist"
authors:
text:
title:
publish_date:
image:
keywords:
summary:
collected_by:


"""
class MetaDataCollector():
    def __init__(self, url):
        """
        Initialize an instance of Meta Data collection on the given url
        :param url:
        """
        # connection to database
        client = MongoClient()
        self.db = client['true-news']
        self.documents = self.db.documents

        # error tracking
        self.error = False
        self.error_msg = ""

        self.news_source_url = url

        self.url = url
        self.authors = None
        self.title = ""
        self.text = ""
        self.published = None
        self.images = None

        self.keywords = ""
        self.summary = ""

        self.news_source = ""

        url_split = self.url.split('://')[1].split('/')

        if '' in url_split:
            url_split.remove('')

        if len(url_split) < 1:
            self.error = True
            self.error_msg = "URL not in recognizable format"

        elif len(url_split) > 1: # URL is an article
            self.news_source = url_split[0]
            if not self.already_visited():  
                self.newspaper_article()

        else: # URL is a root or news_source
            self.news_source = url_split[0]
            if not self.already_visited(True):
                self.newspaper_newsource()
        
        if self.error:
            print(self.error_msg)

    def already_visited(self, news_source=False):
        """
        Returns True if the url is already in the Database, and collects all of the metadata from the database
        :news_source: boolean: cif True, check if the news source has already been visited, else, check the article
        :return: boolean
        """
        if news_source:
            cursor = self.db.newsSource.find_one({'news_source': self.news_source})

            if cursor:
                news_source_id = cursor["_id"]
            else:
                news_source_id = None
            if news_source_id:
                # Add news source to database
                news_source = {
                    "reliability": None, # No automated way to rank reliability at the moment
                    "reliability_source": None, # link for manual research
                    "url": self.news_source_url,
                    "news_source": self.news_source
                }

                # Add article to the article database
                try:
                    self.db.newsSource.insert_one(news_source)
                except:
                    self.error = True
                    self.error_msg = "Failed to add news source to database"


        else:
            cursor = self.documents.find_one({"url": self.url})

            if cursor:
                document_id = cursor["_id"]
            else:
                document_id = None
            if document_id:

                self.db_doc = self.db.documents.find_one({"_id": document_id})

                self.title = self.db_doc["title"]
                self.authors = self.db_doc["authors"]
                self.text = self.db_doc["text"]
                self.published = self.db_doc["publish-date"]
                # try:
                #     self.images = self.db_doc["images"]
                # except:
                #     print("This article is known but is missing the images parameter")
                try:
                    self.keywords = self.db_doc["keywords"]
                except:
                    print("This article is known but is missing the keywords parameter")
                try:
                    self.summary = self.db_doc["summary"]
                except:
                    print("This article is known but is missing the summary parameter")
                return True

            return False


    def newspaper_article(self):
        """
        Use newspaper3k to collect
        -author
        -text
        -title
        -publish_date
        -image

        :return:
        """
        self.article = Article(self.url)

        if self.newspaper_download_and_parse():

            # Meta Collection
            self.authors = self.article.authors
            self.published = self.article.publish_date
            self.text = self.article.text
            self.images = self.article.images
            self.title = self.article.title

        else:
            return self.error_msg

        if self.newspaper_nlp():
            self.keywords = self.article.keywords
            self.summary = self.article.summary

        self.add_to_database()


    def newspaper_newsource(self):
        """

        :return:
        """
        news_source = newspaper.build(self.news_source_url, language='en')

        # Number of articles that have not been scraped on this news source
        size = news_source.size()

        for article in news_source.articles:
            self.url = article.url
            self.newspaper_article()


    def add_to_database(self):
        """

        :return:
        """
        document = {
            "authors": self.authors,
            "title": self.title,
            "text": self.text,
            "url": self.url,
            "publish-date": self.published,
            # "images": self.images,
            "keywords": self.keywords,
            "summary": self.summary
        }
        # Add article to the article database
        try:
            self.documents.insert(document)
        except:
            self.error = True
            self.error_msg = "Failed to add article '" + self.title + "' to database"


    # Helper Functions

    def newspaper_download_and_parse(self):
        """
        Helper function
        :return: boolean
        """
        # Download Article
        try:
            self.article.download()
        except:
            self.error = True
            self.error_msg = "Article failed to download"
            return False

        # Parse Article
        try:
            self.article.parse()
        except:
            self.error = True
            self.error_msg = "Article failed to parse"
            return False

        return True

    def newspaper_nlp(self):
        """
        Helper Function
        :return: boolean
        """
        # Natural Language Processing on Article
        try:
            self.article.nlp()
        except:
            self.error = True
            self.error_msg = "Natural Language Processing failed on Article"
            return False

        return True

    def nltk_keywords_stopwords_removal(self):
        """
        Helper Function
        :return:
        """
        # optimization note: 'in', binary search would optimize this, look into how 'in' searches.
        self.keywords = [word for word in self.keywords if word not in stopwords.words('english')]

# MetaDataCollector("https://www.foxnews.com/")