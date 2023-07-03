# Article Keyword Prediction Flask App

This Flask app predicts keywords for articles using machine learning models. Given an article, the app leverages various libraries to extract relevant keywords.

## Installation

To run this Flask app, you need to install the following libraries:

- [tensorflow](https://www.tensorflow.org/)
- [pke](https://github.com/boudinfl/pke) (Installation command: `pip install git+https://github.com/boudinfl/pke.git`)
- [keybert](https://github.com/MaartenGr/keybert)
- [tensorflow_hub](https://www.tensorflow.org/hub)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [transformer](https://huggingface.co/transformers/)

You can install these libraries using the following command:

```
pip install tensorflow keybert tensorflow_hub beautifulsoup4 transformer
```

## Usage

1. Clone the repository:
   ```
   git clone https://github.com/your-username/your-repo.git
   ```
2. Navigate to the project directory:
   ```
   cd SDU_keyword
   ```
3. Run the Flask app:
   ```
   python3 app.py
   ```
4. Access the app in your browser at `http://localhost:5000`.
## Requirements

- Hard Disk: 20GB or more (recommended)
- RAM: Minimum 6GB
