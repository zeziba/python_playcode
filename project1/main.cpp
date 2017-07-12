/*

  As written, this program can only take one command at a time
  To provide a accurate results, use of an external voltage reference is required!

  Created By: Charles Engen

  Copyright (c) 2017 Charles Engen

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.

 */

#define DEBUG false

#include <Arduino.h>
#include "consts.h"

double time_factor = MAJORDELAY / 1000; // should be 1,000,000 but limitation of 8-bit

long timer;
long work_timer;

uint16_t required_flow;
bool flowing = false;
double total_flow;

bool reset = false;


uint16_t get_voltage () {
  /*
    Analog Read can take from 13us - 270us in time, so some adjustments might be
    needed if this has too gret of affects
   */
  return analogRead(READPIN);
}

uint16_t calculate_flow (uint16_t data) {
  return data; // apply formula here
}

void control_output (bool state) {
  /*
    Use of a pull down resistor is recommened on the control pin so as to not
    have any possiblitly that there is carry over voltage which might trigger
    the pin.
   */
  flowing = state ? true: false;
  digitalWrite(CONTROLPIN, state ? HIGH: LOW);
}

void log (unsigned long function_delay, uint16_t raw_data, double data,
    double current_flow) {
      Serial.println("F_TIME: " + (String) function_delay + ", R_DATA: " +
       (String) raw_data + ", DATA: " + (String) data + ", C_FLOW: " +
       (String) current_flow) + ", R_FLOW: " + (String) required_flow;
}

void run() {
  work_timer = micros();

  uint16_t raw_data = get_voltage();
  double data = calculate_flow(data);

  timer = micros();

  if (DEBUG) data = TESTVOLUME;

  total_flow += data * time_factor;


  if (total_flow >= required_flow) {
    control_output(false);
    delay(10);
    reset = true;
  }

  log(timer - work_timer, raw_data, data, total_flow);
}

void serial_flush() {
  while (Serial.available() > 0) {
    char t = Serial.read();
  }
}

void setup () {
  analogReference(EXTERNAL); //  Must supply an external voltage reference

  pinMode(READPIN, INPUT);
  pinMode(CONTROLPIN, OUTPUT);

  Serial.begin(BAUDRATE);

  timer = micros();

  delayMicroseconds(STARTUPDELAY);

  Serial.println("Ready to get commands.\n Time Factor at: " + (String)time_factor + "\n");
}

void loop () {

  if (!flowing & (Serial.available() > 0)) {
    required_flow = Serial.parseInt();
    required_flow *= 1000; // must adjust for the 9-bit limitation on floating points
    //required_flow = (uint16_t) text;
    control_output(true);

    serial_flush();  // must manually clear the serail line as we are using a fast baud rate
  }

  if ((timer - micros() > MAJORDELAY) & flowing) {
    run();
  }

  if (reset) {
    total_flow = 0;
    reset = false;
  }
}
