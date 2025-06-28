from flask import Flask, request, send_file, jsonify
import numpy as np
from pydub import AudioSegment
import io

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_raw_to_wav():
    try:
        # Step 1: Receive raw data (audio data sent by ESP32/INMP441) as bytes
        raw_data = request.data
        
        # Step 2: Convert the raw data into a numpy array
        sample_rate = 16000  # Assuming 16 kHz sample rate
        channels = 1  # Mono channel
        dtype = np.int16  # Assuming 16-bit PCM raw audio format
        
        # Convert raw data to numpy array
        audio_data = np.frombuffer(raw_data, dtype=dtype)

        # Step 3: Convert numpy array into an AudioSegment
        audio_segment = AudioSegment(
            audio_data.tobytes(),  # Convert numpy array to bytes
            frame_rate=sample_rate,  # Set sample rate
            sample_width=audio_data.itemsize,  # 2 bytes for int16
            channels=channels  # Mono
        )

        # Step 4: Export audio as WAV file in memory
        wav_output = io.BytesIO()
        audio_segment.export(wav_output, format="wav")
        wav_output.seek(0)

        # Step 5: Send the WAV file as a response
        return send_file(wav_output, mimetype="audio/wav", as_attachment=True, download_name="converted_audio.wav")
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
