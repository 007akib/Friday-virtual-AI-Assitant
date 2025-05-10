import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia
import pywhatkit 
import mtranslate
import openai as ai
import openai_request



# friday voice adjustment 
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    engine.setProperty('voice',voice.id)
    engine.setProperty('rate',150)
engine.runAndWait()     


#speak function (friday bolegi)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()   

def command():
    content = " "
    while content == " ": 
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("welcome sir")
            audio = r.listen(source)
            

        # recognize speech using Google Speech Recognition
        try:
            content= r.recognize_google(audio,language='en-in')
            print("you said : \n"+ content)  
        except Exception as e:
            print("please try again....sir") 
               

    return content

def main_process():
    friday_chat =[]
    while True:
        request = command().lower()
        if "hey friday" in request:
            speak("welcome Aakib sir, what i do for you ?")
        elif "satvik sir" in request:
            speak("satvik sir is our mentor.")                      
        elif "play music" in request:
            speak("playing music") 
            song = random.randint(1,5)
            if song == 1 :
                webbrowser.open("https://www.youtube.com/watch?v=e36s_nZCD94")
            elif song == 2:
                webbrowser.open("https://www.youtube.com/watch?v=hHuG7FIKgtc")
            elif song == 3:
                webbrowser.open("https://www.youtube.com/watch?v=Q7kv9nuhTB8")
            elif song == 4:
                webbrowser.open("https://www.youtube.com/watch?v=KUpwupYj_tY")
            elif song == 5:
                webbrowser.open("https://www.youtube.com/watch?v=w9Qo6p4XsXE")            
        elif "time" in request:
            now_time = datetime.datetime.now().strftime("%H:%M")
            speak("curent time" + str(now_time) )
        elif "good" in request:
            print("my pleasure sir")
            speak("my pleasure sir , always there for you")    
        elif "date" in request:    
            now_date = datetime.datetime.now().strftime("%d:%m")
            speak("curent time" + str(now_time) )
        elif "new task" in request:
             task = request.replace("new task","")
             task = task.strip()
             if task !="":
                 speak("adding task: " + task)
                 with open ("todo.txt","a") as file:
                     file.write(task + "\n")
        elif "today task" in request:
            with open ("todo.txt","r") as file:
                speak("todays work to do is : " + file.read())  
        elif "show work" in request :                  
            with open ("todo.txt","r") as file:
                task= file.read()
            notification.notify(
                title = "today work",
                message = task
            ) 
        elif "open youtube" in request:
            webbrowser.open("www.youtube.com")        
        elif "open" in request:
            query = request.replace("open","")
            pyautogui.press('super')
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
        elif "wikipedia" in request:
            request = request.replace("search wikipedia","")
            request = request.strip().lower()
            result = wikipedia.summary(request,sentences=2)
            speak(result)
        elif "search google" in request:
            request = request.replace("serch google","")
            request = request.strip().lower()
            webbrowser.open("https://www.google.com/search?q="+ request)   
        elif "send whatsapp" in request:
            pywhatkit.sendwhatmsg("+919682424081","hi i am friday , shukla ji you are hacked",10,26,15)
        elif "ask ai" in request:
            request=request.replace("friday", "")
            request=request.replace("what", "")

            print(request)

            response = openai_request.send_request(request)
            print(response)
            speak(response) 
        else:
            request=request.replace("friday", "")
            
            friday_chat.append( {"role": "user","content": request})
            print(friday_chat)
            response = openai_request.send_request2(friday_chat)

            friday_chat.append({"role":"assistant","content": response})
            print(friday_chat)
            speak(response)

main_process()
