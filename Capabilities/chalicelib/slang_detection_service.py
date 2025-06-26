# chalicelib/slang_detection_service.py

import boto3

class SlangDetectionService:
    def __init__(self, region='us-east-1'):
        self.client = boto3.client('comprehend', region_name=region)
        self.endpoint_arn = "arn:aws:comprehend:us-east-1:985539802541:entity-recognizer-endpoint/test"
        #arn:aws:comprehend:us-east-1:985539802541:entity-recognizer-endpoint/test
        

    def detect_slang(self, text):
        response = self.client.detect_entities(
            Text=text,
            EndpointArn=self.endpoint_arn
        )
        return response.get("Entities", [])
