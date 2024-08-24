import webbrowser
import win32com.client
import os
from playsound import playsound
# from playsound import playsound
import datetime
from config import gemini_api_key
import google.generativeai as genai
@@ -27,18 +27,14 @@ def chat(prompt):
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=f"you are david, a virtual assistant. you are provided with conversation history {conversation} and your work is to go through the history and analyze it. and if your input prompt is available in history then answer the input from conversation history and if the question is new to you then answer how you normally answer. answers should be to the point and short."
        system_instruction=f"you are david, a virtual assistant, built by 'Darshan Choudhary'. you are provided with conversation history {conversation} and your work is to go through the history and analyze it. if your input prompt is available in history then answer the input from conversation history and if the question is new to you then answer how you normally answer. answers should be to the point and short. act friendly with user, give polite replies and act similar to humans",
    )

    chat_session = model.start_chat(history = [])

    response = chat_session.send_message(prompt)
    response.resolve()

    conversation.append({"role" : "user" , "content" : prompt})
    conversation.append({"role" : "david","content" : response.text})

    return response.text

@@ -56,16 +52,14 @@ def gemini_ai(prompt):
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="Your name is David, an AI assistant. Act as a friendly, smart, supportive, guiding assistant to user. also remember the inputs of user. Keep your answer short, to the point. ",
    )

    chat = model.start_chat(history = [])


    response = chat.send_message(prompt)


    return (response.text)

@@ -120,15 +114,17 @@ def takeCommand():

            return query
        except Exception as e:
            pass
            # print(e)
            say("Some error occurred by David A I")
            # say("Some error occurred by David A I")


basic_category = {
    "other" : ["open text file", "open specific app/file" ,"create a new text file with name", "find specific folder", "give path of specific     file"] , 
    "normal" : ["remember something" , "recall it"]}
    "other" : ["open text file", "open specific app/file" ,"create a new text file with name", "find specific folder", "give path of specific file" , "play specific song, etc.."] , 
    "normal" : ["remember something" , "recall it","tell me a joke"]}

if __name__ == "__main__":
    print("Hello I am David A I")
    say("Hello I am David A I")
    sites = [["Youtube","https://www.youtube.com"],["wikipedia","https://www.wikipedia.org"],["google","https://google.com"]]
    while True:
@@ -138,6 +134,8 @@ def takeCommand():
            print(f"User : {command}")

            if "quit" in command :
                print("OK Thank You Sir , Have a nice day")
                say("Ok Thank You Sir , Hve a nice day")
                exit()

            if command=="david":
@@ -151,28 +149,25 @@ def takeCommand():

                new_category = new_classifier(command)
                # print(new_category)

                if "open music" in command :
                    musicPath = "C:/Users/acer/Downloads/sample_music.mp3"
                    # playsound(musicPath) #alternate way
                    os.system(f"start {musicPath}")

                elif "clear conversation history".lower() in command:
                if "clear conversation history".lower() in command:
                    conversation = []  

                elif "conversation history".lower() in command :
                    # print("here")
                    print(conversation)

                elif "other".lower() in new_category:
                    new_prompt = f"just return the code which will fulfill the command , just return the code of following command and nothing else : {command} consider that the device is of Windows OS"
                    # print("here")
                    new_prompt = f"just return the code which will fulfill the command , just return the code of following command and nothing else , mostly use os module for it,but if not suitable then you can also use webbrowser module to open sites and consider that os module is already imported: {command} consider that the device is of Windows OS"
                    code_response = gemini_ai(new_prompt)
                    final_code = cleaner(code_response)
                    conversation_appender(command,final_code)
                    # print(final_code)
                    exec(final_code)

                else:
                    # print("in command")
                    chat_response = chat(command)
                    conversation_appender(command,chat_response)
                    print(f"Role : David\nContent : {chat_response}")
@@ -181,11 +176,15 @@ def takeCommand():
            elif "question".lower() in category:

                if "time" in command :
                    hour = datetime.datetime.now().strftime("%H")
                    mins = datetime.datetime.now().strftime("%M")
                    hour = int(datetime.datetime.now().strftime("%H"))
                    if hour>12:
                        hour = hour - 12
                    mins = int(datetime.datetime.now().strftime("%H"))
                    print(f"Current time is {hour} hours {mins} minutes")
                    say(f"Current time is {hour} hours {mins} minutes")

                else:
                    # print("in question")
                    chat_response = chat(command)
                    conversation_appender(command,chat_response)
                    print(f"Role : David\nContent : {chat_response}")
@@ -199,6 +198,7 @@ def takeCommand():
                print(response)

            else:
                # print("in else")
                chat_response = chat(command)
                conversation_appender(command,chat_response)
                print(f"Role : David\nContent : {chat_response}")
                say(chat_response)
                
                
        except Exception as e:
            # print(e)
            pass
