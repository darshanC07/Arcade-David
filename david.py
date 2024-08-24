import speech_recognition as sr
import webbrowser
import win32com.client
import os
from playsound import playsound
import datetime
from config import gemini_api_key
import google.generativeai as genai
import time


conversation = []

# user_history = []


def chat(prompt):
    global conversation
    conversation.append({"role" : "Darshan" , "content" : prompt})
    print(f"Role : Darshan \nContent : {prompt}")

    genai.configure(api_key=gemini_api_key)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        #   "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=f"you are jarvis, a virtual assistant. you are provided with conversation history {conversation} and your work is to go through the history and analyze it. and if your input prompt is available in history then answer the input from conversation history and if the question is new to you then answer how you normally answer. answers should be to the point and short."
    )

    chat_session = model.start_chat(history = [])

    response = chat_session.send_message(prompt)
    response.resolve()

    conversation.append({"role" : "Jarvis","content" : response.text})

    if "history".lower() in prompt.lower():
        return chat_session.history

    if "clear conversation history".lower() in prompt.lower():
        conversation = []
    return response.text


def gemini_ai(prompt):

    genai.configure(api_key=gemini_api_key)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        #   "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        system_instruction="Your name is David, an AI assistant. Act as a friendly, smart, supportive, guiding assistant to user. also remember the inputs of user. Keep your answer short, to the point. ",
    )

    chat = model.start_chat(history = [])

    response = chat.send_message(prompt)

    return (response.text)

def summarizer(history):
    summary = gemini_ai(f"summarize the following text : {history}")
    return summary

def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    # r.adjust_for_ambient_noise = 1

    with sr.Microphone() as source:
        r.pause_threshold = 0.8

        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-us")

            return query
        except Exception as e:
            print(e)
            say("Some error occurred by Jarvis A I")

if __name__ == "__main__":
    say("Hello I am Jarvis A I")
    sites = [["Youtube","https://www.youtube.com"],["wikipedia","https://www.wikipedia.org"],["google","https://google.com"]]
