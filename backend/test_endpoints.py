import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("Starting endpoint validation tests...")
print("-" * 50)

# ----------------------------------------
# TEST 1: The /translate Endpoint
# ----------------------------------------
print("Executing [POST /api/v1/translate/]")
translate_payload = {
    "source_model": "gpt-4",
    "source_payload": {
        "system": "You are a helpful assistant.",
        "messages": [
            {"role": "user", "content": "What is the fastest way to learn Python?"}
        ],
        "is_json_mode": False
    }
}

response = client.post("/api/v1/translate/", json=translate_payload)
print(f"Status Code: {response.status_code}")
try:
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(response.text)

print("-" * 50)

# ----------------------------------------
# TEST 2: The /report Endpoint
# ----------------------------------------
print("Executing [POST /api/v1/report/save]")
report_payload = {
    "source_model": "gpt-4",
    "destination_model": "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "metrics": {
        "source": {"latency_ms": 1200, "tokens": 150},
        "bedrock": {"latency_ms": 850, "tokens": 140}
    },
    "timestamp": "2026-04-01T12:00:00Z"
}

response = client.post("/api/v1/report/save", json=report_payload)
print(f"Status Code: {response.status_code}")
try:
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(response.text)

print("-" * 50)
print("Testing complete. If both status codes are 200, the endpoints are perfectly clean!")
