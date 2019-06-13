from nltk.corpus import stopwords, sentiwordnet as swn
import requests
import json
import re
from pymongo import MongoClient

#Select Database
client = MongoClient()
db = client['true-news']

"""
The heart and soul of this app.
Analyze the meta data of an article to build a credibility score.
Identify what information a reader should know about the article they are viewing


Information about each parameter

url:
    Find the root of the url and save it as a news source or as another url for an existing news source

authors:
    compare names to a list of known names to improve collection

text:

title:
    Emotion words. Less reliable if the title is emotion capturing,
    Spelling Mistakes,
    exclamation marks/over capitalized

publish_date:
image:
    reverse image search, find largest quality image as initial source. (Does this affect originality/reliability)

keywords:
    remove stop words,
    stemming m
summary:
collected_by:

credibility score:

title:

"""
class CredibilityCalculator:
    def __init__(self, url):
        """
        Initialize an instance of the credibility calculator
        """
        self.credibility_score = None

        self.title = None
        self.authors = None
        self.text = None
        self.published = None
        self.images = None
        self.keywords = None
        self.summary = None

        self.db_doc = None

        try:
            self.getMetaData()
        except:
            print('MetaData was not collected from database')

        self.analytics_report = {
            "title": {
                "grammar": None,
                "emotion": None
            },
            "news_source": {
                "political_leaning": None,
                "reliability": None,
                "reliability_source": None
            },

        }


    def getMetaData(self):
        """
        Collect metaData from database
        :return:
        """
        document_cursor = db.documents.find_one({"url": self.url})
        if document_cursor:
            document_id = document_cursor["_id"]
        else:
            document_id = None
        if document_id:
            self.db_doc = db.documents.find_one({"_id": document_id})

            self.title = self.db_doc["title"]
            self.authors = self.db_doc["authors"]
            self.text = self.db_doc["text"]
            self.published = self.db_doc["publish-date"]
            self.images = self.db_doc["images"]

            self.keywords = self.db_doc["keywords"]
            self.summary = self.db_doc["summary"]

    def title_analytics(self):
        """
        Return the credibility of the title from 0-1. 0 Is credible, 1 is not.
        analyses emotion words, spelling mistakes and exclamations
        :return: float
        """
        grammar_mistakes = self.grammar_mistakes(self.title)
        title_emotion = self.nltk_emotion_words(self.title)
        emotion_score = title_emotion["score"]
        emotion_words = title_emotion["emotion_analytics"]
        self.analytics_report["title"]["grammar"] = grammar_mistakes
        self.analytics_report["title"]["emotion"] = emotion_words

        grammar_score = len(grammar_mistakes)/len(self.title)

        title_credibility = (emotion_score + grammar_score + self.check_exclamation())/3
        return title_credibility

    def news_source_analytics(self):
        """
        Return credibility of the news source
        :return:
        """
        document_cursor = db.newsSource.find_one({"news_source": self.news_source})
        if document_cursor:
            news_source_id = document_cursor["_id"]
        else:
            news_source_id = None

        if news_source_id:
            self.db_news = db.newsSource.find_one({"_id": news_source_id})

            # add 'reliable' to database, indicating if the source is reliable and where the decision came from
            reliability_score = self.db_news["reliable"]
            if reliability_score == 1: # reliable
                self.analytics_report["reliability"] = "This news source is reliable"
            elif reliability_score == 0: # unknown
                self.analytics_report["reliability"] = "The reliability of this news source is unknown"
            else: # not reliable
                self.analytics_report["reliability"] = "This news source is not reliable"

            # where the decision was made to mark the reliability
            self.analytics_report["reliability_source"] = self.db_news["reliable_source"]

        # political_leaning
        # use media bias fact checker as source. look at how the chrome extension gathers this info

    def nltk_emotion_words(self, text):
        """
        Helper Function

        Returns the average score of emotion words
        :return:
        """
        text = text.split(" ")

        emotion_words = {}

        emotion_score = 0
        words_counted = 0
        for word in text:
            if word in stopwords.words('english'):
                continue

            analyzed_word = swn.senti_synset(word)

            pos_score = analyzed_word.pos_score()
            neg_score = analyzed_word.neg_score()
            obj_score = analyzed_word.obj_score()
            emotion_score += pos_score
            emotion_score += neg_score
            # emotion_score += obj_score

            # build the analytics report
            emotion_words[word] = {
                "pos_score": pos_score,
                "neg_score": neg_score,
                "obj_score": obj_score
            }

        score = emotion_score / words_counted
        return {"emotion_analytics": emotion_words, "score": score}

    def check_grammar(self, text):
        """
        Helper Function

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
        # num_of_errors = len(json_data["errors"])
        return json_data["errors"]

    def check_exclamation(self, text):
        """
        Helper Function

        Return 0 if there is no exclamation mark, 1 if there is.
        :return: int
        """
        for char in text:
            if char == "!":
                return 1
        return 0