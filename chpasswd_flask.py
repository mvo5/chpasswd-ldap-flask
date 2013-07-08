#!/usr/bin/python

from flask import (
    Flask,
    request,
    render_template,
)

from chpasswd import chpasswd_ad
SERVER="salomon.uni-trier.de"


app = Flask(__name__)
app.debug = True

@app.route("/")
def chpasswd_prompt():
    return render_template("chpasswd_prompt.html")


@app.route("/change", methods=["POST"])
def chpasswd_change():
    if request.form["new_pass1"] != request.form["new_pass2"]:
        return "passwords don't match"
    res = chpasswd_ad(SERVER, 
                      request.form["user"], 
                      request.form["old_pass"], 
                      request.form["new_pass1"])
    if not res:
        return "Failed to change password"
    return "Password changed"
    

if __name__ == "__main__":
    app.run()
