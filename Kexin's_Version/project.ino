/*
 * arduino:
    needed input for python:
        - turn signal (when the car locates at each corner and ready to measure)
        - distance (from the 4 directions) (should be sent when the detected distance changes))
        - end signal? (when the car finished mapping)
        
    arduino pseudocode:
        global variables: 
            - stores the previous measurement (should be initialized to 150 cm)
            - stores the number of turns (should be initialized to 0)
        loop function:
            (maybe part 1 should be part of the setup function if the duration between mottor running and the first measurement is very small)
            2. get measurments (store in 4 local variables)
            3. if the main measurement is different (within a certain boundary of error) from the previous measurement
                - if current measure > previous measure 
                    - send the 4 measurements (main measurement is the current one) and duration to python
                - else
                    - send the 4 measurements (main measurement is the previous one) and duration to python
                - previous measurement = current measurement
            4. if the distance between the car and the wall that it's moving toward to is too close
            (probably need test to figure out the number)
                - stop the motor
                - if turn == 3 (reached the beginning position
                    - send ending signal
                - else
                    - turn the car (not sure how that works yet)
                    - set previous measurement to 150 cm
                    - turn += 1
                    - start the motor
 */
 
// error range
const int error = 4; /* may need to change this number by testing */

// module pin for ultrasonic sensors
const int trigPinFront1 = 2; /* need fix */
const int echoPinFront1 = 22;
const int trigPinFront2 = 2;
const int echoPinFront2 = 22;
const int trigPinLeft = 2;
const int echoPinLeft = 22;
const int trigPinRight = 2;
const int echoPinRight = 22;

// module pin for motors 
/* add */

// module pin for switch
/* add */

// previous measurement (should be initialized to 150 cm)
int prevMeasure = 150;

// stores the number of turns (should be initialized to 0)
int turnNum = 0;

// duration
long duration;

// functions

// get ultrasonic data
void getDistance(trigPin, echoPin)
{
  // front1
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // get duration (in micro seconds)
  duration = pulseIn(echoPin, HIGH);
  return duration * 345 / 2 / 10000; // in cm
}

// process measurement
int processMeasurement()
{
  // get distances
  int front = (getDistance(trigPinFront1, echoPinFront1) + getDistance(trigPinFront1, echoPinFront1)) / 2
  int left = getDistance(trigPinLeft, echoPinLeft)
  int right = getDistance(trigPinRight, echoPinRight)

  // detect change in measurement (right sensor always face inward
  if(right - previous >= error) // new distance is larger than old distance -> send new distance
  {
    // send to python
    Serial.println(String(front)+","+String(left)+","+String(right));
  }
  else if(right - previous <= -(error)) // old distance is larger than new distance -> send old distance
  {
    Serial.println(String(front)+","+String(left)+","+String(previous));
  }
  // update old distance
  previous = right

  return front;
}

// make a turn
void turn()
{
  /* need fix */
  
  // signal python after each turn
  Serial.println(-1);
}

// make the car go straight at constant speed
void moveForward()
{
  /* need fix */
}

// stop the car
void stopCar()
{
  /* need fix */
}

void setup()
{ 
  // ultrasonic distance sensor
  pinMode(trigPinFront1, OUTPUT);
  pinMode(echoPinFront1, INPUT);
  pinMode(trigPinFront2, OUTPUT);
  pinMode(echoPinFront2, INPUT);
  pinMode(trigPinLeft, OUTPUT);
  pinMode(echoPinLeft, INPUT);
  pinMode(trigPinRight, OUTPUT);
  pinMode(echoPinRight, INPUT);

  // motor
  /* add */

  // switch
  /* add */
  
  Serial.begin(9600);
  delayMicroseconds(10);
  // start the car
  moveFoward();
}

void loop()
{
  int front = processMeasurement();
  // if the distance between the car and the edge is less than or equal to this number, turn the car
  int stopDistance = 10; /* may need to change this number by testing */
  if(front <= stopDistance)
  {
    stopCar();
    if(turnNum == 3)
    {
      Serial.println(-2);
    }
    else
    {
      turn();
      previous = 150;
      turnNum += 1;
      moveForward();
    }
  }
  /*
            4. if the distance between the car and the wall that it's moving toward to is too close
            (probably need test to figure out the number)
                - stop the motor
                - if turn == 3 (reached the beginning position
                    - send ending signal
                    - stop arduino program if necessary?
                - else
                    - turn the car (not sure how that works yet)
                    - set previous measurement to 150 cm
                    - turn += 1
                    - start the motor
   */

}
