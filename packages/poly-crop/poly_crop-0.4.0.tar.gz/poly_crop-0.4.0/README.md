# Poly_Crop
poly_crop is a Python library for cropping polygons in images.

## Installation
You can install poly_crop via pip:

```python
pip install poly_crop
```
## Usage
### Crop Function
The `crop` function is used to crop a polygonal region from an image.

```python
from poly_crop import crop as pc

# Example usage
image_path = "path/to/your/image.jpg"
image = cv2.imread(image_path)
vertices = [(100, 100), (175, 50), (300, 100), (175, 150), (170, 100)]

cropped_image = pc.crop(image, vertices, resize=False)
```
### Preview Function
The `preview` function is used to draw a preview of a polygonal region on an image.

```python
from poly_crop import preview as pc

# Example usage
image_path = "path/to/your/image.jpg"
image = cv2.imread(image_path)
vertices = [(100, 100), (175, 50), (300, 100), (175, 150), (170, 100)]

preview_image = pc.preview(image, vertices, colour=(255, 0, 0), width=2)
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.