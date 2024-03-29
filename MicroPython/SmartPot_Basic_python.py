# *****************************************************************************************
# FileName     : SmartPot_Basic
# Description  : 스마트 화분 코딩 키트 (기본)
# Author       : 손정인
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2022.02.08
# Reference    :
# Modified     : 2022.11.23 : YSY : 소스 크린징, 수분 %변환, OLED 모터상태 출력 추가
# Modified     : 2022.12.21 : YSY : 변수 명명법 통일
# Modified     : 2023.03.14 : PEJ : 주석 길이 변경
# *****************************************************************************************

# import
import time
from machine import Pin, ADC
from ETboard.lib.OLED_U8G2 import *
from ETboard.lib.pin_define import *
def map(x,input_min,input_max,output_min,output_max): # map 함수 정의
    return (x-input_min)*(output_max-output_min)/(input_max-input_min)+output_min   

#------------------------------------------------------------------------------------------
# ETBoard 핀번호 설정
#------------------------------------------------------------------------------------------
# global variable
oled = oled_u8g2()

moisture_pin = ADC(Pin(A3))                             # 토양 수분 측정 센서

pump_pin1 = Pin(D2)                                     # 워터 펌프 작동 핀 (Motor-L)
pump_pin2 = Pin(D3)                                     # 모터 작동 핀 (Motor-L)

moist_threshold = 30                                    # 토양 수분 임계치(%)

text1 = [0] * 255


#==========================================================================================
# setup
#==========================================================================================
def setup() :
    moisture_pin.atten(ADC.ATTN_11DB)                   # 토양 수분 측정 센서 입력모드 설정
    
    pump_pin1.init(Pin.OUT)                             # 모터 출력 모드 설정
    pump_pin2.init(Pin.OUT)                             # 모터 출력 모드 설정
    
    
#==========================================================================================
# main loop
#==========================================================================================
def loop() :
    #--------------------------------------------------------------------------------------
    # 토양수분 센서로 토양 수분값 구하기
    #--------------------------------------------------------------------------------------
    global moist_threshold
    moisture_result = moisture_pin.read()                   # 토양 수분 측정값 저장
    moisture_value = map(moisture_result, 0, 4095, 100, 0)  # 토양 수분 측정값 % 변환 
    
    print("토양 수분 센서값 : ", moisture_value)

    #--------------------------------------------------------------------------------------
    # 토양수분이 값에 따라 워터 펌프의 작동 제어하기
    #--------------------------------------------------------------------------------------
    if(moisture_value < moist_threshold) :     # 토양 수분 값이 moist_threshold 미만이면
        pump_pin1.value(HIGH)                  # 워터 펌프 작동
        pump_pin2.value(LOW)
        pump_state = "On"                      # 워터 펌프 상태 On
    else :
        pump_pin1.value(LOW)                   # 워터 펌프 작동 멈춤
        pump_pin2.value(LOW)
        pump_state = "Off"                     # 워터 펌프 상태 Off
   
    print("모터 상태 : ", pump_state)
    print("---------------------")
    
    #--------------------------------------------------------------------------------------
    # OLED 텍스트 표시
    #--------------------------------------------------------------------------------------
    text1 = "moist: %d" %(moisture_value) + "%" # text1 수분값 표시
    text2 = "pump : " + pump_state              # text2 워터펌프 상태 표시
    
    oled.clear()
    oled.setLine(1, "* Smart POT *")            # OLED 첫 번째 줄 : 시스템 이름
    oled.setLine(2, text1)                      # OLED 두 번째 줄 : 토양 수분 측정값
    oled.setLine(3, text2)                      # OLED 세 번째 줄 : 모터 작동 상태
    oled.display()
    
    time.sleep(0.5)


if __name__ == "__main__" :
    setup()
    while True :
        loop()

#==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
#==========================================================================================