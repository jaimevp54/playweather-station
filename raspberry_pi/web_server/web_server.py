from flask import Flask, render_template
import configparser

app = Flask(__name__)


@app.route('/')
def index():
    sensor_list=[sensor for sensor in app.config["PW_CONFIG"] if sensor != "PLAYWEATHER_STATION" and sensor!="DEFAULT"]
    return render_template('index.html', sensors=sensor_list, config=app.config['PW_CONFIG'])


@app.route('/save_config')
def save_config():
    with open('config.ini', 'w') as configfile:
        config = app.config['PW_CONFIG']
        config['DEFAULT']['owner'] = "Pedro"
        config['DEFAULT']['freq'] = "23"
        config.write(configfile)

    return 'Done'


def get_pw_config_value(key):
    return app.config['PW_CONFIG']['DEFAULT'][key]


def init(pw_instance):
    app.config['PW_INSTANCE'] = pw_instance
    app.config['PW_CONFIG'] = app.config['PW_INSTANCE'].config

    app.run()


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


    config = configparser.ConfigParser()
    config.read('config.ini')
    # if not validate(config):
    #    config = default_config()

    app.config['PW_CONFIG'] = config

    print(app.config['PW_CONFIG'])
    app.run()
