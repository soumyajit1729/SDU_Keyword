from flask import Flask, render_template, request, redirect, url_for
from keywords import extractor
import requests
from bs4 import BeautifulSoup

# import nltk
# nltk.download('punkt')
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer

app = Flask(__name__)

@app.route('/')
def hello():
    return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    keywords = []
    para = ""
    copy_text = ""
    itext = "NA"
    if request.method == 'POST':
        text = request.form['text']
        para = text
        keywords = extractor(text)
        # keywords.append("Education")
        # keywords.append("Books")
        # keywords.append("Professors")
        for word in keywords:
            copy_text = copy_text+word+", "
        copy_text = copy_text[:-2]

    return render_template('home.html', itext = itext, 
                           keywords=keywords, text=para[:100], copy = copy_text)


@app.route('/get_link', methods=['POST'])
def get_link():
    url = request.form['text']
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the main article content
    article = soup.find('div', class_='entry-content')

    # Get the text of the article
    article_text = article.get_text()
    article_text = article_text.strip()
    article_text = article_text.replace("\n", "")
    keywords = []
    para = ""
    copy_text = ""
    print("/////////////////")
    print(article_text[:200])
    print("/////////////////")
    return render_template('home.html', itext = article_text, 
                           keywords=keywords, text=para[:100], copy = copy_text)
    


if __name__ == '__main__':
    app.run()


# ubuntu@ip-172-31-6-66:~/SDU_Keyword$ python3 app.py
# 2023-04-14 06:31:07.421088: I tensorflow/tsl/cuda/cudart_stub.cc:28] Could not find cuda drivers on your machine, GPU will not be used.
# 2023-04-14 06:31:08.143522: I tensorflow/tsl/cuda/cudart_stub.cc:28] Could not find cuda drivers on your machine, GPU will not be used.
# 2023-04-14 06:31:08.145433: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
# To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
# 2023-04-14 06:31:10.541392: W tensorflow/compiler/tf2tensorrt/utils/py_utils.cc:38] TF-TRT Warning: Could not find TensorRT
