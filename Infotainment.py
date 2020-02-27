import os
import gc
import obd
import vlc
import time
import random
import threading
import tkMessageBox
from Tkinter import *
from vlc import MediaPlayer
from threading import Thread
from PIL import Image, ImageTk, ImageSequence



#########DEBUG###########
import logging
# LOG = "/home/pi/Desktop/loggingData.log"                                                     
# logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)  
# logging.debug("time to kill some bugs because you fucking suck at programming shithead")
# #########################



connection = obd.OBD("/dev/serial/by-id/usb-Tactrix_OpenPort_2.0_TAeCXArE-if00", 115200) 
throttle = 0.0
speed = 0.0
rpms = 0.0
playlist = []
song = vlc.MediaPlayer()
nootFlag = False
nootNum = 0


#
#
#add font to pi
#

class GifThread(threading.Thread):
    logging.debug("gif pressed")

    def __init__(self, parent):
        self.parent = parent
        self.canvas = Canvas(parent,width=500,height=281, bg='black', bd=0, highlightthickness=0, relief='ridge')
        self.canvas.place(x=550,y=200)
        self.sequence = [ImageTk.PhotoImage(img.resize((375,211))) for img in ImageSequence.Iterator(Image.open(r'/home/pi/Infotainment/anigif.gif'))]
        #self.sequence = [ImageTk.PhotoImage(img.resize((375,211))) for img in ImageSequence.Iterator(Image.open(r'/home/david/Desktop/anigif.gif'))]

        self.image = self.canvas.create_image(150,170, image=self.sequence[0])
        self.animating = True
        self.animate(0)
        
    def animate(self, counter):
        self.canvas.itemconfig(self.image, image=self.sequence[counter])
        if not self.animating:
            return
        self.parent.after(33, lambda: self.animate((counter + 1) % len(self.sequence)))
    def run(self):
        self.animate()


def mainExecution():
    global throttle
    global speed
    global rpms
    while True:
        cmd = obd.commands.RELATIVE_ACCEL_POS
        raw_throttle = connection.query(cmd)
        throttle = raw_throttle.value.magnitude
        textvar.set(throttle)
        
        cmd = obd.commands.RPM
        raw_rpms = connection.query(cmd)
        rpms = raw_rpms.value.magnitude

        

        cmd = obd.commands.COOLANT_TEMP
        raw_cTemp = connection.query(cmd)
        mcTemp = raw_cTemp.value.magnitude
        mcTempF = (mcTemp * (9/5) + 32)
        c_T_L_V.set(mcTempF)

        cmd = obd.commands.SPEED
        raw_SPEED = connection.query(cmd)
        mSpeed = raw_SPEED.value.magnitude
        mSpeedUSA = round((mSpeed * 0.6124),0)
        speed = mSpeedUSA
        s_L_V.set(mSpeedUSA)

        cmd = obd.commands.INTAKE_TEMP
        raw_iTemp = connection.query(cmd)
        miTemp = raw_iTemp.value.magnitude
        miTempF = (miTemp * (9/5) + 32)
        i_T_L_V.set(miTempF)

        cmd = obd.commands.INTAKE_PRESSURE
        raw_iPressure = connection.query(cmd)
        miPress = raw_iPressure.value.magnitude
        miPressB = round((miPress * 0.01),2)
        i_M_P_L_V.set(miPressB)



def europedal():
    
    global playlist
    global song

    playlist_len = len(playlist)

    random_song = random.randint(1,(playlist_len - 1))
    print(random_song)
    song = vlc.MediaPlayer(playlist[random_song])


    song.play()

    del playlist[random_song]

    def skipSong():
        global song
        
        song.stop()
         
        

        playlist_len = len(playlist)
        if playlist_len == 0:
            musicPopUp()
        random_song = random.randint(1,(playlist_len - 1))
        song = vlc.MediaPlayer(playlist[random_song])
        song.play()

        del playlist[random_song]

        return song
    
    


    extra = 0
    skipButton = Button(root, command=skipSong, text="skip", state=NORMAL, font=('Spantaran', 18), fg='white', bg='black', relief="raised")
    skipButton.place(x=650,y=50)

    nootButton = Button(root, command=nootNoot, text="NOOT", state=NORMAL, font=('Spantaran', 18), fg='white', bg='black', relief="raised")
    nootButton.place(x=650,y=100)


    
    
    
    
    time.sleep(0.25)
    while True:
        print(len(playlist))
        
        global throttle
        speed_log = [None] * 5
        throttle_log = [None] * 5

        
        caseNum = random.randint(1,7)
        if caseNum == 1:
            eurostring = "/home/pi/Infotainment/eurobeat1.mp3"
        elif caseNum == 2:
            eurostring = "/home/pi/Infotainment/eurobeat2.mp3"
        elif caseNum == 3:
            eurostring = "/home/pi/Infotainment/eurobeat3.mp3"
        elif caseNum == 4:
            eurostring = "/home/pi/Infotainment/eurobeat4.mp3"
        elif caseNum == 5:
            eurostring = "/home/pi/Infotainment/eurobeat5.mp3"
        elif caseNum == 6:
            eurostring = "/home/pi/Infotainment/eurobeat6.mp3"
        elif caseNum == 7:
            eurostring = "/home/pi/Infotainment/eurobeat7.mp3"

        eurobeatTrack = vlc.MediaPlayer(eurostring)
        print(song.is_playing())
        # if len(playlist) == 1:
        #     musicPopUp()
        if (song.is_playing() == 0):
            time.sleep(0.5)
            if (song.is_playing() == 0):
                logging.debug("Skip song")


                skipSong()
    
