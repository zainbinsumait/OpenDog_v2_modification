// includes
#include <HardwareSerial.h>
#include <SoftwareSerial.h>
#include <ODriveArduino.h>
// Printing with stream operator helper functions
template<class T> inline Print& operator <<(Print &obj,     T arg) { obj.print(arg);    return obj; }
template<>        inline Print& operator <<(Print &obj, float arg) { obj.print(arg, 4); return obj; }


////////////////////////////////
// Set up serial pins to the ODrive
////////////////////////////////

// Below are some sample configurations.
// You can comment out the default Teensy one and uncomment the one you wish to use.
// You can of course use something different if you like
// Don't forget to also connect ODrive GND to Arduino GND.

// Teensy 3 and 4 (all versions) - Serial1
// pin 0: RX - connect to ODrive TX
// pin 1: TX - connect to ODrive RX
// See https://www.pjrc.com/teensy/td_uart.html for other options on Teensy
//HardwareSerial& odrive_serial = Serial1;

// Arduino Mega or Due - Serial1
// pin 19: RX - connect to ODrive TX
// pin 18: TX - connect to ODrive RX
// See https://www.arduino.cc/reference/en/language/functions/communication/serial/ for other options
// HardwareSerial& odrive_serial = Serial1;

// Arduino without spare serial ports (such as Arduino UNO) have to use software serial.
// Note that this is implemented poorly and can lead to wrong data sent or read.
// pin 8: RX - connect to ODrive TX
// pin 9: TX - connect to ODrive RX
SoftwareSerial odrive_serial(8, 9);


// ODrive object
ODriveArduino odrive(odrive_serial);

void setup() {
  // ODrive uses 115200 baud
  odrive_serial.begin(115200);

  // Serial to PC
  Serial.begin(115200);
  while (!Serial) ; // wait for Arduino Serial Monitor to open

  Serial.println("ODriveArduino");
  Serial.println("Setting parameters...");

  // In this example we set the same parameters to both motors.
  // You can of course set them different if you want.
  // See the documentation or play around in odrivetool to see the available parameters
//  for (int axis = 0; axis < 2; ++axis) {
//    odrive_serial << "w axis" << axis << ".controller.config.vel_limit " << 10.0f << '\n';
//    odrive_serial << "w axis" << axis << ".motor.config.current_lim " << 11.0f << '\n';
//    // This ends up writing something like "w axis0.motor.config.current_lim 10.0\n"
//  }

  Serial.println("Ready!");
  Serial.println("Send the character '0' or '1' to calibrate respective motor (you must do this before you can command movement)");
  Serial.println("Send the character 's' to exectue test move");
  Serial.println("Send the character 'v' to read bus voltage");
  Serial.println("Send the character 'R' to release motors");

  Serial.println("Send the character 'p' to read motor position");
  Serial.println("Send the character 'a' do the test1");
  Serial.println("Send the character 'b' do the test2");
  Serial.println("Send the character 'c' turn down speed");
  Serial.println("Send the character 'd' turn up speed");
  Serial.println("Send the character 'e' small step");
  Serial.println("Send the character 'f' small step");
  Serial.println("Send the character 'g' stop");

  Serial.println("Send the character '8' go forward");
  Serial.println("Send the character '2' backward");
}

void loop() {

  if (Serial.available()) {
    char c = Serial.read();

    // Run calibration sequence
    if (c == '0' || c == '1') {
      int motornum = c-'0';
      int requested_state;

      requested_state = AXIS_STATE_MOTOR_CALIBRATION;
      Serial << "Axis" << c << ": Requesting state " << requested_state << '\n';
      if(!odrive.run_state(motornum, requested_state, true)) return;

      requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION;
      Serial << "Axis" << c << ": Requesting state " << requested_state << '\n';
      if(!odrive.run_state(motornum, requested_state, true, 25.0f)) return;

      requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL;
      Serial << "Axis" << c << ": Requesting state " << requested_state << '\n' ;
      if(!odrive.run_state(motornum, requested_state, false /*don't wait*/)) return;
    }
    //release motors
    if (c == 'R'){
      int requested_state;
      requested_state = AXIS_STATE_IDLE;
      Serial << "Axis" << 0 << ": Requesting state " << requested_state << '\n' ;
      if(!odrive.run_state(0, requested_state, true ,25.0f)) return;
      Serial << "Axis" << 1 << ": Requesting state " << requested_state << '\n' ;
      if(!odrive.run_state(1, requested_state, true ,25.0f)) return;
      }


    // Sinusoidal test move
    if (c == 's') {
      Serial.println("Executing test move");
      for (float ph = 0.0f; ph < 6.28318530718f; ph += 0.01f) {
        float pos_m0 = 2.0f * cos(ph);
        float pos_m1 = 2.0f * sin(ph);
        Serial.println(pos_m0);
        odrive.SetPosition(0, pos_m0);
        odrive.SetPosition(1, pos_m1);
        //delay(1);
      }
    }
// // Sinusoidal test move
//    if (c == 's') {
//      Serial.println("Executing test move");
//      for (float ph = 0 ; ph < 4.1; ph += 0.003) {
//        odrive.SetPosition(0, ph);
//        Serial.println(ph);
//        delay(5);
//      }
//    }

    // Read bus voltage
    if (c == 'v') {
      odrive_serial << "r vbus_voltage\n";
      Serial << "Vbus voltage: " << odrive.readFloat() << '\n';
      Serial.print("velocity is: ");
      Serial.println(odrive.GetVelocity(0));
    }

    // print motor positions
    if (c == 'p') {
        long encoder = odrive.GetPosition(0);
        Serial.print("encoder position is: ");
        Serial.println(encoder);
      }
    

    if (c == 'a') {
        odrive.SetPosition(0, 34);      // move 100mm
    }
    if (c == 'b') {
        odrive.SetPosition(0, 00000);      
    }
    
    if (c == 'c') {
        odrive.SetVelocity(0, 5.0);    
    }
    if (c == 'd') {
        odrive.SetVelocity(0, 20);              
    }
    if (c == 'e') {
        odrive.SetPosition(0, 0);
    }
    if (c == 'f') {
        odrive.SetPosition(0, 4);                
    }
    if (c == 'g') {
        odrive.SetVelocity(0, 0);
                   
    }
    if (c == '8') {
        float actualP = odrive.GetPosition(0);
        odrive.SetPosition(0, actualP + 1);               
    }
    if (c == '2') {
        float actualP = odrive.GetPosition(0);
        odrive.SetPosition(0, actualP - 1);                 
    }
    if (c == 't') {
        float actualP = odrive.GetPosition(0);
        for (float ph = 0 ; ph < 1.03; ph += 0.03) {
          odrive.SetPosition(0, actualP + ph);
          Serial.println(odrive.GetPosition(0));
          delay(50);
         }    
        actualP = odrive.GetPosition(0);
        for (float ph = 0 ; ph < 1.03; ph += 0.03) {
          odrive.SetPosition(0, actualP - ph);
          Serial.println(odrive.GetPosition(0));
          delay(50);
         }            
    }
    
  }
  
}
