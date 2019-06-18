from flask import Flask
from flask import render_template
from flask import request
from Conditioner import Conditioner
import json

app = Flask(__name__)

conditioner = Conditioner()


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/idealTemp', methods=['POST'])
def ideal_temp():
    conditioner.set_ideal(int(request.form['idealTemp']))
    return "ok"


@app.route('/turnOnTemp', methods=['POST'])
def turn_on_temp():
    conditioner.set_turn_on(int(request.form['turnOnTemp']))
    return "ok"


@app.route('/turnOffTemp', methods=['POST'])
def turn_off_temp():
    conditioner.set_turn_off(int(request.form['turnOffTemp']))
    return "ok"


@app.route('/update', methods=['GET'])
def update():
    items = {
        "status": conditioner.get_status(),
        "currentTemp": conditioner.get_temperature(),
        "idealTemp": conditioner.get_ideal(),
        "turnOnTemp": conditioner.get_turn_on(),
        "turnOffTemp": conditioner.get_turn_off()
    }
    return json.dumps(items)


@app.route('/pause', methods=['POST'])
def pause():
    conditioner.pause()
    return "ok"


@app.route('/resume', methods=['POST'])
def resume():
    conditioner.resume()
    return "ok"

if __name__ == "__main__":
    app.run(port=80)
