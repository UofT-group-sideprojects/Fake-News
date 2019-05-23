from AnalyzeNews import ArticleReputation
# import asyncio
# import websockets
#
# async def url_response():
#     async with websockets.connect('ws://localhost:8080') as websocket:
#         url = await websocket.recv()
#         print(url)
#         print(f"< {url}")
#
#         AR = AnalyzeNews(url)
#         reputation = AR.reputation()
#
#
#         await websocket.send(reputation)
#         print(f"> {AR}")
#         print("end")
#
#
# asyncio.get_event_loop().run_until_complete(url_response())

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
    reputation = ArticleReputation(str(link))
    print(reputation)
    socketIO.emit('reputation', reputation.reputation())
if __name__ == '__main__':
    socketIO.run(app, debug=True)

