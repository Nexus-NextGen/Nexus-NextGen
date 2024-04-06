import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import io

FILLER_WORDS = ['um', 'uh', 'ah', 'umm', 'like', 'so', 'you know', 'actually', 'basically', 'seriously', 'literally']

# Initialize the recognizer
r = sr.Recognizer()

def remove_filler_parts(audio, timestamps):
    # Create a new audio segment without the filler words
    segments = []
    start = 0
    for start_time, end_time in timestamps:
        segment = audio[start:start_time]
        segments.append(segment)
        start = end_time
    segments.append(audio[start:])
    new_audio = AudioSegment.empty()
    for segment in segments:
        new_audio += segment
    return new_audio

def get_audio_from_mic():
    # Record Audio from Microphone
    with sr.Microphone() as source:
        print("Please speak:")
        audio_data = r.listen(source)
        print("Recording done!")
    return audio_data.get_wav_data()

def get_audio_from_file(file_path):
    # Load audio file
    with sr.AudioFile(file_path) as source:
        audio_data = r.record(source)
    return audio_data.get_wav_data()

def transcribe_audio(audio_data):
    # Convert audio data to AudioData type
    audio = sr.AudioData(audio_data, sample_rate=44100, sample_width=2)  # Adjust sample_rate and sample_width if needed
    # Recognize and transcribe the audio
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def identify_filler_timestamps(transcription, audio):
    # Fake timestamps. This step would require actual timestamps from transcription.
    # As of now, there is no direct way to get timestamps using the 'speech_recognition' library.
    # It requires either an enhanced model from a paid API or alternative approach like forced alignment.
    # We will display the transcribed text without filler words instead.
    print(f"Transcription without filler words: {' '.join([word for word in transcription.split() if word.lower() not in FILLER_WORDS])}")
    # Placeholder for timestamps of filler words (start, end)
    return [(0, 1000), (5000, 6000)]

def process_audio(audio_bytes):
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    transcription = transcribe_audio(audio_bytes)
    if not transcription:
        print("No transcription available.")
        return
    timestamps = identify_filler_timestamps(transcription, audio)
    clean_audio = remove_filler_parts(audio, timestamps)
    return clean_audio

def main():
    # For file input
    #file_path = "path_to_your_audio_file.wav"
    #audio_bytes = get_audio_from_file(file_path)
    
    # For microphone input, uncomment the below line and comment the above lines
    audio_bytes = get_audio_from_mic()

    clean_audio = process_audio(audio_bytes)

    if clean_audio:
        print("Playing cleaned audio...")
        play(clean_audio)
        # Optionally save the cleaned audio
        clean_audio.export("cleaned_output.wav", format="wav")

if __name__ == "__main__":
    main()