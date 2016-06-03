from scraper import Scraper
from flask import Flask,render_template,request,url_for,redirect

def data_parser(data):
    pass


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("scraper.html")

@app.route("/result/<data>")
def result(data):
    dataList = data_parser(data)
    scr = Scraper()
    scr.start("sib")
    print scr.output
    return render_template("search.html")


@app.route("/res" ,methods=["Post"])
def check():
    text=request.form["seacrh-input"]
    print text
    return redirect("/result/%s" %text)
app.run(debug=True)