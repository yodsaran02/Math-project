#include <FastLED.h>
#define LED_PIN 7 //specify data pin on the board - D2
#define NUM_LEDS 122 //specify number of LED
uint8_t lg[21][21][2];
byte start,end,len;
char* ptr;
int str_len;
CRGB leds[NUM_LEDS];
void setup(){
  FastLED.addLeds<WS2812, LED_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5,500);
  FastLED.clear();
  FastLED.show();
  Serial.begin(9600);
  Serial.setTimeout(100);
  /////startup///////
  for(int b=0; b<NUM_LEDS;b++){
        leds[b] = CRGB::White;
      }
  FastLED.show();
  delay(2000);
  FastLED.clear();FastLED.show();
  ///////////////////////////////////////
  lg[4][5][1] = 1; lg[4][5][0]=0;
  ///////////////////////////////////////
  lg[14][20][0]=0;lg[14][20][1]=6;
  lg[13][14][0]=6;lg[13][14][1]=4;
  lg[6][13][0]=10;lg[6][13][1]=3;
  lg[6][9][0]=13;lg[6][9][1]=6;
  lg[8][9][0]=19;lg[8][9][1]=2;
  lg[7][8][0]=21;lg[7][8][1]=6;
  lg[6][7][0]=27;lg[6][7][1]=3;
  lg[5][6][0]=30;lg[5][6][1]=3;
  lg[5][10][0]=33;lg[5][10][1]=8;
  lg[9][10][0]=41;lg[9][10][1]=4;
  lg[9][19][0]=45;lg[9][19][1]=4;
  lg[18][19][0]=49;lg[18][19][1]=3;
  lg[10][18][0]=52;lg[10][18][1]=3;
  lg[10][11][0]=55;lg[10][11][1]=4;
  lg[11][17][0]=59;lg[11][17][1]=3;
  lg[15][17][0]=62;lg[15][17][1]=7;
  lg[15][16][0]=69;lg[15][16][1]=3;
  //////////////////////////////////////
  Serial.println("init LEDS path sucessfully");
}
void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readString();
    Serial.println(msg);
    str_len = msg.length() + 1; 
  	char char_array[str_len];
  	msg.toCharArray(char_array, str_len);
    int path[21];
  	ptr = strtok(char_array, ",");
    int count = 0;
    while(ptr){
      path[count] = atol(ptr);
    	ptr = strtok(NULL, ",");
    	count++;
  	}
    FastLED.clear();FastLED.show();
    for (int j=1; j<count;j++){
      if(path[j-1]>path[j]){
          start = path[j];
          end = path[j-1];
        }else{
          start = path[j-1];
          end = path[j];
        }
        //Serial.println(String(swtart)+","+String(end));
        int length = lg[start][end][1];
        int starting = lg[start][end][0];
        Serial.println("LEDS on from "+String(starting)+" to "+String(starting+length-1));
        for(int l=starting; l<(starting+length);l++){
          leds[l] = CRGB::Blue;
          Serial.print(String(l)+"-");
        }
    }
    FastLED.show();
  }
}

