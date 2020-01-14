// displays the test passed in, in the displayer div.
function putInDisplayer(textToDisplay) {
    displayer = document.getElementById('fileContentDisplayer')
    displayer.innerText = ''
    displayer.innerText = textToDisplay
}

// getting array of anchor tags in the titlesContainer div
titleAnchorTags = document.getElementsByClassName('titleAnchor')

// getting the length of the array, so we won't have to compute it repeatedly
iterationLength = titleAnchorTags.length

// iterating over every anchord tag 
// (each of which is a title corresponding to a document uploaded)
for (i = 0; i < iterationLength; i++){
    // adding an event listener on the link for when it's clicked
    titleAnchorTags[i].addEventListener('click', 
    (event) => {
        
        // geting titleName
        let title = event.target.innerText
        
        // generating url based on the titleName extracted previously
        let url = '/getText/' + title

        // fetching the content of the file whose 'title' has been provided
        fetch(url)
        .then(res => res.json())
        .then(result => {
            // assigning the text recieved to a variable called 'text'
            let text = result.text.text
            // calling the putInDisplayer, which displays the passed in content
            // in the fileContentDisplayer div
            putInDisplayer(text)
        })
        // catching errors if any and logging them
        .catch(err => console.log('ERROR:', err))

    })
}