# Function to read menu from a text file
def read_menu_from_file(file_path):
    menu = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Split each line into dish name and ingredients
            dish, ingredients = line.strip().split(':')
            menu.append({'name': dish.strip(), 'ingredients': ingredients.strip()})
    return menu

# Function to prompt user for preferences and restrictions
def get_user_input():
    dietary_preferences = input("Enter your dietary preferences (e.g., vegan, vegetarian, spicy, gluten-free): ")
    dietary_restrictions = input("Enter any dietary restrictions (e.g., nuts, dairy, gluten): ")
    sentiment = input("What is your current food sentiment (e.g., craving something spicy, sweet, etc.)? ")
    return dietary_preferences, dietary_restrictions, sentiment

# Function to recommend dishes based on user input
def recommend_dishes(menu, preferences, restrictions, sentiment):
    recommendations = []
    
    for item in menu:
        # Match preferences in ingredients or dish name
        if preferences.lower() in item['ingredients'].lower() or preferences.lower() in item['name'].lower():
            # Exclude dishes that contain restricted ingredients
            if not any(restriction.lower() in item['ingredients'].lower() for restriction in restrictions.split(',')):
                recommendations.append(item)
    
    # Filter by sentiment if specified
    if 'spicy' in sentiment.lower():
        recommendations = [dish for dish in recommendations if 'spicy' in dish['name'].lower() or 'spicy' in dish['ingredients'].lower()]
    
    return recommendations

# Main function to run the program
def main():
    # Get the path to the menu text file
    file_path = input("Enter the path to the menu text file: ")
    
    # Read the menu from the file
    menu = read_menu_from_file(file_path)
    
    # Get user preferences and restrictions
    preferences, restrictions, sentiment = get_user_input()
    
    # Get recommendations
    recommendations = recommend_dishes(menu, preferences, restrictions, sentiment)
    
    # Print recommendations
    if recommendations:
        print("\nHere are the recommended dishes for you:")
        for dish in recommendations:
            print(f"- {dish['name']}: {dish['ingredients']}")
    else:
        print("Sorry, no recommendations match your preferences and restrictions.")

# Run the app
if __name__ == "__main__":
    main()
