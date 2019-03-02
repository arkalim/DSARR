#include <Servo.h>

int servo_right_mid = 105;
int servo_left_mid = 135;
int servo_left_back = 75;
int servo_right_back = 115;

int forward = 128;
int steer = 128;
int move_forward = 0;


Servo myservo_left_back;
Servo myservo_right_back;
Servo myservo_left_mid;
Servo myservo_right_mid;

int L1 = 0;
int R1 = 0;
int L2 = 0;
int R2 = 0;
int mode_1 = 0;
int mode_2 = 0;
int mode_3 = 0;
int mode_4 = 0;
int mode_5 = 0;
int initial = 0;
int quick_turn = 0;
int arc = 0;



void articulate();
void translate();
void modes();
void go_to_position(int , int, int , int );

void setup() {
  Serial.begin(9600);
  
  pinMode(8, OUTPUT);
  myservo_left_back.attach(8);
  
  pinMode(9, OUTPUT);
  myservo_right_back.attach(9);

  pinMode(10, OUTPUT);
  myservo_left_mid.attach(10);
  
  pinMode(11, OUTPUT);
  myservo_right_mid.attach(11);

  pinMode(12, OUTPUT);  //left
  pinMode(13, OUTPUT);  //left
  pinMode(5, OUTPUT);   //right
  pinMode(6, OUTPUT);   //right

}

void ser()
{
  while(!Serial.available());
  L1=Serial.readStringUntil('\t').toInt();
  L2=Serial.readStringUntil('\t').toInt();
  R1=Serial.readStringUntil('\t').toInt();
  R2=Serial.readStringUntil('\t').toInt();
  forward = Serial.readStringUntil('\t').toInt();
  steer = Serial.readStringUntil('\t').toInt();
  initial = Serial.readStringUntil('\t').toInt();
  quick_turn = Serial.readStringUntil('\t').toInt();
  mode_1 = Serial.readStringUntil('\t').toInt();
  mode_2 = Serial.readStringUntil('\t').toInt();
  mode_3 = Serial.readStringUntil('\t').toInt();
  mode_4 = Serial.readStringUntil('\t').toInt();
  mode_5 = Serial.readStringUntil('\t').toInt();
  arc = Serial.readStringUntil('\n').toInt();
}


void loop() {
  ser();  
  articulate();
  translate();
  modes();
  
}

void articulate()
{
  if(servo_left_back < 180 && servo_right_back < 180 && servo_left_mid < 180 && servo_right_mid < 180 && servo_left_back > 0 && servo_right_back > 0 && servo_left_mid > 0 && servo_right_mid > 0)
  { 
  if(L1)  //back up  - 4
  {
    servo_right_back-=5;
    servo_left_back+=5;
  }
  
  if(R1)   //front up   -  5
  {
    servo_right_mid-=5;
    servo_left_mid+=5;
  }

  if(L2)   //back down   -  6
  {
    servo_right_back+=5;
    servo_left_back-=5;
  }

  if(R2)    //front down   -  7
  {
    servo_right_mid+=5;
    servo_left_mid-=5;
  }

  myservo_left_back.write(servo_left_back);
  myservo_right_back.write(servo_right_back);
  myservo_left_mid.write(servo_left_mid);
  myservo_right_mid.write(servo_right_mid);
  }
  
  if(servo_left_back >= 180 || servo_right_back <= 0) 
  {
    servo_left_back--;
    servo_right_back++;
  }

  if(servo_left_mid >= 180 || servo_right_mid <= 0) 
  {
    servo_left_mid--;
    servo_right_mid++;
  }

  if(servo_left_back <= 0 || servo_right_back >= 180) 
  {
    servo_left_back++;
    servo_right_back--;
  }

  if(servo_left_mid <= 0 || servo_right_mid >= 180) 
  {
    servo_left_mid++;
    servo_right_mid--;
  }
  
}

void translate() 
{
  if(forward < 125) //move forward
  {
    analogWrite(12, 255-forward);
    analogWrite(13, 0);
    analogWrite(5, 255-forward);
    analogWrite(6, 0);
  }

  else if(forward > 135) //move back
  {
    analogWrite(12, 0);
    analogWrite(13, forward);
    analogWrite(5, 0);
    analogWrite(6, forward);
  }

  else if(steer > 135) //turn right
  {
    analogWrite(12, steer);
    analogWrite(13, 0);
    analogWrite(5, 0);
    analogWrite(6, steer);
  }

  else if(steer < 125) //turn left
  {
    analogWrite(12, 0);
    analogWrite(13, 255-steer);
    analogWrite(5, 255-steer);
    analogWrite(6, 0);
  }
  
  else    //stop
  {
    analogWrite(12, 0);   
    analogWrite(13, 0);
    analogWrite(5, 0);
    analogWrite(6, 0);
  }
  
}

void modes()
{
  ser();
  if(initial) 
  {
    move_forward = 0;
    go_to_position(75,115,135,105);
  }
  
  else if(quick_turn)
  {
    move_forward = 0;
    go_to_position(120,70,130,110);
  }
  else if(mode_1) 
  {
    move_forward = 0;
    go_to_position(75,115,190,50);
    
  }
  else if(mode_2) 
  {
    move_forward = 0;
    go_to_position(15,175,130,110);
  }
  else if(mode_3) 
  {
    move_forward = 0;
    go_to_position(105,85,100,140);
  }
  else if(mode_4) 
  {
    move_forward = 0;
    go_to_position(75,115,100,140);

  }
  else if(mode_5) 
  {
    move_forward = 0;
    go_to_position(135,55,130,110);
    
  }
}

void go_to_position(int lb, int rb, int lm, int rm)
{
    if(move_forward)
    {
      analogWrite(12, 200);
      analogWrite(13, 0);
      analogWrite(5, 200);
      analogWrite(6, 0);
    }
    else
    {
      analogWrite(12, 0);
      analogWrite(13, 0);
      analogWrite(5, 0);
      analogWrite(6, 0);
    }
      
    int count = 0;

    while(servo_left_back >= lb || servo_right_back <= rb)
    { 
      count++;
      servo_left_back--;
      servo_right_back++;
      myservo_left_back.write(servo_left_back);
      myservo_right_back.write(servo_right_back);
      delay(10);
      if(count>=90) break;
    }
    count = 0;
    
    while(servo_left_back < lb || servo_right_back > rb)
    {
      count++;
      servo_left_back++;
      servo_right_back--;
      myservo_left_back.write(servo_left_back);
      myservo_right_back.write(servo_right_back);
      delay(10);
      if(count>=90) break;
    }

    count = 0;

    while(servo_left_mid >= lm || servo_right_mid <= rm)
    { 
      count++;
      servo_left_mid--;
      servo_right_mid++;
      myservo_left_mid.write(servo_left_mid);
      myservo_right_mid.write(servo_right_mid);
      delay(10);
      if(count>=90) break;
    }

    count = 0;

    while(servo_left_mid < lm || servo_right_mid > rm)
    {
      count++;
      servo_left_mid++;
      servo_right_mid--;
      myservo_left_mid.write(servo_left_mid);
      myservo_right_mid.write(servo_right_mid);
      delay(10);
      if(count>=90) break;
    }
}
