from flask import Flask, request, url_for
from response import generate_response
from twilio.twiml.voice_response import VoiceResponse, Gather, Say
from twilio import twiml

app = Flask(__name__)

@app.route('/welcome', methods =['GET', 'POST'])
def welcome():
    resp = VoiceResponse()
    with resp.gather(input='speech', action=url_for('response')) as g:
        g.say('Hello, this is your AI assistant. How can I help you today?')
    return str(resp)

@app.route('/response', methods = ['GET', 'POST'])
def response():
    resp = VoiceResponse()
    user_text = request.values.get('SpeechResult')
    if not user_text:
        return twiml(resp)
    
    elif 'goodbye' in user_text or 'Goodbye' in user_text: 
        with resp.gather(action=url_for('hangUp')) as g:
            g.say('Okay, bye! Have a great day!')
        return str(resp)
    # Generate AI response
    ai_response = generate_response(user_text)
    with resp.gather(input='speech', action=url_for('response')) as g:
        g.say(ai_response)
    return str(resp)

@app.route('/hangUp', methods=['GET', 'POST'])
def hangUp():
    resp = VoiceResponse()
    resp.hangup()

if __name__ =="__main__":
    app.run()