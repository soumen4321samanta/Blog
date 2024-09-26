document.addEventListener('DOMContentLoaded', function() {
    // Add scrollspy to <body>
    $('body').scrollspy({ target: '#navbarNav' });

    // Smooth scrolling for internal links
    $(".nav-link").on('click', function(event) {
        if (this.hash !== "") {
            event.preventDefault();

            var hash = this.hash;

            $('html, body').animate({
                scrollTop: $(hash).offset().top - 70
            }, 800, function(){
                window.location.hash = hash;
            });
        }
    });

    // Toggle full post content
    $('.read-more').on('click', function(event) {
        event.preventDefault();
        var cardBody = $(this).closest('.card-body');
        cardBody.find('.summary').toggleClass('d-none');
        cardBody.find('.full-post').toggleClass('d-none');
        $(this).text($(this).text() === 'Read More' ? 'Read Less' : 'Read More');
    });
});
