# Base modules

# Flask modules
from flask import url_for, request, render_template, Blueprint, redirect, flash

# Services

# Blueprint
player = Blueprint('player', __name__)

@player.route('/')
def players_list():
    return render_template('pages/player/list.html')
