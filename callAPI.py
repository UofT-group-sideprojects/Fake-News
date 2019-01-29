import requests
#grammar mistakes = "https://api.textgears.com/check.php?text=I+is+an+engeneer!&key=75YaNnAeqOCH5nf7"


class callAPI():

    def __init__(self, endpoint, query=""):
        self.endpoint = endpoint
        self.query = query