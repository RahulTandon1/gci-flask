# imports
import os
from flask import Flask, url_for, render_template, request, \
    redirect, flash
from db import *
import json

# declaring/intialising the flask app
app = Flask(__name__)

# list of allowed extensions. Can be easily extended this way.
allowed_extensions = ['txt']

# redirects the site's url or homepage to the viewTitles page
@app.route('/')
def index():
    return redirect(url_for('viewTitles'))

# renders a list of all the titles stored in the db.
@app.route('/viewTitles/')
def viewTitles():
    return render_template('titles.html', titles=getListOfTitles())

# renders the file upload form page
@app.route('/form/')
def form():
    return render_template('form.html')

# the endpoint that handles the form submission
# if it's used through 'GET' by mistake the user is
# rerouted to the uploadFile ('/form/') page.
@app.route('/submitForm', methods=['GET', 'POST'])
def handleForm():

    # variables used in the function
    fileContent = None
    fileTitle = None

    # if the submit is used with GET
    # redirect the user to the main form page
    # (i.e. upload File page) ['/form/']
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

    # if the file's contents and it's title got saved to mongodb successfully,
    # return the viewTitles page so that the user can see their new page.
    if saveStatus == 'okay':
        return redirect(url_for('viewTitles'))

    else:   # i.e. status = duplicateKeyError // see db.py
        # if the title already existed return an error message
        # through the error page
        errMsg = "It seems like you're trying to store a textFile \
            with a title that has been previously used. Please retry \
            with a different title."
        return render_template('error.html', error=errMsg)


# returns the the contents of the file whose title is given.
@app.route('/getText/<title>')
def getText(title):
    # getting content through the db.py function getTextByTitle()
    text = getTextByTitle(title)

    # packing the response in a dictionary
    res = {
        'text': text
    }

    # sending the dictionary
    return res
