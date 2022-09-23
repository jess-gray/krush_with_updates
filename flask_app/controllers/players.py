from flask_app import app
from flask import Flask, render_template, request, redirect, session 
from flask_app.models.team import Team
from flask_app.models.player import Player

#if flash is needed add to line 2