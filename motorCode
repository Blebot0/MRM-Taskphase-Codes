int X1 = A0; 
int Y1 = A1; 
int A = 6,B=5,C=10,D=11;
//A  B
//C  D
int a,b,c,d;
int Xco,Yco;//calibration factor
int n,x1,x2,y1,y2;
int X,Y;
int flag=1;//calibration flag
int l,m;
void setup() 
{
  pinMode(X1, INPUT);
  pinMode(Y1, INPUT);
  pinMode(A,OUTPUT);
  pinMode(B,OUTPUT);
  pinMode(C,OUTPUT);
  pinMode(D,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  
if(flag==1){
  Xco = analogRead(X1);//INITIAL VALUE
  Yco = analogRead(Y1);//INITIAL VALUE
  flag = 0;
}

X = analogRead(X1) - Xco; 
Y = analogRead(Y1) - Yco;
l=analogRead(X1);
m=analogRead(Y1);
x1 = Xco;
x2 = 1023 - x1;
y1 = Yco;
y2 = 1023 - y1;

//functions for cardinal directions
neutral(X,Y);
straight(X,Y,y1);
hardright(X,Y,x2);
softleft(X,Y,x1,y1);
softright(X,Y,x2,y1);
softbackright(X,Y,x1,y2);
softbackleft(X,Y,x2,y2);
hardleft(X,Y,x1);
straightback(X,Y,y2);

octet1(X,Y);
octet2(X,Y);
octet3(X,Y);
octet4(X,Y);
octet5(X,Y);
octet6(X,Y);
octet7(X,Y);
octet8(X,Y);

analogWrite(A,a);
analogWrite(B,b);
analogWrite(C,c);
analogWrite(D,d);

Serial.println("Front Left: ");
Serial.println(a);
Serial.println("Front Right: ");
Serial.println(b);
Serial.println("Back Left: ");
Serial.println(c);
Serial.println("Back Right: ");
Serial.println(d);

}

/*(0,0)        (512,0)      (1023,0)
 *                l
 *                l
 *                l
 *                l
 *(0,512)-----(512,512)----(1023,512)
 *                l
 *                l
 *                l
 *                l
 *(0,1023)   (512,1023)     (1023,1023)
 */

//functions

void neutral(int X, int Y)
{
  if(X==0 && Y==0)//Neutral
{
a = 0;
b = 0;
c = 0;
d = 0;
}
}
void straight(int X, int Y,int y1)
{
  if(X==0 && Y<0 && Y>=-y1)//straight forward
{
n = map(Y,0,-y1,0,255);
a = n;
b = n;
c = 0;
d = 0;
}
}

void straightback(int X, int Y,int y2)
{
  if(X==0 && Y>0 && Y<=y2)//straight back
{
n = map(Y,0,y2,0,255);
a = 0;
b = 0;
c = n;
d = n;
}
}



void softleft(int X, int Y, int x1, int y1)
{
  if(X == -x1 && Y == -y1)//soft left
{

a = 0;
b = 255;
c = 0;
d = 0;  
}
}

void softright(int X,int Y,int x2,int y1)
{
  if(X == x2 && Y == -y1)//soft right
{
a = 255;
b = 0;
c = 0;
d = 0;   
}
}

void softbackright(int X,int Y,int x1,int y2)
{
  if(X == -x1 && Y == y2)//soft back right
{
a = 0;
b = 0;
c = 255;
d = 0; 
}
}

void softbackleft(int X, int Y,int x2,int y2)
{
  if(X == y2 && Y == x2)//soft back left
{

a = 0;
b = 0;
c = 0;
d = n; 
}
}
void hardleft(int X,int Y,int x1)
{
  if(X>=-x1 && X<0 && Y==0)//hard left
{
n = map(X,0,-x1,0,255);
a = 0;
b = n;
c = n;
d = 0;
}
}

void hardright(int X,int Y,int x2)
{
 if(X<=x2 && X>0 && Y==0)//hard right
{
  n = map(X,0,x2,0,255);
a = n;
b = 0;
c = 0;
d = n;
} 
}




void octet1(int X,int Y)
{
//octet1
if(X == x2 && Y<0 && Y>-y1)
{
n = map(Y,-y1,0,0,255);
a = 255;
b = 0;
c = 0;
d = n;
Serial.println("Octet 1");
}
}
void octet2(int X,int Y)
{
//octet2
if(X<x2 && X>0 && Y == -y1)
{
n = map(X,x2,0,0,255);
a = 255;
b = n;
c = 0;
d = 0;
Serial.println("Octet 2");

}
}

void octet3(int X, int Y)
{
//octet3
if(X<0 && X>-x1 && Y == -y1)
{
n = map(X,-x1,0,0,255);
a = n;
b = 255;
c = 0;
d = 0;
Serial.println("Octet 3");

}
}

void octet4(int X, int Y)
{
//octet4
 if(X == -x1 && Y<0 && Y>-y1)
{
n = map(Y,-y1,0,0,255);
a = 0;
b = 255;
c = n;
d = 0;
Serial.println("Octet 4");

}
}

void octet5(int X, int Y)
{
//octet5
 if(X == -x1 && Y<y2 && Y>0)
{
n = map(Y,y2,0,0,255);
a = 0;
b = n;
c = 255;
d = 0;
Serial.println("Octet 5");

}
}

void octet6(int X, int Y)
{
//octet6
 if(X<0 && X>-x1 && Y == y2)
{
n = map(X,-x1,0,0,255);
a = 0;
b = 0;
c = 255;
d = n;
Serial.println("Octet 6");

}
}

void octet7(int X, int Y)
{
//octet7
if(X<x2 && X>0 && Y == y2)
{
n = map(X,x2,0,0,255);
a = 0;
b = 0;
c = n;
d = 255;
Serial.println("Octet 7");

}
}


void octet8(int X, int Y)
{
//octet8
 if(X == x2 && Y<y2 && Y>0)
{
n = map(Y,y2,0,0,255);
a = n;
b = 0;
c = 0;
d = 255;
Serial.println("Octet 8");

}
}
