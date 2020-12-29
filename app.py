from flask import Flask, render_template, request, redirect, url_for
import os
#import numpy as np
from os.path import join, dirname, realpath
import pandas as pd
import mysql.connector

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


# Database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dreams"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

# View All Database
for x in mycursor:
    print(x)





# Root URL
@app.route('/')
def index():
    # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        parseCSV(file_path)
    # save the file
        return redirect(url_for('index'))

def parseCSV(filePath):
    # CVS Column Names
    col_names = ['first_name','last_name','address', 'street', 'state' , 'zip']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath,names=col_names, header=None)
    # Loop through the Rows
    for i,row in csvData.iterrows():
        sql = "INSERT INTO addresses (last_name, address, street, state, zip) VALUES (%s, %s, %s, %s, %s)"
        values = (row['last_name'],row['address'],row['street'],row['state'],str(row['zip']))
        mycursor.execute(sql, values)
        mydb.commit()
        print(i,row['last_name'],row['address'],row['street'],row['state'],row['zip'])

if (__name__ == "__main__"):
    app.run(port = 5000)