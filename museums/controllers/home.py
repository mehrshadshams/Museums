from flask import redirect
from museums import app


@app.route("/", methods=["GET"])
def index():
    return redirect('/api')
