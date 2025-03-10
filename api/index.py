from flask import Flask, request, jsonify
from scipy.spatial import distance
import json
import os

app = Flask(__name__)

# Function to convert hex to RGB
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[i:i+2], 16) for i in (0, 2, 4)]

# Function to find multiple closest colors
def closest_colors(target_color, image_data, top_n=3):
    matches = []

    for image in image_data:
        for color_data in image['color_palette']:
            color_rgb = hex_to_rgb(color_data['hex'])
            dist = distance.euclidean(target_color, color_rgb)
            matches.append({
                "image_name": image['image_title'],
                "image_path": image['image_path'],
                "closest_color": color_data['hex'],
                "distance": dist
            })

    return sorted(matches, key=lambda x: x['distance'])[:top_n]

# Load image data
with open('image_database.image_palettes.json', encoding='utf-8') as f:
    image_data = json.load(f)

@app.route('/')
def home():
    return 'Welcome to the Color Matching API!'    

@app.route('/closest-colors', methods=['POST'])
def get_closest_colors():
    data = request.json
    target_color = data.get('target_color')
    top_n = data.get('top_n', 3)

    if not target_color or len(target_color) != 3:
        return jsonify({"error": "Invalid target_color. Provide a valid RGB array."}), 400

    results = closest_colors(target_color, image_data, top_n)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5002))
