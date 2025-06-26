import boto3

class StorageService:
    def __init__(self, storage_location="1cent301278686"):
        self.client = boto3.client('s3')
        self.bucket_name = storage_location

    def get_storage_location(self):
        return self.bucket_name

    def upload_file(self, file_bytes, file_name):
        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Body=file_bytes,
                Key=file_name,
                ACL='public-read',
                ContentType='audio/mpeg'
            )

            response = self.client.head_object(Bucket=self.bucket_name, Key=file_name)
            print(f"File {file_name} uploaded successfully with response: {response}")

            file_url = self.get_file_url(file_name)
            return {'fileId': file_name, 'fileUrl': file_url}

        except Exception as e:
            print(f"Error uploading file: {e}")
            return {'error': 'Failed to upload file'}

    def get_file_url(self, file_name):
        try:
            return f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
        except Exception as e:
            print(f"Error generating file URL: {str(e)}")
            return None

    def get_file(self, file_name):
        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=file_name)
            file_content = response['Body'].read()
            mime_type = response.get('ContentType', 'audio/mpeg')  # or detect dynamically
            return file_content, mime_type
        except Exception as e:
            print(f"Error retrieving file '{file_name}': {e}")
            raise e
