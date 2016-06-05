from scraper import Scraper
from flask import Flask,render_template,request,url_for,redirect
from buffer import searchInDB
def data_parser(data):
    pass


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("scraper.html")

@app.route("/result/<data>")
def result(data):
    return render_template("search.html",results = searchInDB(data))


@app.route("/res" ,methods=["Post"])
def check():
    text=request.form["seacrh-input"].replace(' ','%')
    #print text
    return redirect("/result/%s" %text)
app.run(debug=True)
