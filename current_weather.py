import requests
from pprint import pprint
import os

url = 'http://api.openweathermap.org/data/2.5/weather'
key = os.environ.get('WEATHER_KEY')
print(key) # not required - only for verification during development

def main():
    location = get_location()
    weather_data, error = get_current_weather(location, key)
    if error:
        print('Sorry, could not get the weather.')
    else:
        current_temp = get_temp(weather_data)
        print(f'The current temperature is {current_temp}F')

#  checking to make sure that the city and the country is valid
def get_location():
    city, country = '', ''
    while len(city) == 0:
        city = input('Enter the name of the city: ').strip()
    
    while len(country) !=2 or not country.isalpha():
        country = input('Enter the 2-letter country code: ')
    
    location = f'{city}, {country}'
    return location

#  using the query string to keep our code cleaner, more readable
def get_current_weather(location, key):
    try:
        query = {'q': location, 'units': 'imperial', 'appid': key}
        response = requests.get(url, params=query)
        response.raise_for_status() # Raise exception for 400/500 errors
        data = response.json() # This may error too, if response is not JSON
        return data, None # Returns tuple of the data and the exception which is None 
    except Exception as ex:
        print(ex)
        print(response.text) # added for debugging
        # If there is a problem, return a tuple of data and exception.
        # But in this case the data will be None and exception will have a value
        return None, ex 
        

def get_temp(weather_data):
    try:
        temp = weather_data['main']['temp']
        return temp
    except KeyError:
        print('This data is not in the format expected')
        return 'Unknown'

if __name__ == "__main__":
    main()    

# http://api.openweathermap.org/data/2.5/forecast?q=minneapolis,mn,us&units=imperial&appid=babe8b7753a71d315181b18dae55b46f

