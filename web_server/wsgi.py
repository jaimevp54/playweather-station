from web_server import app
import sqlite3
from flask import Flask, render_template, request, redirect, jsonify
import subprocess
import configparser

if __name__== "__main__":

    config = configparser.ConfigParser()
    config.read('config.ini')
    app.config['PW_CONFIG'] = config
    app.run(debug=True)
