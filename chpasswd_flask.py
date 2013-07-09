#!/usr/bin/python

import os

import ldap

from flask import (
    request,
    render_template,
    Flask,
)

from chpasswd import chpasswd_ad
from config import (
    DOMAIN,
    MIN_PASSWORD_SIZE,
)


app = Flask(__name__)
app.config["TESTING"] = "CHPASSWD_AD_DEBUG" in os.environ

def ensure_https():
    from werkzeug.exceptions import BadRequest
    if not app.config['TESTING'] and not request.url.startswith("https"):
        raise BadRequest("This service needs https")
# register https check
app.before_request(ensure_https)


@app.route("/")
def chpasswd_prompt():
    return render_template("chpasswd_prompt.html")


@app.route("/change", methods=["POST"])
def chpasswd_change():
    # sanity checks
    if request.form["new_pass1"] != request.form["new_pass2"]:
        return "passwords don't match"

    if len(request.form["new_pass1"]) < MIN_PASSWORD_SIZE:
        return "password too short"

    # auto add domain if not given
    (user, sep, domain) = request.form["user"].partition("@")
    if not domain:
        user = "%s@%s" % (user, DOMAIN)

    # now do the actual change
    try:
        chpasswd_ad(DOMAIN, 
                    user,
                    request.form["old_pass"], 
                    request.form["new_pass1"])
    except ldap.LDAPError:
        return "Failed to change password"
    return "Password changed"
    

if __name__ == "__main__":
    app.run()
