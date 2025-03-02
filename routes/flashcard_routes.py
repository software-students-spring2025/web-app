from flask import Blueprint, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os
from dotenv import load_dotenv

flashcard_bp = Blueprint('flashcard', __name__)

@flashcard_bp.route('/')
def index():
    return render_template('flashcard.html')