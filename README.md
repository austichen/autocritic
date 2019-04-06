# AutoCritic

https://autocritic.herokuapp.com/

A python sentiment analysis model trained to identify positive and negative movie reviews. Scrapes the Rotten Tomatoes site to gather a list of reviews, generates a count vector from the corpus which is then fed to the model.

![image](https://user-images.githubusercontent.com/35405685/54733825-38a1e600-4b72-11e9-8381-9a46665d2fd0.png)
To run locally:

1. `pip install -r requirements.txt`
2. `python manage.py runserver`
5. Navigate to `http://localhost:8000` and type in a movie!

Note: It is recommended that you set up a virtual environment first!
