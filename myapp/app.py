from flask import Flask, render_template, request, url_for, jsonify, Blueprint
import pickle  # or the appropriate library for loading your model
import string
from nltk.corpus import stopwords
import nltk
import sklearn
from nltk.stem.porter import PorterStemmer
from .extensions import db, Session
from .models import SMSMessage, Base


nltk.download('punkt')
nltk.download('stopwords')


#app = Flask(__name__)
main = Blueprint('main', __name__)

session = Session()

ps = PorterStemmer()

def transform_text(text):
     #Lowercase
    text = text.lower()
    
    #Tokenization
    text = nltk.word_tokenize(text)
    
    #alpha numerical values
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
            
    text = y[:]
    y.clear()
    
    #Removing stopwords
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
            
    text = y[:]
    y.clear()
    
    #Stemming
    for i in text:
        y.append(ps.stem(i))
    
    return " ".join(y)  

#2 Loading model and vectorizer

tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))


@main.route("/")
def index():
    return render_template('/index.html')

#3 Getting text from user input

@main.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        
        msg = request.form['textHere']

        transform_text(msg)

        data = [msg]

        vect = tfidf.transform(data)

        result = model.predict(vect)
    
    if result == 1:
        db_msg = 'smishing'
    else:
        db_msg = 'legit'
         

#4. Display result on html page

    if result == 1:
        return render_template("/index.html", data="Smishing")
    else:
        return render_template("/index.html", data="Legit")



#Point for API documentation
@main.route('/API')
def API():
    return render_template('APIDocumentation.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/about')
def about():
    return render_template('about.html')
'''
@main.route('/detect', methods=['GET'])
def detect():
    
    data = request.get_json()
    if 'sms_message' not in data:
        return jsonify({'error': 'Missing "sms_message" field in the request'}), 400
    
    sms_message = data
    transform_text(sms_message)

    # Preprocess the SMS message
    preprocessed_sms = [sms_message]

    vect = tfidf.transform(preprocessed_sms)
    
    # Make predictions using the pre-trained model
    prediction = model.predict(vect)[0]
    
    result = "Smishing" if prediction == 1 else "Legitimate"
    
    # Store the SMS message and result in the database
    new_message = SMSMessage(text=preprocessed_sms, result=result)
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify({'result': result})
'''

if __name__ == '__main__':
    main.run(debug=True)
