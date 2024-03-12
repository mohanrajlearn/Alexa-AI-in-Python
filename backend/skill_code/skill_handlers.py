import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name == "LaunchRequest"

    def handle(self, handler_input):
        speak_output = "Welcome to home controls, how can I help you at the moment dude?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class HelloWorldIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name == "HelloWorldIntent"

    def handle(self, handler_input):
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name == "AMAZON.HelpIntent"

    def handle(self, handler_input):
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (
            handler_input.request_envelope.request.intent.name == "AMAZON.CancelIntent" or
            handler_input.request_envelope.request.intent.name == "AMAZON.StopIntent"
        )

    def handle(self, handler_input):
        speak_output = "Goodbye buddy and have a great day!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name == "AMAZON.FallbackIntent"

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name == "SessionEndedRequest"

    def handle(self, handler_input):
        return handler_input.response_builder.response

class DevicesControlIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name == "DevicesControlIntent"

    def handle(self, handler_input):
        request = handler_input.request_envelope.request
        slots = request.intent.slots

        # Check if the "device" slot exists and has a valid value
        if slots and "device" in slots and slots["device"].value:
            device = slots["device"].value
        else:
            # If the "device" slot is missing or has no value, you can provide a default device name
            device = "device"

        speak_output = f"Your {device} is on. Enjoy the day and relax buddy."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class DevicesCheckIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name == "DevicesCheckIntent"

    def handle(self, handler_input):
        request = handler_input.request_envelope.request
        slots = request.intent.slots

        # Check if the "device" slot exists and has a valid value
        if slots and "device" in slots and slots["device"].value:
            device = slots["device"].value
        else:
            # If the "device" slot is missing or has no value, you can provide a default device name
            device = "device"

        speak_output = f"Your {device} is off. Cool buddy..."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
