from PIL import Image
import boto3
from io import BytesIO
from shared.aws_config.s3 import s3

def resize_and_upload(file_obj, uuid, bucket='trackerr-dp'):
    # 1. Open and resize the image
    content_type = file_obj.content_type
    image = Image.open(file_obj)
    filename = str(uuid)
    image = image.convert('RGB')  # in case it's RGBA or P
    image = image.resize((300, 300))

    # 2. Save the resized image to an in-memory buffer
    buffer = BytesIO()

    if 'JPEG' in str(content_type).upper():
        image.save(buffer, format='JPEG')
        filename += '.jpeg'

    elif 'JPG' in str(content_type).upper():
        image.save(buffer, format='JPG')
        filename += '.jpg'

    elif 'PNG' in str(content_type).upper():
        image.save(buffer, format='PNG')
        filename += '.png'

    buffer.seek(0)

    print(filename)

    Key = f'profile-pics/{filename}'

    # 3. Upload to S3
    s3.upload_fileobj(buffer, bucket, f'{Key}', ExtraArgs={'ContentType': f'{content_type}'})

    # 4. Return the Key
    return [Key, f'https://{bucket}.s3.amazonaws.com/{Key}']
