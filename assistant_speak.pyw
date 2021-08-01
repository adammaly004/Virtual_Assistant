
from tkinter import *
import textwrap
import os
import random
import datetime
import wikipedia
import time
import json
from googlesearch import search
from wikipedia.exceptions import WikipediaException
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
import requests
import math
import pyttsx3
import threading
import speech_recognition as sr


root = Tk()
root.config(bg="light grey")
root.geometry('300x500+10+500')
root.title('Pikachu')
root.iconbitmap('img\Pikachu_Head.ico')

# Main window
canvas = Canvas(root, width=200, height=200, bg="snow")
canvas.grid(row=0, column=0, columnspan=2)
canvas.place(x=10, y=10, width=280, height=430)

# Set pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Load json file with commands
with open("commands.json", "r", encoding='utf-8') as f:
    COMMAND = json.load(f)


messages = []


class Me:
    def __init__(self, master, message=""):
        self.master = master
        self.frame = Frame(master, bg="cyan")
        self.i = self.master.create_window(
            270, 390, window=self.frame, anchor="ne")
        Label(self.frame, text=textwrap.fill(message, 20), font=(
            "Sogue", 10), bg="cyan").grid(row=1, column=0, sticky="w", padx=1, pady=3)
        root.update_idletasks()
        ask.delete(0, END)

        # Apply commands
        if 'translate' in message:
            translator(message)
        elif 'wikipedia' in message:
            Search(message)
        elif 'timer' in message:
            Timer(message)
        elif 'google' in message:
            Google(message)
        elif 'note' in message:
            Note(message)
        elif 'coronavirus' in message:
            try:
                cases, deaths, recovered = get_data(message)
                put_answer(f"Cases {cases}")
                put_answer(f"Deaths {deaths}")
                put_answer(f"Recovered {recovered}")
            except Exception:
                put_answer("I can't find your country")

        elif 'video' in message:
            find_video(message)
            put_answer('Have a nice day!')
        elif 'what is' in message:
            x = Math_Operations(message)
            put_answer(str(x))
        elif 'weather' in message:
            try:
                temp, w = weather(message)
                put_answer(f"The temperature is {temp}°C")
                put_answer(w)
            except Exception:
                put_answer("I can't find your place")
        else:
            keys = COMMAND.keys()

            for key in keys:
                if message in key and len(message) > 1 or key == "error":
                    commands = COMMAND.get(key)
                    for command in commands[0]:
                        os.startfile(command)

                    answer = random.choice(commands[1])
                    put_answer(answer)

                    if "rock" in message or "scissors" in message or "paper" in message:
                        result = Rock(message, answer)
                        put_answer(result)
                    elif 'tell me a joke' in message or "joke" in message:
                        canvas.move(ALL, 0, -120)
                    elif 'clear' in message:
                        canvas.move(ALL, -1000, 0)
                    elif 'time' in message:
                        Time = datetime.datetime.now().strftime("%H:%M:%S")
                        put_answer(Time)
                    elif 'stop' in message or 'bay' in message or 'bey' in message or 'see you soon' in message:
                        root.quit()
                    break


answers = []


class Assistant:
    def __init__(self, master, answer=""):
        self.master = master
        self.frame = Frame(master, bg="dodger blue")
        self.i = self.master.create_window(
            10, 390 + 40, window=self.frame, anchor="nw")
        Label(self.frame, text=textwrap.fill(answer, 25), font=("Sogue", 10),
              bg="dodger blue").grid(row=1, column=0, sticky="w", padx=1, pady=3)
        root.update_idletasks()

# Functions


def send_message():
    canvas.move(ALL, 0, -50)
    message = get_audio()
    me = Me(canvas, message)
    messages.append(me)
    #ask.delete(0, END)
    asking = random.choice(['What can I do for you!', 'How can I help?'])
    put_answer(asking)


def write_message():
    canvas.move(ALL, 0, -50)
    me = Me(canvas, message=ask.get())
    messages.append(me)
    #ask.delete(0, END)
    asking = random.choice(['What can I do for you!', 'How can I help?'])
    put_answer(asking)


def put_answer(answer):
    assistant = Assistant(canvas, answer=answer)
    answers.append(assistant)
    canvas.move(ALL, 0, -35)
    canvas.update()
    q = threading.Thread(target=speak(answer))
    q.start()


def key(event=None):
    q = threading.Thread(target=send_message)
    q.start()


def key1(event=None):
    q = threading.Thread(target=write_message)
    q.start()


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        put_answer("Hello Adam, Good Morning")
        put_answer("How can I help?")
    elif hour >= 12 and hour < 18:
        put_answer("Hi Adam, Good Afternoon")
        put_answer("How can I help?")
    else:
        put_answer("Hello Adam, Good Evening")
        put_answer("How can I help?")


