from datetime import datetime


def media_upload_to(instance, filename):
    current = datetime.now()
    path = current.strftime("%Y%m%d")
    cabin = instance.cabin.id
    time = current.strftime("%H%M%S")
    return '{}/cabin-{}-{}.jpg'.format(path, str(cabin), time)
