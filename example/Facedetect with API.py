import requests
from IPython.display import HTML

subscription_key = "cf9603e7edc841688cf897bd5b38eec2"
assert subscription_key

face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

image_url = 'https://raw.githubusercontent.com/maiyarapkung/PSM-AT-STAMP/master/a.jpg'


headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
faces = response.json()
print(faces)