import numpy as np
import cv2
from PIL import Image, ImageDraw

def crop(image, vertices, resize=True):
    if isinstance(image, np.ndarray):
        # If image is a NumPy array (loaded with cv2), continue with cv2 processing
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif len(image.shape) == 3 and image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

        # Create a mask for the polygon
        mask = np.zeros_like(image)
        pts = np.array(vertices, np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.fillPoly(mask,[pts],(255,255,255))

        # Mask the image
        masked_image = cv2.bitwise_and(image, mask)

        # Find the bounding box of the polygon
        x, y, w, h = cv2.boundingRect(pts)

        if resize:
            # Crop the image and resize it
            cropped_image = masked_image[y:y+h, x:x+w]
        else:
            # Create a masked image without resizing
            cropped_image = masked_image.copy()
            cropped_image[mask == 0] = 0
        
        return cropped_image
    elif isinstance(image, Image.Image):
        # If image is a PIL image, convert to NumPy array and call crop function recursively
        image_array = np.array(image)
        cropped_image_array = crop(image_array, vertices, resize)
        return Image.fromarray(cropped_image_array)
    else:
        raise ValueError("Invalid image type. Supported types are numpy.ndarray (cv2) and PIL.Image.Image.")

def preview(image, vertices, colour=(255, 255, 0), width=2):
    if isinstance(image, np.ndarray):
        # If image is a NumPy array (loaded with cv2), draw bounding box using cv2
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif len(image.shape) == 3 and image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        
        pts = np.array(vertices, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (colour[2], colour[1], colour[0]), width)
        return image
    elif isinstance(image, Image.Image):
        # If image is a PIL image, draw bounding box using PIL
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        draw = ImageDraw.Draw(image)
        draw.polygon(vertices, outline=colour, width=width)
        return image
    else:
        raise ValueError("Invalid image type. Supported types are numpy.ndarray (cv2) and PIL.Image.Image.")