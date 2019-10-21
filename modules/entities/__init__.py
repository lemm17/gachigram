from flask import Flask
from flask import render_template
app = Flask("__name__")

@app.route("/")
def hello_world():
    return "МЯСО СОСАТБ"

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/login") # Страница для логина, хотя особо смысла в ней не будет
def login():
    pass

@app.errorhandler(404)
def page_not_found(error):
    return "Нет такой странички"

if __name__ == "__main__":
    app.config["EXPLAIN_TEMPLATE_LOADING"] = True
    app.debug = True
    app.run()
