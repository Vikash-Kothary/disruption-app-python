import requests
import json
from config import DevelopmentConfig as Config


def Extract(profile_json):

    dictionary = profile_json

    bio_text = profile_json['bio']
    # Text

    BASE_URL = "https://uksouth.api.cognitive.microsoft.com/text/analytics/v2.0/"

    key_phrase_api_url = BASE_URL + "keyPhrases"
    sentiment_api_url = BASE_URL + "sentiment"
    headers = {'Ocp-Apim-Subscription-Key': Config.TEXT_API_KEY}

    documents = {'documents': [
        {'id': '1', 'language': 'en', 'text': bio_text},
    ]}

    phrase_response = requests.post(key_phrase_api_url, headers=headers, json=documents)
    key_phrases = phrase_response.json()

    sentiment_response = requests.post(sentiment_api_url, headers=headers, json=documents)
    sentiment = sentiment_response.json()

    dictionary['key_phrases'] = key_phrases['documents'][0]['keyPhrases']
    dictionary['sentiment'] = sentiment['documents'][0]['score']

    photos = dictionary['photos']

    for i in range(len(photos)):
        # Face

        # You can use this example JPG or replace the URL below with your own URL to a JPEG image.
        img_url = photos[i]['photo_url']

        BASE_URL = 'https://uksouth.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL

        analyze_url = BASE_URL + "detect"

        headers = {'Ocp-Apim-Subscription-Key': Config.FACE_API_KEY}
        params = {'returnFaceAttributes': 'age,gender,smile,facialHair,glasses,emotion,hair,makeup,accessories'}
        data = {'url': img_url}
        response = requests.post(analyze_url, headers=headers, params=params, json=data)
        response.raise_for_status()

        # The 'analysis' object contains various fields that describe the image. The most
        # relevant caption for the image is obtained from the 'description' property.
        face_analysis = response.json()

        # Convert width height to a point in a rectangle
        def getRectangle(faceDictionary):
            rect = faceDictionary['faceRectangle']
            left = rect['left']
            top = rect['top']
            bottom = left + rect['height']
            right = top + rect['width']
            return ((left, top), (bottom, right))

        # Download the image from the url
        img = requests.get(img_url)

        # Vision

        BASE_URL = 'https://uksouth.api.cognitive.microsoft.com/vision/v1.0/'  # Replace with your regional Base URL

        analyze_url = BASE_URL + "analyze"

        headers = {'Ocp-Apim-Subscription-Key': Config.VISION_API_KEY}
        params = {'visualFeatures': 'Categories,Description,Color,Adult'}
        data = {'url': img_url}
        response = requests.post(analyze_url, headers=headers, params=params, json=data)
        response.raise_for_status()

        # The 'analysis' object contains various fields that describe the image. The most
        # relevant caption for the image is obtained from the 'description' property.
        vision_analysis = response.json()

        dictionary['photos'][i]['racy'] = vision_analysis['adult']['racyScore']
        dictionary['photos'][i]['caption'] = vision_analysis['description']['captions'][0]['text']
        dictionary['photos'][i]['image_tags'] = vision_analysis['description']['tags']

        if face_analysis != []:
            dictionary['photos'][i]['face_box'] = face_analysis[0]['faceRectangle']
            dictionary['photos'][i]['estimate_age'] = face_analysis[0]['faceAttributes']['age']
            dictionary['photos'][i]['smile'] = face_analysis[0]['faceAttributes']['smile']
            dictionary['photos'][i]['makeup'] = face_analysis[0]['faceAttributes']['makeup']
            dictionary['photos'][i]['hair'] = face_analysis[0]['faceAttributes']['hair']
            dictionary['photos'][i]['facial_hair'] = face_analysis[
                0]['faceAttributes']['facialHair']
            dictionary['photos'][i]['accessories'] = face_analysis[
                0]['faceAttributes']['accessories']
            dictionary['photos'][i]['emotion'] = face_analysis[0]['faceAttributes']['emotion']
        else:
            dictionary['photos'][i]['face_box'] = None
            dictionary['photos'][i]['estimate_age'] = None
            dictionary['photos'][i]['smile'] = None
            dictionary['photos'][i]['makeup'] = None
            dictionary['photos'][i]['hair'] = None
            dictionary['photos'][i]['facial_hair'] = None
            dictionary['photos'][i]['accessories'] = None
            dictionary['photos'][i]['emotion'] = None

    return dictionary
