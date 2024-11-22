from flask import request, jsonify
from config import app, db
from models import Contact
from googleapiclient.discovery import build
import os

API_KEY = 'AIzaSyC039lcbOWyDRjqpnsXehbqEWtinHLWdiY'


def download_youtube_audio_yt_dlp(url, save_path="."):
    try:
        # Construct yt-dlp command
        command = f'yt-dlp -x --audio-format mp3 -o "{save_path}/%(title)s.%(ext)s" {url}'
        
        # Run the command
        os.system(command)
    except Exception as e:
        print(f"Error occurred: {e}")

        
def search_youtube(video_name, max_results=5):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Search for the video
    request = youtube.search().list(
        part='snippet',
        q=video_name,
        type='video',  # Only search for videos
        maxResults=max_results
    )
    response = request.execute()

    # Extract video details
    videos = []
    for item in response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append({'title': title, 'url': url})
    
    return videos[0]['url']  # Return the URL of the first search result


@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = [contact.to_json() for contact in contacts]  # Properly call the to_json method
    return jsonify({"contacts": json_contacts})


@app.route("/create_video", methods=['POST'])  # Changed URL to "/create_video"
def create_contact():
    name = request.json.get("name")
    if not name:
        return jsonify({"message": "You must include name of the video"}), 400
    
    # Get YouTube video URL using the search function
    video_url = search_youtube(name)
    
    # Create a new contact without manually setting the id
    new_contact = Contact(name=name, url=video_url)  # Let the db generate the id
    
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "URL created", "contact": new_contact.to_json()}), 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist already
    
    app.run(debug=True)
