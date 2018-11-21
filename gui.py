from Tkinter import *
import tkFont
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.LOW)

win = Tk()
myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')

def exitProgram():
    print("Exit button pressed")
    GPIO.cleanup()
    win.quit()

win.title("First GUI")
win.geometry('720x480')

exitButton = Button(win, text="Exit", font = myFont, command=exitProgram, height=2, width=6)
exitButton.pack(side = BOTTOM)

mainloop()