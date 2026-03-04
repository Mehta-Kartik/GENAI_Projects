# print("Jay Ganesh")
import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import load_model
# from tensorflow.keras.layers import Embedding,SimpleRNN,Dense
word_index=imdb.get_word_index()
reverse_word_index={value:key for key,value in word_index.items()}
import tensorflow as tf
from tensorflow.keras.models import load_model
import tensorflow as tf
from tensorflow.keras.models import load_model

# Custom RNN wrapper (if you still need it)
class CompatibleSimpleRNN(tf.keras.layers.SimpleRNN):
    def __init__(self, *args, **kwargs):
        kwargs.pop('time_major', None)
        super().__init__(*args, **kwargs)

custom_objects = {'SimpleRNN': CompatibleSimpleRNN}

model_path = "simple.h5"  # note: .h5 now

model = tf.keras.models.load_model(
    model_path,
    custom_objects=custom_objects,
)


#Step2: Helper functions

def decode_review(encoded_review):
    return ' '.join([reverse_word_index.get(i-3,'?') for i in encoded_review])
def preprocess_text(text):
    words=text.lower().split()
    encoded_review=[word_index.get(word,2)+3 for word in words]
    padding_review=sequence.pad_sequences([encoded_review],maxlen=100)
    return padding_review

##Prediction function
def predict_sentiment(review):
    preprocessed_review=preprocess_text(review)
    prediction=model.predict(preprocessed_review)

    sentiment='Positive' if prediction[0][0]>.5 else 'Negative'
    return sentiment,prediction[0][0]
import streamlit as st

## Streamlit app

st.title('IMDB Movie Review Sentiment Analysis')
st.write('Enter a movie review to classify it as a positive or negative.')

user_inp=st.text_area('Movie Review')

if st.button('Classify'):
    preprocess_inp=preprocess_text(user_inp)

    prediction=model.predict(preprocess_inp)
    sentiment='Positive' if prediction[0][0]>.5 else 'Negative'

    st.write(f"Sentiment: {sentiment}")
    st.write(f"Prediction Score:{prediction[0][0]}")
else:
    st.write('Please enter a movie review')