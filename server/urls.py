from handlers.index import IndexHandler
from handlers.login import LoginHandler
from handlers.create import CreateHandler
from handlers.list import ListHandler
from handlers.approve import ApproveHandler
from handlers.relation import MakeRelationHandler
from handlers.relation import QueryRelationHandler
from handlers.relation import AcceptRelationHandler

url_patterns = [
    (r"/", IndexHandler),
    (r"/login", LoginHandler),
    (r"/create", CreateHandler),
    (r"/list", ListHandler),
    (r"/approve", ApproveHandler),
    (r"/makerelation", MakeRelationHandler),
    (r"/queryrelation", QueryRelationHandler),
    (r"/acceptrelation", AcceptRelationHandler)
]
