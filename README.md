# Slang Detection System using AWS

This project demonstrates a real-time slang detection pipeline built with AWS cloud services. It transcribes spoken content using **Amazon Transcribe**, detects slang entities using **Amazon Comprehend** with a custom NER model, and delivers results via a web interface.

## Features

- 🎤 **Speech-to-Text** with Amazon Transcribe
- 🧠 **Custom NER Model** using Amazon Comprehend for slang detection
- 🌐 **Web UI** built with Flask and a simple, multi-user interface
- ☁️ **Deployed on AWS** using the Chalice framework

## Tech Stack

- Python, Flask, AWS Chalice
- Amazon Transcribe, Amazon Comprehend (Custom NER)
- Hand-annotated training data for NER
- Secure multi-user interface

## Project Structure

```

├── Capabilities/
│   └── .chalice/
│       └── chaliceLib/
├── website/
├── index.html
├── Pipfile
├── Pipfile.lock

```

## Usage

This app is designed to show how cloud-based NLP can help with:
- Content moderation
- Real-time speech analysis
- Scalable language understanding in production environments

## Authors

Developed as part of a Centennial College Cloud Machine Learning course group project.
