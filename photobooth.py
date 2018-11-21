import os
import sys
import time
from time import sleep
from tkinter import *
import tkinter.font
import picamera
import socket
import config
import flickrapi
import webbrowser
from signal import alarm, signal, SIGALRM, SIGKILL

#################
### VARIABLES ###
#################
replayDelay = 2 # how long to show the image before uploading to flickr?
doneDelay = 15 # how long to hold the done screen before restarting the process (in seconds)

testServer = 'www.google.com'
realPath = os.path.dirname(os.path.realpath(__file__))

tagsToTag = 'BrennanAndElla'

monitorWidth = 800
monitorHeight = 480

offsetX = 0 # how far off to left corner to display photos
offsetY = 0 # how far off to left corner to display photos

#################
### FUNCTIONS ###
#################
def takeSnapshot():
    print("Taking screenshot...")

def exitApp():
    print ("Photobooth app ended...")
    win.destroy()

def isConnected():
	try:
		# see if we can resolve the host name -- tells us if there is a DNS listening
		host = socket.gethostbyname(testServer)
		# connect to the host -- tells us if the host is actually reachable
		s = socket.create_connection((host, 80), 2)
		return True
	except:
		 pass
	return False

def showImage(imagePath):
    screen = initPygame()
    img=pygame.image.load(imagePath)
    img = pygame.transform.scale(img,(monitorWidth,monitorHeight))
    screen.blit(img,(offsetX,offsetY))
    pygame.display.flip()

def toUnicodeOrBust(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj

def uploadToFlickr(file,tag):
    connected = isConnected() #check to see if you have an internet connection
    while connected:
        try:
            flickr = flickrapi.FlickrAPI(config.api_key, config.api_secret)

            print('Step 1: authenticate')

            # Only do this if we don't have a valid token already
            if not flickr.token_valid(perms=u'write'):

                # Get a request token
                flickr.get_request_token(oauth_callback='oob')

                # Open a browser at the authentication URL. Do this however
                # you want, as long as the user visits that URL.
                authorize_url = flickr.auth_url(perms=u'write')
                webbrowser.open_new_tab(authorize_url)

                # Get the verifier code from the user. Do this however you
                # want, as long as the user gives the application the code.
                verifier = toUnicodeOrBust(raw_input('Verifier code: '))

                # Trade the request token for an access token
                flickr.get_access_token(verifier)
            flickr.upload(filename=file, tags=tag)
            break
        except ValueError:
            print("Oops. No internect connection. Upload later.")
            try: # make a text file as a note to upload the .gif later
                file = open(config.file_path + f + "-FILENOTUPLOADED.txt",'w') # Trying to create a new file or open one
                file.close()
            except:
                print('Something went wrong. Could not write file.')
            sys.exit(0) # quit Python

def startApp():
    # show the instructions
    #GPIO.output(ledPin,False) #turn the light off
    #showImage(realPath + "/slides/intro.png")
    #showImage(realPath + "/slides/brennan-and-ella-congrats.jpg")

    # get ready to take pictures
    congratsLabel.grid_remove() # use .grid() to add them back
    captureBtn.grid_remove()
    blankScreen = Label(win, bg="#000000")
    blankScreen.grid(row=0, column=1, sticky=W+E+N+S)

    with picamera.PiCamera() as camera: # use the 'with' for faster image taking
        camera.resolution = (monitorWidth, monitorHeight)
        camera.framerate = 30 # adjusting the framerate affects the preview image quality. Careful.
        camera.vflip = True
        camera.hflip = False
        camera.start_preview()
        time.sleep(1) # Let the camera warm up

        # countdown from 3, 2, 1 then the screen flashes white and takes picture
        sleep(0.5)
        #showImage(realPath + "/slides/countdown3.jpg")
        blankScreen.grid_remove()
        countdown3 = Label(win, text="3", font=myFont, fg="#ffffff", bg="#000000")
        countdown3.grid(row=0, column=1, sticky=W+E+N+S)
        camera.stop_preview()
        sleep(0.5)
        camera.start_preview()
        sleep(0.5)
        #showImage(realPath + "/slides/countdown2.jpg")
        countdown3.grid_remove()
        countdown2 = Label(win, text="2", font=myFont, fg="#ffffff", bg="#000000")
        countdown2.grid(row=0, column=1, sticky=W+E+N+S)
        camera.stop_preview()
        sleep(0.5)
        camera.start_preview()
        sleep(0.5)
        #showImage(realPath + "/slides/countdown1.jpg")
        countdown2.grid_remove()
        countdown1 = Label(win, text="1", font=myFont, fg="#ffffff", bg="#000000")
        countdown1.grid(row=0, column=1, sticky=W+E+N+S)
        camera.stop_preview()
        sleep(0.5)
        camera.start_preview()
        sleep(0.5)
        countdown1.grid_remove()
        #showImage(realPath + "/slides/white.jpg")
        whiteScreen = Label(win, bg="#ffffff")
        whiteScreen.grid(row=0, column=1, sticky=W+E+N+S)
        camera.stop_preview()
        sleep(0.5)

        # take one picture
        now = time.strftime("%Y-%m-%d-%H_%M_%S") # get the current date and time for the start of the filename
        fileToUpload = config.file_path + now + ".jpg"
        try: # take the photos
                camera.capture(fileToUpload)
        finally:
                camera.stop_preview()
                camera.close()

    # show the image
    #showImage(fileToUpload) # show the one image until flickr upload complete
    whiteScreen.grid_remove()
    showCapturedImg = PhotoImage(file=fileToUpload)
    showCapturedImg.grid(row=0, column=1, sticky=W+E+N+S)
    time.sleep(replayDelay) # pause for a minimum amount of time

    # upload to flickr
    uploadToFlickr(fileToUpload,tagsToTag)

    # display final screen
    #showImage(realPath + "/slides/brennan-and-ella-link.jpg")
    showCapturedImg.grid_remove()
    lookHereLabel = Label(win, text="Look at your photo here:", fg="#ffffff")
    lookHereLabel.grid(row=0, column=1, sticky=W+E+N+S)
    linkLabel = Label(win, text="flickr.com/photos/brennan_ella_gray")
    linkLabel.grid(row=1, column=1, sticky=W+E+N+S)
    time.sleep(doneDelay)

    # start over
    showImage(realPath + "/slides/brennan-and-ella-congrats.jpg")


#######################
### GUI DEFINITIONS ###
#######################
win = Tk()
win.geometry("800x480")
win.title("Photobooth")
win.protocol("WM_DELETE_WINDOW", exitApp) # exit cleanly
win.mainloop() # Loop forever

myFont = tkinter.font.Font(family="Helvetica", size=12, weight="bold")


#############
## WIDGETS ##
#############
congratsLabel = Label(win, text="Congratulation Brennan and Ella Gray", font=myFont, fg="#ffffff", bg="#00a775")
congratsLabel.grid(row=0, column=1, sticky=W+E+N+S) # for centering, look at the .grid() documentation

captureBtn = Button(win, text="Tap here to begin", font=myFont, command=takeSnapshot, fg="#ffffff", bg="#e82c0c")
captureBtn.grid(row=1, column=1, sticky=W+E+N+S)
