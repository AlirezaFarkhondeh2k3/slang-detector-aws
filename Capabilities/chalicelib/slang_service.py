import boto3
import time

class SlangDetectorService:
    def __init__(self, region='us-east-1'):
        self.client = boto3.client('comprehend', region_name=region)

    def train_slang_detector(self, s3_base_path, role_arn, model_name):
        """
        Train a custom slang detector using documents and annotations in S3.

        Args:
            s3_base_path (str): Base S3 path where documents.txt and annotations.csv are stored.
                                e.g., 's3://your-bucket/custom-slang/'
            role_arn (str): IAM role ARN with Comprehend permissions.
            model_name (str): Name for the custom model.

        Returns:
            dict: ARN and training status or error.
        """
        try:
            response = self.client.create_entity_recognizer(
                RecognizerName=model_name,
                DataAccessRoleArn=role_arn,
                InputDataConfig={
                    'Annotations': {
                        'S3Uri': s3_base_path + 'annotations.csv'
                    },
                    'Documents': {
                        'S3Uri': s3_base_path + 'documents.txt',
                        'InputFormat': 'ONE_DOC_PER_LINE'
                    },
                    'EntityTypes': [
                        {'Type': 'SLANG'}
                    ]
                },
                LanguageCode='en'
            )

            model_arn = response['EntityRecognizerArn']
            print(f"Training started for model: {model_name}, ARN: {model_arn}")

            # Monitor training status
            while True:
                status = self.client.describe_entity_recognizer(
                    EntityRecognizerArn=model_arn
                )['EntityRecognizerProperties']['Status']

                print(f"Current status: {status}")
                if status in ['TRAINED', 'IN_ERROR']:
                    break
                time.sleep(30)

            if status == 'TRAINED':
                return {'modelArn': model_arn, 'status': 'TRAINED'}
            else:
                return {'error': 'Training failed', 'status': status}

        except Exception as e:
            return {'error': str(e)}
