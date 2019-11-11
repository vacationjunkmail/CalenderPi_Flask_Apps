from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g, jsonify, abort

l1 = Blueprint('l1', __name__)

@l1.route('/l1/')
def index():
	title = 'Calendar'
	return render_template('l1/l1.html',title=title)
