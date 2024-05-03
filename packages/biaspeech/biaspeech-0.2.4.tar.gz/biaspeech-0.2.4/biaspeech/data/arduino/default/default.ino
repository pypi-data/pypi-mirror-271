#include <Otto.h>
Otto Otto;

#define LeftLeg 2 // left leg pin, servo[0]
#define RightLeg 3 // right leg pin, servo[1]
#define LeftFoot 4 // left foot pin, servo[2]
#define RightFoot 5 // right foot pin, servo[3]
#define Buzzer 13 //buzzer pin

String s;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  Otto.init(LeftLeg, RightLeg, LeftFoot, RightFoot, true, Buzzer);
  Otto.home();
}

void  loop() {
  while (!Serial.available());
  s = Serial.readString();
  Serial.print(s);

  if (s=="walk") {
    Otto.walk(2,1000,1);
    Otto.home();
  }

  if (s=="back") {
    Otto.walk(2,1000,-1);
    Otto.home();
  }

  if (s=="left") {
    Otto.turn(2,1000,1);
    Otto.home();
  }

  if (s=="right") {
    Otto.home();
    Otto.turn(2,1000,-1);
  }

  if (s=="stop") {
    Otto.home();
  }

  if (s=="happy") {
    Otto.playGesture(OttoHappy);
    Otto.home();
  }

  if (s=="sad") {
    Otto.playGesture(OttoSad);
    Otto.home();
  }

  if (s=="surprise") {
    Otto.sing(S_surprise);
    Otto.home();
  }

  if (s=="moonwalkerleft") {
    Otto.moonwalker(3, 1000, 25,1); 
    Otto.home();
  }

  if (s=="moonwalkerright") {
    Otto.moonwalker(3, 1000, 25,-1); 
    Otto.home();
  }

  if (s=="sing") {
    Otto.sing(S_cuddly);
    Otto.home();
  }

}

