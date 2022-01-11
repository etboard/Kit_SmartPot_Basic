/**********************************************************************************
 * Author : (주)한국공학기술연구원
 * Program ID  : SmartPot_Basic
 * Description : 스마트 화분 코딩(워터펌프 포함)
 *             : LIJ : 2021.09.02
 **********************************************************************************/

//=================================================================================
// Include & definition
//=================================================================================
// OLED 제어를 위한 라이브러리 불러오기
#include "oled_u8g2.h"
OLED_U8G2 oled;

// 토양수분센서를 이용할 ET-보드의 핀 설정
const int moisturePin = A4;

// ET-보드에서 사용할 LED 설정
const int pin1 = D4;
const int pin2 = D5;
const int threshold = 1000;


//================================================================
void setup()
//================================================================
{
  Serial.begin(9600);
  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
  oled.setup();
}

//================================================================
void loop()
//================================================================
{
  display_oled();
  delay(1);
}

//================================================================
void setup_oled()
//================================================================
{
    pinMode(SDA, INPUT);
    pinMode(SCL, INPUT);
}

//================================================================
void display_oled()
//================================================================
{
  // 토양수분센서값 보정
  int moistureValue = 4095-analogRead(moisturePin);
  Serial.print("토양 수분 센서값 : ");
  Serial.println(moistureValue);
  Serial.println("----------------------");

  if (moistureValue < threshold) { // 토양수분 센서값이 threshold 미만이면
    digitalWrite(pin1, HIGH); // 워터펌프 작동
    digitalWrite(pin2, LOW);  //
    } else {
    digitalWrite(pin1, LOW);  // 작동 멈춤
    digitalWrite(pin2, LOW);  //
    }


  // OLED 텍스트 표시
  char text[32] = "moist: ";
  char value[32];
  String str = String(moistureValue, DEC);
  str.toCharArray(value,6);
  strcat(text,value);

  oled.setLine(1,"* Smart POT *");  // OLED 첫 번째 줄
  oled.setLine(2,text);             // OLED 두 번째 줄
  oled.setLine(3,"-------------");  // OLED 세 번째 줄
  oled.display();
  delay(500);
}

//┌────────────────────────────────┐
//│                                                      │
//│     (주)한국공학기술연구원 http://et.ketri.re.kr         │
//│                                                      │
//└────────────────────────────────┘
