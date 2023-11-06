"""This is the file for all etl functions in this project"""

# Importing dependencies
from selenium import webdriver
import pandas as pd
import numpy as np
from tqdm import tqdm
import random
import time
import warnings
warnings.filterwarnings("ignore")

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from bs4 import BeautifulSoup
import requests
import re
import boto3
import getpass
import json
import os

# Notes
# # click on department of interest
# deps_dict['Software'].click()
# # department container
# dept_container = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/ul[5]")

# # department divisions
# dept_divs= dept_container.find_element(By.XPATH, '//*[@id="hmenu-content"]/ul[@class="hmenu hmenu-visible hmenu-translateX"]')

# # Get the division names
# dept_divisions = dept_divs.find_elements(By.CLASS_NAME, 'hmenu-item')
# dept_div_names = [dep.text for dep in dept_divisions]

# # get the links to the various elements
# elec_dept_links = []

# for item in elec_deps[2:]:
#     elec_dept_links.append(item.get_attribute('href'))

# # create a dictionary
# elec_dept_dict = dict(zip(elec_dep_names[2:], elec_dept_links))

# driver.get(elec_deps[2].get_attribute('href'))

# acc_product_container = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[@class="sg-col-inner"]/span/div[@class="s-main-slot s-result-list s-search-results sg-row"]')

# page_1 = acc_product_container.find_elements(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div/div[@class="sg-col-inner"]')

# page_html = item_1.get_attribute("outerHTML")
# soup = BeautifulSoup(page_html, 'html.parser')

# # Access elements using BeautifulSoup
# name = soup.find('h2').find('a').find('span').text
# mean_rating = soup.find('div', class_='a-row a-size-small').find('span', class_='a-icon-alt').text.split()[0]
# num_rating = soup.find('div', class_='a-row a-size-small').find('span', class_='a-size-base s-underline-text').text
# price = soup.find('div', class_='a-row a-size-base a-color-base').find('span', class_='a-offscreen').text.replace('$', '').replace('\n', '.')



