import requests 
import base64 
import json 


trans_api = "http://ai-lb-776202452.us-east-2.elb.amazonaws.com/upload_audio_transcription/"
det_api = "http://ai-lb-776202452.us-east-2.elb.amazonaws.com/detect_objects_in_frame/"
listing_api = "http://ai-lb-776202452.us-east-2.elb.amazonaws.com/generate_listing/"
product_api = "http://ai-lb-776202452.us-east-2.elb.amazonaws.com/product_identification/"


def upload_audio_transcription(file_path):
    files = {
        "audio_file": open(file_path, "rb")
    }
    response = requests.post(
        trans_api, files=files
    )
    return response.json()

def detect_objects_in_frame(image_path, query):
    with open(image_path, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode('utf-8')
    res = requests.post(det_api, json={
        "frame": encoded_string,
        "query": query,
    })
    # print(res.json())
    return res.json()

def generate_listing(trans, det):
    res = requests.post(listing_api, json={"detections": det, 
                                           "transcription": trans})
    # print(res.json())
    return res.json()

def get_products(trans):
    res = requests.post(product_api, json={"transcription": trans})
    # print(res.json())
    return res.json()