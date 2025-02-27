## Idea
Our app allows users to guess the prices of common grocery items, compare their guesses with actual prices, and track their accuracy. It also helps users discover, review, and search for local grocery stores based on factors like price, diversity, and customer service. The app combines fun with practicality, helping users improve their shopping skills and find the best places to shop.

## Features
- Grocery Price Challenge
    - Users can participate in the price guessing challenge for common grocery items (how much a loaf of bread costs, how much eggs are).
    - Users can log their guesses, track their accuracy, and see average prices for items based on user submissions.
- Shop Listings
    - Users can list and search for grocery stores or markets in their area.
    - Each listing can include key details such as location, hours, website, and contact info.
- Shop Reviews
    - Users can leave reviews for shops based on:
    - Price Range: How affordable are the products?
    - Diversity: How well-stocked is the store with various food items, especially for different diets (e.g., vegan, gluten-free)?
    - Atmosphere: How pleasant is the shopping experience?
    - Each review can include a star rating and text feedback.
- Search & Filter
    - Users can search for grocery stores based on location, rating, price range, or other factors. 
    - Filters for specific dietary needs or types of grocery stores (organic, international, budget-friendly) 
- Price Comparison
    - After participating in price guesses, users can compare the real prices they guessed with the ones submitted by others.
    - The app could display the price trends over time for popular items in different regions or shops.
- Community Contributions
    - Users can suggest new stores, upload pictures, or report missing details to make the app more accurate and helpful.
    - Encourage users to contribute by adding a reward system (badges for frequent contributors).

## Sprints
### Sprint 1
Front-End Team:
- Figma Mockups
    - Design the basic layout and UI/UX for the web app. Create mockups for at least 6 screens:
        - Home Page (with quick access to store listings and price guess challenges)
        - Store Listing Page (showing stores with reviews, search/filter options)
        - Store Detail Page (for viewing reviews and more store details)
        - Price Guess Challenge Page (where users can participate in guessing the prices of items)
        - Review Submission Page (for users to submit their reviews for stores)
        - Profile Page (to view and manage user profile, past reviews, and challenge results)
- HTML/CSS Structure
    - Start implementing the basic HTML structure for the app based on the Figma mockups.
    - Focus on mobile-first design, keeping the interface simple and user-friendly for a smaller screen.
    - Use CSS (or a CSS framework like Bootstrap) to ensure the pages are styled according to the mockups.
- Front-End Framework Setup
    - Set up a front-end framework like React (or basic JavaScript if preferred), focusing on the following pages:
        - Store listing and search/filter functionality
        - Displaying individual store reviews
        - Price guessing game interface
Back-End / Database Team
- Backend Setup (Flask & PyMongo)
    - Set up the Flask backend with routing for basic CRUD operations 
        - Users (authentication and registration)
        - Stores (create, read, update, delete stores)
        - Reviews (create and read reviews for stores)
    - Set up MongoDB using pymongo to store and retrieve data for stores and reviews.
- .env File Setup
    - Set up a .env file to securely store database credentials 
    - Include an env.example file with dummy data to guide the team.

FullStack
- Basic Authentication
     - Implement basic user authentication (login and registration) using flask-login for user sessions.
- Initial Data Population
    - Populate the database with a few dummy stores and reviews so that the front-end team has data to display when they begin integrating.

### Sprint 2
Front-End Team:
- UI Integration
    - Connect the front-end with the back-end:
        - Implement fetching and displaying store data from the database (store listings, individual store details, reviews).
        - Display price guessing results and allow users to submit their guesses.
        - Connect the review submission form to the backend, allowing users to submit reviews for stores.
- Advanced Search & Filter
    - Implement advanced search and filter options for stores:
        - Filter stores by price range, type (organic, international, etc), and user ratings.
        - Display relevant search results  on the Store Listing Page.
- UI Enhancements & Finalize Design
    - Refine the UI/UX design to match the mockups.
    - Make sure the app is optimized for mobile view
- User Profile Page
    - Build the User Profile Page to allow users to see their past reviews, price guesses, and account details.

Back-End/Database Team:
- Complete CRUD Operations
    - Implement full CRUD functionality for stores and reviews (users should be able to update and delete reviews, add new stores).
    - Implement functionality to store, retrieve, and compare price guesses for grocery items.
    - Implement logic to store and track the accuracy of guesses.
- APIs for Front-End
    - Build the necessary APIs for front-end interaction:
        - API for fetching stores, reviews, and price guesses.
        - API for submitting reviews, price guesses, and user authentication.
    - Ensure proper validation for user input and handle error messages.
- Testing & Debugging
    - Begin unit testing the backend routes and database operations to ensure data integrity.
    - Ensure API calls are properly integrated and return the correct data.

FullStack
- End-to-End Integration
    - Connect the front-end with all the back-end features, including user authentication, submitting reviews, guessing prices, and viewing store details.
- Bug Fixes & Refinements
    - Ensure smooth functionality of the app (no broken links, slow-loading pages, etc.).
    - Refine the overall user experience based on feedback from initial testing.
- User Feedback
    - Prepare for stakeholder meetings by testing the app with a small group of users to gather feedback.
    - Adjust features based on feedback before the final demo.

### Database Structure
- Users:
    - user_id (unique identifier)
    - username
    - password_hash
    - email
- Stores:
    - store_id (unique identifier)
    - store_name
    - location
    - contact_info
    - store_type (e.g., organic, international, budget)
    - price_range (low, medium, high)
- Reviews:
    - review_id (unique identifier)
    - user_id (foreign key to Users)
    - store_id (foreign key to Stores)
    - rating (1-5 stars)
    - price_range_rating
    - diversity_rating
    - atmosphere_rating
    - review_text
    - date_posted
- Price Guesses:
    - guess_id (unique identifier)
    - user_id (foreign key to Users)
    - item_name
    - guessed_price
    - actual_price (later updated after user submission)
    - date_posted
