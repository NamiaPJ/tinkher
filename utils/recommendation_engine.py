def generate_recommendations(leafy, milk, sunlight, meat):
    recommendations = []

    if leafy < 3:
        recommendations.append("Increase leafy vegetables for iron.")

    if milk < 3:
        recommendations.append("Add dairy products for calcium.")

    if sunlight < 15:
        recommendations.append("Get at least 20 minutes sunlight daily.")

    if meat < 2:
        recommendations.append("Include protein sources like eggs/meat.")

    if not recommendations:
        recommendations.append("Your nutrition looks balanced. Keep it up!")

    return recommendations