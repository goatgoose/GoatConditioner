sudo modprobe w1-gpio
sudo modprove w1-therm
flask run app.py --host=0.0.0.0 --port=1142
