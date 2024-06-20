from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json

# Define Constants
LOGIN_URL = 'https://www.strava.com/login'
CLUB_URL = 'https://www.strava.com/clubs/1157118'
CREDS_FILE = 'strava_creds.json'

# Create a new instance of the Chrome driver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36' # Chrome User Agent
chrome_options.add_argument(f"--user-agent={user_agent}")
driver = webdriver.Chrome(service=Service(), options=chrome_options)


# Get strava email and password
def get_strava_creds():
    with open(CREDS_FILE, 'r') as creds_file:
        creds = json.load(creds_file)
        strava_email = creds['email']
        strava_password = creds['password']
        return strava_email, strava_password


# Login to strava with dev account so I can view pages properly
def login_to_strava():

    driver.get(LOGIN_URL)

    username_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    
    email, password = get_strava_creds()
    username_field.send_keys(email)
    password_field.send_keys(password)

    password_field.submit()

    WebDriverWait(driver, 10).until(
        EC.url_changes(LOGIN_URL)
    )
    print(f'Logged in as {email}.')


# Return a list of club athlete profile urls who logged miles last week
def get_club_athletes():

    # Request the club URL 
    print(f'Scraping athletes for {CLUB_URL}.')  
    driver.get(CLUB_URL)

    # Toggle it to last week to maximize athletes
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.button.last-week')))
    last_week_button = driver.find_element(By.CLASS_NAME, 'last-week')
    last_week_button.click()

    # Find all athlete profile links in the club
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.athlete-name')))
    athlete_links = driver.find_elements(By.CSS_SELECTOR, 'a.athlete-name')
    hrefs = [link.get_attribute('href') for link in athlete_links]
    return hrefs


# Return a list of activity links for this athlete
def get_athlete_activities(profile_url):
    last_week_url = f'{profile_url}?interval=202424&interval_type=week&chart_type=miles&year_offset=0'
    print(f'Scraping activities for {last_week_url}')
    try:
        driver.get(last_week_url) # Last week's mileage chart
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.feed-ui')))
        activity_links = driver.find_elements(By.CSS_SELECTOR, 'a')
        hrefs = list({link.get_attribute('href') for link in activity_links 
                    if re.search('https://www.strava.com/activities/[0-9]+$', link.get_attribute('href'))})
        return hrefs
    
    except Exception:   # Athlete is likely private
        print(f'Failed retrieving activites for {profile_url}. Moving on to next athlete.')
        return []


def main():

    login_to_strava()
    athlete_links = get_club_athletes()
    with open('./Data/activity_links.txt', 'w') as link_file:
        for link in athlete_links:
            activity_links = get_athlete_activities(link)
            for link in activity_links:
                print(f'Writing {link} to link file')
                link_file.write(f'{link}\n')

    # Close the browser
    driver.quit()


if __name__ == '__main__':
    main()