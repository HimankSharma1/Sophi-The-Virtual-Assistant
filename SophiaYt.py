from pytube import YouTube
import pyttsx3
import time
from tkinter import *
import os
import threading
from decouple import config

engine=pyttsx3.init()
voices=engine.getProperty('voices')

class YtDownload:
    def __init__(self, geometry):
        try:
            location=config("Location")
            voice=int(config("Voice"))
            engine.setProperty('vocie', voices[voice].id)

        except:
            from SophiaAddLocation import AddLocation
            AddLocation()
        def speak(auido):
            try:
                engine.endLoop()
            except:
                pass
            engine.say(auido)
            engine.runAndWait()
        self.root=Tk()
        self.root.config(bg="black")
        self.root.title("Download Youtube Video")
        self.root.resizable(False,False)
        self.root.iconbitmap('icon.ico')
        self.root.geometry(geometry)
        self.VideoLink=Entry(self.root, border=4, font=("Times",15))
        Label(self.root, text='Youtube Videos',fg='red', bg='black', font=('Times', 25)).place(x=150,y=30)
        Label(self.root, text='(Enter The url)',fg='red', bg='black', font=('Times', 25)).place(x=160,y=70)
        self.VideoLink.place(x=25, y=120, height=40, width=450)
        
        def GetVideo(resolution, formet):
            try:
                link=self.VideoLink.get()
                link=YouTube(link)
                StartTime=time.time()
                self.root.destroy()
            
                if formet=='mp4':
                    threading.Thread(target=speak, args=(f"starting the download at {resolution}.",)).start()
                    print("ok")
                    DownloadFile=link.streams.filter(resolution=resolution).first().download(output_path=location, filename_prefix=resolution)
                
                elif formet=="mp3":
                    threading.Thread(target=speak, args=("downloading the audio file",)).start()
                    DownloadFile=link.streams.filter(only_audio=True).first().download(output_path=location)
                    base = os.path.splitext(DownloadFile)
                    newfile=f"{base[0]}.mp3"
                    os.path.realpath(DownloadFile)
                    os.rename(DownloadFile, newfile)

                EndTime=time.time()
                TimeTaken=str(EndTime-StartTime)
                TimeTaken=TimeTaken.split(".")
                speak(f"download completed! the time taken is {TimeTaken[0]} seconds")
                self.root.destroy()
            except Exception as a:
                print(a.__class__.__name__)
                if (a.__class__.__name__)=="FileExistsError":
                    threading.Thread(target=speak, args=("File Already Exist",)).start()
                elif a.__class__.__name__=="RegexMatchError":
                    threading.Thread(target=speak, args=("PLease enter a valid url of the video",)).start()
                elif a.__class__.__name__=="AttributeError":
                    threading.Thread(target=speak, args=("Unable to Download File. Please check whether the selected option is available on youtube or not",)).start()

        down_144=lambda : GetVideo('144p', 'mp4')
        down_240=lambda : GetVideo('240p', 'mp4')
        down_360=lambda : GetVideo('360p', 'mp4')
        down_480=lambda : GetVideo('480p', 'mp4')
        down_720=lambda : GetVideo('720p', 'mp4')
        down_1080=lambda : GetVideo('1080p', 'mp4')
        down_1440=lambda : GetVideo('1440p', 'mp4')
        down_2160=lambda : GetVideo('2160p', 'mp4')
        down_mp3=lambda : GetVideo('360p', 'mp3')


        but1=Button(self.root, text="144p", font=('Times', 20,'bold'), fg='red', border=3,command=down_144).place(x=50, y=200)
        but1=Button(self.root, text="240p", font=('Times', 20,'bold'), fg='red', border=3,command=down_240).place(x=150, y=200)
        but1=Button(self.root, text="360p", font=('Times', 20,'bold'), fg='red', border=3,command=down_360).place(x=250, y=200)
        but1=Button(self.root, text="480p", font=('Times', 20,'bold'), fg='red', border=3,command=down_480).place(x=350, y=200)
        but1=Button(self.root, text="720p", font=('Times', 20,'bold'), fg='red', border=3,command=down_720).place(x=50, y=280)
        but2=Button(self.root, text="1080p", font=('Times', 20,'bold'), fg='red', border=3,command=down_1080).place(x=150, y=280)
        but2=Button(self.root, text="1440p", font=('Times', 20,'bold'), fg='red', border=3,command=down_1440).place(x=250, y=280)
        but2=Button(self.root, text="2160p", font=('Times', 20,'bold'), fg='red', border=3,command=down_2160).place(x=350, y=280)
        but3=Button(self.root, text="Audio", font=('Times', 20,'bold'), fg='red', border=3,command=down_mp3).place(x=200, y=360)
        self.root.mainloop()

def yt():
    a=threading.Thread(target=YtDownload, args=("500x500",))
    a.start()
