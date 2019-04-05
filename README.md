# AutoCritic

A python sentiment analysis model trained to identify positive and negative movie reviews. Scrapes the Rotten Tomatoes site to gather a list of reviews, generates a count vector from the corpus which is then fed to the model.

![image](https://user-images.githubusercontent.com/35405685/54733825-38a1e600-4b72-11e9-8381-9a46665d2fd0.png)
To run locally:

1. `npm install`
2. `pip install wordcloud`
3. `pip install matplotlib`
4. `node index.js`
5. Navigate to `http://localhost:3000` and type in a movie!

Note: if you get an error with python, try changing `spawn("python", args)` to `spawn("python3", args)` in `index.js`.