#############################
# this is the basic over 80% mode  

        # while throttle >= 40:
        #     extra = extra + 1
        #     song.set_pause(1)
        #     if (eurobeatTrack.is_playing()) == 0:

        #         eurobeatTrack.play()
        #     if extra > 2:
        #         time.sleep(3)
        #     time.sleep(3)

###################

        logging.debug("In normal loop not full throttle")


        
        if throttle >= 40:
            logging.debug("Gas, Gas, Gas, I stepped on the gas")
            global speed
            global rpms
            global nootFlag
            if nootFlag == True:
                logging.debug("NOOT NOOT Bitch")
                nootAudio = vlc.MediaPlayer("/home/pi/Infotainment/noot.mp3")
                nootAudio.play()
                time.sleep(1.2)
                # should i garbage collect the noot audio object
            
            logging.debug("lets_go = True")
            
            lets_go = True
            initial_avg_speed = speed
            song.set_pause(1)
            if (eurobeatTrack.is_playing()) == 0:
                    eurobeatTrack.play()
                    logging.debug("EUROBEAT INTENSIFIES")

            while lets_go == True:
                logging.debug("in lets go loop")

                
    ################what are these actual values, are they changing?
                time.sleep(0.5)
                speed_log[0] = speed
                throttle_log[0] = throttle
                time.sleep(0.5)
                speed_log[1] = speed
                throttle_log[1] = throttle
                time.sleep(0.5)
                speed_log[2] = speed
                throttle_log[2] = throttle
                time.sleep(0.5)
                speed_log[3] = speed
                throttle_log[3] = throttle
                time.sleep(0.5)
                speed_log[4] = speed
                throttle_log[4] = throttle

                avg_speed = float((sum(speed_log))/(len(speed_log)))
                avg_throttle = float((sum(throttle_log))/(len(throttle_log)))

                if ((avg_speed - initial_avg_speed < 10.0) or rpms < 2550.0):
                    lets_go = False
                    logging.debug("Set lets_go to false")







            #now see if the acutal values are updating?
            #log the values and then take the average of them, compare the avg to the inital_avg_speed
            #if greater than 10 keep going
            #repeat
            #if rpms drop below 2k end
                #add rpms and make global



        if throttle < 40:
            song.set_pause(0)
            eurobeatTrack.stop()

            logging.debug("Stop teh eurobeat")
            

        eurobeatTrack.stop()
        time.sleep(0.1)
        extra = 0
        del eurobeatTrack
        gc.collect()

def exitFunc():
    root.destroy()

def musicPopUp():
    def metaPlst():
        for file in os.listdir("/home/pi/Infotainment/meta"):
            playlist.append(os.path.join("/home/pi/Infotainment/meta",file))
        eurobeatFunc()
        toplevel.destroy()

    def downtempoPlist():
        for file in os.listdir("/home/pi/Infotainment/citypop"):
            playlist.append(os.path.join("/home/pi/Infotainment/citypop",file))
        eurobeatFunc()
        toplevel.destroy()

    def solPlist():
        for file in os.listdir("/home/pi/Infotainment/sol"):
            playlist.append(os.path.join("/home/pi/Infotainment/sol",file))
        eurobeatFunc()
        toplevel.destroy()


    toplevel = Toplevel()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    toplevel.overrideredirect(1)
    toplevel.geometry("%dx%d+0+0" % (w, h))
    toplevel.configure(background='black',cursor="none")

    textLabel = Label(toplevel, text="What kind of music do you want?", font=('Spantaran',32), fg='white',bg='black')
    textLabel.place(x=90,y=210)
    metaButton = Button(toplevel, text="Current Meta", command=metaPlst, state=NORMAL, font=('Spantaran', 18), fg='white', bg='black')
    metaButton.place(x=125,y=300) 

    metaButton = Button(toplevel, text="City Pop", command=downtempoPlist, state=NORMAL, font=('Spantaran', 18), fg='white', bg='black')
    metaButton.place(x=325,y=300) 

    metaButton = Button(toplevel, text="SOL", command=solPlist, state=NORMAL, font=('Spantaran', 18), fg='white', bg='black')
    metaButton.place(x=515,y=300) 
    


