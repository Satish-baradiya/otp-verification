from flask import Flask, render_template, flash
from flask.globals import request, session
import random
import os
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = 'your secret key here'


@app.route('/', methods=["POST", "GET"])
def home():
    return render_template('index.html')


@app.route('/getotp', methods=['POST'])
def getotp():
    number = request.form['number']
    val = getOTPApi(number)
    if val:
        return render_template('enterotp.html')
    else:
        flash("Error")


@app.route('/verifyotp', methods=['POST', 'GET'])
def verifyotp():
    otp = request.form['otp']
    if 'response' in session:
        s = session['response']
        session.pop('response', None)

        if s == otp:
            return "Congratulations you are authorized..!!"
        else:
            return "Incorrect OTP "


def generateOTP():
    return random.randrange(100000, 999999)


def getOTPApi(number):

    account_sid = 'account_id'
    auth_token = 'auth_token'
    client = Client(account_sid, auth_token)
    otp = generateOTP()
    session['response'] = str(otp)
    body = "Your OTP is " + str(otp)
    message = client.messages.create(
        body=body,
        from_='+123456789',
        to=number
    )

    if message.sid:
        return True
    else:
        return False
