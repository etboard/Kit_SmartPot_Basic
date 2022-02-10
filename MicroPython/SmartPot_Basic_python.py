# ******************************************************************************************
# FileName     : SmartPot_Basic_python
# Description  : 스마트화분 코딩 키트 (기본)
# Author       : 손정인
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2022.02.08
# Reference    :
# Modified     :
# ******************************************************************************************

# import
import time
from machine import Pin, ADC
from ETboard.lib.OLED_U8G2 import *
from ETboard.lib.pin_define import *

# global variable
oled = oled_u8g2()
moisture = ADC(Pin(A3))                          # 토양 수분 측정 센서
pin1 = Pin(D4) 
pin2 = Pin(D5)
threshold = 1000                                 # 토양 수분 임계치
text = [0] * 255

# setup
def setup() :
    moisture.atten(ADC.ATTN_11DB)                # 토양 수분 측정 센서 입력 모드 설정
    pin1.init(Pin.OUT)
    pin2.init(Pin.OUT)

# main loop
def loop() :
    display_oled()
    time.sleep(1)
 
def display_oled() :
    global threshold
    moisture_result = moisture.read()            # 토양 수분 측정값 저장
    moistureValue = 4095 - moisture_result       # 토양 수분 측정값 보정
    
    print("토양 수분 센서값 : ", moistureValue)
    print("-------------------------")
    time.sleep(1)
    
    if(moistureValue < threshold) :              # 토양 수분 측정값이 threshold 미만이면
        pin1.value(HIGH)                         # 워터 펌프 작동
        pin2.value(LOW)
    
    else :
        pin1.value(LOW)                          # 작동 멈춤
        pin2.value(LOW)       

    text = "moist : %d" %(moistureValue)         # OLED 텍스트 표시
    
    oled.clear()
    oled.setLine(1, "* Smart POT *")             # OLED 첫 번째 줄 : 시스템 이름
    oled.setLine(2, text)                        # OLED 두 번째 줄 : 토양 수분 측정값
    oled.setLine(3, "----------------")
    oled.display()
    time.sleep(1)



if __name__ == "__main__" :
    setup()
    while True :
        loop()

# ==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# ==========================================================================================