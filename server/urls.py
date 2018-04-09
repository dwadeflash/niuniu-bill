from handlers.index import IndexHandler
from handlers.login import LoginHandler
from handlers.create import CreateHandler
from handlers.list import ListHandler
from handlers.approve import ApproveHandler

url_patterns = [
    (r"/", IndexHandler),
    (r"/login", LoginHandler),
    (r"/create", CreateHandler),
    (r"/list", ListHandler),
    (r"/approve", ApproveHandler)
]
