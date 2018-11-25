import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import json
from pprint import pprint
from config import DevelopmentConfig as Config

### Face

# You can use this example JPG or replace the URL below with your own URL to a JPEG image.
img_url = 'https://images-ssl.gotinder.com/5bd900d5d29f540b0512b67d/1080x1350_c18b5ab6-61ca-48f7-abea-137ce64026ef.jpg'


BASE_URL = 'https://uksouth.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL

analyze_url = BASE_URL + "detect"

headers = {'Ocp-Apim-Subscription-Key': Config.FACE_API_KEY}
params = {'returnFaceAttributes': 'age,gender,smile,facialHair,glasses,emotion,hair,makeup,accessories'}
data = {'url': img_url}
response = requests.post(analyze_url, headers=headers, params=params, json=data)
response.raise_for_status()

# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.
analysis = response.json()
pprint(analysis)

#Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

#Download the image from the url
img = requests.get(img_url)
image = Image.open(BytesIO(img.content))

#For each face returned use the face rectangle and draw a red box.
draw = ImageDraw.Draw(image)

for i in range(len(analysis)):
    draw.rectangle(getRectangle(analysis[i]), outline='red')



#Display the image in the users default image browser.
image.show()

### Vision

BASE_URL = 'https://uksouth.api.cognitive.microsoft.com/vision/v1.0/'  # Replace with your regional Base URL

analyze_url = BASE_URL + "analyze"

headers = {'Ocp-Apim-Subscription-Key': Config.VISION_API_KEY}
params = {'visualFeatures': 'Categories,Description,Color,Adult'}
data = {'url': img_url}
response = requests.post(analyze_url, headers=headers, params=params, json=data)
response.raise_for_status()

# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.
analysis = response.json()
pprint(analysis)

image_caption = analysis["description"]["captions"][0]["text"].capitalize()

# Display the image and overlay it with the caption.
image = Image.open(BytesIO(requests.get(img_url).content))
plt.imshow(image)
plt.axis("off")
_ = plt.title(image_caption, size="x-large", y=-0.1)
plt.show()

### Text

BASE_URL = "https://uksouth.api.cognitive.microsoft.com/text/analytics/v2.0/"

key_phrase_api_url = BASE_URL + "keyPhrases"

text = "Currently studying in the UK.\nProfessional procrastinator and League fan girl.\nCan probably eat more than you.\nLikely to swipe right if you have a dog."

documents = {'documents' : [
  {'id': '1', 'language': 'en', 'text': text},
]}

headers = {'Ocp-Apim-Subscription-Key': Config.TEXT_API_KEY}

response  = requests.post(key_phrase_api_url, headers=headers, json=documents)
key_phrases = response.json()
pprint(key_phrases)

sentiment_api_url = BASE_URL + "sentiment"

response  = requests.post(sentiment_api_url, headers=headers, json=documents)
sentiment = response.json()
pprint(sentiment)