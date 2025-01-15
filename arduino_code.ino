// 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
#include <Servo.h>      // Library for I2C communication (used by the LCD)  
#include <LiquidCrystal_I2C.h> 
#include<Wire.h>  // Library to control LCD via I2C communication

// Déclaration de deux objets Servo
Servo servo1;
Servo servo2;

// int Conveyor_Speed = 255;        // Speed of the conveyor (PWM value)

LiquidCrystal_I2C lcd(0x27, 20, 4);  // LCD address 0x27, 20x4 display size


// #define IN1 11              
// #define IN2 10
// // #define ENA 12

int relay_Red = 6;             // Red LED for plastic
int relay_Green = 5;           // Green LED for unknown items
int relay_Blue = 4;            // Blue LED for metal

// Définir les broches pour les servos
const int servoPin1 = 3;
const int servoPin2 = 2;

// void Move_Conveyor_Forward() {
//   digitalWrite(IN1, HIGH);      // Set conveyor motor forward
//   digitalWrite(IN2, LOW);
//   analogWrite(ENA, Conveyor_Speed);  // Set speed
// }

// void Move_Conveyor_Backward() {
//   digitalWrite(IN1, LOW);       // Set conveyor motor backward
//   digitalWrite(IN2, HIGH);
//   analogWrite(ENA, Conveyor_Speed);
// }

// void Stop_Conveyor() {
//   digitalWrite(IN1, LOW);       // Stop conveyor motor
//   digitalWrite(IN2, LOW);
//   analogWrite(ENA, 0);
// }

// // Display functions for categories on the LCD
// void Display_Plastic_Category() {
//   lcd.clear();
//   lcd.setCursor(0, 2);
//   lcd.print("Plastic Detected");
// }

// void Display_Metal_Category() {
//   lcd.clear();
//   lcd.setCursor(0, 2);
//   lcd.print("Metal Detected");
// }

void Display_Unknown_Category() {
  lcd.clear();
  lcd.setCursor(0, 2);
  lcd.print("Unknown Category");
}

// LED control functions
void Red_LED_ON() {
  digitalWrite(relay_Red, HIGH);     // Turn on red LED
}

void Red_LED_OFF() {
  digitalWrite(relay_Red, LOW);      // Turn off red LED
}

void Green_LED_ON() {
  digitalWrite(relay_Green, LOW);   // Turn on green LED
}

void Green_LED_OFF() {
  digitalWrite(relay_Green, HIGH);    // Turn off green LED
}

void Blue_LED_ON() {
  digitalWrite(relay_Blue, LOW);    // Turn on blue LED
}

void Blue_LED_OFF() {
  digitalWrite(relay_Blue, HIGH);     // Turn off blue LED
}

void All_LEDs_ON() {
  digitalWrite(relay_Red, LOW);     // Turn on all LEDs
  digitalWrite(relay_Green, HIGH);
  digitalWrite(relay_Blue, HIGH);
}

void All_LEDs_OFF() {
  digitalWrite(relay_Red, HIGH);      // Turn off all LEDs
  digitalWrite(relay_Green, LOW);
  digitalWrite(relay_Blue, LOW);
}

void setup() {

  // Initialiser la communication série à 9600 bauds
  Serial.begin(9600);
  // Attacher les servos aux broches respectives
  // pinMode(IN1, OUTPUT);
  // pinMode(IN2, OUTPUT);
  // pinMode(ENA, OUTPUT);
  pinMode(relay_Red, OUTPUT);
  pinMode(relay_Green, OUTPUT);
  pinMode(relay_Blue, OUTPUT);
  servo1.attach(servoPin1);
  servo2.attach(servoPin2);

  // // Initialize LCD
  // Wire.begin();
  // lcd.begin(20, 4);
  // lcd.backlight();
  // lcd.setCursor(0, 2);
  // lcd.print("Welcome Everyone");

  // Stop motors initially for safety
  // digitalWrite(IN1, LOW);
  // digitalWrite(IN2, LOW);
  // analogWrite(ENA, 0);
  // Stop_Conveyor();
  All_LEDs_OFF();
  // delay(1000);
  All_LEDs_ON();

  // Position initiale des servos
  servo1.write(0); // Position centrale pour le servo1
  servo2.write(90); // Position centrale pour le servo2
}

void loop() {
  // Vérifier si des données série sont disponibles
  // Move_Conveyor_Backward();
  if (Serial.available() > 0) {
    // Lire la commande reçue (jusqu'à la fin de ligne '\n')
    String command = Serial.readStringUntil('\n');
    Serial.println("Command");
    command.trim(); // Nettoyer la commande des espaces et retours à la ligne

    // Contrôle des servos selon la commande reçue
    if (command == "E") {
      Green_LED_ON();
      Red_LED_OFF();
      Blue_LED_OFF();
      // Display_Unknown_Category();
      servo1.write(0);   // Déplacer le servo1 à 0°
      servo2.write(90);
        // Déplacer le servo2 à 0°
      // Green_LED_OFF();
    } else if (command == "P") {
      Red_LED_ON();
      Green_LED_OFF();
      Blue_LED_OFF();
      // Display_Plastic_Category();
      servo1.write(90);  // Déplacer le servo1 à 90° (position centrale)
      servo2.write(90); 
    // Déplacer le servo2 à 90° (position centrale)
      // delay(1500);
      delay(500) ;
      // Red_LED_OFF();
    } else if (command == "M") {
      Blue_LED_ON();
      Red_LED_OFF();
      Green_LED_OFF();
      // Display_Metal_Category();
      servo1.write(0); // Déplacer le servo1 à 180°
      servo2.write(0); 
      delay(500) ;// Déplacer le servo2 à 180°
      // delay(1500);
      // Blue_LED_OFF();
    }

    // // Petite pause pour assurer la stabilité
     
  }
}