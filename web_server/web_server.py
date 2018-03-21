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

        sensor_list = [sensor for sensor in config if sensor != "PLAYWEATHER_STATION" and sensor != "DEFAULT"]
        return render_template('settings.html', sensors=sensor_list, config=config)
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


@app.route('/start')
def start_station():
    pw_station_process = app.config.get('pw_station_process', None)

    if pw_station_process is not None:
        return "A station is already running?"

    pw_station_process = subprocess.Popen(['python', '-m', 'initialize'])
    app.config['pw_station_process'] = pw_station_process

    return redirect(url_for('index'))


@app.route('/stop')
def stop_station():
    pw_station_process = app.config.pop('pw_station_process', None)

    if pw_station_process is None:
        return "A station is already running?"

    pw_station_process.terminate()

    return redirect(url_for('index'))


def update_config(form,config):
    form = form.to_dict()
    with open('config.ini', 'w') as configfile:
        config["PLAYWEATHER_STATION"]["id"] = form.pop('station-id')
        config["PLAYWEATHER_STATION"]["delivery_interval"] = form.pop("delivery-interval")

        for sensor in {sensor.replace("-id", "").replace("-collection-interval", "") for sensor in form}:
            config[sensor]['id'] = form[sensor + '-id']
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
    app.run(debug=True, host='0.0.0.0', port=8080)
