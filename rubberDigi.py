#! /usr/bin/env python

import argparse
import os
from datetime import datetime
from shutil import copyfile


sketchOpening = '''
#include "keymap.h"
#include "DigiKeyboard.h"

//// Delay between keystrokes
#define KEYSTROKE_DELAY 1000

int iterationCounter = 0;


void setup() {
  // initialize the digital pin as an output.
  pinMode(0, OUTPUT); //LED on Model B
  pinMode(1, OUTPUT); //LED on Model A
  digitalWrite(0, LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(1, LOW);
  // don't need to set anything up to use DigiKeyboard
}

void loop(){

  DigiKeyboard.update();

  // this is generally not necessary but with some older systems it seems to
  // prevent missing the first character after a delay:
  DigiKeyboard.sendKeyStroke(0);

  // It's better to use DigiKeyboard.delay() over the regular Arduino delay()
  // if doing keyboard stuff because it keeps talking to the computer to make
  // sure the computer knows the keyboard is alive and connected
  DigiKeyboard.delay(KEYSTROKE_DELAY);

  //START:  Parsed by rubberDigi Script
'''

sketchClosing = '''
  //END:  Parsed by rubberDigi Script

  delay(1000);
  while(1){
  }
}'''

#See keymap.h file for more HID codes
rubberDigi = \
 {"gui" : "KEY_LEFT_GUI",
  "windows" : "KEY_LEFT_GUI",
  "enter" : "KEY_ENTER",
  " " : "KEY_SPACEBAR",
  "space" : "KEY_SPACEBAR",
  "escape" : "KEY_ESCAPE",
  "backspace" : "KEY_BACKSPACE",
  "tab" : "KEY_TAB",
  "capslock" : "KEY_CAPS_LOCK",
  "printscreen" : "KEY_PRINTSCREEN",
  "scrolllock" : "KEY_SCROLL_LOCK",
  "pause" : "KEY_PAUSE",
  "insert" : "KEY_INSERT",
  "home" : "KEY_HOME",
  "pagup" : "KEY_PAGEUP",
  "delete" : "KEY_DELETE",
  "end" : "KEY_END",
  "pagedown" : "KEY_PAGEDOWN",

  "uparrow" : "KEY_UPARROW",
  "downarrow" : "KEY_DOWNARROW",
  "leftarrow" : "KEY_LEFTARROW",
  "rightarrow" : "KEY_RIGHTARROW",
  "up" : "KEY_UPARROW",
  "down" : "KEY_DOWNARROW",
  "left" : "KEY_LEFTARROW",
  "right" : "KEY_RIGHTARROW",

  "numlock" : "KEYPAD_NUMLOCK",
  "keypad_enter" : "KEYPAD_ENTER",

  "mute" : "KEY_MUTE",
  "volumeup" : "KEY_VOLUME_UP",
  "volumedown" : "KEY_VOLUME_DOWN",

  "lockingcaps" : "KEY_LOCKING_CAPS_LOCK",
  "lockingnum" : "KEY_LOCKING_NUM_LOCK",
  "lockingscroll" : "KEY_LOCKING_SCROLL_LOCK",

  "leftcontrol" : "KEY_LEFTCONTROL",
  "leftshift" : "KEY_LEFTSHIFT",
  "shift" : "KEY_LEFTSHIFT",
  "leftalt" : "KEY_LEFTALT",
  "alt" : "KEY_LEFTALT",
  "leftgui" : "KEY_LEFT_GUI",
  "rightcontrol" : "KEY_RIGHTCONTROL",
  "ctrl" : "KEY_RIGHTCONTROL",
  "rightshift" : "KEY_RIGHTSHIFT",
  "rightalt" : "KEY_RIGHTALT",
  "rightgui" : "KEY_RIGHT_GUI",
  "menu" : "KEY_MENU",


  "f1": "KEY_F1",
  "f2": "KEY_F2",
  "f3": "KEY_F3",
  "f4": "KEY_F4",
  "f5": "KEY_F5",
  "f6": "KEY_F6",
  "f7": "KEY_F7",
  "f8": "KEY_F8",
  "f9": "KEY_F9",
  "f10": "KEY_F10",
  "f11": "KEY_F11",
  "f12": "KEY_F12",

  "a": "KEY_A",
  "b": "KEY_B",
  "c": "KEY_C",
  "d": "KEY_D",
  "e": "KEY_E",
  "f": "KEY_F",
  "g": "KEY_G",
  "h": "KEY_H",
  "i": "KEY_I",
  "j": "KEY_J",
  "k": "KEY_K",
  "l": "KEY_L",
  "m": "KEY_M",
  "n": "KEY_N",
  "o": "KEY_O",
  "p": "KEY_P",
  "q": "KEY_Q",
  "r": "KEY_R",
  "s": "KEY_S",
  "t": "KEY_T",
  "u": "KEY_U",
  "v": "KEY_V",
  "w": "KEY_W",
  "x": "KEY_X",
  "y": "KEY_Y",
  "z": "KEY_Z",

  "1": "KEY_1",
  "2": "KEY_2",
  "3": "KEY_3",
  "4": "KEY_4",
  "5": "KEY_5",
  "6": "KEY_6",
  "7": "KEY_7",
  "8": "KEY_8",
  "9": "KEY_9",
  "0": "KEY_0",

  }

