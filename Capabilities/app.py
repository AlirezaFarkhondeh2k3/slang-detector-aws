from chalice import Chalice, Response
from chalicelib import storage_service
from chalicelib import transcribe_service
from chalicelib import translation_service
from chalicelib import slang_detection_service
from chalicelib import slang_service
import base64
import json

# Chalice app configuration
app = Chalice(app_name='AudioTranscription')
app.debug = True

# Services initialization
storage_location = '1cent301278686'  # Your S3 bucket
storage_service = storage_service.StorageService(storage_location)
transcribe_service = transcribe_service.TranscribeService(storage_service)
translation_service = translation_service.TranslationService()
slang_detector_service = slang_service.SlangDetectorService()
slang_service = slang_detection_service.SlangDetectionService()

# Upload audio
@app.route('/audio', methods=['POST'], cors=True)
def upload_audio():
    try:
        request_data = json.loads(app.current_request.raw_body)
        file_name = request_data['filename']
        file_bytes = base64.b64decode(request_data['filebytes'])

        audio_info = storage_service.upload_file(file_bytes, file_name)
        return {'message': 'Upload successful', 'fileId': audio_info['fileId']}

    except Exception as e:
        return {'error': str(e)}, 500

# Play audio
@app.route('/audio/{audio_id}/play', methods=['GET'], cors=True)
def play_audio(audio_id):
    try:
        file_content, mime_type = storage_service.get_file(audio_id)
        return Response(
            body=file_content,
            status_code=200,
            headers={
                'Content-Type': mime_type,
                'Content-Disposition': f'inline; filename="{audio_id}"'
            }
        )
    except Exception as e:
        return {'error': str(e)}, 500

# Transcribe audio
@app.route('/audio/{audio_id}/transcribe', methods=['POST'], cors=True)
def transcribe_audio(audio_id):
    try:
        text = transcribe_service.transcribe_audio(audio_id)
        if not text:
            return {'error': 'No transcription available'}, 400
        return {'transcription': text}

    except Exception as e:
        return {'error': str(e)}, 500

# Transcribe and translate audio
@app.route('/audio/{audio_id}/translate-text', methods=['POST'], cors=True)
def translate_audio_text(audio_id):
    try:
        request_data = json.loads(app.current_request.raw_body)
        from_lang = request_data['fromLang']
        to_lang = request_data['toLang']

        transcribed_text = transcribe_service.transcribe_audio(audio_id)
        if not transcribed_text:
            return {'error': 'Transcription failed'}, 400

        translated_text = translation_service.translate_text(transcribed_text, from_lang, to_lang)
        return {'translatedText': translated_text}

    except Exception as e:
        return {'error': str(e)}, 500

# Train slang detector
@app.route('/slang/train', methods=['POST'], cors=True)
def train_slang_model():
    try:
        request_data = json.loads(app.current_request.raw_body)
        training_data_s3_path = request_data['s3Path']
        role_arn = request_data['roleArn']
        model_name = request_data['modelName']

        result = slang_detector_service.train_slang_detector(training_data_s3_path, role_arn, model_name)
        return result

    except Exception as e:
        return {'error': str(e)}, 500

# Transcribe and detect slang
@app.route('/audio/{audio_id}/transcribe-and-detect', methods=['POST'], cors=True)
def transcribe_and_detect_slang(audio_id):
    try:
        text = transcribe_service.transcribe_audio(audio_id)
        print(f"Transcribed text: '{text}'")

        if text is None:
            return {'error': 'Transcription failed'}, 400

        slang_entities = slang_service.detect_slang(text)
        slang_terms = [e['Text'] for e in slang_entities if e['Type'] == 'SLANG']

        return {
            'transcription': text,
            'slang': slang_terms
        }

    except Exception as e:
        return {'error': str(e)}, 500
