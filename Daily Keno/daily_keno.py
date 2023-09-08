import os
from datetime import datetime
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
import schedule

daily_keno_numbers = []

def scrape_numbers():
    try:
        toronto = timezone('America/Toronto')
        current_date = datetime.now(toronto).strftime('%Y-%m-%d')
        current_time = datetime.now(toronto).strftime('%H:%M:%S')
        print(f'Starting scrape at {current_time} Toronto time...')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.olg.ca/en/lottery/play-daily-keno-encore/past-results.html')
        time.sleep(5)
        page_content = driver.page_source
        draw_time = 'e' if 'EVENING DRAW' in page_content else 'm'
        ul_element = driver.find_element(By.CLASS_NAME, 'dkeno')
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
        numbers = [li.find_element(By.CLASS_NAME, 'ball-number').text for li in li_elements]
        daily_keno_numbers.append({'date': current_date, 'time': draw_time, 'numbers': numbers})
        print(f'Successfully scraped numbers for {current_date}, draw time: {draw_time}')
        driver.quit()
        json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'daily_keno_numbers.json')
        with open(json_file_path, 'w') as f:
            json.dump(daily_keno_numbers, f)
        print('Successfully updated JSON file.')
    except Exception as e:
        print(f'An error occurred: {e}')

schedule.every().day.at('16:00').do(scrape_numbers)
schedule.every().day.at('23:49').do(scrape_numbers)

while True:
    schedule.run_pending()
    time.sleep(1)