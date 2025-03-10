!pip install pymongo

import cv2
import numpy as np
from sklearn.cluster import KMeans
from pymongo import MongoClient
import os

def connect_to_mongodb():
    client = MongoClient("mongodb+srv://ranjancitulb:LSaBeKHZ0OqvsT4R@cluster0.rpuy0.mongodb.net/")  # Change URL as needed
    db = client["image_database"]  # Database name
    return db["image_palettes"]  # Collection name

def color_palette(image_path, k=5):
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not read image at {image_path}")
            return None

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_reshaped = img.reshape((-1, 3))

        kmeans = KMeans(n_clusters=k, n_init=10, max_iter=200)
        kmeans.fit(img_reshaped)
        colors = kmeans.cluster_centers_

        color_palette = [
            {"hex": f"#{int(c[0]):02x}{int(c[1]):02x}{int(c[2]):02x}"}
            for c in colors
        ]

        return color_palette

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def process_images_and_store(directory_path):
    collection = connect_to_mongodb()
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg','.webp')):
            image_path = os.path.join(directory_path, filename)
            palette = color_palette(image_path)
            if palette:
                data = {"image_name": filename, "color_palette": palette}
                collection.insert_one(data)
                print(f"Inserted: {filename}")

# Example usage
directory_path = "/content/drive/MyDrive/Public-image-for-colorsearch"  # Change to your desired path
process_images_and_store(directory_path)






-----------------------------------
import cv2
import numpy as np
from sklearn.cluster import KMeans
from pymongo import MongoClient
import requests
import os
import json
from io import BytesIO

def connect_to_mongodb():
    client = MongoClient("mongodb+srv://ranjancitulb:LSaBeKHZ0OqvsT4R@cluster0.rpuy0.mongodb.net/")
    db = client["image_database"]
    return db["image_palettes"]

def color_palette_from_url(image_url, k=5):
    try:
        # Download image from URL
        response = requests.get(image_url)
        if response.status_code != 200:
            print(f"Error: Could not download image from {image_url}")
            return None
            
        # Convert to OpenCV format
        img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        if img is None:
            print(f"Error: Could not process image from {image_url}")
            return None
            
        # Convert from BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Reshape for KMeans
        img_reshaped = img.reshape((-1, 3))
        
        # Extract dominant colors
        kmeans = KMeans(n_clusters=k, n_init=10, max_iter=200)
        kmeans.fit(img_reshaped)
        colors = kmeans.cluster_centers_
        
        # Format color palette
        color_palette = [
            {"hex": f"#{int(c[0]):02x}{int(c[1]):02x}{int(c[2]):02x}"}
            for c in colors
        ]
        
        return color_palette
    except Exception as e:
        print(f"An error occurred with {image_url}: {e}")
        return None

def process_image_data_from_file(json_file_path):
    # Read JSON data from file
    try:
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)
        
        # Connect to MongoDB collection
        collection = connect_to_mongodb()
        
        for item in json_data:
            image_id = item.get("id")
            image_title = item.get("title")
            image_path = item.get("imagePath")
            
            # Skip if missing essential data
            if not image_path:
                print(f"Skipping item {image_id}: Missing image path")
                continue
                
            # Extract color palette
            palette = color_palette_from_url(image_path)
            
            if palette:
                # Prepare data for MongoDB
                data = {
                    "image_id": image_id,
                    "image_title": image_title,
                    "image_path": image_path,
                    "color_palette": palette
                }
                
                # Insert or update in MongoDB
                collection.update_one(
                    {"image_id": image_id},
                    {"$set": data},
                    upsert=True
                )
                
                print(f"Processed: {image_title} (ID: {image_id})")
            else:
                print(f"Failed to process: {image_title} (ID: {image_id})")
                
        print("Processing complete.")
        
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file {json_file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Specify the path to your JSON file
json_file_path = "/content/tranning.json"  # Change this to your actual JSON file path

# Process the JSON file
process_image_data_from_file(json_file_path)
