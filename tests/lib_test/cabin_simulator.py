import requests, random, time, io, base64, numpy, json
from PIL import Image


class CabinSimulador:

    def __init__(self, url, token ,verbose = True):
        self.url = url
        self.token = token
        self.verbose = verbose

    def send_capture(self):
        data =self.generate_capture()
        response = requests.post(self.url, data = json.dumps(data))
        if self.verbose:
            print('SEND: ', list(data.items())[:-1])
            try:
                txt = response.json()
            except:
                print('Error, see html file for details')
                with io.open('error.html', "w", encoding="utf-8") as f:
                    f.write(response.text)
            else:
                print('RESPONSE: ',txt)

    def generate_capture(self):
        data = {
                'token': self.token,
                'temp': random.uniform(36, 43),
                'is_wearing_mask': random.uniform(0, 1) > 0.5,
                'is_image_saved': True,
                'image_base64': self.create_image(),
        }
        return data

    def create_image(self, width=512, height=256):
        rgb_array = numpy.random.rand(int(height), int(width), 3) * 255
        image = Image.fromarray(rgb_array.astype('uint8')).convert('RGB')
        image_bytes = io.BytesIO()
        image.save(image_bytes, "JPEG")
        img_str = base64.b64encode(image_bytes.getvalue())
        return str(img_str)
