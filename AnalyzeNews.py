
# requests to connect to the grammar check API
import requests
# Article to scrape the webpage of the given url
from newspaper import Article
# json to parse the API response
import json
# regular expressions to search the article for quotes and citations
import re

import socket

import pprint

from pymongo import MongoClient

#Server
# import http.server
# import socketserver
#
# PORT = 8080
# Handler = http.server.SimpleHTTPRequestHandler
#
# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()
#end of server

import sys

client = MongoClient()
db = client['true-news']


# async def listen(socket, path):
#     name = await socket.recv()
#     print(f"< {name}")
#
# start_server = socket.getservbyport(12345, 'localhost')
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
# HOST = '127.0.0.1'
# PORT = 12345
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#
# s.bind((HOST, PORT))
# s.listen(1)

class ArticleReputation():
    def __init__(self,url=""):
        """
        Initialize building the reputation for an Article
        """
        self.url = url
        self.credible_host = 0 #0 is an unknown host, -1 is an unreliable host, 1 is a reliable host (host is the site the news is hosted on)
        self.documents = db.documents
        self.get_article()
        self.reputation()


    def check_grammar(self, text):
        """
        Returns number or spelling mistakes in the Article
        uses textgear API and my token

        :param text: string
        :return: int
        """
        url = "https://api.textgears.com/check.php?text=" + text + "!&key=75YaNnAeqOCH5nf7"
        response = requests.get(url)
        try:
            json_data = json.loads(response.text)
        except:
            print("JSON data from grammar check could not be loaded")
            return 0
        num_of_errors = len(json_data["errors"])
        return num_of_errors

    def add_article_to_db(self):
        """
        Add a document of the articles information to the database

        :return:
        """
        document = {
            "authors":  self.authors,
            "title": self.title,
            "text": self.text,
            "url": self.url,
            "publish-date": self.publish_date
        }
        if self.credible_host == 1:
            document_id = self.reliable.insert_one(document).inserted_id
            self.documents.insert_one(document).inserted_id
        elif self.credible_host == 0:
            document_id = self.documents.insert_one(document).inserted_id
        else:
            document_id = self.unreliable.insert_one(document).inserted_id
            self.documents.insert_one(document).inserted_id

        print(document_id)
        return document_id

    # def socket(self):
    #     """
    #     Listen for a url from chrome extension
    #     :return:
    #     """
    #     #print("Waiting")
    #     #conn1, addr1 = s.accept()
    #     #print('Connected by', addr1)
    #     print("entering while loop")
    #     conn1, addr1 = s.accept()
    #     while 1:
    #         #cfile = conn1.makefile('rw', 0)
    #
    #         try:
    #             data = conn1.recv(1024)
    #         except socket.error:
    #             print('error')
    #         if data:
    #             print("Data Recieved")
    #             print(data.decode('utf-8'))
    #             self.url = data.decode('utf-8')



    def get_article(self):
        """
        Given the url of an article
        :param url:
        :return:
        """

        document_cursor = db.documents.find_one({"url": self.url})
        if document_cursor:
            document_id = document_cursor["_id"]
        else:
            document_id = None
        if document_id:
            print("This article was already in the database")
            self.db_doc = db.documents.find_one({"_id": document_id})
            self.title = self.db_doc["title"]
            self.authors = self.db_doc["authors"]
            self.text = self.db_doc["text"]
            self.publish_date = self.db_doc["publish-date"]
            return None

        self.article = Article(self.url)
        grammar_mistakes = self.check_grammar(self.article.title)

        # try to download the article
        try:
            self.article.download()
        except:
            print("couldnt download")
            return None

        # try to parse the article
        try:
            self.article.parse()
        except:
            print("couldnt parse")
            return None

        # Try to use nlp on the article
        try:
            self.article.nlp()
        except:
            print("couldnt use nlp")
            return None

        self.title = self.article.title
        self.authors = self.article.authors
        self.text = self.article.text
        self.publish_date = self.article.publish_date
        print(self.title)
        print(self.authors)

        #self.grammar_mistakes = self.check_grammar(self.text)

        # document_cursor = db.documents.find_one({"url": self.url})
        # if document_cursor:
        #     document_id = document_cursor["_id"]
        # else:
        #     document_id = None
        # if document_id:


        document_id=self.add_article_to_db()

        for author in self.authors:
            author_cursor = db.authors.find_one({"author":author})

            if author_cursor:
                #author_id = author_cursor["_id"]
                if document_id != author_cursor["known_articles"]:
                    db.authors.updateOne({"author":author},{"known_articles":author_cursor["known_articles"].extend(document_id)})
            else:
                db.authors.insert_one({
                    "author": author,
                    "known_articles": [document_id]
                })

    def reputation(self):
        """
        Calulates how likely this article is to be trust worthy
        :return:
        """
        rep_dict = {}

        if self.text != "":
            grammar_mistakes = self.check_grammar(self.text)
            if grammar_mistakes > 0:
                print("This article has "+ str(grammar_mistakes)+" spelling mistakes")
                rep_dict["grammar_mistakes"] = "This article has "+ str(grammar_mistakes)+" spelling mistakes"
            else:
                print("This article does not have any spelling mistakes")
                rep_dict["grammar_mistakes"] = "This article does not have any spelling mistakes"

        bad_news = self.check_bad_newsource()
        reliable_news = self.check_reliable_news()

        if bad_news:
            print("This article is from a source that is known for hosting unreliable news")
            rep_dict["news_source"] = "This article is from a source that is known for hosting unreliable news"
        elif reliable_news:
            print("This article is from a reliable news source")
            rep_dict["news_source"] = "This article is from a reliable news source"
        else:
            print("This article is hosted on an unknown news source")
            rep_dict["news_source"] = "This article is hosted on an unknown news source"
        return rep_dict


    def collect_quotes(self):
        """
        Return all quotes in the text of this article
        :return:
        """
        # use the regex
        quotes = re.findall('"(.*?)"', self.text)

        if quotes:
            print(quotes)
            return quotes

    def hoaxy_api_lookup(self, query):
        """
        Return information about the article's meta data from hoaxy_api:
        More info: https://rapidapi.com/truthy/api/hoaxy
        :return:

        header = "default-application_3628393"
        xkey = "a2412dd557mshf6c4ce57635dc78p1daa1bjsna5cf0cfd6317"
        URL = "https://api-hoaxy.p.rapidapi.com/articles?sort_by=relevant&use_lucene_syntax=true&query"
                                "=pizzagate+AND+date_published%3A%5B2016-10-28+TO+2016-12-04%5D",
        header=("X-RapidAPI-Key", "a2412dd557mshf6c4ce57635dc78p1daa1bjsna5cf0cfd6317"))

        """
        #ToDo:
        return None

    def check_fake_news_detector(self):
        """
        Return information if article is in fake news detector database.
        more info https://github.com/fake-news-detector/fake-news-detector/blob/master/api/README.md

        (currently look up has been unsuccessful)
        :return:
        """
        response = requests.get("https://api.fakenewsdetector.org/link/all",)
        if response.status_code == 200:
            x = json.loads(response.text)
            return x
        else:
            return None

    def check_bad_newsource(self):
        """
        Returns True if the newsource is from a hardcoded list of not trustworthy news sources
        Based on https://www.marketwatch.com/story/these-are-the-most-and-the-least-trusted-news-sources-in-the-us-2017-08-03
        :return: boolean
        """
        bad_news_sources = ["theonion.com", "70news.wordpress.com","Abcnews.com.co",
                            "Alternativemediasyndicate.com", "Americannews.com"]
        for bad_news in bad_news_sources:
            if bad_news in self.url:
                self.credible_host = -1
                return True

        return False

    def check_reliable_news(self):
        """
        Returns True if the news source is from a hardcoded list of reliable news sources
        Based on https://www.marketwatch.com/story/these-are-the-most-and-the-least-trusted-news-sources-in-the-us-2017-08-03
        :return: boolean
        """
        reliable_news_sources = ["economist.com","reuters.com","bbc.com","npr.org","pbs.org","theguardian.com","wsj.com","latimes.com"]
        for reliable_news in reliable_news_sources:
            if reliable_news in self.url:
                self.credible_host = 1
                return True

        return False

#AR = ArticleReputation("https://educateinspirechange.org/nature/earth/cigarette-butts-are-the-oceans-single-largest-source-of-pollution/?fbclid=IwAR1z7VY0ZNpG2JkcWrRixiJvt2G0HAnX-3JTGnU6MLD4meO3jF5zhjzhRVc")
# AR.authors = "test_authors"
# AR.title = "test title"
# AR.text = "test text"
#AR.get_article()
#AR.add_article_to_db()
#AR.socket()
#AR.get_article()
# AR.collect_quotes()
# AR.reputation()

