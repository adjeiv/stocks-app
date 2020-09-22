import os
import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from stock_graph import create_plot
from bokeh.embed import components
import itertools
from news import get_news

API_KEY = ""

symbol_list = list(pd.read_csv("symbols.csv", names=["sym"])["sym"])

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "stocks.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Company(db.Model):
    __tablename__ = "STOCKS"

    country = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(255), nullable=False)
    exchange = db.Column(db.String(255), nullable=False)
    ipo = db.Column(db.Integer, nullable=False)
    marketCapitalization = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    shareOutstanding = db.Column(db.Integer, nullable=True)
    ticker = db.Column(db.String(255), nullable=False, primary_key=True)
    weburl = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=False)
    finnhubIndustry = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<Company name: {}>".format(self.name)

companies = Company.query.all()
news_list = get_news(companies)

@app.route("/", methods=["GET", "POST"])
def home():
    companies = Company.query.all()
    if request.form:
        symbol = request.form.get("symbol").upper()
        ##now check for validity
        if symbol in symbol_list and symbol not in [sym.ticker for sym in companies]:
            r = requests.get("https://finnhub.io/api/v1/stock/profile2?symbol=" + symbol + "&token=" + API_KEY)
            company = Company(**(r.json()))

            db.session.add(company)
            db.session.commit()

    companies = Company.query.all()
    graphs = [create_plot(c.ticker) for c in companies]
    graphs = [components(g) for g in graphs]
    scrpts = [g[0] for g in graphs]
    graphs = [g[1] for g in graphs]
    #can send bool flag
    return render_template("home.html", companies=companies, graphs=graphs, scrpts=scrpts, news_articles=news_list, num_companies=len(companies), num_news = len(news_list))

if __name__ == "__main__":
    app.run(debug=True)
 



