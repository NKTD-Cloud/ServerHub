document.addEventListener('DOMContentLoaded', function() {
    const body = document.getElementById('body');

    function handleFadeOut(event) {
        event.preventDefault();
        const targetUrl = event.currentTarget.href || event.currentTarget.getAttribute('data-href');
        body.classList.add('fade-out');

        setTimeout(function() {
            window.location.href = targetUrl;
        }, 250);
    }

    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', handleFadeOut);
    });

    document.querySelectorAll('button[data-href]').forEach(button => {
        button.addEventListener('click', handleFadeOut);
    });
});
