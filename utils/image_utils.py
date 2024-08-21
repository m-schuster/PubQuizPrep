import io
from PIL import Image

def is_valid_image_format(img_data):
    valid_image_signatures = [
        b'\xff\xd8\xff',  # JPEG
        b'\x89PNG\r\n\x1a\n',  # PNG
        b'GIF87a',  # GIF
        b'GIF89a',  # GIF
        b'BM'  # BMP
    ]
    for s in valid_image_signatures:
        if img_data.startswith(s):
            return True
    return False

def save_image(img_data, filename):
    img_byte_stream = io.BytesIO(img_data)
    img = Image.open(img_byte_stream).convert('RGB')
    img.save(filename, "JPEG")