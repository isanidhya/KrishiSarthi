import flet as ft
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr

def main(page: ft.Page):
    page.title = "KrishiSarthi: AI Chat Helper for Indian Farmers"
    
    # Configure Google Gen AI
    genai.configure(api_key="YOUR_API_KEY_HERE") #Make sure to replace "YOUR_API_KEY_HERE" with your actual Google API key
    model = genai.GenerativeModel('gemini-pro')
    
    page.scroll = "auto"
    
    def get_voice_input():
        engine = pyttsx3.init()
        engine.setProperty('rate', 130)
        engine.say('What do you think?')
        engine.runAndWait()
        
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        
        try:
            text = r.recognize_google(audio, language='hi-IN')
            print(text)
            return text
        except sr.UnknownValueError:
            print("I couldn't understand what you said.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""
    
    def gotoAi(text):
        if text:
            response = model.generate_content(f"answer in Hindi {text} and context of farming in India without mentioning it and answer in crisp and in simpler way")
            page.add(
                ft.Text(text, style=ft.TextStyle(color="blue")),
                ft.Markdown(
                    response.text,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    on_tap_link=lambda e: page.launch_url(e.data),
                )
            )
    
    def handle_text_input(e):
        gotoAi(e.control.value)
    
    cmdtext = ft.TextField(hint_text="What do you think?")
    cmdtext.on_change = handle_text_input
    search_btn = ft.ElevatedButton("Search", on_click=handle_text_input)
    voice_btn = ft.IconButton(icon="mic", on_click=lambda _: gotoAi(get_voice_input()))
    
    page.add(ft.Column(controls=[cmdtext, ft.Row(controls=[search_btn, voice_btn])]))

ft.app(target=main)