global lastCommand

def sendKeyStroke(i):
    split = i.split(" ")
    o = "DigiKeyboard.sendKeyStroke("
    if len(split) > 1:
        for x in range(0, len(split)):
          if x>=1 and x<len(split):
            o = o + ", "
          o = o + rubberDigi[split[x].lower()]

          if x == len(split) - 1:
            o = o + ");"
    else:
        o = o + rubberDigi[split[0].lower()]
        o = o + ");"
    return o

def sendModKeyStroke(i):
    split = i.split(" ")
    o = "DigiKeyboard.sendKeyStroke("
    if len(split) > 1:
        for x in range(1, len(split)):
          if x>=2 and x<len(split):
            o = o + ", "
          o = o + rubberDigi[split[x].lower()]

          if x == len(split) - 1:
            o = o + ", " + rubberDigi[split[0].lower()] + ");"
    else:
        o = o + rubberDigi[split[0].lower()]
        o = o + ");"
    return o

def parseDuckyLine(i):
  global lastCommand
  o = ""
  split = i.split(" ")

  if split[0] == "DELAY":
    o = "\n  DigiKeyboard.delay(" + split[1] + ");"

  elif split[0] == "REM":
    o = "// " + split[1]

  elif split[0] == "STRING":
    string = i[7:]
    string = string.replace("\\", "\\\\")
    string = string.replace("\"", "\\\"")
    o = "DigiKeyboard.print(\""
    o = o + string
    o = o + "\");"

  elif split[0] == "REPLAY":
    o = "for (int i=0; i < " + split[1] + "; i++) {\n"
    o = o + '    ' + lastCommand
    o = o + "\n  }"

  elif split[0] == "GUI" or split[0] == "ALT" or split[0] == "CTRL" or split[0] == "SHIFT":
    o = sendModKeyStroke(i)

  elif split[0] == "CTRL-SHIFT":
    split = i.split(" ")
    o = "DigiKeyboard.sendKeyStroke(" + rubberDigi[split[1].lower()] + ", " + "KEY_LEFTCONTROL | KEY_LEFTSHIFT);"

  elif split[0] == "CTRL-ALT":
    split = i.split(" ")
    o = "DigiKeyboard.sendKeyStroke(" + rubberDigi[split[1].lower()] + ", " + "KEY_LEFTCONTROL | KEY_LEFTALT);"

  elif split[0] == "ALT-SHIFT":
    split = i.split(" ")
    o = "DigiKeyboard.sendKeyStroke(" + rubberDigi[split[1].lower()] + ", " + "KEY_LEFTALT | KEY_LEFTSHIFT);"

  else:
    o = sendKeyStroke(i)

  lastCommand = o
  return o

#Arguement Parser
parser = argparse.ArgumentParser(description='Converts USB rubber ducky scripts to an DigiSpark arduino script. ', epilog="Quack Quack")
parser.add_argument('duckyscript', help='Ducky script to convert')
parser.add_argument('outdirname', help='Output script directory')

args = parser.parse_args()

# Input file is argument / output file is output.txt
infile = open(args.duckyscript)
print "Input File: " + args.duckyscript
outdir = os.getcwd() + '/' + args.outdirname
print "Output Directory: " + outdir
if os.path.isdir(outdir) == False:
    os.mkdir(outdir)
destpath = outdir + '/' + args.outdirname + '.ino'
dest = open(destpath, 'w')
print "Desitination: " + destpath

dest.write("//Converted at " + str(datetime.now()))
dest.write(sketchOpening)

for line in infile:
  if line.strip() != '':
    outString = parseDuckyLine(line.strip())
    dest.write('  ' + outString + '\n')

dest.write(sketchClosing)

copyfile("keymap.h", outdir + '/' + "keymap.h")


