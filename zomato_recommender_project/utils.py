def explain_recommendation(row):
    details = []
    if row['Primary Cuisine']:
        details.append(f"{row['Primary Cuisine'].title()} cuisine")
    if row['Price Bucket']:
        details.append(f"{row['Price Bucket'].lower()} budget")
    if 'Has Online delivery' in row and row['Has Online delivery'] == 1:
        details.append("online delivery available")
    details.append(f"{row['Aggregate rating']}/5 rating from {int(row['Votes'])} votes")
    return "Recommended because it matches: " + ", ".join(details) + "."

def get_map_link(city, locality):
    query = f"{locality}, {city}".replace(" ", "+")
    return f"https://www.google.com/maps/search/?api=1&query={query}"