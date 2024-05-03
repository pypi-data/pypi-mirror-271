# --------------------------
# Utils folder
# Class definition
#
# Lang : lang
# --------------------------

""" imports: logging, config and language libs """
import logging
import logging.config
from biaspeech.utils.config import Config

""" objects:  """
conf = Config() # config

if conf.OS == "macos":
    import argostranslate.package
    import argostranslate.translate
    from py3langid.langid import LanguageIdentifier, MODEL_FILE 

class Lang:

    """ constructor """
    def __init__(self): 
        self.logger = logging.getLogger(__name__) # logger
    
    """ translate """
    def get_translate(self, text, source, dest):       
        result = text
        if source == dest or conf.OS != "macos":
            result = text
        else:
            result = argostranslate.translate.translate(text, source, dest)
        
        result = result.lower()
        
        return result
    
    """ get_lang """
    def get_lang(self, text):
        try:
            result = "fr"
            if conf.OS == "macos":
                language_identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
                language_identifier.set_languages(langs=['en','fr','de','es','nl'])
                result = language_identifier.classify(text)[0]
                
        except Exception as err:
            result = "fr"

        return result
                
