import os
import requests
import csv
from datetime import datetime
from typing import List, Dict, Optional, Union
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenWeather API key from .env file
API_KEY = os.getenv("openweather")
# Cities for weather data... base on the front end version of this https://openweathermap.org/find.. maybe add an "error" when a valid country code is not found. 
cities = ["Tokyo, JP", "Chicago, US", "Bremen, US", "London, UK"]

def get_openweather_data(city: str) -> Optional[Dict]:
    # API call to OpenWeatherMap to get current weather data for the specified city
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        
        # Check for rate limiting
        if response.status_code == 429:
            print("rate limited, check api using postman")
            return None
            
        response.raise_for_status()
        data = response.json()
        
        # check response data
        if not isinstance(data, dict) or "cod" not in data:
            print(f"Invalid format for {city}. Check country code and city")
            return None
            
        return data
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch OpenWeather data for {city}: {str(e)}")
        return None

def calculate_comfort_index(temp_celsius: float, humidity: float, wind_speed: float) -> float:
    # Calculate comfort index based on temperature, humidity, and wind speed
    try:
        # checking inpute types
        if not all(isinstance(x, (int, float)) for x in [temp_celsius, humidity, wind_speed]):
            raise ValueError("All inputs must be numeric values")
            
        # checking input range
        if not -273.15 <= temp_celsius <= 100:  # Reasonable temperature range
            raise ValueError("Temperature out of  range")
        if not 0 <= humidity <= 100:
            raise ValueError("Humidity must be between 0 - 100")
        if not 0 <= wind_speed:
            raise ValueError("Wind speed cannot be -x")
        
        # Normalize temperature between 15-30°C (comfortable range)
        temp_normalized = max(0, min(1, (temp_celsius - 15) / (30 - 15)))
        
        # Normalize humidity (ideal range 30-60%)
        humidity_normalized = max(0, min(1, 1 - abs(humidity - 45) / 45))
        
        # Normalize wind speed (ideal range 0-5 m/s)
        wind_normalized = max(0, min(1, 1 - min(wind_speed, 10) / 10))
        
        # Weighted comfort index
        comfort_index = (
            0.4 * temp_normalized +
            0.3 * humidity_normalized +
            0.3 * wind_normalized
        )
        return round(comfort_index, 2)
    except Exception as e:
        print(f"Error calculating comfort index: {str(e)}")
        return 0.0

def save_to_csv(openweather_data: List[List[Union[str, float]]]) -> bool:
    # Check if "openweather_data.csv" exists. 
    filename = "openweather_data.csv"
    try:
        file_exists = os.path.exists(filename)
        #creates the file if it doesn't exist and includes the columns 
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow([
                    'Timestamp',
                    'City',
                    'Temperature (C)',
                    'Temperature (F)',
                    'Humidity (%)',
                    'Wind Speed (m/s)',
                    'Comfort Index'
                ])
            writer.writerows(openweather_data)
        return True
    except IOError as e:
        print(f"Error saving to openweather_data.csv: {str(e)}")
        return False

def main():
    try:
        if not API_KEY:
            raise ValueError("OpenWeather api is not found in .env.")

        openweather_data = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for city in cities:
            data = get_openweather_data(city)
            if data and data.get("cod") == 200:
                try:
                    city_name = data["name"]
                    temp_celsius = float(data["main"]["temp"])
                    temp_fahrenheit = round(temp_celsius * 9/5 + 32, 2)
                    humidity = float(data["main"]["humidity"])
                    wind_speed = float(data["wind"]["speed"])
                    
                    comfort_index = calculate_comfort_index(temp_celsius, humidity, wind_speed)
                    
                    openweather_data.append([
                        timestamp,
                        city_name,
                        temp_celsius,
                        temp_fahrenheit,
                        humidity,
                        wind_speed,
                        comfort_index
                    ])
#perhaps add a log? 
                except (KeyError, ValueError) as e:
                    print(f"Data collection error{city}: {str(e)}")
                    continue

        if not openweather_data:
            print("Data collection error; not found")
            return

        # Save data to CSV
        if save_to_csv(openweather_data):
            print("Data saved to openweather_data.csv")
        else:
            print("Failed to save data in openweather_data.csv")

        # Print the collected data
        for data in openweather_data:
            print(f"City: {data[1]}")
            print(f"Temperature: {data[2]}°C / {data[3]}°F")
            print(f"Humidity: {data[4]}%")
            print(f"Wind Speed: {data[5]} m/s")
            print(f"Comfort Index: {data[6]}")
            print("-" * 40)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
