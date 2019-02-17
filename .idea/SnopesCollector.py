import sqlite3
import newspaper
import time

class ScrapeOustingNewsSite():
    def __init__(self, sleep_time=0):
        #self.url = "https://www.breitbart.com/"
        #self.url = "https://OustingNewsSite.com/"
        #self.url = "https://www.theonion.com"
        #self.url = "http://abcnews.com.co/?ts=fENsZWFuUGVwcGVybWludHx8ZjgyNTJ8YnVja2V0MDI4fHxidWNrZXQwNDV8fHx8NWM1OGJiNjgwNzhlY3x8fDE1NDkzMTkwMTYuMDM5fGI5NGEyODFkN2VlMjlhYWNkZDFmYzBjNTM4OWIzODU3NjI3NzRkY2J8fHx8fDF8fHwwfDVjNThiYjY4OGJhMTVjYmI2ZjhiNjAwYXx8fDB8fHx8fDB8MHx8fHx8fHx8fHwwfDF8NWM1OGJiNjg4YmExNWNiYjZmOGI2MDBhfDB8MHwxfDB8MHxXMTA9&query=ABC%20News%20Com&afdToken=3B1gihDjMZ-xy1sc0fXXvhLyov8rl4sDrAhpZ2hP4245Y_H3TI0yP9zO5yN7LzlHqWXvCgsJ9KjH3MIMzLBEfuGz9kvpPIiILrdHus9LES2E&pcsa=false"
        #self.url = "http://cnn.com"
        self.url = "https://foxnews.com/"
        self.connection = sqlite3.connect("FakeNews.db")
        self.cursor = self.connection.cursor()
        self.sleep_time = sleep_time


    def create_database(self):
        self.cursor.execute("CREATE TABLE articles (authors text, url text, publish_date text, title text, trustworthiness float);")
        self.connection.commit()

    def query_db(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def add_row(self, authors, title, publish_date, article_url, trustworthiness):
        query = """INSERT INTO articles(authors, url, publish_date, title, trustworthiness) VALUES (?,?,?,?,?)"""
        print(query)
        self.cursor.execute(query , (str(authors) , str(article_url) , str(publish_date) , str(title) ,str(trustworthiness)) )
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def view_table(self):
        results = self.cursor.fetchall()

        for r in results:
            print(r)

    def scrape(self):
        OustingNewsSite = newspaper.build(self.url, memoize_article=False)

        for article in OustingNewsSite.articles:

            try:
                OustingNewsSite.download()
                time.sleep(self.sleep_time)
            except:
                print("could not download")
                continue

            try:
                OustingNewsSite.parse()
            except:
                print("could not parse")
                continue

            # try:
            #     OustingNewsSite.nlp()
            # except:
            #     print("Could not use NLP")
            #     continue

            authors = article.authors
            title = article.title
            publish_date = article.publish_date
            url = article.url
            trustworthiness = 0.00

            print(str(authors) +"\n")
            print(str(title) + "\n")
            print(str(publish_date) + "\n")
            print(url)
            self.add_row(authors, title, publish_date, url, trustworthiness)
        print("end")



OustingNewsSite = ScrapeOustingNewsSite()
OustingNewsSite.scrape()
