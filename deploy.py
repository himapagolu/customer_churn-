from flask import Flask, render_template, request, redirect, url_for, flash
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
label = LabelEncoder()

model = pickle.load(open('trained_model.sav', 'rb'))

@app.route('/')
def index():
    result  = ''
    return render_template('index.html', **locals())

@app.route('/predict', methods=['POST'])


def predict():
    
    CustomerID = request.form['CustomerID']
    Name = request.form['Name']
    Age = float(request.form['Age'])
    Gender = request.form['Gender']
    Location = request.form['Location']
    Subscription_Length_Months = float(request.form['Subscription_Length_Months'])
    Monthly_Bill = float(request.form['Monthly_Bill'])
    Total_Usage_GB = float(request.form['Total_Usage_GB'])

    print('CustomerID: ', CustomerID)

    user_data  = {
        'CustomerID': CustomerID,
        'Name': Name,
        'Age': Age,
        'Gender' : [Gender],
        'Location': [Location],
        'Subscription_Length_Months': [Subscription_Length_Months],
        'Monthly_Bill': [Monthly_Bill],
        'Total_Usage_GB': [Total_Usage_GB]
    }

    user_data = pd.DataFrame(user_data)
    user_data = user_data.drop(['CustomerID' ,'Name'], axis=1)
    user_data['Location'] = label.fit_transform(user_data['Location'])
    user_data['Gender'] = label.fit_transform(user_data['Gender'])

    result = model.predict(user_data)
    print(result)
    return render_template('index.html', prediction_text=result)
if __name__ == '__main__':
    app.run(debug=False)