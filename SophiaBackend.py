from SophiaAddMysql import speak
import SophiaWindow
import SophiaYt
import requests
import time, datetime
from Screen_Recorder import rec_function
import wikipedia
import webbrowser, os 
import requests
from decouple import config
import pygame
import mysql.connector as mp
import openai
import os
import struct
import pyaudio
import pvporcupine
from tkinter import *

porcupine = None
pa = None
audio_stream = None


openai.api_key = "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"
pygame.init()
sound=pygame.mixer.Sound("Activation beep.wav")
audio=int(config("Voice"))
SophiaWindow.engine.setProperty('voice', SophiaWindow.voices[audio].id)


def auto(name, pin, state):
    url = f"https://blr1.blynk.cloud/external/api/get?token=tvCkVGOBKsoX948oGZXWWIW0HP8PT9lz&{pin}"
    print(url)
    response = requests.get(url)
    response_json = response.json()
    if response_json==state:
        if state==False:
            win.out(f"{name} is already on", output=False)
        else:
            win.out(f"{name} is already off", output=False)
    if response_json!=state:
        if state == False:
            url = requests.get(f"https://blr1.blynk.cloud/external/api/update?token=tvCkVGOBKsoX948oGZXWWIW0HP8PT9lz&{pin}=0")
            print(url)
            win.out(f"Turning {name} on", output=False)
        else:
            url = requests.get(f"https://blr1.blynk.cloud/external/api/update?token=tvCkVGOBKsoX948oGZXWWIW0HP8PT9lz&{pin}=1")
            win.out(f"Turning {name} off", output=False)

def ai_out(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=text,
        max_tokens=200
        )
    return(response.choices[0].text.strip())

