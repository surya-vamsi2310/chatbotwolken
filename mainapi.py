import warnings

warnings.filterwarnings("ignore")
from flask_api import FlaskAPI
from flask_cors import CORS
from flask import jsonify, render_template
from flask import request
from rasa_core.agent import Agent
from rasa_core.interpreter import NaturalLanguageInterpreter
import re
from Apps.apis import create_request, get_all_request, get_case_details

interpreter = NaturalLanguageInterpreter.create("./models/current/nlu")
agent = Agent.load('./models/current/dialogue', interpreter=interpreter)

app = FlaskAPI(__name__, template_folder='templates')
CORS(app)


@app.route("/", methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def start():
    return render_template("index.html")


@app.route('/get_response/<text>', methods=['GET', 'POST'])
def process(text):
    responses = agent.handle_text(text)
    print(responses)

    res = interpreter.parse(text)
    print(res)

    if text.lower() in ['ok', 'okay']:
        responses[0]['text'] = "Okay."
    elif res['intent']['name'] == "greet":
        responses.append({"recipient_id": 'default', 'text': 'How would you like to proceed?'})
    elif "@" in text:
        responses[0]['text'] = "Please wait for a sec while i fetch you the status..."
        found = get_case_details(text.strip()) # this is for gettng details
        if found['status'] == "Success" and found['message'] == "Success":
            responses.append({"recipient_id": 'default', 'text': "Here's your ticket details:<br><pre><code>"+str(found['data'])+"</code><pre>"})
        else:
            responses.append({"recipient_id": 'default', 'text': "Didn't found your ticket, could you please create it?"})

    return jsonify({"status": "Success", "data": responses})


# this is for creating requst
@app.route('/save_details', methods=['GET', 'POST'])
def save_details():
    print(request.json)
    create_request(request.json) # no, here we will get json filled in form, i am passing that form data to create_request method , so in that method, fill the main json with this form data 
    return jsonify({"status": "Success"})




if __name__ == '__main__':
    app.run(port=7896, debug=False, host="localhost", threaded=False)
