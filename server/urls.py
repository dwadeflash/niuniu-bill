from handlers.index import IndexHandler
from handlers.login import LoginHandler

url_patterns = [
    (r"/", IndexHandler),
    (r"/login", LoginHandler)
]
