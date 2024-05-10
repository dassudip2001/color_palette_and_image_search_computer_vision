import math

def euclidean_distance(color1, color2):
    """
    The function calculates the Euclidean distance between two colors represented as RGB values.
    
    :param color1: The `color1` parameter is a tuple containing the RGB values of a color. It should be
    in the format `(red, green, blue)`, where each value represents the intensity of the corresponding
    color channel
    :param color2: It seems like you have provided the definition of a function `euclidean_distance`
    that calculates the Euclidean distance between two colors represented as RGB tuples. However, you
    have not provided the definition of `color2`. If you can provide the RGB values for `color2`, I can
    help you calculate
    :return: The function `euclidean_distance` calculates the Euclidean distance between two colors
    represented as RGB tuples. It returns the Euclidean distance as a floating-point number.
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

def search_by_color(user_color, database):
    # This code snippet defines a function `search_by_color` that takes a user-selected color
    # (`user_color`) and a database of colors and image URLs. It iterates through each color in the
    # database, calculates the Euclidean distance between the user's color and the database color
    # using the `euclidean_distance` function, and finds the closest images based on color similarity.
    closest_images = []
    min_distance = float('inf')
    for color, image_url in database:
        distance = euclidean_distance(user_color, color)
        if distance < min_distance:
            min_distance = distance
            closest_images = [image_url]
        elif distance == min_distance:
            closest_images.append(image_url)
    return closest_images

# Example usage:
user_color = (242, 156, 48) # User's selected color
database = [((167, 186, 136), '../assets/1jpg.jpg'), ((122, 122, 80), '../assets/2jpg.jpg')]
closest_images = search_by_color(user_color, database)
print("Closest images:", closest_images)
