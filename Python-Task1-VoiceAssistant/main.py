import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
from urllib.parse import quote_plus

engine = pyttsx3.init()
engine.setProperty("rate", 160)
recognizer = sr.Recognizer()


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    try:
        with sr.Microphone() as source:
            print("Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

        command = recognizer.recognize_google(audio, language="en-IN")
        print("You said:", command)
        return command.lower()

    except sr.WaitTimeoutError:
        speak("I did not hear anything. Please try again.")
    except sr.UnknownValueError:
        speak("Sorry, I could not understand. Please repeat.")
    except sr.RequestError:
        speak("Speech recognition needs internet.")
    except OSError as error:
        print("Microphone error:", error)
        speak("Please check your microphone.")

    return ""


def process_command(command):
    if not command:
        return True

    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you?")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The current time is " + current_time)

    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        speak("Today's date is " + current_date)

    elif "search" in command or "google" in command:
        query = command.replace("search", "", 1).strip()
        query = query.replace("for", "", 1).strip()
        query = query.replace("google", "", 1).strip()

        if query:
            speak("Searching for " + query)
            webbrowser.open(
                "https://www.google.com/search?q=" + quote_plus(query)
            )
        else:
            speak("Please tell me what to search for.")

    elif "help" in command:
        speak("Say hello, ask for the time or date, "
              "or say search for Python tutorials.")

    elif any(word in command for word in ["bye", "exit", "stop"]):
        speak("Goodbye! Have a nice day.")
        return False

    else:
        speak("I do not know that command yet. Please try again.")

    return True


def main():
    speak("Hello! I am your Python voice assistant.")
    speak("Say help to hear the available commands.")

    running = True
    while running:
        command = listen()
        running = process_command(command)


if __name__ == "__main__":
    main()
    
