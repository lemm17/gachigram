from flask import Flask
from flask import render_template

app = Flask("__name__")


@app.route("/")
def hello_world():
    return ""


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/login")  # Страница для авторизации
def login():
    pass


@app.errorhandler(404)
def page_not_found(error):
    return "<b>Страница не найдена</b><br>ERROR 404"


if __name__ == "__main__":
    app.config["EXPLAIN_TEMPLATE_LOADING"] = True
    app.debug = True
    app.run()
