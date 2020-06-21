from flask import *
from retrieve_trends import *

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():

    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("index.html", trendingSearches=get_trending_list())


@app.route("/<usr>")
def user(usr):
    if(usr == "results"):
        return render_template("results.html", trendingSearches=get_trending_list());
    else:
        return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    app.run(debug=True)