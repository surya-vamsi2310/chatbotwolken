import warnings
warnings.filterwarnings("ignore")
from rasa_core.agent import Agent
from rasa_core.interpreter import NaturalLanguageInterpreter
interpreter = NaturalLanguageInterpreter.create("/home/shireesh/Voice_all_audio_files/public_git/iplbot/complete_version/models/current/nlu")
agent = Agent.load('/home/shireesh/Voice_all_audio_files/public_git/iplbot/complete_version/models/current/dialogue',
                   interpreter=interpreter)
print("Your bot is ready to talk! Type your messages here or send 'stop'")
while True:
    a = "hi"
    if a == 'stop':
        break
    responses = agent.handle_text(a)
    for response in responses:
        print(response["text"])
