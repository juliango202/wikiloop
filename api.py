import logging
from flask import Flask

from WikipediaLinkFollower import WikipediaLinkFollower

logging.basicConfig(filename='api.log',level=logging.DEBUG)
app = Flask(__name__)


@app.route("/")
def hello():
    l_follow = WikipediaLinkFollower("https://en.wikipedia.org/wiki/Water", "https://en.wikipedia.org/wiki/Philosophy")
    return 'OK'

