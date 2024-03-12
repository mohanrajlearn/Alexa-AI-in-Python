import os
import pywhatkit
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import wikipedia
from gtts import gTTS
from pydub import AudioSegment


app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alexa/skill', methods=['POST'])
def alexa_skill():
    request_data = request.get_json()

    # Extract user input from the frontend
    user_input = request_data.get('user_input', '')

    # Call the backend Alexa skill implementation
    response = handle_alexa_request(user_input)

    return jsonify(response)

def handle_alexa_request(user_input):
    try:
        if user_input.lower() == "home controls":
            return LaunchRequestHandler().handle()
        elif user_input.lower() == "hello world":
            return HelloWorldIntentHandler().handle()
        elif user_input.lower() == "help":
            return HelpIntentHandler().handle()
        elif user_input.lower() in ["cancel", "stop"]:
            return CancelOrStopIntentHandler().handle()
        elif any(keyword in user_input.lower() for keyword in ["turn on", "start", "open", "switch on"]):
            device_name = get_device_name(user_input)
            return DevicesControlIntentHandler().handle(device_name)
        elif any(keyword in user_input.lower() for keyword in ["end", "stop", "turn off", "switch off", "check"]):
            device_name = get_device_name(user_input)
            return DevicesCheckIntentHandler().handle(device_name)
        elif "play" in user_input.lower():
            video_name = user_input.lower().replace("play", "").replace("video", "").strip()
            return PlayVideoIntentHandler().handle(video_name)
        elif "time" in user_input.lower() or "current time" in user_input.lower():
            return CurrentTimeIntentHandler().handle()
        elif "what is" in user_input.lower():
            search_query = user_input.lower().replace("what is", "").strip()
            return WikipediaIntentHandler().handle(search_query)
        elif "who is" in user_input.lower():
            search_query = user_input.lower().replace("who is", "").strip()
            return WikipediaIntentHandler().handle(search_query)

        else:
            return FallbackIntentHandler().handle()
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Exception: {e}")
        # Return a generic error response
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "SSML",
                    "ssml": "<speak>Sorry, there was an error. Please try again later.</speak>"
                },
                "shouldEndSession": False
            },
            "mp3_output": ""  # Provide an empty URL for the audio response since there's an error
        }

def get_device_name(user_input):
    # Extract device name from the user input using a simple pattern match
    # You can implement more sophisticated NLP-based methods for extracting device names
    # Here, we are assuming that the device name is the last word in the user input
    words = user_input.lower().split()
    return words[-1] 

 

class WikipediaIntentHandler:
    def handle(self, search_query):
        try:
            # Search Wikipedia for the given query
            wikipedia_result = wikipedia.summary(search_query, sentences=1)
            # Trim the result to only 25 characters
            wikipedia_result = wikipedia_result[:170]
            speak_output = f"On Wikipedia, {wikipedia_result}."

            # Generate audio from the text using gTTS
            audio_path = "static/output.mp3"
            tts = gTTS(text=speak_output, lang="en", slow=False)
            tts.save(audio_path)

            # Extend the audio play time to at least 30 seconds
            output_file_path = "static/extended_output.mp3"
            self.extend_audio_play_time(audio_path, output_file_path, 30)

            # Create the response to send back to frontend
            response = {
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "SSML",
                        "ssml": "<speak>" + speak_output + "</speak>"
                    },
                    "shouldEndSession": False
                },
                "mp3_output": "/static/extended_output.mp3"  # Provide the URL for the extended audio response
            }

            return response
        except wikipedia.exceptions.PageError:
            speak_output = "Sorry, I couldn't find any information on that topic."
            return self.generate_alexa_response(speak_output)
        except wikipedia.exceptions.DisambiguationError:
            speak_output = "Sorry, I found multiple results for that topic. Can you please be more specific?"
            return self.generate_alexa_response(speak_output)

    def extend_audio_play_time(self, input_file_path, output_file_path, min_duration):
        audio = AudioSegment.from_file(input_file_path)

        # Calculate the duration of the audio in milliseconds
        audio_duration = len(audio)

        if audio_duration >= min_duration * 1000:
            # If the audio duration is already greater than or equal to the minimum duration, do nothing
            audio.export(output_file_path, format="mp3")
        else:
            # Calculate the number of times to repeat the audio to reach the minimum duration
            repetitions = int(min_duration * 1000 / audio_duration) + 1

            # Repeat the audio to meet the minimum duration
            extended_audio = audio * repetitions

            # Trim the extended audio to the minimum duration
            extended_audio = extended_audio[:min_duration * 1000]

            # Export the extended audio
            extended_audio.export(output_file_path, format="mp3")

 
class CurrentTimeIntentHandler:
    def handle(self):
        # Get the current time in 12-hour format
        current_time = datetime.now().strftime("%I:%M %p")
        speak_output = f"The current time is {current_time}."
        return self.generate_alexa_response(speak_output)

    def generate_alexa_response(self, speak_output):
        # Generate speech using espeak and save it as 'output.mp3'
        os.system(f'espeak -ven "{speak_output}" -w static/output.mp3')

        # Create the response to send back to frontend
        response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "SSML",
                    "ssml": "<speak>" + speak_output + "</speak>"
                },
                "shouldEndSession": False
            },
            "mp3_output": "/static/output.mp3"  # Provide the URL for the audio response
        }

        return response
 
