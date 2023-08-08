// Function to change the background to the clicked movie poster
function changeBackground(posterUrl) {
    const backgroundOverlay = document.querySelector('.background-overlay');
    backgroundOverlay.style.backgroundImage = `url(${posterUrl})`;
    backgroundOverlay.style.opacity = 0.3; // Set the opacity of the background overlay
}

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
