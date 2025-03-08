from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

@app.route('/generate-menu', methods=['POST'])
def generate_menu():
    try:
        data = request.json  # Get JSON data from frontend

        # Validate input fields
        vendor_name = data.get('vendor_name', 'Unknown Vendor')
        cuisine_type = data.get('cuisine_type', 'Various Cuisines')
        popular_dishes = ", ".join(data.get('popular_dishes', [])) or "No dishes provided"
        price_range = data.get('price_range', 'Affordable')
        add_ons = ", ".join(data.get('add_ons', [])) or "No add-ons"
        dietary_preferences = data.get('dietary_preferences', 'No specific preferences')
        print("data_fetched")
        # Create AI prompt
        prompt = f"""
        Generate a visually appealing menu for a street food vendor:
        Vendor Name: {vendor_name}
        Cuisine Type: {cuisine_type}
        Popular Dishes: {popular_dishes}
        Price Range: {price_range}
        Add-ons: {add_ons}
        Dietary Preferences: {dietary_preferences}
        
        Format the menu like a professional restaurant menu with catchy names, dish descriptions, and pricing.
        """

        # Call DeepSeek-R1 via Ollama
        response = ollama.chat(model='deepseek-r1', messages=[{'role': 'user', 'content': prompt}])

        # Check response
        if 'message' in response:
            ai_generated_menu = response['message']['content']
            return jsonify({'menu': ai_generated_menu})
        else:
            return jsonify({'error': 'Failed to generate menu'}), 500

    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
