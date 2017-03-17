# Game Store Project Plan

## Table of contents
#### 1. Team
#### 2. Goal
#### 3. Plans
#### 4. Resources
#### 5. Process and Time Schedule
#### 6. Testing
#### 7. Risk Analysis
#### 8. Project report
## 1. Team
![alt text](http://as.fi/images/naamat/tuomas_tiira2.jpg "Tuomas") **294379 Tuomas Tiira**

![alt text](http://as.fi/images/naamat/noora_vanttinen2.png "noora") **294609 Noora Vänttinen**

![alt text](http://as.fi/images/naamat/matti_ojala2.png "matti") **84375T Matti Ojala**

## 2. Goal

Goal is to create online game store for JavaScript games. Game store will provide functionalities for players and developers. We plan to implement all mandatory functional requirements and on top of that at least few additional requirements. Our intention is to get grade four or higher from the project.

## 3. Plans
### 3.1. Code Structure
#### Models
* **Developer**
	* A model for a developer, which can be an individual person or a company. The developers have access to their own games and can add/remove/set prices on them. The model includes information about the developer such as its name, username (id) and owned games.
* **Player**
	* Contains the username (id), owned games and personal information of the normal users. A player can buy games and play the ones that are free or that the player owns.
* **Admin**
	* Contains the username (id) and personal information of the admin user. An admin can remove developers and players.

* **Game**
	* Contains information about the games such as the game url, name, category and game developer information.
* **SaveState**
	* A model which can be used to save a games state. Different games might need their own SaveState models.
* **Score**
	* A model for high scores that can be sent out of the javascript game to the server. Different games might need their own Score models.


![alt text](http://i.imgur.com/OwFf03a.png "kuva1")

Picture 1: Django model structure


#### Views
* **Home**
	* Top games, links to login/register views, (sales) etc.
* **Game(s)**
	* A view for individual games. Contains an iframe for the javascript games and django blocks for high scores and other possible content.
* **Browse games**
	* A view where users can search for a game or browse the games by their category/popularity/etc.
* **High scores**
	* A view where the users can browse/search for high scores for different games.
* **Login**
* **Register**

#### Templates
* **Templates for each view**
* **Navigation bar (Views: all)**
* **High scores (Views: High scores, Game)**
* **Games list (Views: Browse games)**
* **Categories (Views: Browse games)**
* **Errors: 403, 404, 500 etc.**

#### Static
* **CSS style files**
* **Javascript files**
* **Pictures**

### 3.2. Functional Requirements Mandatory
#### Authentication
Users are able to register, login and logout to the game store. In registration users can select either player or developer.

User authentication is implemented using Django’s authentication methods. ([Django authentication](https://docs.djangoproject.com/en/1.10/topics/auth/))

Email validation is planned to be implemented as well. ([Django email validation](https://docs.djangoproject.com/en/1.10/topics/auth/))

#### Basic player functionalities

Player must be able to browse the games. The games can be listed at least by their name, popularity and category. Games have also a category by which they are arranged so that player can browse only games from desired category.

Player must be able to search for a specific game. Search results are listed in the same way as when browsing by category or listed property.

Player must be able to see a list of purchased games. This list is viewable from player’s personal account page.

Player must be able to buy a desired game. When player wishes to play a game, the purchase list is checked and if the game in question is not on the list and it is not free to play, game is not loaded to the player’s game view. This way the game store prevents the player from playing games that are not purchased.
Payment is handled by the course’s mockup payment service: [Niksula mockup payment](http://payments.webcourse.niksula.hut.fi/)

Payment service handles the transaction and returns a response of confirmed payment to the game store. The game store then adds the bought game to the player’s list of purchased games thus allowing the player to play the game.

#### Basic developer functionalities
Developer must be able to add a game to the game store. Developer does this by submitting a URL to the Javascript game.

Developer can add properties and information (such as price, category and description) to the game, and modify them later.

Developer must be able to view game sale statistics like how many times a game has been bought, time values of individual buyings and possibly also individual buyer information.
Additionally, developer could also be able to receive data about gaming statistics, like how many has played the game and how many hours. This is, however, a bonus feature that is not implemented by default.

#### Game/service interaction

The game/service interaction, such as score submitting, will be implemented using iframes and postMessages.

#### Quality of Work

Basic security will be achieved by proper testing and using Django’s internal modules such as authentication and CSRF middleware.

The web user interface will be tested by performing user tests. In addition, we will use unit tests to make sure that the site is crash-free. We will also focus on code readability (e.g. by following pep8 style guide) and modular code structure.

#### Non-functional requirements

Project plan is produced and it will give details of this project. History and development of this project can bee seen from Gitlab.

### 3.3. Functional Requirements Optional
#### Own game
Game will be implemented possibly using Quintus. It will be pretty simple game that is only giving perspective to how the game store works with actual games. ([Quintus](http://www.html5quintus.com/))
#### Mobile Friendly
This will be implemented using bootstrap’s responsive layout tools. ([Bootsrap layout](http://getbootstrap.com/css/))
#### 3rd party login

## 4. Resources

### 4.1. External Libraries
#### [Django](https://www.djangoproject.com/)
Used as a main framework.
#### [Bootstrap](http://getbootstrap.com/)
Used for styling and responsive layouts.
#### [jQuery](https://jquery.com/)
Used for functionalities that can not be implemented with Django.
#### [Quintus](http://www.html5quintus.com/)
Possibly used for a demo game development.

### 4.1. Tools
#### [Niksula](https://git.niksula.hut.fi/tiirat2/game-store/tree/master)
Git servervice for this project.
#### [Telegram](https://web.telegram.org/)
Used for fast communication between team members.
#### [PyCharm](https://www.jetbrains.com/pycharm/)
Code editor of our choice.
#### [Heroku](https://www.heroku.com/)
Cloud computing service that is used in this project.

## 5. Process and Time Schedule
We will start implementing the website in the week 1 of 2017 so we will have seven weeks to complete the project. However we might start to implement the javascript game before new year.

We will start by implementing the authentication and basic developer/player functionalities. After this we should include the game-website communication and a simple version of our own game. When all this is working, we will implement the load/save feature. We will also implement 3rd party login and social media sharing features. These can be implemented during development of the basic features if it seems that we have enough time to implement these extra features. RESTful API is probably one of the last thing we will implement if we have enough time.

### 5.1 Initial schedule:
**Weeks 1-2:** Authentication, basic developer/player functionalities
**Week 3:** Game-website communication, include a simple version of our own game
**Weeks 4-5:** Game-website communication, implement the final version of our own game, save/load feature, 3rd party login, social media sharing features
**Week 6:** Make sure that existing code works, RESTful API
**Week 7:** Make sure that everything works, final reporting

### 5.2 Working methods
We plan to implement the project in one week sprints. The team meets once a week for couple of hours in order to keep up good communication. During these meetings we make sure that every team member is aware of the state of other members, see if someone needs help with their tasks and decide the goal for the next week’s sprint.

We start the project by creating the base of the backend together. After first week we split the project into smaller segments and divide tasks to team members so that everyone gets an equal workload and is able to participate in every part of the project.

## 6. Testing
We will write unit tests with Python to test the functionality of the whole website. The plan is to start writing unit tests early on so that we can use the same tests also later. The tests can be used to create users and games to the game store and perform purchases and other actions automatically. The individual game(s) will be tested separately.

Additionally, we will test the website by hand by our selves and later on by persons outside our group. This way we can make the website functionality idiot proof and we can also test the intuitiveness of the user interface.
### 6.1. User Stories

In this section is listed some user stories that help us to define some functional requirements and plan test cases to verify that the requirements are met at the end of the project.

1. As a developer, I want to register as a developer to the webshop and login to be able to sell games.
	* Register to the webshop filling in personal information or using facebook/google/etc. to authenticate, and login to the webshop.
	* Tests
		* Register with personal information
		* Register with 3rd party authentication
		* Register existing developer with personal info
		* Register existing developer with 3rd party authentication
		* Register with invalid information
		* Login with credentials
		* Login with 3rd party authentication
		* Login with invalid credentials
		* Login with unauthenticated 3rd party authentication

2. As a developer, I want to add a game I designed to be purchased and played
Add a game to the developer’s hosted games by providing URL link to the game
	* Tests
		* Add a game
		* Add an existing game
		* Add game with invalid URL

3. As a developer, I want to manage my games to see selling statistics and remove old games.
	* View selling information of all games hosted by the developer, see individual purchases and their time data, delete existing game.
	* Tests
		* See selling informations
		* Delete game
		* Delete last game

4. As a player, I want to register and login to the webshop to be able to play the games
	* Registering with personal information or 3rd party authentication
	* Tests
		* Register with personal information
		* Register with 3rd party authentication
		* Register existing player with personal info
		* Register existing player with 3rd party authentication
		* Register with invalid personal information
		* Login with credentials
		* Login with 3rd party authentication
		* Login with invalid credentials
		* Login with unauthenticated 3rd party authentication

5. As a player, I want to browse the games and search a desired game to find a suitable game to purchase
	* Browsing games listed by their name, category, price, searching by the game name
	* Tests
		* Browse by name
		* … by category
		* … by price
		* Search by name
		* Search with invalid name

6. As a player, I want to purchase a game to be able to play it
	* Purchase the game using payment mockup service
	* Tests
		* Finalize the payment
		* Cancel the payment in different states

7. As a player, I want to play a game I have purchased
	* Open a purchased game and play it
	* Tests
		* Play purchased game
		* Try playing unpurchased game

8. As a player, I want to submit my score to global score board to be able to bask in the glory.
	* After playing the game, submit scores, see global game scores, see own scores among the others
	* Tests
		* Submit the score
		* View other scores
		* Submit the score before the game ends
		* Submit high score
		* Submit zero score
		* Submit more than the amount of scores in the top score board


## 7. Risk Analysis
In this section we address some possible risks the project can face and also plans to minimize the effect to the project.

* **A team member drops the course.**
	* Try to convince the team member to continue with the course
	* Arrange hackathon-like sessions to raise coding motivation
	* If team member is lost, rethink the project goals and possibly drop out optional functional requirements
* **Project deadlines are not met.**
May be due to several reasons
	* One or more team members lack some important skills
		* Offer support and rethink task dividing
	* Lack of communication
		* Add communication between team members, arrange face-to-face meetings at least once a week.
	* Deadlines are unreasonable
	* Rethink team capabilities
	* Lack of motivation or prioritization issues
	* Face-to-face meetings and hackathon get-togethers.

## 8. Project report
In this section we look into the project and what was the outcome. We also discuss about points we would give ourselves and features we managed to implement.

The final project is hosted in Heroku at http://nilkan-mikrosorto.herokuapp.com/

### 8.1. Feature evaluation, functional requirements
#### Authentication (200p)
Authentication supports register/login/logout and has email validation using a real SMTP server (Google mail server).

Mail server credentials are stored in Heroku config vars but can be also imported in mailconfig.py file if the gamestore is desired to run locally.
#### Basic player functionalities (300p)
Player can buy games, play games, search games with names or category. Player cannot play games he/she has not purchased.
#### Basic developer functionalities (200p):
Developer can see add and edit own games and see sales statics. They can only add games to their own inventory.
#### Game/service interaction (200p):
Games have highscores and leader boards. Also save and load feature. Iframe scales based on the games settings.
#### Quality of Work (90p)
The code structure is modular and we followed pep8 style guide in our Python code. The code is also mostly commented. We have widely used the frameworks (django, jQuery, Bootstrap) to our advantage. We tested all functionality with user tests after implementing each feature.
#### Non-functional requirements (200p)
Project plan was well formed and informative. It is hard to say about the demo yet.
 Team worked well together and everyone learned new things. We programed together and separately and saw each other many times during the project work. We started early but still the project was a little bit final deadline oriented.

### Feature evaluation, optional requirements
#### Save/load and resolution feature (100p)
Our game supports save, load and resolution features when playing the game.
#### Own game (100p)
We made our own game. In this game you are a red box which tries to avoid the blue box by jumping and moving. To get point player must go from another wall to another.
The game supports highscore, save and load features and also scales the iFrame with its own width ang height.

[Own Game](http://www.norri.fi/testi/peli.html) can be found here on Noora' site. The code is also located to the root of the project in file own_game.html.
#### RESTful API (100p)
With restfull api you can fetch data from our database. It supports restfull applications.
You can for example fetch high scores for specific games with it.
#### Mobile Friendly (50p)
We used bootstrap to get more mobile friendly and scaling application. Everything including the iFrame scales.
#### Social media sharing (50p)
You can share the game your playing to Facebook. It also shares some metadata like the description of the game.

### 8.2. Written work evaluation
Overall project went well. The team worked great together and we all worked hard towards the goal. Mostly we were able to solve problems quickly.
We had most problems with third party login and that is why we decided to skip it. We also had some problems
with different browser because save and load did not work properly in all of them.

We managed to follow our plan mostly. All did not work as we planned but we were able to improvise. For example we
dropped the use of quintus in our own game and made the game purely with javascript and jQuery for posting messages.

### 8.3. Team's workload
Mostly everyone did everything. We met frequently and divided new task for everyone.
This worked until the time was getting limited so in order to save time everyone did what they had learned best.
Some of us did more backend and some of us more frontend or features they were familiar with.

We programmed estimated 8 hours per person per week.

### 8.4. Instructions

Site is hosted on Heroku at http://nilkan-mikrosorto.herokuapp.com/

All users must login to the page as a developer or player using registration form. The account will be validated using real email verification, so the user must supply a real email address. After validation the user can log in.

For players:
Games can be browsed through the home page of our gamestore. The games can be bought from the games individual pages. After buying the game the player can play it. Free games can be played without buying the game. Players can save the game and load it afterwards. Multiple save games are not supported, and the latest save will be always loaded.

For developers:
Games can be added through the account page. There you can also see sales statistics for your own games and edit game information. Note that if the game price is put to 0, the game cannot be bought but it can be player by the users. The reason for this is that the developers can now put their games free to play for e.g. a month so that the players cannot buy it when it is free to play. Afterwards you can put the price back on and the players cannot play the game anymore and must buy it to play it.

RESTful:
RESTful api supports fetching game, high score and sales statistic data. The returned value is JSON. There are more information about GET parameters and return values at /rest/ info page.

### 8.5. Known bugs

We did not implement any separate error handling for forms. It shows only errorcode pages.
