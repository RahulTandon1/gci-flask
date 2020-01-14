**Try it out!!**
https://rt-flask.herokuapp.com/

**Contents**
1. app.py - the main flask app.
2. templates & static - the html, css, js side of things i.e. frontend
3. db.py - connnects with mongodb using the 'connectionString' which is left empty for security purposes
4. testFiles - sample .txt files if you want to you use them
5. Procfile - for heroku deployment
6. requirements.txt - lists all the requirements
7. env - virtual environment stuff
8. .gitignore

**Overall Working of the Project**
**Frontend**
We have basically 2 interfaces on the front end:
1. viewTitles - that lists all files by title and let's us view the file's contents by clicking on the title
2. form - that's meant for uploading new files with a given title.

Used template inheritance to simplify the process of making html pages. 
Templates:
1. base.html - the base documnet
2. form.html - the form page that takes the form as input
3. titles.html - the page that lists all the titles of the files uploaded and let's the user view their respective contents.
4. error.html (VERY IMPORTANT) - any error that occurs during execution is reported to the user using this page. I could've used the 'flash' method by that would've taken some time to get working, and I was really tired of doing research.

**NOTE**: The except the 1 .js file the front isn't documented. If you'd like the front end documented as well, please contact me. I'd gotten very tired working on the project so I let it be.

**Backend**
At the backend, we take the uploaded file, extract it's contents, store the contents in a mongodb database
where the given 'title' of the file acts as the unique id, i.e. no two 'files' (actually documents in the db) can have the same name. By default though, if the name is not provided, we make it 'Title' by default, but this will only run once and the user WILL have to give a unique name afterwards. 

For fetching:
1. titles - we have a separate endpoint to that corresponds to a separate mongodb function in db.py
2. text - we have a separate endpoint which returns the text of any 'file' (now extracted in a mongodb document) given the unique title. This endpoint too corresponds to a unique function in db.py. 

**Research**
While I had to do a very reasonable amount for research, one the main milestones was figuring out how to handle the file upload process. 

This link [https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/] helped a lot for that. 
Youtube channels like Tech with Tim, Sentedex, freecodecamp, Pretty Prined came in great use.
The heart of the program, the handling of the form that takes the file as input, was first directly picked up from the flask documentation linked above, then understood gradully over a period of time as I kept messing thrings up, and modified/rewritten.