from flask import Flask, request, jsonify
from flask_cors import CORS
import instaloader
import re

app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

def get_reel_url(instagram_url):
    loader = instaloader.Instaloader()
    shortcode = re.findall(r"instagram\.com/reel/([^/?]+)", instagram_url)

    if not shortcode:
        return None

    shortcode = shortcode[0]

    try:
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        return post.video_url
    except Exception:
        return None

@app.route('/download', methods=['POST'])
def download_reel():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    video_url = get_reel_url(url)

    if video_url:
        return jsonify({"video_url": video_url})
    else:
        return jsonify({"error": "Invalid Instagram link or private account"}), 400

if __name__ == '__main__':
    app.run(debug=True)
