from flask import *
from retrieve_trends import *
from summary import *


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        user = request.form["nm"]
        user = stripSpecial(user)
        quantity = request.form["quant"]
        un = request.form["units"]
        country = request.form["region"]
        return redirect(url_for("user", usr=user, quant = quantity, units = un, region = country))
    else:
        return render_template("index.html", trendingSearches=get_trending_list())

@app.route("/<usr>", methods=["POST", "GET"])
def trending(usr):
    return redirect(url_for("user", usr=usr, quant="7", units="D", region="WW"));


@app.route("/<usr>/<quant>/<units>/<region>", methods=["POST", "GET"])
def user(usr,quant,units,region):
    if region != "CA" and region != "US" and region != "UK" and region != "WW":
        return redirect(url_for("trending", usr=usr))

    entries = get_results(usr, quant, units, region)
    if request.method == "POST":
        user = request.form["nm"]
        user = stripSpecial(user)
        quantity = request.form["quant"]
        un = request.form["units"]
        country = request.form["region"]
        return redirect(url_for("user", usr=user, quant = quantity, units = un, region = country))
    else:
        return render_template("results.html", trendingSearches=get_trending_list(), entries=entries)

if __name__ == "__main__":
    from gevent import monkey
    monkey.patch_all()
    app.run(debug=True)