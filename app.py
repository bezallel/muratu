from flask import Flask, request, render_template
import pandas as pd
import pickle
import numpy as np
import time

model = pickle.load(open('house.pkl', 'rb'))

# Mappings for displaying labels
housing_type_mapping = {0: "Duplex", 1: "Flat/Apartment", 2: "Mini Flat", 3: "Selfcon"}
bedroom_mapping = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6"}
bathroom_mapping = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6"}
guest_toilet_mapping = {0: "0", 1: "1", 2: "2", 3: "3"}
parking_space_mapping = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}
district_mapping = {
    0: "Abraham Adesanya", 1: "Abule Egba", 2: "Adeniyi Jones", 3: "Agege", 4: "Agege-Oko-oba", 5: "Ago Palace",
    6: "Ajah", 7: "Ajah-Addo", 8: "Ajah-Badore", 9: "Alagbado", 10: "Alapere", 11: "Alimosho", 12: "Allen Avenue", 13: "Amuwo Odofin", 14: "Apapa", 15: "Awoyaya", 16: "Badagry", 17: "Bode Thomas", 18: "Ebute Metta", 19: "Egbeda", 21: "Epe", 22: "Festac", 23: "Gbagada", 24: "Idimu", 25: "Ifako", 26: "Igando", 27: "Iju-Ishaga", 28: "Ikeja", 29: "Ikeja G.R.A", 30: "Ikorodu", 31: "Ikosi", 32: "Ikotun", 33: "Ikoyi", 34: "Ikoyi-Awolowo-Road", 36: "Ilupeju", 37: "Isheri", 38: "Isheri-Olowora", 39: "Isolo", 40: "Isolo-Oke-Afa", 41: "Iyana Ipaja", 42: "Ketu", 43: "Kosofe", 44: "Lagos Island", 45: "Lekki", 46: "Lekki Phase 1", 47: "Lekki Phase 2", 48: "Lekki Second Toll Gate", 49: "Lekki VGC", 50: "Lekki-Admiralty-Way", 51: "Lekki-Agungi", 52: "Lekki-Chevron", 53: "Lekki-Ibeju", 54: "Lekki-Idado", 55: "Lekki-Igbo-Efon", 56: "Lekki-Ikate", 57: "Lekki-Ikota", 58: "Lekki-Jakande", 59: "Lekki-Ologolo", 60: "Lekki-Orchid", 61: "Lekki-Osapa-London", 62: "Magodo", 63: "Magodo Brooks", 64: "Magodo Phase 1",  65: "Magodo Phase 2", 66: "Maryland", 67: "Maryland-Mende", 68: "Mushin", 69: "Ogba", 70: "Ogudu", 71: "Ojo", 72: "Ojodu Berger", 73: "Ojota", 74: "Okota", 76: "Omole", 77: "Omole Phase 2", 78: "Onike", 79: "Opebi", 80: "Opic", 81: "Oregun", 82: "Oshodi", 83: "Oshodi-Ajao", 84: "Oshodi-Mafoluku", 85: "Sangotedo", 86: "Shangisha", 87: "Shomolu", 88: "Surulere", 89: "Victoria Island", 90: "Victoria-Island-Oniru", 91: "Yaba", 92: "Yaba-Akoka", 93: "Yaba-Alagomeji"
}

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return (render_template('index1.html',
                                housing_type_mapping=housing_type_mapping,
                                bedroom_mapping=bedroom_mapping,
                                bathroom_mapping=bathroom_mapping,
                                guest_toilet_mapping=guest_toilet_mapping,
                                parking_space_mapping=parking_space_mapping,
                                district_mapping=district_mapping))


@app.route('/estimate', methods=['POST'])
def predict():
    try:

        int_features = [int(x) for x in request.form.values()]
        features = [np.array(int_features)]
        prediction = model.predict(features)[0]

        formatted_prediction = '{:,.2f}'.format(prediction)

        # time.sleep(2)

        return render_template('index1.html',
                               prediction_text='Your estimated annual rent based on your selected amenities is ₦{}'.format(
                                   formatted_prediction))
    except ValueError:
        return render_template('index1.html',
                               prediction_text='Oops! Looks like you left something out...Please complete your selection.')


if __name__ == '__main__':
    app.run(debug=True)