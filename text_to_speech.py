import pyttsx3
from pdfhandler import pdf_to_text

def text_to_speech(text, output = "test.mp3", rate = 200, volume = 1.0, gender = 1, saving = False):
    engine = pyttsx3.init() # object creation

    """ RATE"""
    engine.setProperty('rate', rate)     # setting up new voice rate

    """VOLUME"""
    engine.setProperty('volume', volume)    # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[gender].id)   #changing index, changes voices. 1 for female

    if not saving:
        engine.say('My current speaking rate is ' + str(rate))
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    else:
        """Saving Voice to a file"""
        # On linux make sure that 'espeak' and 'ffmpeg' are installed
        engine.save_to_file(text, output)
        engine.runAndWait()

if __name__ == '__main__':
    text = pdf_to_text("C:/Users/calli/Testing/LA1040_VLE.pdf", 12, 13, 2)
    text_to_speech(text, output="C:/Users/calli/Testing/testing.mp3", saving=True)