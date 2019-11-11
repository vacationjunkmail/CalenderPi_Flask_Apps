from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g, jsonify, abort

l2 = Blueprint('l2', __name__)

@l2.route('/l2/')
def index():
	return render_template('l2/l2.html')
