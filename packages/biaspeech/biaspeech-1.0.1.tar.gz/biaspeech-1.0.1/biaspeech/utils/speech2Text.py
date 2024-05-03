# --------------------------
# Models folder
# Class definition
#
# Speech2Text : define the speech to text model
# --------------------------

""" imports: logging and config """
import logging
import logging.config
from biaspeech.utils.config import Config
import os
import sounddevice

""" imports: speech_recognition """
import speech_recognition as sr 

""" objects:  """
conf = Config() # config
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=conf.LOGLEVEL)

class Speech2Text:
    
    """ constructor """
    def __init__(self, language): 

        """ util objects """
        self.conf = Config() # config
        self.logger = logging.getLogger(__name__) # logger

        """ attributes """
        self.language = language # language
        self.input = "" # input text
        
    """ get_input """        
    def get_input(self):
        return self.input
                                  
    """ do_listen """ 
    def do_listen(self):
        recognizer = sr.Recognizer() # initialize the recognizer
        r = sr.Recognizer()

        try:
            if (conf.OS == "macos"): # macos                                                    
                with sr.Microphone() as source: # microphone                                    
                    recorded_audio = recognizer.listen(source) # listen
                    #recognizer.adjust_for_ambient_noise(source, duration=conf.ADJUST)
                    #recorded_audio = recognizer.listen(source,timeout=0,phrase_time_limit=conf.TIMEOUT)
                    text = recognizer.recognize_google(recorded_audio, language=self.language) # w language

            else: # raspberry
                mic = sr.Microphone(device_index=1)
                with mic as source: # set the deviceIndex
                    recognizer.adjust_for_ambient_noise(source, duration=conf.ADJUST) # w adjust duration
                    recorded_audio = recognizer.listen(source) # listen
                    text = recognizer.recognize_google(recorded_audio, language=self.language) # w language

            self.input = format(text) # format

        except sr.UnknownValueError:
            self.logger.warning(conf.ERR_A) # inform the user
        except sr.RequestError:
            self.logger.warning(conf.ERR_B) # inform the user
        except Exception as ex:
            self.logger.warning(conf.ERR_C) # inform the user

