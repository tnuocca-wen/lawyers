document.addEventListener('DOMContentLoaded', () => {
    
    document.body.classList.add('no-transition');

    themeBtn = document.getElementById("theme-button");
    body = document.body;

    if (body.classList.contains('dark-mode')) {
        
    }

    else if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark-mode');
    }

    document.body.classList.remove('no-transition');

    themeBtn.addEventListener('click', () => {
        body.classList.toggle('dark-mode');

        // if (themeBtn.innerText == 'light') {
        //     themeBtn.innerText = 'dark';
        // }

        // else {
        //     themeBtn.innerText = 'light';
        // }

        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
        } else {
            localStorage.removeItem('theme');
        }
    });
});