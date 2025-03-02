from flask import Blueprint, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os
from dotenv import load_dotenv

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/')
def index():
    return render_template('quiz.html')