import speech_recognition as sr
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import write
import datetime
import wikipedia
import webbrowser
import pywhatkit
import os
import subprocess
from difflib import SequenceMatcher
import urllib.parse

# =========================
# SPEAK FUNCTION
# =========================

def speak(text):

    try:

        print("Assistant:", text)

        # Create fresh engine every time
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')

        engine.setProperty('voice', voices[0].id)

        engine.setProperty('rate', 170)

        engine.setProperty('volume', 1.0)

        engine.say(str(text))

        engine.runAndWait()

        engine.stop()

    except Exception as e:

        print("Voice Error:", e)
# =========================
# RECORD AUDIO FUNCTION
# =========================

def record_audio(filename="voice.wav", duration=5, fs=44100):

    print("\nSpeak now...")

    audio = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype='int16'
    )

    sd.wait()

    write(filename, fs, audio)

    print("Recording completed.\n")

# =========================
# LISTEN FUNCTION
# =========================

def listen():

    record_audio()

    recognizer = sr.Recognizer()

    try:

        with sr.AudioFile("voice.wav") as source:

            print("Recognizing...")

            audio = recognizer.record(source)

            command = recognizer.recognize_google(audio)

            command = command.lower()

            print("You said:", command)

            return command

    except sr.UnknownValueError:

        speak("Sorry, I could not understand.")

        return ""

    except sr.RequestError:

        speak("Internet connection problem.")

        return ""

    except Exception as e:

        print("Error:", e)

        speak("Something went wrong.")

        return ""

# =========================
# OWNER VOICE VERIFICATION
# =========================

AUTHORIZED_PHRASE = "jarvis "

def verify_owner(command):

    similarity = SequenceMatcher(
        None,
        AUTHORIZED_PHRASE,
        command
    ).ratio()

    print("Voice Match Similarity:", similarity)

    # 80% similarity required
    if similarity > 0.80:

        return True

    return False


# =========================
# ASSISTANT BRAIN
# =========================

# =========================
# APPLICATION DATABASE
# =========================

apps = {

    "vs code": "code",
    "visual studio code": "code",

    "chrome": "chrome",
    "google chrome": "chrome",
    "google": "chrome",

    "edge": "msedge",

    "notepad": "notepad",

    "calculator": "calc",

    "paint": "mspaint",

    "spotify": "spotify"
}




