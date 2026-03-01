document.addEventListener("DOMContentLoaded", function () {
    const scoreElement = document.querySelector("h1");

    if (scoreElement) {
        let score = parseInt(scoreElement.innerText);
        scoreElement.style.transition = "0.5s";

        if (score >= 80) {
            scoreElement.style.color = "green";
        } else if (score >= 50) {
            scoreElement.style.color = "orange";
        } else {
            scoreElement.style.color = "red";
        }
    }
});