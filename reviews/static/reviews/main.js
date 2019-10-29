document.addEventListener('DOMContentLoaded', function() {
    const submitBtn = document.querySelector('button');
    const textField = document.querySelector('input');
    const inputDiv = document.querySelector('#searchbar');
    const resultsSection = document.querySelector('#results');

    submitBtn.addEventListener('click', function(evt){
        const title = textField.value
        if(title!=='') getMovieAnalysis(title);
    })

    textField.addEventListener('keydown', function(evt) {
        const title = textField.value;
        if(title!=='' && evt.key==='Enter') getMovieAnalysis(title);
    })

    function getMovieAnalysis(title) {
        resultsSection.innerHTML = getLoadingSpinnerHTML();
        fetch(`/api/movie?title=${title}`)
            .then(res => res.json())
            .then(res => {
                renderResult(res);
            })
            .catch(err => {
                renderError(err);
            })
    }

    function getDescriptionText(rating) {
        if (rating >= 90) {
            return "A definite must watch! This movie has got to be truly amazing.";
        } else if (rating >=80) {
            return "Great choice! Time to bring out the popcorn.";
        } else if (rating >=70) {
            return "Not bad, but I would consider other options.";
        } else if (rating >= 60) {
            return "Do not watch this. You have been warned...";
        }
        return "Terrible! Why would you even search this autrocity?";
    }

    function renderResult(movie) {
        const rating = Math.round(movie.rating * 10000) / 100
        resultsSection.innerHTML = `
            <div class="ui card">
                <div class="image">
                    <img src="${movie.imageURL}">
                </div>
                <div class="content">
                    <p class="header">Autocritic rating: ${rating}%</p>
                    <div class="meta">
                        <span class="date">${movie.title}</span>
                    </div>
                    <div class="description" style="white-space: pre-line">${getDescriptionText(rating)}\nTomatometer Score: ${movie.tomatometerScore}</div>
                </div>
                <div class="extra content">
                    <i class="video"></i>
                    ${movie.numReviews} reviews analyzed
                </div>
            </div>
            <div class="word-cloud container">
                <div class="word-cloud">
                    <h3 class="green ui header">Most frequent positive words</h3>
                    <img src="/static/reviews/positiveWordCloud.png?dummy=${Math.floor(rating)}">
                </div>
                <div class="word-cloud">
                    <h3 class="black ui header">Most frequent negative words</h3>
                    <img src="/static/reviews/negativeWordCloud.png?dummy=${Math.floor(rating)}">
                </div>
            <div/>
        `
    }

    function renderError(err) {
        resultsSection.innerHTML = "<div class='grey ui header'>Oops! An error occurred. Sorry :(</div>";
    }

    function getLoadingSpinnerHTML() {
        return `<div class="ui segment">
        <div class="ui active inverted dimmer">
          <div class="ui indeterminate text loader">Performing sentiment analysis...</div>
        </div>
        <img src="https://semantic-ui.com/images/wireframe/short-paragraph.png"></img>
      </div>`
    }
});