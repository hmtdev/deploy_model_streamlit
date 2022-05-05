import streamlit as st
import random
import streamlit as st
from pydub import AudioSegment
import numpy as np
import os
import pyaudio
import wave
from pydub import AudioSegment
from pydub.silence import split_on_silence
import keyboard
def handle_uploaded_audio_file(uploaded_file):
    a = AudioSegment.from_wav(uploaded_file)

    st.write(a.sample_width)

    samples = a.get_array_of_samples()
    fp_arr = np.array(samples).T.astype(np.float32)
    fp_arr /= np.iinfo(samples.typecode).max
    st.write(fp_arr.shape)

    return fp_arr, 22050



mark_down = """
## This is my project at 2a.m :)
"""
st.write(mark_down)
st.write("*Hello , My name is Toan *")
gen_otp_btn = st.button("Sent OTP")
if gen_otp_btn:
    st.write("Otp:",random.randint(1000,4999))

file_uploader = st.file_uploader("Upload File",type='.wav')
d = st.audio(file_uploader)

if file_uploader is not None:
   st.write(file_uploader)
   y, sr = handle_uploaded_audio_file(file_uploader)

def handle_uploaded_audio_file(uploaded_file):
    a = AudioSegment.from_wav(uploaded_file)
    return a
if st.button("Record Voice"):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    RECORD_SECONDS = 6
    WAVE_OUTPUT_FILENAME = "toan.wav"
    device_index = 1
    audio = pyaudio.PyAudio()

    # numdevices = info.get('deviceCount')
    # for i in range(0, numdevices):
    #         if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
    #             print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))

    # print("-------------------------------------------------------------")

    # index = int(input())
    # print("recording via index "+str(index))

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,input_device_index = device_index,
                    frames_per_buffer=CHUNK)
    st.write("recording started")
    Recordframes = []
    st.write("## Pressed q on keyboard to end record")
    while(True):
        data = stream.read(CHUNK)
        Recordframes.append(data)
        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            st.write('recording done')
            break
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()

    def match_target_amplitude(aChunk, target_dBFS):
            ''' Normalize given audio chunk '''
            change_in_dBFS = target_dBFS - aChunk.dBFS
            return aChunk.apply_gain(change_in_dBFS)

    song = AudioSegment.from_file(file = "toan.wav", 
                                  format = "wav")
    chunks = split_on_silence(
            song,
            min_silence_len = 500,
            silence_thresh = song.dBFS - 16,
            keep_silence = 250,
        )
    for i, chunk in enumerate(chunks):

        normalized_chunk = match_target_amplitude(chunk, -20.0)

        # Export the audio chunk with new bitrate.
        st.write("Exporting toan_{0}.wav.".format(i))
        normalized_chunk.export(
            "./output/toan_{0}.wav".format(i),
            bitrate = "192k",
            format = "wav"
        )
files = os.listdir("./output")
st.write(files)
for i in files:
    st.audio("./output/" + i)