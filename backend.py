from flask import *
from retrieve_trends import *

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():

    if request.method == "POST":
        user = request.form["nm"]
        quantity = request.form["quant"]
        un = request.form["units"]
        country = request.form["region"]
        #flash(quantity);
        return redirect(url_for("user", usr=user, quant = quantity, units = un, region = country))
        #return redirect(url_for("user", usr=user))
    else:
        return render_template("index.html", trendingSearches=get_trending_list())


@app.route("/<usr>/<quant>/<units>/<region>")
def user(usr,quant,units,region):
    if(usr == "results"):
        return render_template("results.html", trendingSearches=get_trending_list())
    else:
        return f"<h1>{usr + quant + units + region}</h1>"

if __name__ == "__main__":
    app.run(debug=True)