# ******************************************************************************************
# FileName     : SmartPot_Basic_python
# Description  : 스마트화분 코딩 키트 (기본)
# Author       : 손정인
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2022.02.08
# Reference    :
# Modified     : 2022.11.23 : YSY : 소스 크린징, 수분 %변환, OLED 모터상태 출력 추가
# Modified     : 
# ******************************************************************************************

# import
import time
from machine import Pin, ADC
from ETboard.lib.OLED_U8G2 import *
from ETboard.lib.pin_define import *
def map(x,input_min,input_max,output_min,output_max):
    return (x-input_min)*(output_max-output_min)/(input_max-input_min)+output_min   # map 함수 정의

# global variable
oled = oled_u8g2()
moisture = ADC(Pin(A3))                                                              # 토양 수분 측정 센서
pin1 = Pin(D2)                                                                       # 모터 작동 핀 (Motor-L)
pin2 = Pin(D3)
threshold = 30                                                                       # 토양 수분 임계치(%)
text = [0] * 255


# setup
def setup() :
    moisture.atten(ADC.ATTN_11DB)                                                    # 토양 수분 측정 센서 입력 모드 설정
    pin1.init(Pin.OUT)
    pin2.init(Pin.OUT)

# main loop
def loop() :
    display_oled()
    time.sleep(0.001)
 
def display_oled() :
    global threshold
    moisture_result = moisture.read()                                                # 토양 수분 측정값 저장
    moistureValue = map(moisture_result, 0, 4095, 100, 0)                            # 토양 수분 측정값 % 
    
    print("토양 수분 센서값 : ", moistureValue)
    print("-------------------------")
        
    if(moistureValue < threshold) :                                                  # 토양 수분 측정값이 threshold 미만이면
        pin1.value(HIGH)                                                             # 워터 펌프 작동
        pin2.value(LOW)
        pump_state = "On"

    
    else :
        pin1.value(LOW)                                                              # 워터 펌프 작동 멈춤
        pin2.value(LOW)
        pump_state = "Off"
   
   
    text = "moist: %d" %(moistureValue) + "%"                                        # OLED 텍스트 표시
    text2 = "pump : " + pump_state
    
    
    oled.clear()
    oled.setLine(1, "* Smart POT *")                                                 # OLED 첫 번째 줄 : 시스템 이름
    oled.setLine(2, text)                                                            # OLED 두 번째 줄 : 토양 수분 측정값
    oled.setLine(3, text2)                                                           # OLED 두 번째 줄 : 토양 수분 측정값
    oled.display()
    time.sleep(0.5)



if __name__ == "__main__" :
    setup()
    while True :
        loop()

# ==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# ==========================================================================================