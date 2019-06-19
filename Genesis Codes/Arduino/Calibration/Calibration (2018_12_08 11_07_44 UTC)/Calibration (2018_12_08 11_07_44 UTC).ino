#include<Servo.h>
Servo left_servo ,right_servo,back_servo;
 
 double angle_left,angle_right;

void lift()                                       
{
  back_servo.write(50);
}
void drop()
{
  back_servo.write(0);
}
void setup() 
{
  Serial.begin(9600);
  left_servo.attach(10);
  right_servo.attach(9);
  back_servo.attach(5); 
  /* 
  lift();
  _delay_ms(500);
  */
}

void loop()
{
  angle_left = 60 ;
  angle_left = map(angle_left , 0 , 180 , 10 , 180);
  left_servo.write(angle_left);
  
/*
 * Both the o's are on the right side 
 */
 
  angle_right = 60;
  angle_right = map(angle_right , 0 , 180 , 20 , 180);
  right_servo.write(angle_right);

 drop();
}