# New Intent Handler for Playing a Song
class PlayVideoIntentHandler:
    def handle(self, video_name):
        speak_output = f"Playing the video {video_name}."
        pywhatkit.playonyt(video_name)
        return self.generate_alexa_response(speak_output)

    def generate_alexa_response(self, speak_output):
        # Generate speech using espeak and save it as 'output.mp3'
        os.system(f'espeak -ven "{speak_output}" -w static/output.mp3')

        # Create the response to send back to frontend
        response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "SSML",
                    "ssml": "<speak>" + speak_output + "</speak>"
                },
                "shouldEndSession": False
            },
            "mp3_output": "/static/output.mp3"  # Provide the URL for the audio response
        }

        return response


# Launch Request Handler
class LaunchRequestHandler:
    def handle(self):
        speak_output = "Welcome to home controls, how can I help you at the moment dude?"
        return self.generate_alexa_response(speak_output)

    def generate_alexa_response(self, speak_output):
        # Generate speech using espeak and save it as 'output.mp3'
        os.system(f'espeak -ven "{speak_output}" -w static/output.mp3')

        # Create the response to send back to frontend
        response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "SSML",
                    "ssml": "<speak>" + speak_output + "</speak>"
                },
                "shouldEndSession": False
            },
            "mp3_output": "/static/output.mp3"  # Provide the URL for the audio response
        }

        return response

# Hello World Intent Handler
class HelloWorldIntentHandler:
    def handle(self):
        speak_output = "Hello World!"
        return self.generate_alexa_response(speak_output)

    def generate_alexa_response(self, speak_output):
        # Generate speech using espeak and save it as 'output.mp3'
        os.system(f'espeak -ven "{speak_output}" -w static/output.mp3')

        # Create the response to send back to frontend
        response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "SSML",
                    "ssml": "<speak>" + speak_output + "</speak>"
                },
                "shouldEndSession": False
            },
            "mp3_output": "/static/output.mp3"  # Provide the URL for the audio response
        }

        return response

# Help Intent Handler
class HelpIntentHandler:
    def handle(self):
        speak_output = "You can say hello to me! How can I help?"
        return self.generate_alexa_response(speak_output)

    def generate_alexa_response(self, speak_output):
        # Generate speech using espeak and save it as 'output.mp3'
        os.system(f'espeak -ven "{speak_output}" -w static/output.mp3')

        # Create the response to send back to frontend
        response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "SSML",
                    "ssml": "<speak>" + speak_output + "</speak>"
                },
                "shouldEndSession": False
            },
            "mp3_output": "/static/output.mp3"  # Provide the URL for the audio response
        }

        return response

# Cancel and Stop Intent Handler
class CancelOrStopIntentHandler:
    def handle(self):
        speak_output = "Goodbye buddy and have a great day!"
        return self.generate_alexa_response(speak_output)

    def generate_alexa_response(self, speak_output):
        # Generate speech using espeak and save it as 'output.mp3'
        os.system(f'espeak -ven "{speak_output}" -w static/output.mp3')

        # Create the response to send back to frontend
        response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "SSML",
                    "ssml": "<speak>" + speak_output + "</speak>"
                },
                "shouldEndSession": False
            },
            "mp3_output": "/static/output.mp3"  # Provide the URL for the audio response
        }

        return response

# Fallback Intent Handler
class FallbackIntentHandler:
    def handle(self):
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"
        return self.generate_alexa_response(speech, reprompt)

    def generate_alexa_response(self, speak_output, reprompt_output):
        # Generate speech using espeak and save it as 'output.mp3'
        os.system(f'espeak -ven "{speak_output}" -w static/output.mp3')

        # Create the response to send back to frontend
        response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "SSML",
                    "ssml": "<speak>" + speak_output + "</speak>"
                },
                "reprompt": {
                    "outputSpeech": {
                        "type": "SSML",
                        "ssml": "<speak>" + reprompt_output + "</speak>"
                    }
                },
                "shouldEndSession": False
            },
            "mp3_output": "/static/output.mp3"  # Provide the URL for the audio response
        }

        return response

# Devices Control Intent Handler
class DevicesControlIntentHandler:
    def handle(self, device_name):
        speak_output = f"Your {device_name} is on. Enjoy the day and relax buddy."
        return self.generate_alexa_response(speak_output)

    def generate_alexa_response(self, speak_output):
        # Generate speech using espeak and save it as 'output.mp3'
        os.system(f'espeak -ven "{speak_output}" -w static/output.mp3')

        # Create the response to send back to frontend
        response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "SSML",
                    "ssml": "<speak>" + speak_output + "</speak>"
                },
                "shouldEndSession": False
            },
            "mp3_output": "/static/output.mp3"  # Provide the URL for the audio response
        }

        return response

# Devices Check Intent Handler
class DevicesCheckIntentHandler:
    def handle(self, device_name):
        speak_output = f"Your {device_name} is off. Cool buddy..."
        return self.generate_alexa_response(speak_output)

    def generate_alexa_response(self, speak_output):
        # Generate speech using espeak and save it as 'output.mp3'
        os.system(f'espeak -ven "{speak_output}" -w static/output.mp3')

        # Create the response to send back to frontend
        response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "SSML",
                    "ssml": "<speak>" + speak_output + "</speak>"
                },
                "shouldEndSession": False
            },
            "mp3_output": "/static/output.mp3"  # Provide the URL for the audio response
        }

        return response

# Catch-all error handler
@app.errorhandler(Exception)
def catch_all_exception_handler(error):
    speech_output = "Sorry, there was an error. Please try again later."
    response = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "SSML",
                "ssml": f"<speak>{speech_output}</speak>",
            },
            "shouldEndSession": False
        },
        "mp3_output": ""  # Provide an empty URL for the audio response since there's an error
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)