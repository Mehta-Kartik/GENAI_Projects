import streamlit as st
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

##Load the LSTM model
model=load_model('lstm_gutenberg.h5')

with open('tokenizer.pickle','rb') as f:
    tokenizer=pickle.load(f)


#Function to predict the next word
def predict_next_word(model,tokenizer,text,maxseq):
    token_list=tokenizer.texts_to_sequences([text])[0]
    if len(token_list)>maxseq:
        token_list=token_list[-(maxseq-1):] # This ensures that the max sequence length is preserved    
    token_list=pad_sequences([token_list],maxlen=maxseq-1,padding='pre')
    predicted=model.predict(token_list,verbose=0)
    predicted_word_index=np.argmax(predicted,axis=1)
    for word,index in tokenizer.word_index.items():
        if index==predicted_word_index:
            return word
    
    return None

##streamlit app now
st.title('Next Word Prediction using LSTM')
inpt=st.text_input("Enter the sequence of word","To be or not to be a human")
if st.button("Predict next word"):
    maxseqlen=model.input_shape[1]+1
    next_word=predict_next_word(model,tokenizer,inpt,maxseqlen)
    st.write(f"Next Word: {next_word}")