def eurobeatFunc():
    eurobeatThread = Thread( target=europedal)
    eurobeatThread.setDaemon(True)
    eurobeatThread.start()
    # eurobeatButton['state'] = 'disabled'

def gif():
    gifThread = GifThread(root)
    gifThread.__init__(root)
    gifButton['state'] = 'disabled'

def nootNoot():
    global nootNum
    nootNum = nootNum + 1

    if (nootNum % 2) == 0:
        nootFlag = False
        print(nootFlag)
    else:
        nootFlag = True
        print(nootFlag)


def reconnect():
    del connection
    gc.collect()
    connection = obd.OBD("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AL05Y098-if00-port0", 38400)
    return connection




root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.configure(background='black', cursor="none")

textvar = IntVar(value=0)
testLabelThrottle = Label(root,textvariable=textvar)
testLabelThrottle.place(x=10,y=10)

c_T_L_V = IntVar(value=0)
coolant_Temperature_Label_Text = Label(root, text = "Coolant Temp: ", font=16, fg='white',bg='black')
coolant_Temperature_Label_Text.place(x=25,y=50)
coolant_Temperature_Label = Label(root, textvariable = c_T_L_V, font=16, fg='white',bg='black')
coolant_Temperature_Label.place(x=350,y=50)
coolant_Temperature_Label_Unit = Label(root, text = "F", font=16, fg='white',bg='black')
coolant_Temperature_Label_Unit.place(x=470,y=50)


s_L_V = IntVar(value=0)
speed_Label_Text = Label(root, text = "Current Speed: ", font=('Spantaran',16), fg='white',bg='black')
speed_Label_Text.place(x=25, y=125)
speed_Label = Label(root, textvariable = s_L_V, font=('Spantaran',32), fg='white',bg='black')
speed_Label.place(x=350,y=125)
speed_Label_Unit = Label(root, text = "mph", font=('Spantaran',32), fg='white',bg='black')
speed_Label_Unit.place(x=470,y=125)


i_T_L_V = IntVar(value=0)
intake_Temperature_Label_Text = Label(root, text = "Intake Temp: ", font=('Spantaran',12), fg='white',bg='black')
intake_Temperature_Label_Text.place(x=25,y=200)
intake_Temperature_Label = Label(root, textvariable = i_T_L_V, font=('Spantaran',32), fg='white',bg='black')
intake_Temperature_Label.place(x=350,y=200)
intake_Temperature_Label_Unit = Label(root, text = "F", font=('Spantaran',32), fg='white',bg='black')
intake_Temperature_Label_Unit.place(x=470,y=200)


i_M_P_L_V = IntVar(value=0)
intake_Manifold_Pressure_Label_Text = Label(root, text = "Boost Pressure: ", font=16, fg='white',bg='black')
intake_Manifold_Pressure_Label_Text.place(x=25,y=275)
intake_Manifold_Pressure_Label = Label(root, textvariable = i_M_P_L_V, font=('Spantaran',32), fg='white',bg='black')
intake_Manifold_Pressure_Label.place(x=350,y=275)
intake_Manifold_Pressure_Label_Unit = Label(root, text = "bar", font=('Spantaran',32), fg='white',bg='black')
intake_Manifold_Pressure_Label_Unit.place(x=470,y=275)


exitButton = Button(root, text="Exit", command=exitFunc, font=('Spantaran', 18), fg='white', bg='black')
exitButton.place(x=25,y=380)

eurobeatButton = Button(root, command=musicPopUp, state=NORMAL, text="Music", font=('Spantaran', 18), fg='white', bg='black')
eurobeatButton.place(x=100,y=380)

gifButton = Button(root, command=gif, text="GIF", state=NORMAL, font=('Spantaran', 18), fg='white', bg='black', relief="raised")
gifButton.place(x=197,y=380)





reconnectButton = Button(root, command=reconnect, text="Reconnect", state=NORMAL, font=('Spantaran', 18), fg='white', bg='black', relief="raised")
reconnectButton.place(x=268,y=380)

execute = Thread( target=mainExecution)
execute.setDaemon(True)
execute.start()

root.mainloop()


#added reconnect...will it work, maybe have to use a setter and getter???