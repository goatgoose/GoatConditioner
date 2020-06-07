import sys
from subprocess import Popen, PIPE
import multiprocessing
import time
import RPi.GPIO as GPIO
import atexit
import temp_logger

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

class Conditioner:
    def __init__(self):
        self.TEMP_SENSOR_PATH = "/sys/bus/w1/devices/28-00000a29d9a3"
        self.CONDITIONER_GPIO_NUMBER = 13

        self.temperature = 0
        self.last_temperature_read = multiprocessing.Queue()

        self.status = "off"
        self.ideal = 72
        self.turn_off = 2
        self.turn_on = 2
        self.paused = False

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.CONDITIONER_GPIO_NUMBER, GPIO.OUT)

        self.sensor_process = multiprocessing.Process(target=self.read_sensor_forever)
        self.sensor_process.start()

        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(
            func=self.update_conditioner,
            trigger=IntervalTrigger(seconds=1),
            name="update conditioner",
            replace_existing=True
        )

    def conditioner_on(self):
        GPIO.output(self.CONDITIONER_GPIO_NUMBER, GPIO.HIGH)
        self.status = "on"

    def conditioner_off(self):
        GPIO.output(self.CONDITIONER_GPIO_NUMBER, GPIO.LOW)
        self.status = "off"

    def pause(self):
        if not self.paused:
            self.paused = True
            self.conditioner_off()

    def resume(self):
        if self.paused:
            self.paused = False
            self.conditioner_on()

    def get_temperature(self):
        if not self.last_temperature_read.empty():
            self.temperature = int(self.to_fahrenheit(self.last_temperature_read.get(block=False)))
        return self.temperature

    def get_status(self):
        return self.status

    def get_ideal(self):
        return self.ideal

    def get_turn_off(self):
        return self.turn_off

    def get_turn_on(self):
        return self.turn_on

    def set_ideal(self, temp):
        self.ideal = temp
        print(temp)

    def set_turn_off(self, temp):
        self.turn_off = temp
        print(temp)

    def set_turn_on(self, temp):
        self.turn_on = temp
        print(temp)

    @staticmethod
    def to_fahrenheit(c):
        return c * 1.8 + 32

    def read_temp_sensor(self):
        process = Popen("cat " + self.TEMP_SENSOR_PATH + "/w1_slave", shell=True, stdout=PIPE)
        for line in process.stdout:
            line = str(line)
            if "t=" in line:
                return int(line[line.find("t=") + 2:line.find(" ", line.find("t="))].replace("\\n", "")) / 1000.0

    # def read_temp_sensor(self):
    #     return temp_logger.get_temperature()

    def read_sensor_forever(self):
        while True:
            read = self.read_temp_sensor()
            while not self.last_temperature_read.empty():
                self.last_temperature_read.get()
            self.last_temperature_read.put(read)
            time.sleep(10)

    def update_conditioner(self):
        if not self.last_temperature_read.empty():
            self.temperature = int(self.to_fahrenheit(self.last_temperature_read.get(block=False)))
        if not self.paused:
            if self.get_status() == "off":
                if self.temperature >= self.get_ideal() + self.get_turn_on():
                    self.conditioner_on()
            elif self.get_status() == "on":
                if self.temperature <= self.get_ideal() - self.get_turn_off():
                    self.conditioner_off()
