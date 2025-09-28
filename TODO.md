AllerSafe App Concept (Next.js)
Core Idea
AllerSafe helps people with dietary restrictions or allergies quickly find safe alternatives to foods by scanning products or meals and returning verified alternatives—either groceries or restaurants.

Problem & Target Users
Problem:
 Consumers with food allergies or dietary restrictions struggle to confidently find safe alternatives when trying new foods.
Target Users (ICP):
Individuals with dietary restrictions:


Allergies (peanut, dairy, shellfish, etc.)


Halal


Vegan


Vegetarian


Pescatarian


Gluten-free
Etc.


Businesses catering to dietary-restricted consumers (potential revenue stream).



Solution Overview
Product Scanning (Groceries)


Take a photo of a grocery item.


System identifies the product and finds safe alternative brands.


Results show images + links to online stores (Amazon, Walmart, etc.).


Restaurant Scanning (Dining Out)


Take a photo of a dish or food item.


System identifies the food type.


Shows safe restaurant alternatives nearby on a map.


Each restaurant includes safety details, menu highlights, and reviews.


Personalized Recommendations


A profile stores the user’s dietary restrictions and allergies (checkbox format showing possible allergens, dietary restrictions, etc.).


Results are filtered automatically based on these preferences.



UI/UX Structure
1. Navigation
Top Tabs:


Groceries


Restaurants


Bottom Tabs:


Home (default: scan area)


Profile (manage allergies/dietary restrictions)



2. Home Screen (default)
Large green scan button (centered).


Camera icon (photo scan).


Action changes based on selected top tab:


If Groceries tab → scan grocery item for grocery alternatives.


If Restaurants tab → scan meal for restaurant alternatives.



3. Groceries Flow
User scans a grocery item.


App detects product → shows:


Image of original product.


Safe alternatives (same category, filtered by allergies/diet).


Store links (Amazon, Walmart, etc.).



4. Restaurants Flow
User scans a meal.


App detects dish → shows:


Map of nearby restaurants with alternatives.


Each restaurant card:


Distance + directions.


Menu safety info (allergen guarantees, certifications).


Ratings & reviews.



5. Profile Tab
Checklist of dietary restrictions:


Allergens (nuts, shellfish, dairy, etc.).


Lifestyle choices (Halal, Vegan, Vegetarian, Gluten-free).


User checks what applies → app automatically filters results.




Example User Journey
User opens AllerSafe → sees green scan button.
User fills out allergy profile if not already done.


User selects Groceries tab → scans peanut butter jar.


App detects peanuts (allergy).


Suggests safe alternatives (sunflower seed butter, soy butter).


Shows purchase links.


Later, user switches to Restaurants tab → scans picture of ramen.


App detects gluten-free on profile.
App finds local ramen restaurants with gluten-free options.


Displays them on a map with ratings & safety tags.



This gives you a clean blueprint:
Navigation (top & bottom tabs).


Central scan feature.


Two flows (Groceries vs Restaurants).


Profile customization.

