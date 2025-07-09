from PIL import Image
import boto3
from io import BytesIO
from shared.aws_config.s3 import s3

def resize_and_upload(file_obj,key, bucket='trackerr-dp'):
    # 1. Open and resize the image
    content_type = key.split('/')[-1]
    content_type = f"image/{content_type}"
    if isinstance(file_obj, bytes):
        file_obj = BytesIO(file_obj)

    image = Image.open(file_obj)
    image = image.convert('RGB')  # in case it's RGBA or P
    image = image.resize((300, 300))

    # 2. Save the resized image to an in-memory buffer
    buffer = BytesIO()

    if 'JPEG' in str(key).upper():
        image.save(buffer, format='JPEG')
   #     filename += '.jpeg'

    elif 'JPG' in str(key).upper():
        image.save(buffer, format='JPG')
   #     filename += '.jpg'

    elif 'PNG' in str(key).upper():
        image.save(buffer, format='PNG')
   #     filename += '.png'

    buffer.seek(0)

    # 3. Upload to S3
    s3.upload_fileobj(buffer, bucket, f'{key}', ExtraArgs={'ContentType': f'{content_type}'})
    print('Image uploaded successfully')
