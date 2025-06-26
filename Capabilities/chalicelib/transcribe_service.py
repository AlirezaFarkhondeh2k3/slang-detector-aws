import boto3
import time
import uuid
import json
from urllib.parse import urlparse

class TranscribeService:
    def __init__(self, storage_service, output_bucket="1cent301278686"):
        self.storage_service = storage_service
        self.transcribe_client = boto3.client('transcribe')
        self.s3_client = boto3.client('s3')
        self.output_bucket = output_bucket  # Explicitly set the output bucket

    def transcribe_audio(self, audio_id):
        """Transcribes an audio file using Amazon Transcribe."""
        try:
            # Get the file URL from S3
            audio_file_url = self.storage_service.get_file_url(audio_id)

            if not audio_file_url:
                raise Exception("File URL not found.")

            # Generate a unique job name to avoid conflicts
            job_name = f"transcription-job-{audio_id}-{uuid.uuid4().hex[:8]}"

            # Start the transcription job and explicitly specify the output bucket
            print(f"Starting transcription job: {job_name}")
            self.transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': audio_file_url},
                MediaFormat='wav',  # Change this if your format is different
                LanguageCode='en-US',  # Change this if your language is different
                OutputBucketName=self.output_bucket  # Explicit output bucket
            )

            # Wait for the job to complete
            while True:
                result = self.transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
                status = result['TranscriptionJob']['TranscriptionJobStatus']

                if status in ['COMPLETED', 'FAILED']:
                    break

                print("Waiting for transcription to complete...")
                time.sleep(5)

            if status == 'COMPLETED':
                print(f"Transcription completed! Fetching from bucket: {self.output_bucket}")

                # Fetch the transcript directly from the output bucket
                transcript = self._download_transcript_from_s3(job_name)
                return transcript

            print("Transcription failed.")
            return None

        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return None

    def _download_transcript_from_s3(self, job_name):
        """Download the transcript JSON file from S3 and extract the text."""
        try:
            object_key = f"{job_name}.json"  # AWS saves the transcript using the job name

            # Download the transcript file from the explicitly set bucket
            response = self.s3_client.get_object(Bucket=self.output_bucket, Key=object_key)
            transcript_json = json.loads(response['Body'].read().decode('utf-8'))

            # Extract and return the transcript text
            return transcript_json.get('results', {}).get('transcripts', [{}])[0].get('transcript', '')

        except Exception as e:
            print(f"Error downloading transcript: {str(e)}")
            return None
