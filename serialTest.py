import tkinter
from tkinter import *
import serial
from time import sleep

# Enter your COM port in the below line
ard = serial.Serial('/dev/ttyACM0', 9600)
sleep(2)
print (ard.readline(ard.inWaiting()))

top = tkinter.Tk()

def TrunOn():
  ard.write('1'.encode())
  sleep(0.1)
  data = ard.readline(ard.inWaiting())
  label1.config(text=str(data))

def Turnoff():
  ard.write('0'.encode())
  sleep(0.1)
  data = ard.readline(ard.inWaiting())
  label1.config(text=str(data))

OnButton = tkinter.Button(top, text ="LED ON", command = TrunOn)
OffButton = tkinter.Button(top, text ="LED OFF", command = Turnoff)
label1 = Label(top, fg="green")

label1.pack()
OnButton.pack()
OffButton.pack()
top.mainloop()
