import sqlite3
from flask import Flask, render_template, request, redirect, jsonify, url_for,current_app
import subprocess
import configparser
import traceback

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        if request.method == "POST":
            update_config(request.form,config)
            subprocess.call("sudo supervisorctl restart playweather-core".split(" "))

        sensor_list = [sensor for sensor in config if sensor != "PLAYWEATHER_STATION" and sensor != "DEFAULT"]
        return render_template('settings.html', sensors=sensor_list, config=config )
    except Exception:
        return traceback.print_exc()


@app.route('/data_tables')
def data_tables():
    return render_template('data_tables.html')


@app.route('/data_tables/sensor_readings')
def get_sensor_readings():
    db_filename = "pw.sqlite3"
    with sqlite3.connect(db_filename) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM readings ORDER BY reading_date DESC Limit 10")
        result = {'data': c.fetchall()}
    return jsonify(result)


@app.route('/data_tables/gps_readings')
def get_gps_readings():
    db_filename = "pw.sqlite3"
    with sqlite3.connect(db_filename) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM gps ORDER BY reading_date DESC Limit 10")
        result = {'data': c.fetchall()}
    return jsonify(result)


@app.route('/restart')
def restart():
    # do something here
    return "Restart not implemented"



def update_config(form,config):
    form = form.to_dict()
    with open('config.ini', 'w') as configfile:
        config["PLAYWEATHER_STATION"]["delivery_interval"] = form.pop("delivery-interval")

        for sensor in {sensor.replace("-id", "").replace("-collection-interval", "") for sensor in form}:
            config[sensor]['collection_interval'] = form[sensor + '-collection-interval']

        config.write(configfile)

    return 'Done'


def get_pw_config_value(key):
    return app.config['PW_CONFIG']['DEFAULT'][key]



def default_config():
    new_config = configparser.ConfigParser()
    new_config["PLAYWEATHER_STATION"] = {
        "id": "station",
        "delivery_interval": "5",
    }
    return new_config


def validate(config):
    if "PLAYWEATHER_STATION" not in config:
        return False
    if "id" not in config["PLAYWEATHER"]:
        return False
    return True


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
