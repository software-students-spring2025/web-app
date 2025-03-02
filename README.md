# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

Our product aims to provide information and purchase functions to consumers who would like to make a purchase at our bakery, while also increasing profits with intentional marketing through its design.


## User stories

- As a user, I want to be able to view item information, so that I know what the item tastes like.
- As a user, I want to be able to view common allergens, so that I can make safe purchases.
- As a user, I want to be able to select items and place them in my shopping cart, so that I can collect the goods that I want to buy.
- As a user, I want to be able to search for specific items using keywords, so that I can find what I am looking for efficiently.
- As a user, I want to be able to view my shopping cart, so that I see what items I have currently listed.
- As a user, I want to be able to delete order history, so that I can keep my orders secret so I can surprise my friends with baked goods without them knowing.
- As a user, I want to be able to view my order history, so that I can keep track of the purchases I made with this bakery.
- As a user, I want to be able to contact the bakery, so that I can file complaints.
- As a user, I want to be able to view what the item looks like, so I know what to expect.
- As a user, I want to be able to remove items from my shopping cart, so I don’t have to buy items I changed my mind about.
- As a user, I want to be able to view items by category, so that I have an easier time searching through the menu.
- As a user, I want to be able to specify whether my order is for pickup or delivery, so that I can use the appropriate delivery method.
- As a user, I want to be able to enter my credit card information, so I can pay directly through the website.
- As a user, I want to see the subtotal in the cart, so that I know how much my order is as I add items.
- As a user, I want to be able to get lists of what items the bakery has, so I can see what items are available
- As a user, I want to indicate the name on the purchase, so the bakery knows who it is for.
- As a user, I want to view calorie information, so I can keep track of my daily calories.
- As a user, I want to be able to enter a shipping address, so the bakery can ship my goods to the correct location.



## Steps necessary to run the software

### Mac

1. Set up virtual environment


```
python3 -m venv venv
```


2. Activate environment


```
source venv/bin/activate
```


3. Install dependencies


```
pip install -r requirements.txt
```


4. Enter app

```
cd app/
```

5. Set Flask app environment variable


```
export FLASK_APP=app.py

```
6. Start MongoDB

```
brew install mongodb-community@6.0
brew services start mongodb-community@6.0
```

7. Set Mongo URI

```
export MONGO_URI='mongodb://localhost:27017/anatidelicious'
```

8. Run App

```
flask run
```

9. Open page at http://127.0.0.1:5000

## Task boards

[Task Board Sprint 1 Link](https://github.com/orgs/software-students-spring2025/projects/10/)

[Task Board Sprint 2 Link](https://github.com/orgs/software-students-spring2025/projects/73/)