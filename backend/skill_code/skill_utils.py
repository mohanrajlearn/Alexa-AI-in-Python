# skill_code/skill_utils.py

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_speak_output(device, status):
    """Helper function to generate the speak output for devices."""
    return f"Your {device} is {status}. Enjoy the day and relax buddy."


def get_fallback_output():
    """Helper function to generate fallback response."""
    speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
    reprompt = "I didn't catch that. What can I help you with?"
    return speech, reprompt


def get_error_output():
    """Helper function to generate error response."""
    return "Sorry, I had trouble doing what you asked. Please try again."
