# Askaway PDF Chatbot

Askaway PDF Chatbot is a Streamlit web application that allows users to ask questions about the content of PDF files using Google Gemini Large Language Model (LLM)

## Features

- Upload PDF files and ask questions about their content.
- Receive answers based on the provided context and question.

## Getting Started

### Prerequisites

- Python 3.9 or later
- Pip (Python package manager)
- Virtualenv (optional, but recommended)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/joelsiby02/Askaway_PDF.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Askaway_PDF # i may have already done that for you!😁
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Activate the virtual environment (if you're using one):

   ```bash
   source /path/to/venv/bin/activate  # Unix/Linux/macOS
   ./path/to/venv/Scripts/activate     # Windows
   ```

2. Set up Google API key:

    if deployed:
    - Visit 'https://aistudio.google.com/app/apikey'
    - Create an API key and Paste it into the application

3. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

4. Open your web browser and go to [http://localhost:8501](http://localhost:8501) to access the Askaway PDF.

### Configuration

- The `app.py` file contains the main Streamlit application.
- Configuration settings such as page title and icon can be adjusted in the `main()` function of `app.py`.
- You can customize the chatbot behavior, including prompt templates and temperature settings, in the `user_input()` function of `app.py`.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/new-feature`).
6. Create a new pull request.

## License

This project is licensed under the [MIT License](LICENSE).
