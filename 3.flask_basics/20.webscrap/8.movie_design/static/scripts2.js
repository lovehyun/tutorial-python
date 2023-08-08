document.addEventListener('DOMContentLoaded', function () {
    const carousel = document.querySelector('.movie-carousel');
    const cardContainer = carousel.querySelector('.card-container');
    const prevButton = carousel.querySelector('.carousel-prev');
    const nextButton = carousel.querySelector('.carousel-next');

    prevButton.addEventListener('click', function () {
        cardContainer.scrollBy({ left: -cardContainer.clientWidth, behavior: 'smooth' });
    });

    nextButton.addEventListener('click', function () {
        cardContainer.scrollBy({ left: cardContainer.clientWidth, behavior: 'smooth' });
    });
});
