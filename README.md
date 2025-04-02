# getweatherapp
Python script to get the weather from cities and inputs them in a csv file " openweather_data.csv". If file does not exist create it.

Tools:
Installed python dot env 
Installed pip 25.01
Installed Python 3.13.2
CSV file opener (Libre Calc in this case)

Code currently set for the following cities: "Tokyo, JP", "Chicago, US", "Bremen, US", "London, UK" but can be modified on Line 14. 
.env should utilized gitignore (not shown but future state) to ensure api key is only saved locally.  

Follow info will show for cities:
Temp in Celsius and Frenheit
Humidity 
Wind speed
Comfort temp

All info will be saved in openweather_data.csv

Future state using Google Sheet, Google Cloud and potentially app scrit? 
