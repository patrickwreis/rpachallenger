import argparse
import logging
import os
import sys
from time import time

import pandas as pd
import selenium.webdriver.support.expected_conditions as EC
from playwright.sync_api import sync_playwright
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from settings import NAME, URL_INPUT_CHALLENGE, VERSION

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class RpaInputChallenger:
    columns_to_fields = {
        'First Name': 'ng-reflect-name="labelFirstName"',
        'Last Name ': 'ng-reflect-name="labelLastName"',
        'Company Name': 'ng-reflect-name="labelCompanyName"',
        'Role in Company': 'ng-reflect-name="labelRole"',
        'Address': 'ng-reflect-name="labelAddress"',
        'Email': 'ng-reflect-name="labelEmail"',
        'Phone Number': 'ng-reflect-name="labelPhone"',
    }

    def __init__(self):
        self.name = NAME
        self.version = VERSION
        self.default_directory = os.path.dirname(os.path.abspath(__file__))
        self.filepath = os.path.join(self.default_directory, 'challenge.xlsx')
        self.delete_file(self.filepath)
        self.url_input_challenge = URL_INPUT_CHALLENGE
        logging.info(f'{self.name} version {self.version} initialized.')

    @staticmethod
    def delete_file(pathfile):
        """
        Delete a file if it exists.
        """
        if os.path.exists(pathfile):
            os.remove(pathfile)
            logging.info(f'Deleted file: {pathfile}')
        else:
            logging.warning(f'File not found: {pathfile}')

    @staticmethod
    def wait_download_complete(pathfile, timeout=60):
        """
        Wait for the download to complete.
        :param pathfile: Path to the file being downloaded.
        :param timeout: Maximum time to wait for the download to complete.
        """
        logging.info(f'Waiting for download to complete: {pathfile}')
        end_time = time() + timeout
        while time() < end_time:
            if os.path.exists(pathfile) and os.path.getsize(pathfile) > 0:
                logging.info('Download completed successfully.')
                return True
        logging.error('Download did not complete within the specified timeout.')
        return False

    def setup_webdriver(self):
        logging.info('Setting up the WebDriver...')
        try:
            prefs = {
                'download.default_directory': self.default_directory,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True,
            }
            options = ChromeOptions()
            options.add_experimental_option('prefs', prefs)
            self.driver = webdriver.Chrome(service=ChromeService(), options=options)
            logging.info('WebDriver initialized.')
        except Exception as e:
            logging.error(f'Failed to set up WebDriver: {e}')
            sys.exit(1)

    def input_challenge_selenium(self):
        logging.info(f'Navigating to {self.url_input_challenge}...')
        try:
            self.driver.get(self.url_input_challenge)
            wait = WebDriverWait(self.driver, 10)
            download_button = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="challenge.xlsx"]'))
            )
            download_button.click()
            self.wait_download_complete(self.filepath)

            df = pd.read_excel(self.filepath)
            logging.info('Challenge data loaded successfully.')

            columns_to_fields = self.columns_to_fields

            start_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start')]"))
            )
            start_button.click()
            logging.info('Clicked the Start button.')

            for idx, row in df.iterrows():
                for col, selector in columns_to_fields.items():
                    value = str(row[col]) if pd.notnull(row[col]) else ''
                    self.driver.find_element(By.CSS_SELECTOR, f'[{selector}]').send_keys(value)
                submit_btn = self.driver.find_element(By.XPATH, "//input[@type='submit']")
                submit_btn.click()

            wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Congratulations!')]"))
            )

            message2 = self.driver.find_element(By.CSS_SELECTOR, '.message2').text
            time_to_complete = ' '.join(message2.split()[-2:])
            logging.info(f'Challenge completed successfully in {time_to_complete}.')

            self.driver.quit()

        except Exception as e:
            logging.error(f'Failed to complete challenge: {e}')
            sys.exit(1)

    def input_challenge_playwright(self):
        logging.info(f'Navigating to {self.url_input_challenge}...')
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                page.goto('https://rpachallenge.com')

                download_link = page.wait_for_selector('a[href*="challenge.xlsx"]', timeout=10000)
                if download_link is not None:
                    with page.expect_download() as download_info:
                        download_link.click()
                    download = download_info.value
                    download.save_as('challenge.xlsx')
                else:
                    logging.error('Download link not found.')

                df = pd.read_excel('challenge.xlsx')
                logging.info('Challenge data loaded successfully.')

                columns_to_fields = self.columns_to_fields

                start_button = page.wait_for_selector("//button[contains(text(), 'Start')]", timeout=10000)
                if start_button is not None:
                    start_button.click()
                    logging.info('Clicked the Start button.')

                for idx, row in df.iterrows():
                    for col, selector in columns_to_fields.items():
                        value = str(row[col]) if pd.notnull(row[col]) else ''
                        page.fill(f'[{selector}]', value)

                    page.click("//input[@type='submit']")

                page.wait_for_selector("//div[contains(text(), 'Congratulations!')]", timeout=10000)
                message2 = page.query_selector('.message2').text_content()  # type: ignore
                if message2 is None:
                    logging.error('Could not find the completion message element.')
                    sys.exit(1)

                time_to_complete = ' '.join(message2.split()[-2:])
                logging.info(f'Challenge completed successfully in {time_to_complete}.')

                browser.close()
        except Exception as e:
            logging.error(f'Failed to complete challenge: {e}')
            sys.exit(1)

    def run(self, mode='selenium'):
        logging.info('Running RPA Challenger...')
        if mode not in {'selenium', 'playwright'}:
            logging.error('Unsupported mode. Please use "selenium" or "playwright".')
            sys.exit(1)

        ini_time = time()
        if mode == 'selenium':
            logging.info('Using Selenium mode.')
            self.setup_webdriver()
            self.input_challenge_selenium()
        elif mode == 'playwright':
            self.input_challenge_playwright()

        elapsed_time = time() - ini_time
        logging.info(f'RPA Challenger completed in {elapsed_time:.2f} seconds.')


def main():
    parser = argparse.ArgumentParser(description='RPA Challenger CLI')
    parser.add_argument(
        '--mode',
        choices=['selenium', 'playwright'],
        default='selenium',
        help='Escolha o modo de execução: selenium (padrão) ou playwright',
    )
    args = parser.parse_args()

    rpa_challenger = RpaInputChallenger()
    rpa_challenger.run(mode=args.mode)


if __name__ == '__main__':
    main()