def runAssistant(final):
    host=config("Host")
    user=config("User")
    sql_pass=config("SqlPassword")
    import pywhatkit
    if 'sophia' in final or 'sofia' in final:
        a=final.split()
        if a[0]=="sophia" or a[0]=="sofia":
            final=final.replace('sophia','',1)
            final=final.replace('sofia','',1)
        else:
            pass         
    
    if 'search on google' in final or 'google' in final or 'search' in final:
        search=str(final)
        check=search.split()
        search=search.replace("search on google",'',1)
        if "search" in check[0:2]:
            search=search.replace("search",'',1)
        search=search.replace("on google",'',1)
        win.out(f'You asked me to search {search}')
        pywhatkit.search(search)
    elif 'turn on' in final:
        print("listen")
        print(final)
        data=mp.connect(host = host, user = user, password = sql_pass, database="Sophia")
        ed=data.cursor()
        final=final.replace('turn on','',1)
        final=final.replace(' ','',1)
        print(final)
        ed.execute("select name from pins")
        a=ed.fetchall()
        filecontent=[]
        for i in range(len(a)):
            filecontent.append(str(a[i][0]).lower())
        print("found")
        for i in filecontent:
            if final in i:
                ed.execute(f"select vpin from pins where name ='{i}'")
                pin=ed.fetchall()
                print(pin)
                auto(i,pin[0][0],0)
            # else:
            #     win.out(f"sorry, no pin found name {final}")
    elif 'turn off' in final:
        data=mp.connect(host = host, user = user, password = sql_pass, database="Sophia")
        ed=data.cursor()
        final=final.replace('turn off','',1)
        final=final.replace(' ','',1)
        ed.execute("select name from pins")
        a=ed.fetchall()
        filecontent=[]
        for i in range(len(a)):
            filecontent.append(str(a[i][0]).lower())
        for i in filecontent:
            if final in i:
                ed.execute(f"select vpin from pins where name ='{i}'")
                pin=ed.fetchall()
                auto(i,pin[0][0],1)
            # else:
            #     win.out(f"sorry, no pin found name {final}")
    elif 'open' in final:
        data=mp.connect(host = host, user = user, password = sql_pass, database="Sophia")
        ed=data.cursor()
        FOUND=False
        final=final.replace('open','',1)
        final=final.replace(' ','',1)
        ed.execute("select name from files")
        a=ed.fetchall()
        filecontent=[]
        for i in range(len(a)):
            filecontent.append(str(a[i][0]).lower())
        for i in filecontent:
            if final in i:
                ed.execute(f"select file from files where name ='{i}'")
                location=ed.fetchall()
                os.startfile(location[0][0])
                FOUND=True
                break
        if FOUND==False:
            ed.execute("select name from Folder")
            a=ed.fetchall()
            filecontent=[]
            for i in range(len(a)):
                filecontent.append(str(a[i][0]).lower())
            for i in filecontent:
                if final in i:
                    ed.execute(f"select folder from folder where name ='{i}'")
                    location=ed.fetchall()
                    os.startfile(location[0][0])
                    FOUND=True
                    break
            if FOUND==False:
                ed.execute("select name from web")
                b=ed.fetchall()
                web=[]
                for i in range(len(b)):
                    web.append(str(b[i][0]).lower())
                for i in web:
                    if final in i:
                        FOUND=True
                        ed.execute(f"select web from web where name ='{i}'")
                        location=ed.fetchall()
                        webbrowser.open(location[0][0])
                        break
                
            if FOUND==False:
                win.out(f"No Keyword found name '{final}'")
        if FOUND==True:
            win.out(f"Opening '{final}'")
    elif "message" in final:
        host=config("Host")
        user=config("User")
        sqlpassword=config("SqlPassword")
        data=mp.connect(
            host=host, password=sqlpassword, user=user, database="Sophia")
        ed=data.cursor()
        ed.execute("select Name from phone")
        a=ed.fetchall()
        contact_name=[]
        for i in range(len(a)):
            contact_name.append(str(a[i][0]).lower())
        sp=final.split()
        for i in contact_name:
            if i in sp:
                ed.execute(f"Select number from phone where name='{i}'")
                name=i
                break
        no=ed.fetchall()
        data.close()
        if no==[]:
            win.out("contact not found", output=False)
        else:
            SophiaWindow.speak("please tell the message")
            sound.play()
            message=SophiaWindow.SpeechRecognition()
            win.out(f"sending '{message}' to '{name}'")
            no="+91 "+str(no[0][0])
            pywhatkit.sendwhatmsg_instantly(no,message)
            SophiaWindow.speak("message sent!")
    elif 'play' in final or 'on youtube' in final:
        content=final.replace('play', '', 1)   
        content=content.replace('on youtube', '', 1)   
        content=content.replace('search', '', 1)
        win.out(f"Opening {content} on youtube. Have fun")
        pywhatkit.playonyt(content)
    elif 'show' in final:
        if "contacts" in final or "numbers" in final or "contact" in final or "number" in final or "phone" in final or "phones" in final:
            try:
                data=mp.connect(host = host, user = user, password = sql_pass, database="Sophia")
                ed=data.cursor()
                ed.execute("Select name from phone")
                names=ed.fetchall()
                if len(names)==0:
                    win.out("Database empty for contacts")
                else:
                    ed.execute("Select number from phone")
                    contact=ed.fetchall()
                    data.close()
                    win.out("-"*30,say=False)
                    for i in range(len(names)):
                        win.out(f"{names[i][0]}={contact[i][0]}", say=False)
                    win.out("-"*30, say=False)
            except Exception as err:
                if err.__class__.__name__ == "DatabaseError":
                    win.out("unable to connect to my s q l server. please add again", output=False)
        elif "keywords" in final or "keyword" in final or "keyboard" in final or "keyboards" in final:
            try:
                data=mp.connect(host = host, user = user, password = sql_pass, database="Sophia")
                ed=data.cursor()
                ed.execute("Select name from files")
                filenames=ed.fetchall()
                ed.execute("Select file from files")
                filelocation=ed.fetchall()
                ed.execute("Select name from web")
                webnames=ed.fetchall()
                ed.execute("Select web from web")
                weblocation=ed.fetchall()
                ed.execute("select name from folder")
                foldernames=ed.fetchall()
                ed.execute("select folder from folder")
                folderlocation=ed.fetchall()
                data.close()
                if len(filenames)==0 and len(webnames)==0 and len(foldernames)==0:
                    win.out("Database empty for Keywords")
                else:
                    if len(filenames)!=0:
                        win.out("-"*30,say=False)
                        for i in range(len(filenames)):
                            win.out(f"{filenames[i][0]}={filelocation[i][0]}", say=False)
                        win.out("Keywords for System Files", say=False)
                        win.out("-"*30,say=False)
                    if len(webnames)!=0:
                        win.out("-"*30,say=False)
                        for i in range (len(webnames)):
                            win.out(f"{webnames[i][0]}={weblocation[i][0]}", say=False)
                        win.out("Keywords for URL", say=False)
                        win.out("-"*30,say=False)
                    if len(foldernames)!=0:
                        win.out("-"*30,say=False)
                        for i in range(len(foldernames)):
                            win.out(f"{foldernames[i][0]}={folderlocation[i][0]}", say=False)
                        win.out("Keywords for System Folders", say=False)
                        win.out("-"*30, say=False)
            except Exception as err:
                if err.__class__.__name__ == "DatabaseError":
                    win.out("unable to connect to my s q l server. please add again", output=False)
    elif "time" in final:
        current_time=str(datetime.datetime.now().strftime("%I:%M %p"))
        d=f"The Current Time is {current_time}"
        win.out(d)
    elif "weather" in final:
        speak("please tell the city name")
        sound.play()
        city=SophiaWindow.SpeechRecognition()
        w_api_key="0e1b90a815ec5b572fb4eac00e579175" #openweathermap api key
        link=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={w_api_key}"
        data=requests.get(link)
        data=data.json()
        temp=f"Weather in {city.title()}:\nTemperature={int(data['main']['temp']-273)}\N{DEGREE SIGN}C\nCondition={data['weather'][0]['main'].title()}"
        tempsp=f"temperature in {city} is {int(data['main']['temp']-273)} degree celcius and have a {data['weather'][0]['main']} weather condition"
        win.out(tempsp, output=False)
        time.sleep(1)
        win.out(temp, say=False)
    elif "type with me" in final or "tie with me" in final or "type" in final:
        SophiaWindow.speak("ready to recognise")
        sound.play()
        data=SophiaWindow.SpeechRecognition(20)
        SophiaWindow.speak("recognition completed")
        win.out(data,say=False)                   
    elif "shutdown the pc" in final or "shutdown the computer" in final or "shutdown pc" in final or 'shutdown computer' in final or 'turn off the pc' in final or "turn off the computer" in final or 'turn off computer' in final or "turn off computer" in final:
        SophiaWindow.speak("Turning off the pc")
        time.sleep(1.5)
        pywhatkit.shutdown(time=1)                
    elif "download" in final and "youtube" in final:
        SophiaYt.yt()
    elif "change" in final and "location" in final:
        from SophiaAddLocation import ChangeLocation
        ChangeLocation()
    elif "repeat after me" in final:
        SophiaWindow.speak("ready to recognise")
        sound.play()
        data=SophiaWindow.SpeechRecognition()
        win.out(data)
    elif 'tell me about' in final or "tell me who is" in final:
        win.out('searching wikipedia', output=False)
        final=final.replace('tell me about', '')
        final=final.replace('tell me who is', '')
        final=final.replace('tell me what is', '')
        final=final.replace('what is', '')
        final=final.replace('who is', '')
        title=wikipedia.search(final,results=1)
        result=wikipedia.summary(title[0], sentences=1, auto_suggest=False)
        result=f"According to wikipedia, {result}"
        win.out(result)
        time.sleep(0.1)
        SophiaWindow.speak("Should i open the wikipedia page?")
        while True:   
            sound.play()
            try:
                ans=SophiaWindow.SpeechRecognition()
                if "no" in ans or "don't" in ans:
                    SophiaWindow.speak("ok, no issue")
                    break
                elif "yes" in ans or 'sure' in ans or "open" in ans or "take" in ans or 'show' in ans:
                    win.out(f'Opening "{title[0]}" on Wikipedia')
                    webbrowser.open(f"https://en.wikipedia.org/wiki/{title[0]}")
                    break
                else:
                    SophiaWindow.speak("sorry, can you repeat that again") 
            except:
                SophiaWindow.speak("please answer again") 
    elif "on" in final and "screen recording" in final:
        rec_function()   
    else:
        # win.out("sorry, didn't recognised that", output=False) 
        out=ai_out(final)
        win.out(out)
        win.out(f"The Responce of '{final}'",say=False)
      


