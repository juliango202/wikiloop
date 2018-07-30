import logging
from flask import Flask
from flask import jsonify
from flask import request

from WikipediaLinkFollower import follow_between
from errors import FollowerError


logging.basicConfig(filename="api.log", level=logging.INFO)
app = Flask(__name__)


@app.route("/")
def hello():
    return "Server is up!"


@app.route("/api/wikiloop", methods=["POST"])
def compute_wikiloop():
    try:
        data = request.get_json()
        path = follow_between(data["start_url"], data["stop_url"])
        return jsonify(journey=path)
    except FollowerError as exc:
        return jsonify(exc.serialize())
    except Exception as exc:
        logging.error(exc)
        logging.error("OUHOUH")
        return jsonify(error="Oups. There was an unexpected server error."), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
