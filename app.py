#Importing Dependencies
from flask import Flask
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import LanguageTranslatorV3
from ibm_watson import TextToSpeechV1
import sys

app = Flask(__name__)
var_input = sys.argv[1]

@app.route('/')
def first():
    #Importing Dependencies
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_watson import LanguageTranslatorV3
    #credentials for Language Translation 
    apiKey = "85F10cR61mJSFha9bnrEvGJ2jopIBKLKJnH_H6kygiKu"
    url = "https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/033994a0-07cc-4051-99db-1df755ff86fb"

    #setting up the services
    authenticator = IAMAuthenticator(apiKey)
    lt = LanguageTranslatorV3(version='2018-05-01', authenticator=authenticator)
    lt.set_service_url(url)

    #translating from English to Hindi 
    translation = lt.translate(text= var_input, model_id='en-hi').get_result()

    print (translation) 
    output1= translation['translations'][0]['translation']

    ##TTS
    #Credentials for Text to Speech
    ttsapikey  = "WEUGgt1b6VvQvKEnxpfSWDBu_8cjOTdl_g0RZ-xtSJSv"
    ttsurl  = "https://api.eu-de.text-to-speech.watson.cloud.ibm.com/instances/3ca40d3a-9ab8-49fe-86c4-607b175ffa15"

    # Authenticate
    ttsauthenticator = IAMAuthenticator(ttsapikey)
    tts = TextToSpeechV1(authenticator=ttsauthenticator)
    tts.set_service_url(ttsurl)

    #English to German [as audio translation to Hindi is "unavailable" within IBM we are trying with another language ]
    translation = lt.translate(text= var_input, model_id='en-de').get_result()

    text = translation['translations'][0]['translation']

    with open('./recommendation.mp3', 'wb') as audio_file:
        res = tts.synthesize(text, accept='audio/mp3', voice='de-DE_BirgitV3Voice').get_result()
        #res = tts.synthesize(text, accept='audio/mp3').get_result()
        audio_file.write(res.content)
     

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)