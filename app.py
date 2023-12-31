from flask import Flask, render_template, request
import pickle
import locale
from sklearn.preprocessing import StandardScaler
from datetime import datetime

app = Flask(__name__)
model = pickle.load(open('file.pkl', 'rb'))

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html', show_form=True)

standard_to = StandardScaler()

def format_indian_currency(number):
    locale.setlocale(locale.LC_MONETARY, 'en_IN')
    return locale.currency(number, grouping=True)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        year = int(request.form['year'])
        current_year = datetime.now().year

        vehicle_age = current_year - year
        sellertype = request.form['sellertype']
        seats = int(request.form['seats'])
        new_price = float(request.form['new_price'])
        kmdriven = int(request.form['kmdriven'])
        fueltype = request.form['fuel']
        transmissiontype = request.form['transmissiontype']
        enginecc = int(request.form['enginecc'])
        mileage = float(request.form['mileage'])
        
        if fueltype == 'Petrol':
            fueltype = 0
        elif fueltype == 'Diesel':
            fueltype = 1
        else:
            fueltype = 2

        if transmissiontype == 'Manual':
            transmissiontype = 0
        else:
            transmissiontype = 1

        if sellertype == 'Individual':
            sellertype = 0
        else:
            sellertype = 1

        # prediction = model.predict([[new_price, year, fuel, transmissiontype, mileage, enginecc, kmdriven]])
        prediction = model.predict([[vehicle_age, kmdriven, sellertype, fueltype, transmissiontype,mileage, enginecc, seats, new_price]])
        output = round(prediction[0]*100000, 2)

        # Convert output into Indian currency format
        if output < 0:
            return render_template('index.html', prediction_text='Sorry! You cannot sell this car', show_form=False)
        else:
            formatted_output = format_indian_currency(output)
            return render_template('index.html', prediction_text=f'{formatted_output}', show_form=False)

    else:
        return render_template('index.html', show_form=True)

if __name__ == '__main__':
    app.run(debug=True)
