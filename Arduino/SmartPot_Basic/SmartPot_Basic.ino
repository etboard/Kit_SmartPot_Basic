/******************************************************************************************
 * FileName     : SmartPot_Basic
 * Description  : 스마트 화분 코딩 키트 (기본)
 * Author       : 이인정
 * CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
 * Warning      : Arduino IDE에서 u8g2 라이브러리를 추가해서 컴파일 해야함
 * Created Date : 2021.09.02
 * Modified     : 2022.01.12 : SCS : 소스 크린징
 * Modified     : 2022.10.03 : SCS : support arduino uno with ET-Upboard
 * Modified     : 2022.11.23 : YSY : 소스 크린징
 * Modified     : 2022.11.23 : YSY : 수분값 %변환, 시리얼통신값변경, OLED 모터상태 출력
 * Modified     : 2022.12.21 : YSY : 변수 명명법 통일
 * Modified     : 2023.03.14 : PEJ : 주석 길이 변경
 *****************************************************************************************/

// OLED 제어를 위한 라이브러리 불러오기
#include "oled_u8g2.h"
OLED_U8G2 oled;

//-----------------------------------------------------------------------------------------
// ETBoard 핀번호 설정
//-----------------------------------------------------------------------------------------
#include "pins_arduino.h"                          // support arduino uno with ET-Upboard

const int moisture_pin = A3;                       // 토양 수분 측정 센서

const int pump_pin1 = D2;                          // 워터 펌프 작동 핀 (pump-L)
const int pump_pin2 = D3;                          // 워터 펌프 작동 핀 (pump-L)
 
const int moist_threshold = 30;                    // 토양 수분 임계치 (%)


//=========================================================================================
void setup()
//=========================================================================================
{
    Serial.begin(115200);                          // 시리얼통신 준비
    oled.setup();                                  // OLED 셋업
  
    pinMode(pump_pin1, OUTPUT);                    // 워터 펌프 출력 모드 설정
    pinMode(pump_pin2, OUTPUT);                    // 워터 펌프 출력 모드 설정

    pinMode(SDA, INPUT);                           // OLED 입력 모드 설정
    pinMode(SCL, INPUT);                           // OLED 입력 모드 설정
}


//=========================================================================================
void loop()
//=========================================================================================
{
    char pump_state[5] = "";                       // 워터 펌프 상태 초기화
  
    //-------------------------------------------------------------------------------------
    // 토양수분 센서로 토양 수분값 구하기
    //-------------------------------------------------------------------------------------
    int moisture_value = map(analogRead(moisture_pin), 0, 4095, 100, 0); // 토양수분 %변환
  
    Serial.print("토양 수분 센서값 : ");
    Serial.println(moisture_value);
  
    //-------------------------------------------------------------------------------------
    // 토양수분이 값에 따라 워터 펌프의 작동 제어하기
    //-------------------------------------------------------------------------------------
    if (moisture_value < moist_threshold) {        // 토양수분 값이 moist_threshold 미만이면
        digitalWrite(pump_pin1, HIGH);             // 워터펌프 작동
        digitalWrite(pump_pin2, LOW);
        strcpy(pump_state, "On");                  // 워터 펌프 상태 On
    } 
    else {
        digitalWrite(pump_pin1, LOW);              // 워터 펌프 작동 멈춤
        digitalWrite(pump_pin2, LOW);
        strcpy(pump_state, "Off");                 // 워터 펌프 상태 Off
    }
  
    Serial.print("모터 상태 : ");
    Serial.println(pump_state);
    Serial.println("---------------------");

    //-------------------------------------------------------------------------------------
    // OLED 텍스트 표시
    //-------------------------------------------------------------------------------------
    char text1[32] = "moist: ";                    // text1 수분값 표시
    char value1[32];
    String str1 = String(moisture_value, DEC);
    str1.toCharArray(value1, 6);
    strcat(text1, value1);
    strcat(text1, "%");

    char text2[32] = "pump: ";                     // text2 워터펌프 상태 표시
    strcat(text2, pump_state);

    oled.setLine(1,"* Smart POT *");               // OLED 첫 번째 줄 : 시스템 이름
    oled.setLine(2, text1);                        // OLED 두 번째 줄 : 토양 수분 측정값
    oled.setLine(3, text2);                        // OLED 세 번째 줄 : 모터 작동 상태
    oled.display();
    
    delay(500);
}

//=========================================================================================
//
// (주)한국공학기술연구원 http://et.ketri.re.kr
//
//=========================================================================================
