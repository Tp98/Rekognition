import boto3
import numpy as np
import cv2
import csv
import os
from PIL import Image
from datetime import datetime, timezone, timedelta
from django.utils import timezone

from rekognition.models import Employees


filename = 'video.avi'
frames_per_seconds = 24.0
res = '720p'

cap = cv2.VideoCapture(0)


while(True):

    users = Employees.objects.all()
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray2 = gray
    cv2.imshow('frame',gray)
    
    im = Image.fromarray(gray2)
    im.save('img.jpg')
    
    imageFile = 'img.jpg'
    bucket='alexandrebfaces'
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
    
    if(confidence > 99.0):
        for user in users :
            similarity = 0.0 
            print("I work for this user " + user.firstname)
            try:
                sourceFile=imageFile
                targetFile="../webappRekognition"+user.image.url
                                
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
                td = timedelta(seconds = 10)
                
                if(user.onBuilding == False):
                    tooFast = (datetime.now(timezone.utc)+timedelta(hours=1)-user.timeOfArrival) < td
                else:
                    tooFast = (datetime.now(timezone.utc)+timedelta(hours=1)-user.timeOfLeaving) < td
                    
                print(tooFast)
                
                print("similarity : " + str(similarity))
                
                if(similarity > 98 and tooFast == False):
                    csvFile = "./logs/" + str(user.id) + "/log.csv"
                    with open(csvFile, mode='a') as logFile:
                        check_dir(csvFile)
                        logWriter = csv.writer(logFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        if(user.onBuilding == False):
                            print("Welcome " + user.firstname +  " " + user.lastname + " time : " + str(datetime.now(timezone.utc)+timedelta(hours=1)))
                            user.timeOfArrival = timezone.now()+timedelta(hours=1)
                            user.onBuilding = True
                            user.save()
                            logWriter.writerow(['Arrival :',user.timeOfArrival])
                            break
                        else:
                            print("Goodbye " + user.firstname +  " " + user.lastname + " time : " + str(datetime.now(timezone.utc)+timedelta(hours=1)))
                            user.timeOfLeaving= timezone.now()+timedelta(hours=1)
                            user.onBuilding = False
                            user.save()
                            logWriter.writerow(['Leaving :',user.timeOfLeaving])
                            break
                else :
                    print("Sorry I don't know who is this person")
            except Exception as e:
                print(e)
            print("\n")
                
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
        
cap.release()
cv2.destroyAllWindows()

def check_dir(dir):
    csvFile = os.path.dirname(dir)
    if not os.path.exists(csvFile):
        os.makedirs(csvFile)

