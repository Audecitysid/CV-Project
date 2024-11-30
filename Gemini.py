import requests
import json

# Your API key
API_KEY = "AIzaSyB9Ckkd0gffScQWXsl0D2r8vhB0mAP4x2U"

# Function to call Gemini API
def get_gemini_response(prompt_text):
    """
    Call the Gemini API with the given prompt text and return the text response.

    Args:
        prompt_text (str): The text prompt for the API.

    Returns:
        str: The text response from the API.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt_text
                    }
                ]
            }
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()
        try:
            # Extracting the text response
            text_response = result["candidates"][0]["content"]["parts"][0]["text"]
            return text_response.strip()
        except (KeyError, IndexError):
            return "Error: Unexpected response format."
    else:
        return f"Error: {response.status_code}, {response.text}"


# Example usage
if __name__ == "__main__":

    
    prompt = "What is the weather like today?"
    response_text = get_gemini_response(prompt)
    print("Gemini's Response:", response_text)
