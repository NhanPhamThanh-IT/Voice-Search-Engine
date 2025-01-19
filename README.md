# Voice-Search-Engine

## Project Description
Voice-Search-Engine is a comprehensive application that processes audio files to extract and return corresponding text content. The project is divided into two main parts: the backend and the frontend. The backend is built using Flask and handles audio processing and news content retrieval, while the frontend provides a user interface for interacting with the application.

## Backend

### Description
The backend provides APIs for uploading audio files, processing them, and returning the corresponding text content. It integrates various utilities for audio processing and news content retrieval.

### Installation
To install the backend dependencies, run the following command:
```bash
pip install -r backend/requirements.txt
```

### Usage
To start the backend server, run:
```bash
python backend/app.py
```
This will launch the backend server at `http://localhost:5000`.

### Folder Structure
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

## Frontend

### Description
The frontend provides a user interface for interacting with the Voice-Search-Engine application. It allows users to upload audio files and view the processed text content.

### Installation
To install the frontend dependencies, navigate to the `frontend` directory and run:
```bash
npm install
```

### Usage
To start the frontend development server, run:
```bash
npm start
```
This will launch the frontend server at `http://localhost:3000`.

### Folder Structure
```
frontend/
├── public/             # Static files
├── src/                # Source files
│   ├── components/     # React components
│   ├── pages/          # Page components
│   ├── services/       # API services
│   ├── styles/         # CSS and styling files
│   ├── App.js          # Main app component
│   ├── index.js        # Entry point
│   └── ...             # Other files
├── package.json        # Project metadata and dependencies
└── README.md           # Project documentation
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
