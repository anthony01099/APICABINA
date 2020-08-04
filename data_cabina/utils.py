import io, base64
from datetime import datetime
from PIL import Image

def media_upload_to(instance, filename):
    current = datetime.now()
    path = current.strftime("%Y%m%d")
    cabin = instance.cabin.id
    time = current.strftime("%H%M%S")
    return '{}/cabin-{}-{}.txt'.format(path, str(cabin), time)


def get_image_base64(django_file):
    """
        Transform a django image to a base64 string
    """
    image = Image.open(django_file)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")
    img_str = base64.b64encode(image_bytes.getvalue())
    return img_str
