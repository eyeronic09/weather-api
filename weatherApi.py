import requests
import redis
import json

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Function to fetch weather data
def get_weather(city):
    cache_key = f"weather:{city.lower()}"
    
    # Step 1: Check if data exists in Redis
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("Fetching data from cache...")
        return json.loads(cached_data)
    
    # Step 2: Fetch data from the weather API
    print("Fetching data from API...")
    api_key = "your_api_key_here"  # Replace with your Weather API key
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = response.json()
        
        # Step 3: Save the data to Redis with a TTL (e.g., 1 hour)
        redis_client.setex(cache_key, 3600, json.dumps(weather_data))
        return weather_data
    else:
        return {"error": "Unable to fetch weather data"}

# Example Usage
city_name = "London"
weather_info = get_weather(city_name)
print(weather_info)
