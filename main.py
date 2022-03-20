'''
Mailroom Flask app
'''

import os
import base64
import peewee

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)


@app.route('/')
def home():
    '''
    home page for app
    '''
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    '''
    displays a list of donors and their donations
    '''
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create', methods=['GET', 'POST'])
def create():
    '''
    creates a new donation record for an existing or new donor
    '''
    if request.method == 'GET':
        return render_template('create.jinja2')
    else:
        donor = request.form['name']
        donation = request.form['donation']

        try:
            donor_record = Donor.get(Donor.name == donor)
        except peewee.DoesNotExist:
            new_donor = Donor.create(name=donor)
            Donation.create(value=donation, donor=new_donor)
        else:
            Donation.create(value=donation, donor=donor_record)

        donations = Donation.select()
        return render_template('donations.jinja2', donations=donations)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)