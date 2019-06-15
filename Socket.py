from AnalyzeNews import ArticleReputation
from metaDataCollector import MetaDataCollector
from credibilityCalculator import CredibilityCalculator
#from Newsfeed import Newsfeed
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketIO = SocketIO(app)

@socketIO.on('connect')
def handle_connect():
    print("Connected")

@socketIO.on('link')
def handle_link(data):
    link = data['link']
    print("link: " + link)
    print(data)

    mdc = MetaDataCollector(link)
    if mdc.error:
        socketIO.emit('error', mdc.error_msg)
        print("error sent on socket")
    else:
        cc = CredibilityCalculator(link)
        socketIO.emit('analytics_report', cc.get_analytics_report())
        print("sent on socket \n")
        print(cc.analytics_report)

    # if data['newsfeedButton']:
    #     all_articles = Newsfeed(str(link))
    #     print(all_articles)
    #     socketIO.emit('reputation', all_articles.reputation())
    # else:
    #     reputation = ArticleReputation(str(link))
    #     print(reputation)
    #     socketIO.emit('reputation', reputation.reputation())

if __name__ == '__main__':
    socketIO.run(app, debug=True)

