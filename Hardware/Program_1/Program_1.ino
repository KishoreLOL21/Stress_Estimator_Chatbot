#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "MAX30100_PulseOximeter.h"

#define REPORTING_PERIOD_MS     1000

LiquidCrystal_I2C lcd(0x27, 16, 2);

byte smile[] = {
  B00000,
  B00000,
  B01010,
  B00000,
  B10001,
  B01110,
  B00000,
  B00000
};
byte mod[] = {
  B00000,
  B00000,
  B01010,
  B00000,
  B11111,
  B00000,
  B00000,
  B00000
};
byte sad[] = {
  B00000,
  B00000,
  B01010,
  B00000,
  B01110,
  B10001,
  B00000,
  B00000
};

PulseOximeter pox;
uint32_t tsLastReport = 0;

String receivedMessage = "";

void onBeatDetected() {
  Serial.println("Beat!!!");
}

void setup() {
  lcd.init();
  lcd.backlight();
  Serial.begin(9600);
  lcd.createChar(1 , smile);
  lcd.createChar(2 , mod);
  lcd.createChar(3 , sad);
  lcd.setCursor(0, 0);
  lcd.print("      Pulse");
  lcd.setCursor(0, 1);
  lcd.print("    Oximeter");
  delay(2000);

  if (!pox.begin()) {
    Serial.println("FAILED");
    for (;;);
  } else {
    Serial.println("SUCCESS");
  }
  pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);
  pox.setOnBeatDetectedCallback(onBeatDetected);
}

void loop() {
  pox.update(); // Update sensor data continuously
  
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    if (receivedChar == '\n') {
      if (receivedMessage == "TERMINATE") {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Thank you");
        delay(2000);
        lcd.clear();
        receivedMessage = "";
      }
      else if (receivedMessage == "on") {
        receivedMessage = ""; // Clear the received message
      }
    } 
    else {
      receivedMessage += receivedChar;
    }
  }

  if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
    lcd.clear();
    lcd.setCursor(0 , 0);
    lcd.print("BPM : ");
    lcd.print(pox.getHeartRate());
    lcd.setCursor(0 , 1);
    lcd.print("SpO2: ");
    lcd.print(pox.getSpO2());
    lcd.print("%");
    tsLastReport = millis();
    if (pox.getSpO2() >= 96) {
      lcd.setCursor(15 , 1);
      lcd.write(1);                 
    } 
    else if (pox.getSpO2() <= 95 && pox.getSpO2() >= 91) {
      lcd.setCursor(15 , 1);
      lcd.write(2);                 
    } else if (pox.getSpO2() <= 90) {
      lcd.setCursor(15 , 1);
      lcd.write(3);
    }

    if (pox.getSpO2() > 90 && pox.getHeartRate() > 70){
      Serial.print("BPM: ");
      Serial.print(pox.getHeartRate());
      Serial.print(", SpO2: ");
      Serial.println(pox.getSpO2());
    }
  }
}
