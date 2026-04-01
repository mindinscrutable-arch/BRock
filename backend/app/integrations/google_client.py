import requests
import time
from app.core.config import settings

def invoke_target_model(target_model: str, google_schema: dict) -> dict:
    """
    Pushes the newly translated Google Vertex schema to the Gemini API Endpoint natively!
    """
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:generateContent?key={settings.GEMINI_API_KEY}"
    
    start_time = time.time()
    
    try:
        response = requests.post(api_url, json=google_schema, headers={'Content-Type': 'application/json'})
        response_data = response.json()
        latency = int((time.time() - start_time) * 1000)
        
        # Check for API error
        if "error" in response_data:
            print("Google Gemini API error:", response_data["error"]["message"])
            return {
                "text": f"Google Gemini API error: {response_data['error']['message']}",
                "latency_ms": 0,
                "tokens": 0
            }
            
        output_text = response_data['candidates'][0]['content']['parts'][0]['text']
        output_tokens = response_data.get('usageMetadata', {}).get('candidatesTokenCount', len(output_text)//4)
        
        return {
            "text": output_text,
            "latency_ms": latency,
            "tokens": output_tokens
        }
    except Exception as e:
        print("Google Model execution error:", e)
        return {
            "text": f"Failed to reach Google APIs: {e}",
            "latency_ms": 0,
            "tokens": 0
        }
