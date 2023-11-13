// Get the tags and input elements from the DOM
const tags = document.getElementById('tags');
const input = document.getElementById('input-tag');

function addTags(text) {
    event.preventDefault();
    let tagContent = null;
    if (text) {
        tagContent = text;
    } else {
        tagContent = input.value.trim();

    }
    var parts = tagContent.split(":");
    if (parts.length !== 1 && tagContent.slice(-1) !== ":") {
        const tagList = document.getElementById('tags');
        const listItems = tagList.getElementsByTagName('li');
        let exists = false;
        for (let i = 0; i < listItems.length; i++) {
            if (listItems[i].innerText.includes(tagContent.toLowerCase().split(':')[0])) {
                exists = true;
                break;
            }
        }
        if (!exists) {
            // Create a new list item element for the tag
            const tag = document.createElement('li');

            // Get the trimmed value of the input element

            // If the trimmed value is not an empty string
            if (tagContent !== '') {

                // Set the text content of the tag to
                // the trimmed value
                tag.innerText = tagContent;
                const searchField = document.getElementById('searchbar')
                if(!searchField.value.includes(tagContent)){
                    if (searchField.value) {
                        searchField.value += '&&'
                        searchField.value += tagContent
                    } else {
                        searchField.value += tagContent
                    }
                }
                }

                // Add a delete button to the tag
                tag.innerHTML += `<button class="delete-button" value="${tagContent}">X</button>`;

                // Append the tag to the tags list
                tags.appendChild(tag);

                // Clear the input element's value
                input.value = '';
            }
        }

}


input.addEventListener('keydown', function (event) {

    // Check if the key pressed is 'Enter'
    if (event.key === 'Enter') {
        addTags()

    }
});

// Add an event listener for click on the tags list
tags.addEventListener('click', function (event) {

    // If the clicked element has the class 'delete-button'
    if (event.target.classList.contains('delete-button')) {
        console.log(event.target.getAttribute('value'))
        // Remove the parent element (the tag)
        event.target.parentNode.remove();
        const searchField = document.getElementById('searchbar')
        const value = event.target.getAttribute('value')
        const text = searchField.value.replace(value, '');
        // searchField.value = text
        let textFormat = text.replace(/^&&|&&$/g, '');
        let t = textFormat.replace('&&&&', '&&');
        searchField.value = t;

    }
});

function updateInput(value) {
    const input = document.getElementById('input-tag');
    const tagList = document.getElementById('tags');
    const listItems = tagList.getElementsByTagName('li');
    let exists = false;
    for (let i = 0; i < listItems.length; i++) {
        if (listItems[i].innerText.includes(value)) {
            exists = true;
            break;
        }
    }
    if (!exists) {
        if (input.value.includes(':')) {
            addTags()
            document.getElementById('input-tag').value = "";
            document.getElementById('input-tag').value += value;
            document.getElementById('input-tag').focus();
        } else {
            document.getElementById('input-tag').value = "";
            document.getElementById('input-tag').value += value;
            document.getElementById('input-tag').focus();
        }
    }

}


window.addEventListener('load', (event) => {
    const input = document.getElementById('input-tag');
    const text = input.value
    const words = text.split("&&");
    for (let word of words) {
        addTags(word)
    }

});
