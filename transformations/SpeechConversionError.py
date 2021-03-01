from transformations.SentenceTransformation import SentenceTransformation
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

class SpeechConversionError(SentenceTransformation):

    def __init__(self):
        self.speech_recognizer = sr.Recognizer()

    def generate(self, sentence: str):
        words = sentence.split(" ")
        SPLIT_SIZE = 5
        groups_of_words = [" ".join(words[i:i + SPLIT_SIZE]) for i in range(0, len(words), SPLIT_SIZE)]
        return " ".join([self.tts_stt(snippet) for snippet in groups_of_words])

    def tts_stt(self, sentence: str):
        speech = gTTS(text=sentence, slow=True)
        filename = 'temp.mp3'
        speech.save(filename)  # this actually saves it as an mp3
        # convert mp3 to wav
        audio_file = convert_to_wav(filename)
        sentence = get_large_audio_transcription(self.speech_recognizer, audio_file)
        return sentence


def convert_to_wav(src_file: str):
    # convert wav to mp3
    sound = AudioSegment.from_mp3(src_file)
    dst = src_file.replace(".mp3", ".wav")
    sound.export(dst, format="wav")
    return dst

""" a function that splits the audio file into chunks and applies speech recognition.
    Source: https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
"""
def get_large_audio_transcription(recognizer, path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = recognizer.record(source)
            # try converting it to text
            try:
                text = recognizer.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            else:
                #text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text

if __name__ == '__main__':
    sc = SpeechConversionError()
    text = sc.generate("This speech conversion error needs improvement!")
    print(text)
