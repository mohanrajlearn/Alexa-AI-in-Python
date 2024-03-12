import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Check if the environment variable 'CODE_ENV' is set to 'frontend'
# If it's set to 'frontend', import frontend code
# If not, import backend code
if os.getenv('CODE_ENV', 'backend') == 'frontend':
    from skill_code.skill_handlers import (
        LaunchRequestHandler,
        HelloWorldIntentHandler,
        HelpIntentHandler,
        CancelOrStopIntentHandler,
        FallbackIntentHandler,
        SessionEndedRequestHandler,
        DevicesControlIntentHandler,
        DevicesCheckIntentHandler,
        CatchAllExceptionHandler,
    )
else:
    from skill_code.skill_handlers import (
        LaunchRequestHandler,
        HelloWorldIntentHandler,
        HelpIntentHandler,
        CancelOrStopIntentHandler,
        FallbackIntentHandler,
        SessionEndedRequestHandler,
        DevicesControlIntentHandler,
        DevicesCheckIntentHandler,
        CatchAllExceptionHandler,
    )

from ask_sdk_core.skill_builder import SkillBuilder

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(DevicesControlIntentHandler())
sb.add_request_handler(DevicesCheckIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

# If the CODE_ENV is set to 'frontend', execute the following block
if os.getenv('CODE_ENV', 'backend') == 'frontend':
    # Additional frontend-specific code can be added here
    pass

lambda_handler = sb.lambda_handler()
