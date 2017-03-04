# Online Game Store

## Team

**Kalaiarasan Saminathan** <br/>
**Rajagopalan Ranganathan**<br/>
**Sunil Kumar Mohanty**

## Description

Online Game Store is a project developed for the Web Software Development (CS-C3170) course for the year 2016-17. 
The project is based on Django framework.

Game developers have an inventory of game which they upload to the game store (just the urls). 

Players can 
- register in the application and purchase the game from the store and play on their mobile or desktop. The application maintains a leaderboard for each application.
- share their score in social media
- Register/Login using facebook
- Resume game from previous saved state

### Development Tools/Languages
IDE - JetBrains PyCharm
Languages - Python 3.5, HTML5, CSS (bootstrap), jquery, django

### Authentication

- User Registration
- Login
- Logout
- Email Validation
- Use Secret Key
- Login using Facebook

### Basic player functionalities

- Buy games
- payment service
- play games
- Game and Service interaction
- Player allowed to play the games which he has purchased and cannot play other games
- Search for games:
  - Arranged based on topics
  - arranged based on editor picks
  - Arranged based on date (new ones first)
  - Search based on
    - name
    - Game types (like arcade, simulation)
    - cost ? price

### Basic developer functionalities

- Add Game URL to game store
- Set price and remove/modify the posted game
- Statistics about the game (ex-purchases)
- Security restrictions (Only developers allowed to add/remove game)

### Game/service interaction

- Save player Score
- Save in High Score
- Display High scores for the game (top 10)

### Quality of Work

- Coding style to be followed as mentioned in - [https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)
- MTV (Model Template View) pattern to be followed
- Non-technical user can use the website comfortably
- Minimize the number of clicks to complete a task
- Should be accessible by mobile touch devices
- Validate the website against W3C validator

### Save/load and resolution feature

- Save the state of the game (Score)
- Allow the user to resume the game
- Save the user preferred Resolution (Height, Width)

### RESTful API

- Implement Restful API for all services even for internal templates and views
- Versioning support to be provided in the API

### Own game

- It should communicate the score to game store application
- Save/load the game
- Can be hosted as a static file in service, It should be available in the store

### Mobile Friendly

- Use bootstrap CSS framework to make a responsive design
- Use only div based layout in html

### Social media sharing

- Sharing the games in Facebook - Facebook share
- Sharing the games in Twitter - Twitter share
- sharing the games in Google+ - Google+ share
- Meta data retrieval from backend
- Icon or an image for the game - create and store in the backend
- Retrieved metadata added as an advertisement or description message and shared in the frontend
- verify that the shared game has meaningful and attractive messages