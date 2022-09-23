from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash 
from flask_app.models.team import Team
from flask_app.models.player import Player
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def route():
    return render_template('index.html')