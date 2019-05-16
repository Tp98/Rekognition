import boto3
import numpy as np
import cv2
from PIL import Image
import time

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webappRekognition.settings")
django.setup()

from rekognition.model import User

def run():
    filename = 'video.avi'
    frames_per_seconds = 24.0
    res = '720p'

    cap = cv2.VideoCapture(0)
    while(True):

        users = User.Objects.All()
        ret, frame = cap.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray2 = gray
        cv2.imshow('frame',gray)
        
        im = Image.fromarray(gray2)
        im.save('img.jpg')
        
        imageFile = 'img.jpg'
        bucket='c00243743faces'
        client = boto3.client('rekognition')
        
        clientS3 = boto3.client('s3')
        clientS3.upload_file('img.jpg', bucket, 'img.jpg')
        
        response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':imageFile}},Attributes=['ALL'])
                                                                                                          
        if(response['FaceDetails'] != []):
            for details in response['FaceDetails']:
                confidence = details['Confidence']
        else:
            confidence = 00.0
        
        print(confidence)
        
        if(confidence == 100.0):
            for user in users : 
                sourceFile=imageFile
                targetFile=user.image
                client=boto3.client('rekognition')
       
                imageSource=open(sourceFile,'rb')
                imageTarget=open(targetFile,'rb')

                response=client.compare_faces(SimilarityThreshold=70,
                                              SourceImage={'Bytes': imageSource.read()},
                                              TargetImage={'Bytes': imageTarget.read()})
                
                for faceMatch in response['FaceMatches']:
                    similarity = faceMatch['Similarity']
                   
                imageSource.close()
                imageTarget.close()
                if(similarity > 95):
                    print("Welcome " + user.firstname +  " " + user.lastname) 
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
            
    cap.release()
    cv2.destroyAllWindows()

