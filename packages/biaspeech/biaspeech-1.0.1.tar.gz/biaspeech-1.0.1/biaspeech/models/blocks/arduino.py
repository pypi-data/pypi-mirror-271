# --------------------------
# Models folder
# Class definition
#
# Arduino : define the Arduino (Block) model
# --------------------------

""" imports: logging, config, etc """
import logging
import logging.config
from biaspeech.utils.config import Config
from datetime import datetime
import pyduinocli
import os
import serial
import time

""" objects:  """
conf = Config()  # config
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=conf.LOGLEVEL)

""" MVC """
from biaspeech.models.blocks import block
from biaspeech.utils.text2Speech import Text2Speech

class Arduino(block.Block):

    """ constructor """
    def __init__(self, prompt, ai):
        block.Block.__init__(self, prompt, ai)

    """ get_output """
    def get_output(self):
        return(conf.OUTPUT_ARDUINO)

    """ get_file """
    def get_file(self):
        self.logger.info("get_file")  # inform the user

        search = self.prompt.mia.input_en.replace("robot ", "")  # cleanup the prompt
        if not ( search in conf.ARDUINO_INPUT_C ): # not a keyword like walk, etc
            input_en = conf.ARDUINO_INPUT_A + search + conf.ARDUINO_INPUT_B  # build the inout for OpenAI
            code_raw = self.ai.get_output_nolimit(input_en)  # ask OpenAI an arduino code

            code = code_raw

            now = datetime.now()  # current date and time
            date_time = now.strftime("%Y%m%d_%H%M%S")  # put to string nice format
            folder = conf.ARDUINO_FOLDER + date_time
            fname = folder + "/" + date_time + ".ino"  # build the folder / file name

            os.mkdir(folder)  # will save the file
            file = open(fname, 'a')  # open up the file
            file.write(code)  # write
            file.close()  # close

            return(folder)

    """ run """
    def run(self, folder):
        try:
            search = self.prompt.mia.input_en.replace("robot ", "")  # cleanup the prompt
            if ( search in conf.ARDUINO_INPUT_C ): #  keyword like walk, etc => serial communication with arduino

                if os.environ['ARDUINO'] != "default":  # load the default code
                    self.load_default()

                arduino = serial.Serial(port=conf.ARDUINO_PORT,  baudrate=115200, timeout=.1)
                time.sleep(1.5)
                arduino.write(bytes(search, 'utf-8'))

            else: #  not a known keyword like walk, etc => ask chatgpt to generate a script
                arduino = pyduinocli.Arduino(conf.ARDUINO_PROGRAM)  # program
                arduino.compile(fqbn=conf.ARDUINO_BOARD, sketch=folder)  # compile
                arduino.upload(fqbn=conf.ARDUINO_BOARD, sketch=folder, port=conf.ARDUINO_PORT)  # upload
                self.logger.info("chatgpt arduino code uploaded")  # inform the user

                time.sleep(10)
                self.load_default()
                os.environ['ARDUINO'] = "default" # flag that an upload was done, the default will need to be reloaded

        except Exception as err:
            self.text2Speech = Text2Speech(conf.LANGUAGE, conf.RATE, conf.VOLUME, conf.VOICE_MACOS, conf.VOICE_RASPBERRY)  # object for text2speech
            self.text2Speech.do_speech(conf.PROBLEM)  # inform the user
            self.logger.warning(f"conf.ERR_D {err=}, {type(err)=}")  # inform the user

    """ load default """
    def load_default(self):
        folder = conf.ARDUINO_FOLDER + "default"
        arduino = pyduinocli.Arduino(conf.ARDUINO_PROGRAM)  # program
        arduino.compile(fqbn=conf.ARDUINO_BOARD, sketch=folder)  # compile
        arduino.upload(fqbn=conf.ARDUINO_BOARD, sketch=folder, port=conf.ARDUINO_PORT)  # upload
        os.environ['ARDUINO'] = "default" # flag that an upload was done
        self.logger.info("default arduino code uploaded")  # inform the user
 
