import newspaper

# ToDo: maybe I should keep the web crawling to one class with all of the methods for affiliation, adding to database, updating etc...
"""
Scrape news sources with known political affiliation. add the articles if they are not in the database,
add affiliation if article is know but databse is not

To keep in mind, if an article is politically affiliated, it does not mean that the article itself represents that view
"""
class PoliticalAffiliationCollector():

    def __init__(self, affiliation, url_list):
        """

        :param affiliation:
        :param url_list:
        """
        self.affiliation = affiliation
        self.url_list = url_list

    def start(self):
