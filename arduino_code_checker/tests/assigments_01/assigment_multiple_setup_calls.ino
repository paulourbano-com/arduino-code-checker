// C++ code
void setup()
{
  pinMode(7, OUTPUT);
  pinMode(5, OUTPUT);
  delay(1000);
  digitalWrite(7, HIGH);
}

void loop()
{
  digitalWrite(7, HIGH);
  delay(1000);
  digitalWrite(7, LOW);
  delay(1000);
}