from flask import Flask, jsonify, render_template, request, g, session, flash, redirect,url_for
app = Flask(__name__)
@app.route("/")
def test():
	return "here"