def Timer(message):
    t = message.replace("timer", "")
    try:
        time.sleep(int(t))
        put_answer('Time is over')
    except Exception:
        put_answer("Write your time")


def Rock(message, answer):
    if message == 'rock' or message == 'paper' or message == 'scissors':
        if answer == 'Rock' and message == 'paper':
            result = 'You won'
        elif answer == 'Paper' and message == 'rock':
            result = 'I won'
        elif answer == 'Scissors' and message == 'rock':
            result = 'You won'
        elif answer == 'Rock' and message == 'scissors':
            result = 'I won'
        elif answer == 'Paper' and message == 'scissors':
            result = 'You won'
        elif answer == 'Scissors' and message == 'paper':
            result = 'I won'
        else:
            result = 'Draw'
        return result


def Search(message):
    put_answer('Searching Wikipedia...')
    statement = message.replace("wikipedia", "")
    try:
        results = wikipedia.summary(statement, sentences=3)
        put_answer(results)
        canvas.move(ALL, 0, -len(results)*0.68)
    except WikipediaException:
        put_answer('I can not find it')


def Google(message):
    query = message.replace("google ", "")
    j = search(query)
    put_answer(f"Google {query}")
    os.startfile(j[0])
    # root.clipboard_clear()
    # root.clipboard_append(j[0])
    # root.update()
    canvas.move(ALL, 0, -20)


def Note(message):
    message = message.replace('note ', '')
    root.clipboard_clear()
    root.clipboard_append(message)
    root.update()
    os.startfile(COMMAND[0]['note'][0])
    put_answer('Paste a note!')


def get_data(message):
    coutry = message.replace("coronavirus ", "")
    if coutry == "czech republic":
        coutry = "czech-republic"
    url = f"https://www.worldometers.info/coronavirus/country/{coutry}/"

    # Make a request
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extract and store in top_items according to instructions on the left
    products = soup.select('div.content-inner')
    for elem in products:
        total_cases = elem.select('div.maincounter-number')[0].text
        total_deaths = elem.select('div.maincounter-number')[1].text
        total_recovered = elem.select('div.maincounter-number')[2].text
    return total_cases, total_deaths, total_recovered


def find_video(message):
    video = message.replace("video ", "")
    videosSearch = VideosSearch(video, limit=1)
    info = videosSearch.result()
    url = f"https://www.youtube.com/watch?v={info['result'][0]['id']}"
    os.startfile(url)


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ''
        try:
            said = r.recognize_google(audio)
        except Exception:
            put_answer('Error')
    return said.lower()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def Math_Operations(operation):
    ex = operation.replace("what is ", "")
    try:
        if "sin" in ex:
            ex = ex.replace("sin ", "")
            result = math.sin(float(ex))

        elif "cos" in ex:
            ex = ex.replace("cos ", "")
            result = math.cos(float(ex))

        elif "factorial" in ex:
            ex = ex.replace("factorial ", "")
            result = math.factorial(int(ex))

        elif "binary" in ex:
            ex = ex.replace("binary ", "")
            ex = bin(int(ex))
            result = ex.replace("0b", "")

        else:
            result = str(eval(ex))

        return result

    except Exception:
        result = "I don't understand"

    return result


def translator(sentence):
    sentence = sentence.replace("translate to ", "")
    if 'czech' in sentence:
        sentence = sentence.replace("czech", "csech")
    try:
        sentence = sentence.split(" ", 1)
        url = f'https://translate.google.cz/?hl=cs&sl=auto&tl={sentence[0][:2]}&text={sentence[1]}&op=translate'
        os.startfile(url)
        put_answer("I get advice from google")
    except Exception:
        put_answer("Try again")


def weather(city):
    city = city.replace('weather ', '')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=8ef61edcf1c576d65d836254e11ea420"
    r = requests.get(url)
    r = r.json()
    temp = r['main']['temp'] - 273.15
    weather = r['weather'][0]['description'].capitalize()

    temp = round(temp, 1)
    return temp, weather


# Entry
ask = Entry(root, bd=0, width=26, font=("Sogue", 12))
ask.place(x=10, y=450, width=230, height=35)
ask.focus()
ask.insert(0, "")


button = Button(root, justify=LEFT, command=key)
photo = PhotoImage(file="img/Pikachu_Head.gif")
button.config(image=photo, width="32", height="30", relief=FLAT)
button.pack(side=LEFT)
button.place(x=250, y=450)

root.bind('<Return>', key1)
root.resizable(width=False, height=False)
root.lift()
root.call('wm', 'attributes', '.', '-topmost', True)
root.update()
wishMe()
root.mainloop()
threading.Thread._keep_alive = False
