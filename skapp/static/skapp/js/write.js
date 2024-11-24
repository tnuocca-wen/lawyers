document.addEventListener("DOMContentLoaded", function() {
    console.log("js loaded");

    csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value');

    genForm = document.querySelector(".part1 form"); 
    genBtn = document.querySelector(".part1 form button");
    outArea = document.querySelector(".part2");

    loaderPlaceholder = document.querySelector(".loaderPlaceholder");

    console.log(genForm, csrfToken);

    genForm.addEventListener("submit", (e) => {
        e.preventDefault();
        addLoader();

        genBtn.disabled = true;

        const formData = new FormData(genForm);

        fetch(genURL, {
            method: 'POST',
            headers: {
                'X-CSRF-Token': csrfToken,
            },
            body: formData,
        }).then(response => {
            if (!response.ok){
                throw new Error('Network response was not ok.');
            }
            return response.json();
        }).then(data => {
            // console.log(data);
            loaderPlaceholder.innerHTML = ``;

            genBtn.disabled = false;

            outArea.innerHTML = `<h1 class="title mx-auto" style="width: fit-content;">Summary</h1>
            <div class="mt-3">${ data.summary }</div>
            <hr>` +
            `<h1 class="title mx-auto" style="width: fit-content;">Key Points</h1>
            <div class="mt-3">${ data.keytakeaways }</div>
            <hr>`
            // });
            handlersForPublish();
        }).catch(error => {
            console.error('Error:', error);
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