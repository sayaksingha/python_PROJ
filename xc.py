from flask import Flask, request, jsonify
from pytube import YouTube
import os
import re  # Add this import statement for the 're' module
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for your app

# Function to sanitize a string for use as a filename
def sanitize_filename(filename):
    # Remove any characters that are not alphanumeric, underscores, or spaces
    return re.sub(r'[^\w\s]', '', filename)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        video_url = data.get('url')

        if not video_url:
            return jsonify({'error': 'URL parameter is required'}), 400

        yt = YouTube(video_url)
        video_title = yt.title
        sanitized_video_title = sanitize_filename(video_title)

        download_path = os.path.join('C:\\Users\\Sayak Singha\\Desktop', f'{sanitized_video_title}.mp4')

        video = yt.streams.get_highest_resolution()
        video.download(output_path='C:\\Users\\Sayak Singha\\Desktop', filename=sanitized_video_title)
        
        return jsonify({'message': f'Downloaded video: {video_title}', 'file_path': download_path}), 200
    except Exception as e:
        error_message = str(e)
        print(error_message)  # Log the error to the console for debugging
        return jsonify({'error': error_message}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Hello, world'})

if __name__ == '__main__':
    app.run(debug=True)
