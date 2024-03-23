
# ClearSpeak

Developed by Pavan Kumar, ClearSpeak is a Python application that utilizes Google's Speech-to-Text API for real-time audio transcription. The application includes a user-friendly graphical interface built with Tkinter, designed to provide clear transcription of human speech while filtering out background noise.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
  - [Clone the Repository](#clone-the-repository)
  - [Environment Setup](#environment-setup)
  - [Install Dependencies](#install-dependencies)
  - [Configure GCP Credentials](#configure-gcp-credentials)
- [Running the Application](#running-the-application)
- [How to Use](#how-to-use)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Real-Time Transcription**: Instantaneous transcription of speech from the microphone.
- **Noise Filtering**: Distinguishes between human speech and background noise.
- **User Interface**: Easy-to-use GUI for starting and stopping transcription.

## Prerequisites

Before starting, ensure you have the following:

- Python 3.x installed.
- An active Google Cloud Platform (GCP) account.
- Speech-to-Text API enabled in your GCP account.
- Your GCP service account key file downloaded.

## Setup and Installation

### Clone the Repository

```bash
git clone https://github.com/ascender1729/ClearSpeak.git
cd ClearSpeak
```

### Environment Setup

Create a virtual environment to manage your project's dependencies:

```bash
python -m venv myenv
.\myenv\Scripts\Activate.ps1  # On Windows
source myenv/bin/activate  # On Unix or MacOS
```

### Install Dependencies

Install the required libraries:

```bash
pip install google-cloud-speech pyaudio
```

### Configure GCP Credentials

Set your credentials to authenticate with Google Cloud:

```python
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path_to_your_service_account_key.json'
```

## Running the Application

Execute the application with:

```bash
python transcribe.py
```

## How to Use

- Click "Start Transcription" to begin.
- Click "Stop Transcription" to end. The transcribed text will be displayed in the application window.

## Troubleshooting

For `pyaudio` installation issues:

```bash
pip install pipwin
pipwin install pyaudio
```

## Contributing

To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## License

This project is available under the MIT License.

## Contact

Pavan Kumar - pavankumpavankumard.pg19.ma@nitp.ac.in

LinkedIn: [linkedin.com/in/im-pavankumar](https://www.linkedin.com/in/im-pavankumar/)

Project Link: [ClearSpeak](https://github.com/ascender1729/ClearSpeak)

