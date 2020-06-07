sudo modprobe w1-gpio
sudo modprobe w1-therm

export FLASK_APP=GoatConditioner.py
flask run --host=0.0.0.0 --port=1142
