from flask_restx.reqparse import RequestParser


page_parser: RequestParser = RequestParser()
page_parser.add_argument(name='page', type=int, required=False)
page_parser.add_argument(name='status', type=str, required=False)
