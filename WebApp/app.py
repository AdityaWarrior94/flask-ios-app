from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

def get_google_sheet_data():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
    client = gspread.authorize(creds)

    sheet_url = 'https://docs.google.com/spreadsheets/d/1W6MQtReptFkbjE2RxGWKZcgJ7Aph2jtqMdWzPONCn38/edit?gid=1730742277#gid=1730742277'
    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.worksheet('Python App')
    records_data = worksheet.get_all_records()
    return records_data

@app.route('/')
def index():
    data = get_google_sheet_data()
    return render_template('index.html', data=data)

@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.json
    update_google_sheets(form_data)
    return jsonify({"message": "Form submitted successfully"}), 200

def update_google_sheets(form_data):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
    client = gspread.authorize(creds)

    sheet_url = 'https://docs.google.com/spreadsheets/d/1W6MQtReptFkbjE2RxGWKZcgJ7Aph2jtqMdWzPONCn38/edit?gid=1730742277#gid=1730742277'
    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.worksheet('FormResponses')

    for student in form_data['Students']:
        row = [
            form_data['Date'], form_data['Time'], form_data['Branch'], form_data['Grade'],
            form_data['Batch'], form_data['Teacher'], form_data['Subject'], form_data['Class Type'],
            form_data['Chapter'], form_data['Sub-Topic'], student['Student Name'], student['Present'],
            student['Quiz Marks'], student['Assignment Grades']
        ]
        worksheet.append_row(row)

if __name__ == '__main__':
    app.run(debug=True)