def StartTheProgram():
    def wish():
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            a = "Good Morning. your assistance is now online and ready to assist you on your command"
            speak(a)
        elif hour >= 12 and hour < 18:
            a = "Good after noon. your assistance is now online and ready to assist you on your command"
            speak(a)
        else:
            a = "Good evening. your assistance is now online and ready to assist you on your command"
            speak(a)
    wish()
    try:
        porcupine = pvporcupine.create(keyword_paths=["./Sophia_en_windows_v2_1_0.ppn"], access_key="BJZ18LSgiD+GUE5Ky/4n9JCV7FGPINmyMfqjHNSTU0wliYVBPowBrQ==")

        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
                        rate=porcupine.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=porcupine.frame_length)

        
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print('key is pressed')
                try:
                    import pywhatkit
                    sound.play()
                    final=SophiaWindow.SpeechRecognition()
                    print(final)
                    runAssistant(final)
                except Exception as a:
                    print(a)
                    if (a.__class__.__name__)=="InternetException":
                        SophiaWindow.speak("Please check your internet connection")
    except Exception as a:
        print(a)
            
 
if __name__=="SophiaBackend":
    from threading import Thread
    win=SophiaWindow.MainWindow()
    def textrun(n):
        final=win.input.get()
        if final!='':
            win.input.delete(0,'end')
            runAssistant(final)
        else:
            win.out("Leaving the Entry empty")
    def start():
        win.StartTheWindow("800x600+250+80", "Sophia, The Virtual Assistant", "#3AA8EC",) 
        win.input=Entry(win.root,width=550, bg="black", font=("Times", 14), fg= 'light green')
        win.input.place(x=268, y=536, height=40, width=510) 
        win.input.bind('<Return>', textrun)
        win.root.mainloop()
    Thread(target=start).start()

    time.sleep(1.5)
    StartTheProgram()