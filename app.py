# coding: utf-8
from wsgiref.simple_server import make_server

import json
import RPi.GPIO as GPIO
import time

# ON/INCボタンに接続しているGPIOピン(BCM番号)
INCPIN = 17
# OFF/DECボタンに接続しているGPIOピン(BCM番号)
DECPIN = 27
# 制御信号の長さ[sec]
SIGNAL_DURATION = 0.05

# 指定したピンに制御信号を送る
# pin: ピン番号
# ite: 信号を送る回数
def EMSPadCtrl(pin, ite):
  for i in range(ite):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(SIGNAL_DURATION)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(SIGNAL_DURATION)

# EMSPadのINCボタンを押す動作を行う
# ite: ボタンを押す回数
def EMSPadInc(ite):
  EMSPadCtrl(INCPIN, ite)

# EMSPadのDECボタンを押す動作を行う
# ite: ボタンを押す回数
def EMSPadDec(ite):
  EMSPadCtrl(DECPIN, ite)

# EMSPadのDECボタンを11回押す動作を行い、電源オフ状態までもっていく
def EMSPadOff():
  EMSPadCtrl(DECPIN, 11)

def app(environ, start_response):
  status = '200 OK'
  headers = [
    ('Content-type', 'application/json; charset=utf-8'),
    ('Access-Control-Allow-Origin', '*'),
    ]
  # GPIOの初期化
  GPIO.cleanup()
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(INCPIN, GPIO.OUT)
  GPIO.setup(DECPIN, GPIO.OUT)
  
  start_response(status, headers)
  
  EMSPadInc(1)
  time.sleep(0.5)
  EMSPadOff()

  return [json.dumps({'message':'Execution was successful', 'time' : time.time()}).encode("utf-8")]

with make_server('', 3000, app) as httpd:
  print("Serving on port 3000...")
  httpd.serve_forever()

GPIO.cleanup()