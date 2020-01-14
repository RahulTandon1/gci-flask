import os
from flask import Flask, url_for, render_template, request, \
    redirect, flash
from db import *
import json

# declaring/intialising the flask app
app = Flask(__name__)
allowed_extensions = ['txt']

@app.route('/')
def index():
    return redirect(url_for('viewTitles'))

@app.route('/viewTitles/')
def viewTitles():
    return render_template('titles.html', titles=getListOfTitles())


@app.route('/form/')
def form():
    return render_template('form.html')


@app.route('/submitForm', methods=['GET', 'POST'])
def handleForm():

    # variables used in the function
    fileContent = None
    fileTitle = None

    # if the submit is used with GET r
    # edirect the user to the main form page
    # (i.e. upload File page)
    if request.method == 'GET':
        return redirect(url_for('form'))

    # checking for existence of file in request.files
    # if the file is not there, it would mean that there's some problem
    # with the client side code and not particularly with the user's file
    if 'clientFile' not in request.files:
        errMsg = 'Error: clientFile not in request.files!'
        return render_template('error.html', error=errMsg)

    # if the program passed the above if statment,
    # that would mean that the 'clientFile' file exists
    file = request.files['clientFile']

    # checking if user did not submit the file
    # in which case the filename would be empty
    if file.filename == '':
        errMsg = 'Error: Filename empty!'
        print('\n\n', errMsg)
        return render_template('error.html', error=errMsg)

    # given that the program got till here,
    # it means that the filename is not empty,
    # i.e. the client sent a file

    # we now check if the file is a .txt or not
    # it it's NOT a .txt we return an error
    # approaching from right side since the
    # file extension will be right at the end
    # looking for '.' (dot)
    # if we pass in 1, we get an list of 2 elements
    # the latter will house the extension
    tempExtension = file.filename.rsplit('.', 1)[1].lower()

    if tempExtension in allowed_extensions:
        fileContent = file.read()
    else:
        errMsg = f'''Error: .{tempExtension} is not an allowed extension!. \
            Only the following extension(s) is/are allowed: \
            {allowed_extensions}'''
        print('\n\n', errMsg)
        return render_template('error.html', error=errMsg)

    # if the user send a title, we keep that as the title,
    # else we keep the title the name of the file sent to us
    if request.form['fileTitle']:
        fileTitle = request.form['fileTitle']
    else:
        fileTitle = file.filename

    # saving the file's contents to mongodb database
    saveStatus = storeFile(fileTitle, fileContent)

    if saveStatus == 'okay':
        return redirect(url_for('viewTitles'))
    else:
        errMsg = "It seems like you're trying to store a textFile \
            with a title that has been previously used. Please retry \
            with a different title."
        return render_template('error.html', error=errMsg)


@app.route('/getText/<title>')
def getText(title):
    text = getTextByTitle(title)
    res = {
        'text': text
    }
    return res


# running flask app!
app.run(debug=True)
