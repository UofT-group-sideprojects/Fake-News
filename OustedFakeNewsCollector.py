import newspaper
import re

ousting_sites = [
    "https://www.cnn.com/",
    "https://www.economist.com/"
]
"""
This class endlessly scrapes data from the given urls and adds the info to the database
under the assumption that all of the articles found are known 'fake news'

Areas to focus on:
    -  Making certain that only fake news articles are actually added
"""
class GatherFakeNews():

    def __init__(self, list_of_ousting_sites: list) -> None:
        """
        Initialize the gathering of fake news articles
        """
        self.sites = list_of_ousting_sites
    
    def start(self) -> None:
        """
        Start the process of scraping and collecting from the given sites
        :return: 
        """
        for url in self.sites:
            site = newspaper.build(url)
            
            for article in site.articles:
                if self.in_database(article):
                    # Maybe update?
                    continue

                successful = self.download(article)
                # ToDo: check if the article being processed in another method affect what can be called on article here

                meta_data = self.collect_meta_data(article, successful)
                        
                self.add_to_database(meta_data)
                
    def download(self, article) -> dict:
        """
        Returns the success status of the Download, parsing and nlp on the given article
        
        :param article: 
        :return: dict of fixed params 
        """
        # Track what failed to avoid calling methods that cannot be used
        download_success = True
        parse_success = True
        nlp_success = True

        # download the html of the article
        try:
            article.download()
        except:
            download_success = False

        # ToDo: check if parse is reliant on download
        if download_success != False:
            try:
                article.parse()
            except:
                parse_success = False
                
        # ToDo: check if nlp is reliant on parse  
        if parse_success != False:
            try:
                article.nlp()
            except:
                nlp_success = False
                
        return {"download": download_success, "parse": parse_success, "nlp": nlp_success}

    def collect_meta_data(self, article, successful):
        """
        Must be called after 'download', collects and returns the meta_data of the given article
        :param article:
        :return:
        """
        if not successful["download"]:
            return article

        title = article.title
        keywords = None
        authors = None

        # ToDo: could cause overlap. untested
        quote_regexes = ["\(\D*\d{4}(;\D*\d{4})*\)", "[A-Z]\w+ \(\d{4}\)", "[A-Z]\w+ +\(\d{4}:\d+\)"]
        # ToDo: place title into grammar check API
        # ToDo: place text into grammar check API (is this in parse? or after download?

        if successful["parse"]:
            # ToDo: whatever can be done after being only parsed
            collected_regexes = self.find_regexes(quote_regexes, article)


        # if successful["nlp"]:
            # keywords = article.keywords()
            #keywords = self.filter_keywords(keywords)
            #  ToDo: all nlp required data gathering
        print("Title: " + str(title))
        print("\n Authors: " + str(authors))
        #print("\n Keywords: " + str(keywords))
        print("\n Collected_regexes: ")
        for collected in collected_regexes:
            print(collected + "\n")


    def find_regexes(self, regexes, article):
        """
        Return all words that match the regex in the Article

        :param regex: list of strings
        :param article:
        :return: dict with "text" and "title" matches
        """
        matches = {"text": [], "title": []}
        for regex in regexes:
            matches["text"].extend(re.findall(regex, article.text))
            matches["title"].extend(re.findall(regex, article.title))

        return matches

    def filter_keywords(self, keywords):
        """
        Returns filtered and lemonized keywords

        :param keywords:
        :return:
        """
        # ToDo: use lemonizer, filter stop words
        return keywords

    def add_to_database(self, meta_data):
        """
        Add the already gathered meta_data to the database

        :param meta_data:
        :return:
        """
        return None

    def in_database(self, article):
        """
        Returns if this article is already in the database

        :param article:
        :return: boolean
        """
        return False

gather = GatherFakeNews(ousting_sites)
gather.start()
