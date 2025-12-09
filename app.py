from flask import Flask, request, jsonify
import yt_dlp
from urllib.parse import urlparse, parse_qs
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_info():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,  # Just get info, no download
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            thumbnail = info.get('thumbnail', '')
            
            formats = []
            for f in info.get('formats', []):
                if f.get('url') and f.get('vcodec') != 'none' or f.get('acodec') != 'none':  # Video or audio
                    formats.append({
                        'quality': f.get('quality', f.get('height', 'Audio')),
                        'url': f['url'],
                        'ext': f.get('ext', 'mp4'),
                        'filesize': f.get('filesize') if f.get('filesize') else None
                    })
            
            return jsonify({
                'title': title,
                'thumbnail': thumbnail,
                'formats': formats[:10]  # Limit to 10 for UI
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
