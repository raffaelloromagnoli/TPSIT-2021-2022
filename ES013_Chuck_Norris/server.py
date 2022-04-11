from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True