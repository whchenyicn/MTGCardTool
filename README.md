#MTG Card Tool

Team ID: 7555  
Team Name: Codewalkers  
Chen Yilin  
Yeo Yong Xuan  

Proposed Level of Achievement: Apollo 11

Motivation
As a long time player of collectible card game Magic the Gathering, acquiring all the necessary cards for a deck has always been the most tedious part. Some cards are only available in select stores, prices change quickly depending on demand and identical cards often have different prices across different stores. The more expensive cards often have price differences in the tens of dollars. Considering there are 100 cards in a deck, carefully choosing which stores to buy from could save players a lot of money.

Aim
Rather than spending hours manually comparing prices across different stores, we hope to provide a way for players to quickly compare card prices on a single platform, allowing them to make better decisions of their purchases. We plan to do this by webscraping the online stores of every MTG shop in Singapore and displaying consolidated data on a website

User Stories
As a user, I want to be able to quickly find the best prices for the card I want
As a user, I want to quickly find which version is available at which store
As a user, I want to be able to search for the cards I want


Project Scope
Setup
1. Frontend Development
1.1. User Interface Prototype
We designed a simple interface to see the cards available from different stores. The card price showed is the cheapest one with the same name.
After clicking on view details, user will then be able to see the same card available from different stores at different prices and conditions.

2. Backend Development
We first need to scrape the data from the various MTG websites using BeautifulSoup. The card data will be retrieved and stored in csv files together with its price and other information.
The scraped data are stored in csv files that needs to be processed in the backend. We currently converted the csv file to json format and uploaded the json file directly to the webpage for simplicity and testing
Later on we will use Flask joined with Neon as the database to host all this data. This will help with efficiency since the amount of card data will be very large.

Core - Main Features

Dashboard
The dashboard is the main screen that is displayed to users. There are currently 2 features for users on the dashboard.

1. Searching for Cards
Users will be able to search for the card they want quickly with the search bar. They can get information of the card they want quickly and see which store has it for the cheapest.

2. Price Comparison across stores
Users will be able to see and compare the prices of the same card across different stores through the view details function. This will help them to get the information they want quickly and effectively.

3. Card Information Comparison across stores
Users will be able to compare the conditions and art style of each card across different stores quickly using the view details function.
