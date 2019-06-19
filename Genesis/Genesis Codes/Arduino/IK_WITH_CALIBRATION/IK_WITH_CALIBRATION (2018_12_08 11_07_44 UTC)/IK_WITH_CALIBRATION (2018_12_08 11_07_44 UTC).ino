#include<Servo.h>
Servo left_servo ,right_servo,back_servo;
 
 double angle_left,angle_right;
 int xs,ys;

float link_fl = 4.3,link_all = 11.0,x=3 , y = 20; // range of x is from -10 to 15 
void lift()                                       // range of y is from 10 to 20
{
  back_servo.write(50);
}

void drop()
{
  back_servo.write(90);
}

void setup() 
{
  Serial.begin(9600);
  left_servo.attach(10);
  right_servo.attach(9);
  back_servo.attach(6); 
}

void ik()
{
  double sqrt_l=sqrt((x*x + y*y));
  double ac1=acos( x/sqrt_l )+acos( sqrt_l / (2.0*link_all) );
  angle_left = (ac1*180)/3.1416;
  
  double sqrt_r=sqrt(((x-link_fl)*(x-link_fl) + y*y));
  double ac2=acos( (x - link_fl)/sqrt_r ) - acos( sqrt_r / (2.0*link_all) );
  angle_right = (ac2*180)/3.1416;
}

void loop()
{
  ik();
  angle_left = map(angle_left , 0 , 180 , 25 , 185);
  left_servo.write(angle_left);

  angle_right = map(angle_right , 0 , 180 , 25 , 195);
  right_servo.write(angle_right);
}