def assistant(command):

    # =====================
    # GREETINGS
    # =====================

    if "hello" in command:

        speak("Hello! How can I help you?")

    elif "how are you" in command:

        speak("I am fine and ready to help you.")

    elif "your name" in command:

        speak("I am your Python voice assistant.")

    # =====================
    # TIME AND DATE
    # =====================

    elif "time" in command:

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        speak(f"The current time is {current_time}")

    elif "date" in command:

        today = datetime.datetime.now().strftime("%d %B %Y")

        speak(f"Today's date is {today}")

    # =====================
    # OPEN WEBSITES
    # =====================

    elif "open youtube" in command:

        speak("Opening YouTube")

        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:

        speak("Opening Google")

        webbrowser.open("https://www.google.com")

    elif "open github" in command:

        speak("Opening GitHub")

        webbrowser.open("https://github.com")

    # =====================
    # DEEP RESEARCH
    # =====================

    elif "deep research" in command:

        topic = command.replace("deep research", "").strip()

        if topic:

            speak(f"Starting deep research on {topic}")

            search_url = (
                    "https://www.google.com/search?q="
                    + urllib.parse.quote(topic)
            )

            try:
                chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
                webbrowser.get(chrome_path).open(search_url)

            except:
                webbrowser.open(search_url)

        else:

            speak("Please tell me a topic to research.")


    # =====================
    # PLAY SONGS
    # =====================

    elif "play" in command:

        song = command.replace("play", "")

        speak(f"Playing {song}")

        pywhatkit.playonyt(song)

    # =====================
    # WIKIPEDIA SEARCH
    # =====================

    elif "who is" in command:

        person = command.replace("who is", "")

        try:

            info = wikipedia.summary(person, 2)

            speak(info)

        except:

            speak("Sorry, I could not find information.")

    elif "what is" in command:

        topic = command.replace("what is", "")

        try:

            info = wikipedia.summary(topic, 2)

            speak(info)

        except:

            speak("Sorry, I could not find information.")

    # =====================
    # MATH OPERATIONS
    # =====================

    elif "plus" in command:

        try:

            parts = command.split("plus")

            num1 = int(parts[0])

            num2 = int(parts[1])

            result = num1 + num2

            speak(f"The answer is {result}")

        except:

            speak("Please say numbers correctly.")

    elif "minus" in command:

        try:

            parts = command.split("minus")

            num1 = int(parts[0])

            num2 = int(parts[1])

            result = num1 - num2

            speak(f"The answer is {result}")

        except:

            speak("Please say numbers correctly.")

    elif "multiply" in command:

        try:

            parts = command.split("multiply")

            num1 = int(parts[0])

            num2 = int(parts[1])

            result = num1 * num2

            speak(f"The answer is {result}")

        except:

            speak("Please say numbers correctly.")

    elif "divide" in command:

        try:

            parts = command.split("divide")

            num1 = int(parts[0])

            num2 = int(parts[1])

            result = num1 / num2

            speak(f"The answer is {result}")

        except:

            speak("Please say numbers correctly.")

    # =====================
    # GENERAL KNOWLEDGE
    # =====================

    elif "capital of pakistan" in command:

        speak("The capital of Pakistan is Islamabad.")

    elif "capital of india" in command:

        speak("The capital of India is New Delhi.")

    elif "largest planet" in command:

        speak("Jupiter is the largest planet in our solar system.")

    elif "fastest animal" in command:

        speak("Cheetah is the fastest land animal.")

    elif "largest ocean" in command:

        speak("Pacific Ocean is the largest ocean in the world.")

    elif "python" in command:

        speak("Python is a powerful and beginner friendly programming language.")

    elif "artificial intelligence" in command:

        speak("Artificial intelligence allows machines to simulate human intelligence.")

    elif "machine learning" in command:

        speak("Machine learning is a branch of artificial intelligence.")


    # =====================
    # OS CONTROL COMMANDS
    # =====================

    elif "open notepad" in command:
        speak("Opening Notepad")
        subprocess.run("notepad")

    elif "open" in command:

        app_name = command.replace("open", "").strip()

        found = False

        for key in apps:

            if key in app_name:
                speak(f"Opening {key}")

                os.system(f"start {apps[key]}")

                found = True

                break

        if not found:
            speak("Application not found")

    elif "open calculator" in command:
        speak("Opening Calculator")
        subprocess.run("calc")

    elif "open paint" in command:
        speak("Opening Paint")
        subprocess.run("mspaint")

    elif "open file explorer" in command:
        speak("Opening File Explorer")
        subprocess.run("explorer")

    elif "open chrome" in command:
        speak("Opening Chrome")
        subprocess.run("start chrome", shell=True)

    elif "open edge" in command:
        speak("Opening Microsoft Edge")
        subprocess.run("start msedge", shell=True)

    elif "open downloads" in command:
        speak("Opening Downloads folder")
        subprocess.run("explorer C:\\Users\\%USERNAME%\\Downloads", shell=True)

    elif "lock pc" in command:
        speak("Locking your system")
        subprocess.run("rundll32.exe user32.dll,LockWorkStation")

    elif "restart pc" in command:
        speak("Restarting your computer")
        subprocess.run("shutdown /r /t 5")

    elif "shutdown pc" in command:
        speak("Shutting down your computer")
        subprocess.run("shutdown /s /t 5")

    elif "system info" in command:
        speak("Opening system information")
        subprocess.run("msinfo32")
    # =====================
    # EXIT
    # =====================

    elif "thank you" in command:

        speak("You are welcome.")

    elif "bye" in command:

        speak("Goodbye! Have a nice day.")

        exit()



    # =====================
    # DEFAULT RESPONSE
    # =====================

    else:

        speak("I could not understand")


# =========================
# WAKE WORD SETTINGS
# =========================

WAKE_WORD = "jarvis"

# =========================
# MAIN PROGRAM
# =========================

speak("Voice assistant started.")

active = False

while True:

    # =====================
    # WAIT FOR WAKE WORD
    # =====================

    if not active:

        print("\nWaiting for wake word...")

        wake_command = listen()

        if WAKE_WORD in wake_command:

            active = True

            speak("Yes, I am listening.")

    # =====================
    # ASSISTANT ACTIVE MODE
    # =====================

    else:

        print("\nListening for command...")

        user_command = listen()

        if user_command == "":

            continue

        # Sleep mode
        if "sleep" in user_command or "stop listening" in user_command:

            active = False

            speak("Going to sleep.")

            continue

        # Run assistant commands
        assistant(user_command)