from flask import *
from retrieve_trends import *
from summary import *

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():

    if request.method == "POST":
        user = request.form["nm"]
        quantity = request.form["quant"]
        un = request.form["units"]
        country = request.form["region"]
        return redirect(url_for("user", usr=user, quant = quantity, units = un, region = country))
    else:
        return render_template("index.html", trendingSearches=get_trending_list())

@app.route("/<usr>")
def trending(usr):
    entries = get_results(usr, "1", "M", "WW")
    return render_template("results.html", trendingSearches=get_trending_list(), entries=entries)


@app.route("/<usr>/<quant>/<units>/<region>")
def user(usr,quant,units,region):
    entries = get_results(usr, quant, units, region)

    return render_template("results.html", trendingSearches=get_trending_list(), entries=entries)

if __name__ == "__main__":
    app.run(debug=True)