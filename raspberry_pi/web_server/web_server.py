from flask import Flask, render_template
import configparser

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', config=app.config['PW_CONFIG'])


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


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    app.config['PW_CONFIG'] = config
    print(app.config['PW_CONFIG'])
    app.run()
