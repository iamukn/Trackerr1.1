from PIL import Image
from io import BytesIO

def resize_image(image_file,content_type, max_size=(300, 300)):
    img = Image.open(image_file)
    #img = img.convert("RGB")  # Optional: for JPEG consistency

    img.thumbnail(max_size)

    buffer = BytesIO()
    if 'jpeg' in content_type.lower() or 'jpg' in content_type.lower():
        img.save(buffer, format='JPEG')  # or 'PNG'
    elif 'png' in content_type.lower():
        img.save(buffer, format='PNG')
    else:
        return False
    buffer.seek(0)
    return buffer
