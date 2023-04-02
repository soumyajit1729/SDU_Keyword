from flask import Flask, render_template, request
from keywords import extractor

# import nltk
# nltk.download('punkt')
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    keywords = []
    para = ""
    if request.method == 'POST':
        text = request.form['text']
        para = text
        # keywords = extractor(text)
        keywords.append("Education")
        keywords.append("Books")
        keywords.append("Professors")
        
    return render_template('home.html', keywords=keywords, text=para[:100])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)