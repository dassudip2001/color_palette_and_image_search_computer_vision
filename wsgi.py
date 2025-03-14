from flask import Flask, request, jsonify, render_template
from scipy.spatial import distance
import json

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
                "image_name": image['accession_number'],
                "image_path": image['primary_image'],
                "closest_color": color_data['hex'],
                "distance": dist
            })
    return sorted(matches, key=lambda x: x['distance'])[:top_n]

# Load image data
with open('map_database.image_palettes.json', encoding='utf-8') as f:
    image_data = json.load(f)

@app.route('/')
def home():
    return "Flask App Running on Vercel"

@app.route('/closest-colors', methods=['POST'])
def get_closest_colors():
    target_color = request.json.get('target_color')
    top_n = int(request.json.get('top_n', 3))

    if not target_color:
        return jsonify({"error": "Please provide a valid hex color code."}), 400

    target_rgb = hex_to_rgb(target_color)
    results = closest_colors(target_rgb, image_data, top_n)
    
    return jsonify(results)

# Vercel needs a callable named `app`
def handler(event, context):
    return app(event, context)
