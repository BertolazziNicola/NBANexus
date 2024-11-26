from flask import url_for, request, render_template, Blueprint

base = Blueprint('base', __name__)

@base.route('/')
def index():
    return render_template('pages/index.html')
