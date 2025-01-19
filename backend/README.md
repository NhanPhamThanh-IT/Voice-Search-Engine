# Voice-Search-Engine Backend

## Project Description
This project is the backend part of the Voice-Search-Engine application. It provides APIs for uploading audio files, processing them, and returning the corresponding text content. The backend is built using Flask and integrates various utilities for audio processing and news content retrieval.

## Installation
To install the project dependencies, run the following command:
```bash
pip install -r requirements.txt
```

## Usage
To start the backend server, run:
```bash
python app.py
```
This will launch the backend server at `http://localhost:5000`.

## Folder Structure
The project structure is organized as follows:
```
backend/
├── __pycache__/        # Compiled Python files
├── uploads/            # Uploaded audio files
├── utils/              # Utility modules
│   ├── __pycache__/    # Compiled Python files
│   ├── .env            # Environment variables
│   ├── audio.py        # Audio processing utilities
│   ├── helper.py       # Helper functions
│   └── news.py         # News content retrieval utilities
├── app.py              # Main Flask application
├── main.py             # Main processing logic
├── README.md           # Project documentation
└── requirements.txt    # Project dependencies
```

## Contributing
If you would like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License
This project is licensed under the MIT License.
