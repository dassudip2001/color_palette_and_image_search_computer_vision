from scipy.spatial import distance

# Function to convert hex to RGB
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[i:i+2], 16) for i in (0, 2, 4)]

# Function to find multiple closest colors
def closest_colors(target_color, image_data, top_n=3):
    matches = []

    for image in image_data:
        # print(image)
        for color_data in image['color_palette']:
            color_rgb = hex_to_rgb(color_data['hex'])
            dist = distance.euclidean(target_color, color_rgb)
            matches.append({
                "image_name": image['image_title'],
                "image_path": image['image_path'],
                "closest_color": color_data['hex'],
                "distance": dist
            })

    # Sort matches by distance and return top N
    return sorted(matches, key=lambda x: x['distance'])[:top_n]

# Example usage
target_color = [24, 35, 15]  # Red
import json

with open('/content/image_database.image_palettes.json') as f:
    image_data = json.load(f)

top_n_results = closest_colors(target_color, image_data, top_n=5)
for idx, result in enumerate(top_n_results, 1):
    print(f"{idx}. Image: {result['image_name']} |Path: {result['image_path']} | Color: {result['closest_color']} | Distance: {result['distance']:.2f}")
