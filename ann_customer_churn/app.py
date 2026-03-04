import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder
import pandas as pd
import pickle

model=tf.keras.models.load_model('model.h5')

#Loader encoder and scaler
with open('label_encoder_gender.pkl','rb') as f:
    label_encoder_gender=pickle.load(f)

with open('ohe.pkl','rb') as f:
    ohegeo=pickle.load(f)

with open('scaler.pkl','rb') as f:
    scaler=pickle.load(f)

##Let's work on streamlit app
st.title('Customer Churn Predictions')

geography=st.selectbox('Geography',ohegeo.categories_[0])
gender=st.selectbox('Gender',label_encoder_gender.classes_)
age=st.slider('Age',18,92)
balance=st.number_input('Balance')
credit_score=st.number_input('Credit Score')
estimated_salary=st.number_input('Estimated Salary')
tenure=st.slider('Tenure',0,10)
numofproduct=st.slider('Number of Product',1,4)
has_cr_card=st.selectbox("Has Credit car",[0,1])
is_active_member=st.selectbox("Is active Members",[0,1]) 

input_data={
    'CreditScore':[credit_score],
    # 'Geography':geography,
    'Gender':[label_encoder_gender.transform([gender])[0]],
    'Age':[age],
    'Tenure':[tenure],
    'Balance':[balance],
    'NumOfProducts':[numofproduct],
    'HasCrCard':[has_cr_card],
    'IsActiveMember':[is_active_member],
    'EstimatedSalary':[estimated_salary]
}

geoencoded=ohegeo.transform([[geography]]).toarray()
geoencodeddf=pd.DataFrame(geoencoded,columns=ohegeo.get_feature_names_out(['Geography']))
input_data=pd.DataFrame(input_data)
input_data=pd.concat([input_data.reset_index(drop=True),geoencodeddf],axis=1)
input_data_scaled=scaler.transform(input_data)
## Let's predict churn
prediction=model.predict(input_data_scaled)
prediction_scalar = prediction.item() if prediction.size == 1 else prediction[0][0]
st.write(f"Churn Probability: {prediction_scalar:.2f}")

# prediction
# st.write(f"Churn Probability: {prediction:.2f}")
if prediction>0.5:
    st.write('The customer is likely to churn')
else:
    st.write('Customer is not going to churn')