# Define a function to set up and initialize the driver
def initialize_driver():
    """This is a function to initialize the webdriver

    Returns:
        _type_: Web element
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_driver_path = '/usr/bin/chromedriver'
    driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)
    return driver

# Define a function to perform actions
def perform_actions(driver, url):
    """ This allows the user to perform actions using the driver already created

    Args:
        driver (web element): selenium driver object
        url (str): url to be scraped
    """
    url = url
    driver.get(url)
    
    # Define a wait
    wait = WebDriverWait(driver, 10)
    
    # maximize window
    driver.maximize_window()
    
    try:
        # Your actions here
        all_departments = driver.find_element(By.XPATH, "/html/body/div[1]/header/div/div[4]/div[1]/a")
        all_departments.click()
        
    except NoSuchElementException:
        print("An exception occurred. Restarting the driver and retrying...")
        driver.quit()  # Close the current driver
        driver = initialize_driver()  # Reinitialize the driver
        perform_actions(driver, url)  # Retry the actions
        
        
def find_dept_divisions(selected_dept, department_dict, driver):
    """Find the divisions within a certain department

    Args:
        selected_dept (str): name of the division
        department_dict (dict): key-value pairs of the department name and the links
        driver (web element): selenium driver object

    Returns:
        dict: division names and their hrefs
    """
    if selected_dept == 'Electronics':
        print('valid department')
        
        department_dict[selected_dept].click()
        
        # Wait for the electronics container to be present
        electronics_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div/ul[5]"))
        )
        
        # Wait for electronics departments to be visible
        elec_deps = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "hmenu-item"))
        )
        elec_dep_names = [dep.text for dep in elec_deps]
        
        # Get the links to the various elements
        elec_dept_links = [item.get_attribute('href') for item in elec_deps[2:]]

        # Create a dictionary to match the divisions to their links
        elec_dept_dict = dict(zip(elec_dep_names[2:], elec_dept_links))
        
        return elec_dept_dict
        
    elif selected_dept in department_dict.keys() and selected_dept != 'Electronics':
        print('valid department')
        
        # Click the department
        department_dict[selected_dept].click()

        # Wait for the department container to be present
        dept_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div/ul[5]"))
        )

        # Wait for department divisions to be visible
        dept_divs = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="hmenu-content"]/ul[@class="hmenu hmenu-visible hmenu-translateX"]'))
        )

        # Get the division names
        dept_divisions = dept_divs.find_elements(By.CLASS_NAME, 'hmenu-item')
        dept_div_names = [dep.text for dep in dept_divisions]

        # List to hold division links
        div_links = [division.get_attribute('href') for division in dept_divisions[2:]]

        # Dictionary to capture division name as key and the link as value
        divs_dict = dict(zip(dept_div_names[2:], div_links))
        
        return divs_dict
    
    
def scrape_dept(dept_dict, driver):
    """Scrape the department that has been chosen

    Args:
        dept_dict (str): key-value pairs of a department's divisions and their web elements
        driver (web element): selenium driver object

    Returns:
        dict: details of product like name, price and ratings.
    """
    # Dictionary to store items by division
    divisions = {}
    
    # Iterate through each division
    for division_name, division_link in dept_dict.items():
        driver.get(division_link)
        
        # A list to accumulate items from this division
        division_items = []
        
        while True:
            try:
                # Find the product container for the current page
                product_container = WebDriverWait(driver, 
                                                  30).until(EC.presence_of_element_located((By.XPATH, 
                                                                                                    '/html/body/div[1]/div[1]/div[1]/div[1]/div[@class="sg-col-inner"]/span/div[@class="s-main-slot s-result-list s-search-results sg-row"]')))
                page = WebDriverWait(product_container, 
                                     30).until(EC.presence_of_all_elements_located((By.XPATH, 
                                                                                            '/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div/div[@class="sg-col-inner"]')))
    
                for item in page:
                    try:
                        item_html = item.get_attribute("outerHTML")
                        soup = BeautifulSoup(item_html, 'html.parser')
    
                        item_name = soup.find('h2').find('a').find('span').text
                        item_mean_rating = soup.find('div', class_='a-row a-size-small').find('span', class_='a-icon-alt').text.split()[0]
                        item_num_rating = soup.find('div', class_='a-row a-size-small').find('span', class_='a-size-base s-underline-text').text
                        item_price = soup.find('div', class_='a-row a-size-base a-color-base').find('span', class_='a-offscreen').text.replace('$', '').replace('\n', '.')
    
                        division_items.append({
                            "name": item_name,
                            "mean_rating": item_mean_rating,
                            "num_ratings": item_num_rating,
                            "price": item_price
                        })
    
                    except AttributeError:
                        print("Item not found")
    
                try:
                    next_page_element = driver.find_element(By.PARTIAL_LINK_TEXT, "Next")
                    next_page = next_page_element.get_attribute('href')
                    driver.get(next_page)
                    
                except TimeoutException:
                    print("Timeout exception - No 'Next' button found, exiting loop")
                    break
                    
                except NoSuchElementException:
                    print("No 'Next' button found, exiting loop")
                    break
    
            except NoSuchElementException:
                print("No product container found on this page, exiting loop")
                break
                
            except TimeoutException:
                print("Timeout exception - did not find product, exiting loop")
                break

        # Store the items from this division in the dictionary with the division name as the key
        divisions[division_name] = division_items

    return divisions


def save_dept_json(file_path, dept):
    """save the scraped department to json

    Args:
        file_path (str): where the scraped data is to be stored
        dept (dict): product details
    """
    # Check if the file already exists
    if os.path.exists(file_path):
        print(f"Warning: The file '{file_path}' already exists.")

        # You can choose to overwrite or keep the existing file
        user_choice = input("Do you want to overwrite the file? (y/n): ").strip().lower()
        if user_choice != 'y':
            # If the user chooses not to overwrite, exit the script
            print("Exiting without overwriting the file.")
            exit()
            
            
    # Write data to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(dept, json_file)
        
def make_df(dept_dict, dept_name:str):
    """make a pandas dataframe from the json

    Args:
        dept_dict (dict): scraped data dictionary
        dept_name (str): name of the department

    Returns:
        pandas dataframe: products dataframe
    """
    df = pd.DataFrame()
    
    dept_name = dept_name
    
    # Iterate trhough each division in the department
    for key, val in dept_dict.items():
        division_df = pd.DataFrame(val)
        division_df['division'] = key
        division_df['department'] = dept_name
        df = df.append(division_df, ignore_index=True)
        
    return df


def concat_dfs(folder_path:str):
    """Concatenate all the departments in the folder path into one df

    Args:
        folder_path (str): location of the respective json files

    Returns:
        pandas_dataframe: A concatenated data frame of all the departments
    """
    # Create an empty list to store the DataFrames
    dataframes = []

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            name = filename.replace('.json', '').strip()
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    df = make_df(data, name)  # Create a DataFrame using your make_df function
                    dataframes.append(df)  # Append the DataFrame to the list
                    print(f"Loaded data from {filename}")
            except json.JSONDecodeError as e:
                print(f"JSON decoding error in {filename}: {e}")

    final_df = pd.concat(dataframes, ignore_index=True)
    
    return final_df

# Function to remove non-standard characters and lowercase the text
def preprocess_text(text):
    lowercase_text = text.lower()  # Lowercase the text
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', lowercase_text)  # Remove non-standard characters
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Replace multiple spaces with a single space
    cleaned_text = cleaned_text.strip() # Remove leading and trailing whitespaces
    tokens = cleaned_text.split()
    text = [token for token in tokens]
    
    return " ".join(tokens)


def export_data_to_s3(data, file_name):
    """export data to s3 buckets using aws cli

    Args:
        data (pandas dataframe): Dataframe containing all the concatenated data
        file_name (str): filename that is to be used in aws s3
    """
    # s3 client
    s3 = boto3.client('s3')
    csv_data = data.to_csv(index=False)

    bucket_name = "amazon-scraped-products"

    s3.put_object(Body=csv_data, Bucket=bucket_name, Key=file_name)

    print("Dataframe is saved as CSV in S3 bucket.")
    
