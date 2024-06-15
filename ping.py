import requests
import time
import random
from configparser import ConfigParser

# Configs
config = ConfigParser()
config.read('config.ini')
supabase_apikey = config.get('supabase', 'api_key')
supabase_url = config.get('supabase', 'url')
ntfy_url = config.get('ntfy', 'url')
 
# Define the headers for the GET request
headers = {
    'apikey': supabase_apikey,
    'Authorization': supabase_apikey,
}

# Delay range in seconds (1 second to 23 hours)
min_delay = 1
max_delay = 23 * 3600

def calculate_random_delay(min_seconds: int, max_seconds: int) -> int:
    return random.randint(min_seconds, max_seconds)

def format_delay(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:  # Include seconds if no hours/minutes
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    if len(parts) > 1:
        return ', '.join(parts[:-1]) + f", and {parts[-1]}"
    else:
        return parts[0]

def notify_failure(message: str):
    requests.post(ntfy_url, data=message, headers={
        "Title": "Supabase keep-alive failed",
        "Tags": "rotating_light"
    })

def make_get_request(url: str, headers: dict):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print('Failed:', response.status_code, response.text)
        notify_failure(response.text)

def main():
    # Calculate and format the random delay
    delay = calculate_random_delay(min_delay, max_delay)
    pretty_delay = format_delay(delay)
    print(f'Waiting for {pretty_delay} before making the request...')

    # Wait for the calculated delay
    time.sleep(delay)

    # Make the GET request
    make_get_request(supabase_url, headers)

if __name__ == '__main__':
    main()
