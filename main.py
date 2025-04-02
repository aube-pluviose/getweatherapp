import os
import requests
import csv
from datetime import datetime
from typing import List, Dict, Optional, Union
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenWeatherMap API key from .env file
API_KEY = os.getenv("openweather")
