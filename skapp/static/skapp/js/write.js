document.addEventListener("DOMContentLoaded", function() {
    console.log("js loaded");

    csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value');

    genForm = document.querySelector(".part1 form"); 
    genBtn = document.querySelector(".part1 form button");
    outArea = document.querySelector(".part2");


    loaderPlaceholder = document.querySelector(".loaderPlaceholder");

    // console.log(genForm, csrfToken);

    // allnotes = [];
    // endtimeline = '';

    genForm.addEventListener("submit", (e) => {
        e.preventDefault();
        addLoader();
        
        genBtn.disabled = true;  // Disable the button to prevent multiple submissions
    
        const formData = new FormData(genForm);
    
        fetch(genURL, {
            method: 'POST',
            headers: {
                'X-CSRF-Token': csrfToken,
            },
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        })
        .then(data => {
            loaderPlaceholder.innerHTML = ``;  // Remove the loader
    
            genBtn.disabled = false;  // Re-enable the button after the request
    
            outArea.innerHTML = ``;  // Clear previous output
            console.log(data.notes);  // Debug: Log the notes data
    
            // Render Notes
            data.notes.forEach(element => {
                for (const [key, value] of Object.entries(element)) {
                    // Create note container and append elements dynamically
                    const noteContainer = document.createElement('div');
                    noteContainer.classList.add('note-container');
                    
                    //Header div
                    const noteHead = document.createElement('div');
                    noteHead.classList.add('d-flex', 'justify-content-between');

                    // Title for the note
                    const noteTitle = document.createElement('h1');
                    noteTitle.classList.add('title', 'mx-auto');
                    noteTitle.style.width = 'fit-content';
                    noteTitle.innerText = `Notes for ${key}`;
                    
                    // Download button for the note
                    const downloadButton = document.createElement('button');
                    downloadButton.classList.add('btn');
                    downloadButton.id = `${key}_Notes`;
                    downloadButton.innerText = 'Download';
                    
                    // Content of the note
                    const noteContent = document.createElement('div');
                    noteContent.classList.add('mt-3');
                    noteContent.innerHTML = value[0];  // Use innerHTML if you're expecting HTML content
                    
                    // Append all elements to the note container
                    noteHead.appendChild(noteTitle);
                    noteHead.appendChild(downloadButton);
                    noteContainer.appendChild(noteHead);
                    noteContainer.appendChild(noteContent);
                    
                    // Add the note container to outArea
                    outArea.appendChild(noteContainer);
                    
                    // Event listener for download button
                    downloadButton.addEventListener('click', function() {
                        console.log("Entered the event listener to download.");
                        saveTextToFile(value[1], `${downloadButton.id}.md`);
                    });
    
                    // Append a horizontal line after each note
                    const hr = document.createElement('hr');
                    noteContainer.appendChild(hr);
                }
            });
    
            // Timeline section
            const timelineSection = document.createElement('div');

            const timelineHead = document.createElement('div');
            timelineHead.classList.add('d-flex', 'justify-content-between');

            const timelineTitle = document.createElement('h1');
            timelineTitle.classList.add('title', 'mx-auto');
            timelineTitle.style.width = 'fit-content';
            timelineTitle.innerText = 'Timeline';

            const tdownloadButton = document.createElement('button');
            tdownloadButton.classList.add('btn');
            tdownloadButton.id = `Timeline`;
            tdownloadButton.innerText = 'Download';
    
            const timelineContent = document.createElement('div');
            timelineContent.classList.add('mt-3');
            timelineContent.innerHTML = data.timeline[0];  // Add timeline content
            
            timelineHead.appendChild(timelineTitle);
            timelineHead.appendChild(tdownloadButton);
            timelineSection.appendChild(timelineHead);
            timelineSection.appendChild(timelineContent);
    
            outArea.appendChild(timelineSection);  // Append the timeline to outArea
    
            const hr = document.createElement('hr');
            outArea.appendChild(hr);  // Add horizontal line after timeline

            tdownloadButton.addEventListener('click', function() {
                console.log("Entered the event listener to download.");
                saveTextToFile(data.timeline[1], `${tdownloadButton.id}.md`);
            });
    
            handlersForPublish();  // Call any additional handlers for publishing

        })
        .catch(error => {
            console.error('Error:', error);  // Handle any errors
            loaderPlaceholder.innerHTML = ``;  // Ensure the loader is cleared on error
            genBtn.disabled = false;  // Re-enable the button on error
        });
    });
    

    const alertPlaceholder = document.getElementById('alert-container');
    const appendAlert = (message, type) => {
      const wrapper = document.createElement('div')
      wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible" role="alert">`,
        `   <div>${message}</div>`,
        '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>'
      ].join('');
    
      alertPlaceholder.append(wrapper)
      setTimeout(() => {
        alertPlaceholder.removeChild(wrapper);
      }, 5000);
    }

});

function handlersForPublish(){
    try {
        const forms = document.querySelectorAll(".part2 form");
        forms.forEach(form => {
            form.addEventListener('submit', function(event) {
                event.preventDefault();
                console.log("intercepted");
                console.log(event.currentTarget);

                clickedForm = event.currentTarget;

                const actionUrl = '/write';
                const formData = new FormData(clickedForm);
                const params = new URLSearchParams(formData).toString();

                const urlWithParams = `${actionUrl}?${params}`;

                fetch(urlWithParams)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        const published = document.createElement('div');
                        published.innerHTML = `✅`;
                        published.style.fontSize = 'x-large';
                        published.classList.add('published', 'mx-auto');

                        clickedForm.replaceWith(published);
                        return;
                    })
                    .catch(error => {
                        console.error("There was a problem with the fetch operation:", error);
                    });
            });
        });
    } catch (error) {
        console.error(error);
    }
}

function addLoader(){
    loaderPlaceholder.innerHTML = `<span class="loader"></span>`;
}


function saveTextToFile(text, filename) {

    const blob = new Blob([text], { type: 'text/plain' });

    const link = document.createElement('a');

    const url = URL.createObjectURL(blob);

    link.download = filename;

    link.href = url;

    link.click();

    URL.revokeObjectURL(url);
}