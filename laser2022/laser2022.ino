/*---------------------------------------------------------------------------*/
// Original code by Mark Orchard-Webb < 2017.12.31
// Additional comments and cleaning by James Fraser, summer 2018
// Further cleaning and updating by
// robert.turner@mcgill.ca
// 2021.12.20
/*---------------------------------------------------------------------------*/
// Pre-Compiler Commands tell the compiler what libraries we will be using
#include <Adafruit_MotorShield.h>
#include <Wire.h>

// Gives a name to a constant value before program gets compiles.
// This method uses no program memory space.
#define ADDRESS 0x62

/*---------------------------------------------------------------------------*/
// Global Variables
unsigned int counter = 0;
// Memory space to write strings to
char buf[256];
int mode = 0;
unsigned steps = 1000;
unsigned delays = 20;
unsigned value = 0;

/*---------------------------------------------------------------------------*/
// Prepare Motor Shield
// Create a motor shield object with the default I2C address*/
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
 
// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)...
// This value you will refine from your data!
Adafruit_StepperMotor *myMotor = AFMS.getStepper(200, 1);

/*---------------------------------------------------------------------------*/
void setup() {
  // Leave this in, in case of compiler bug....
  ///unsigned getSlope(unsigned history[]) __attribute__((__optimize__("O2")));
  Serial.begin(115200);
  Serial.println("LASER 2022");
  // Create with the default frequency 1.6KHz
  //AFMS.begin();
  // Or with a different frequency, say 1KHz
  AFMS.begin(500);

  myMotor->setSpeed(10);
  for (int i = 12; i < 14; i++) pinMode(i,OUTPUT);
}

/*---------------------------------------------------------------------------*/
void loop() {
  if (Serial.available()) parse_input();
  if (!mode) return;
  
  // This steps the motor forward one step in SINGLE mode //
  // Other available modes include DOUBLE (more torque)   //
  // INTERLEAVE (SINGLE followed by DOUBLE) and MICROSTEP //
  myMotor->step(1, FORWARD, SINGLE);
  delay(delays);
  // Send steps and value read to serial (python) //
  sprintf(buf,"%04d:%04d",counter,analogRead(A0));
  Serial.println(buf);
  Serial.flush();
  counter++;
  if (steps == counter) counter = 0;
  // waiting to stop
  if (!counter && (2 == mode)) mode = 0;
}

/*---------------------------------------------------------------------------*/
// Function for Using DAC
void setDAC(int word) {
  char cmd[3];
  word <<= 4;
  // 0x40 = 64
  cmd[0] = 0x40;
  cmd[1] = word >> 8;
  // 0xff = 255
  cmd[2] = word & 0xff;
  Wire.beginTransmission(ADDRESS);
  if (3 != Wire.write(cmd,3)) {
    Serial.println("FOUL!");
  }
  Wire.endTransmission();
}

/*---------------------------------------------------------------------------*/
// Functions to Interpret Python Commands
void parse_input() {
  long start = millis();
  // fill buffer
  for (int i = 0; i < 255; i++) {
    while (!Serial.available()) {
      // if 2 seconds pass before command, give up //
      // and return to avoid waiting forever       //
      if ((millis() - start) > 2000) {
        Serial.println("Timeout!");
        return;
      }
    }
    buf[i] = Serial.read();
    if ('\n' == buf[i]) {         
      if (!strncmp("LASER",buf,5)) {
        parse_laser();
        return;
      } else if (!strncmp("STEPS",buf,5)) {
        parse_steps();
        return;
      } else if (!strncmp("DELAY",buf,5)) {
        parse_delays();
        return;
      } else if (!strncmp("START",buf,5)) {
        if (mode) return;
        mode = 1;
        return;
      }
        // set flag to stop at end of loop
        else if (!strncmp("STOP",buf,4)) {
        if (!mode) return;
        mode = 2;
        return;
      } else if (!strncmp("ABORT",buf,5)) {
        mode = 0;
        counter = 0;
        return;
      }
    }
  }
}

/*---------------------------------------------------------------------------*/
void parse_laser(void) {
  if (1 != sscanf(buf+6,"%d",&value)) {
    Serial.println("Syntax: LASER <number>\n where <number> is 0..4095");
    return;
  }
  if ((value < 0) || (value > 4095)) {
    Serial.println("LASER range error");
    return;
  }
  setDAC(value);
  return;
}

/*---------------------------------------------------------------------------*/
void parse_steps(void) {
  if (1 != sscanf(buf+6,"%ud",&steps)) {
    Serial.println("Syntax: STEPS <number>");
    return;
  }
  return;
}

/*---------------------------------------------------------------------------*/
void parse_delays(void){
  if (1 != sscanf(buf+6,"%ud",&delays)) {
    Serial.println("Syntax: DELAY <number>");
  }
  return;
}
