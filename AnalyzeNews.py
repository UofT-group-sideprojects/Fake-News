
# requests to connect to the grammar check API
import requests
# Article to scrape the webpage of the given url
from newspaper import Article
# json to parse the API response
import json
# regular expressions to search the article for quotes and citations
import re

import asyncio

import socket


# async def listen(socket, path):
#     name = await socket.recv()
#     print(f"< {name}")
#
# start_server = socket.getservbyport(12345, 'localhost')
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
HOST = '127.0.0.1'
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen(1)

class ArticleReputation():
    def __init__(self):
        """
        Initialize building the reputation for an Article
        """
        self.url = ""
        #self.get_article()

    def check_grammar(self, text):
        """
        Returns number or spelling mistakes in the Article
        uses textgear API and my token

        :param text: string
        :return: int
        """
        url = "https://api.textgears.com/check.php?text=" + text + "!&key=75YaNnAeqOCH5nf7"
        response = requests.get(url)
        json_data = json.loads(response.text)
        num_of_errors = len(json_data["errors"])

        return num_of_errors

    def socket(self):
        """
        Listen for a url from chrome extension
        :return:
        """
        #print("Waiting")
        #conn1, addr1 = s.accept()
        #print('Connected by', addr1)
        print("entering while loop")
        while 1:

            conn1, addr1 = s.accept()
            #cfile = conn1.makefile('rw', 0)


            try:
                data = conn1.recv(1024)
            except socket.error:
                print('error')
            if data:
                print("Data Recieved")
                print(data.decode('utf-8'))
                self.url = data.decode('utf-8')



    def get_article(self):
        """
        Given the url of an article
        :param url:
        :return:
        """
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
        print(self.title)
        print(self.authors)

        self.grammar_mistakes = self.check_grammar(self.text)


    def reputation(self):
        """
        Calulates how likely this article is to be trust worthy
        :return:
        """
        grammar_mistakes = self.check_grammar(self.text)
        if grammar_mistakes > 0:
            print("This article has spelling mistakes")

        bad_news = self.check_bad_newsource()

        if bad_news:
            print("This article is from a source that is known for hosting unreliable news")


    def collect_quotes(self):
        """
        Return all quotes in the text of this article
        :return:
        """
        # use the regex
        quotes = re.findall('"(.*?)"', self.text)

        if quotes:
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
        Returns if the newsource is from a hardcoded list of not trustworthy news sources
        :return: boolean
        """
        bad_news_sources = ["theonion.com", "70news.wordpress.com","Abcnews.com.co",
                            "Alternativemediasyndicate.com", "Americannews.com"]
        for bad_news in bad_news_sources:
            if bad_news in self.url:
                return True

        return False

AR = ArticleReputation()
AR.socket()
#AR.get_article()
#AR.collect_quotes()
#AR.reputation()

