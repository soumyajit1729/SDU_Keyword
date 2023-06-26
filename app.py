from flask import Flask, render_template, request, redirect, url_for
from keywords import extractor5
import requests
from bs4 import BeautifulSoup, NavigableString
# from gevent.pywsgi import WSGIServer

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
    itext = ""
    if request.method == 'POST':
        text = request.form['text']
        para = text
        keywords = extractor5(text)
        # keywords.append("Education")
        # keywords.append("Books")
        # keywords.append("Professors")
        for word in keywords:
            copy_text = copy_text+word+", "
        copy_text = copy_text[:-2]

    return render_template('home.html', itext = itext, 
                           keywords=keywords, text=para[:100], copy = copy_text)

def get_text(login_url):
  # Step 1: Send a GET request to the login page
  response = requests.get(login_url)
  # Define session
  session = requests.session()

  # Step 2: Extract nonces from the response HTML
  soup = BeautifulSoup(response.text, 'html.parser')
  pf_nonce = soup.find('input', {'name': 'pf_nonce'})['value']
  um_post_method_nonce = soup.find('input', {'name': 'um_post_method_nonce'})['value']
  login_data = {
      "user_login": "soumyajit1729",
      "user_pass": "Sahaj@123",
      "form_key": "Login",
      "action_type": "login",
      "user_id": 0,
      "pf_nonce": pf_nonce,
      "_wp_http_referer": "",
      "method_name": "Login",
      "um_post_method_nonce": um_post_method_nonce,
      "um_submit_button": "Login"
  }
  wp_http_referer = login_url.replace("www.epicpeople.org","")
  wp_http_referer = wp_http_referer.replace("epicpeople.org","")
  wp_http_referer = wp_http_referer.replace("https://","")

  login_data["_wp_http_referer"] = wp_http_referer
  # Login to website
  response = session.post(login_url, data=login_data)
  soup = BeautifulSoup(response.text, "html.parser")

  # Find article content
  article_content = soup.find("div", {"class": "entry-content"})
  print("//////////////////////////////////////////////////////////////")
  print(login_url)
  print(article_content.text[-100:])
  return article_content

def process(arg_article):
    # preprocessing
    a_tags = []
    flag = 0
    for tag in arg_article.descendants:
        # Do something with the tag
        if(tag.name=='h1' or tag.name=='h2' or tag.name=='h3' or tag.name=='strong'):
            txt = tag.text.lower()
            if("references" in txt or "related" in txt or "notes" in txt or "images" in txt ):
                flag = 1
                a_tags.append(tag)
        elif(flag == 1):
            a_tags.append(tag)

    for tag in a_tags:
        if not isinstance(tag, NavigableString):
            tag.decompose()

    # Get the text of the arg_article
    arg_article_text = arg_article.get_text()
    arg_article_text = arg_article_text.strip()
    arg_article_text = arg_article_text.replace("\n", " ")
    return arg_article_text


def get_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    ppns = soup.find_all(class_='post-page-numbers')

    # Find the main article content
    article = get_text(url)
    final_text = process(article)
    if len(ppns)>1:
        for i in range(2, len(ppns)+1):
            new_link = url+str(i)+"/"
            article_content = get_text(new_link)
            final_text = final_text + " " + process(article_content)
           
    return final_text
    

@app.route('/get_link', methods=['GET','POST'])
def get_link():
    if request.method == 'GET':
        return redirect(url_for('home'))
    url = request.form['text']
    article_text = get_text_from_url(url)
    keywords = []
    para = ""
    copy_text = ""
    print("/////////////////")
    print(article_text[:200])
    print("/////////////////")
    return render_template('home.html', itext = article_text, 
                           keywords=keywords, text=para[:100], copy = copy_text)
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()


# ubuntu@ip-172-31-6-66:~/SDU_Keyword$ python3 app.py
# 2023-04-14 06:31:07.421088: I tensorflow/tsl/cuda/cudart_stub.cc:28] Could not find cuda drivers on your machine, GPU will not be used.
# 2023-04-14 06:31:08.143522: I tensorflow/tsl/cuda/cudart_stub.cc:28] Could not find cuda drivers on your machine, GPU will not be used.
# 2023-04-14 06:31:08.145433: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
# To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
# 2023-04-14 06:31:10.541392: W tensorflow/compiler/tf2tensorrt/utils/py_utils.cc:38] TF-TRT Warning: Could not find TensorRT
