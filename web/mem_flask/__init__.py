from flask import Flask

server = Flask(__name__)

server.config['DEBUG'] = True

from web.mem_flask import routes
