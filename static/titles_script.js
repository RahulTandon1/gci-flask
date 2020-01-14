function putInDisplayer(textToDisplay) {
    displayer = document.getElementById('fileContentDisplayer')
    displayer.innerText = ''
    displayer.innerText = textToDisplay
}

titleAnchorTags = document.getElementsByClassName('titleAnchor')
iterationLength = titleAnchorTags.length

for (i = 0; i < iterationLength; i++){
    titleAnchorTags[i].addEventListener('click', 
    (event) => {
        let title = event.target.innerText
        let url = '/getText/' + title

        fetch(url)
        .then(res => res.json())
        .then(result => {
            let text = result.text.text
            putInDisplayer(text)
        })
        .catch(err => console.log('ERROR:', err))

    })
}