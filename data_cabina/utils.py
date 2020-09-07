import io, base64, random, string
from datetime import datetime
from PIL import Image
from django.conf import settings
from pyfcm import FCMNotification

from api_cabina.settings import FIREBASE_TOKEN, ALERT_TEMPERATURE
from auth_cabina.models import UserToken


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


def generate_token():
    """
        Generate an alphanumeric token of a specified length
    """
    length = settings.CABIN_TOKEN_LENGTH
    letters_and_digits = string.ascii_letters + string.digits * 4
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


def get_comapany_tokens(company):
    current_tokens = UserToken.objects.filter(user__client__company=company).values_list("token", flat=True)
    return current_tokens


def send_notification_to_token_list(tokens, message):
    server_token = FIREBASE_TOKEN
    push_service = FCMNotification(api_key=server_token)
    title = "Bio Booth Alert"
    body = "A new person has been registered with high temerature" if int(message["temp"]) > ALERT_TEMPERATURE else "A new person without mask has been registered"
    result = push_service.notify_multiple_devices(registration_ids=list(tokens), message_title=title, message_body=body)
    return result
