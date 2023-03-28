from django.shortcuts import render
# from .models import Job
from django.http import HttpResponse
from django.urls import reverse
from django.http import JsonResponse

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .models import Job
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from django.views.decorators.csrf import csrf_exempt


# home page scraper page
def home(request):
    context = {
        'title': 'Find a Job',
        'link': reverse('select_location')
    }
    return render(request, 'applications/home.html', context)


# location selection page
def select_location(request):
    return render(request, "applications/location.html")


# main page
def linked_jobs(request):
    lst = []
    if request.method == 'POST':
        # Retrieve filter values from frontend
        location_filter = request.POST.get('selectOption', '')
        if location_filter:
            jobs = scrapper(location_filter)
            jobs = pd.DataFrame(jobs).dropna().to_dict('list')
            for i in range(len(jobs['job_role'])):
                lst.append((jobs['job_role'][i],jobs['company'][i],jobs['Location'][i],jobs['Posted_date'][i],
                   jobs['JD'][i],jobs['Link'][i],jobs["id"][i]))
                
    return render(request, "applications/job.html", {"details":lst})



# store the job in the database selected by user 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def save_job(request):
    if request.method == 'POST':
        company = request.POST.get('company')
        job_role = request.POST.get('job_role')
        location = request.POST.get('location')
        posted = request.POST.get('posted')
        jd = request.POST.get('jd')
        link = request.POST.get('link')
        job = Job(Company=company, job_role=job_role, Location=location, posted=posted, Jd=jd, link=link)
        job.save()
        response = JsonResponse({"status":"success"})
        response['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


    

# scrapper
def scrapper(Location):

    link = []
    url = f"https://in.linkedin.com/jobs/search?keywords=&location={Location}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    service = Service('C:\Chrome web =driver\chromedriver_win32\chromedriver.exe')  # replace with your own path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    # Scroll through the page to load all job listings

    scroll_pause_time = 2 # You can set your own pause time. dont slow too slow that might not able to load more data
    screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web

    A = 1

    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{A});".format(screen_height=screen_height, A=A))
        A += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        # if (screen_height) * A > scroll_height:
        if A==2:
            break
        # try:
        #     see_more_button = driver.find_element(By.XPATH, '//*[@id="main-content"]/section/button')
        #     see_more_button.click()
        #     time.sleep(scroll_pause_time)
        # except:
        #     pass



    # store all anchor tag link
    links = driver.find_elements('tag name','a')
    for i in links:
        link.append(i.get_attribute('href'))



# Extracting job link from anchor tag

    job_link = []
    for i in link:
        if 'jobs/view/' in i:
            job_link.append(i)


    # Itrate job and extract required things  
    id = []
    job_role = []
    company = []
    Location = []
    Posted_date = []
    JD = []

    k = 0

    for i in job_link:
    # for i in job_link:

        # driver = webdriver.Chrome("C:\Chrome web =driver\chromedriver_win32\chromedriver.exe")
        driver.get(i)
        try:
            see_more = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/button[1]')
            see_more.click()
        except:
            pass

        id.append(k)

        try:
            job_role.append(driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h1').text)
        except:
            job_role.append(np.nan)
        try:
            company.append(driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a').text)
        except:
            company.append(np.nan)
        try:
            Location.append(driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[2]').text)
        except:
            Location.append(np.nan)
        try:
            Posted_date.append(driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[2]/span[1]').text)
        except:
            Posted_date.append(np.nan)
        try:
            JD.append(driver.find_element(By.CLASS_NAME, 'show-more-less-html__markup').text)
        except:
            JD.append(np.nan)

        k+=1


# store all contain in dictionary
    dic = {
    "company":company,
    "job_role":job_role,
    "Location":Location,
    'JD':JD,
    "Posted_date":Posted_date,
    "Link":job_link,
    "id":id
    }
    return dic 

 





