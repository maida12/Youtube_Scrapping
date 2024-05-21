# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time



# def get_comments(video_url, driver):
#     driver.get(video_url)
    
#     driver.execute_script("window.scrollBy(0,700)","")
#     time.sleep(2)
    
#     list=[]

#     comment=driver.find_elements(By.XPATH,"""//*[@id="content-text"]/span""")
#     for i in comment:
#         list.append(i.text)
#     print(list)
    

# def scrape_channel(channel_url):
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.get(channel_url + '/videos')
    
    
    
    
    
#     item = []
        

#     data = []
#     video_data = []
#     item1=[]
#     try:
#         for e in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#details'))):
#             title = e.find_element(By.CSS_SELECTOR,'a#video-title-link').get_attribute('title')
#             vurl = e.find_element(By.CSS_SELECTOR,'a#video-title-link').get_attribute('href')
#             views= e.find_element(By.XPATH,'.//*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][1]').text
#             date_time = e.find_element(By.XPATH,'.//*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][2]').text
#             data.append({
#                 'video_url':vurl,
#                 'title':title,
#                 'date_time':date_time,
#                 'views':views
#                 })
#     except:
#         pass
    
#     video_data = []
#     # for link in video_links[:5]:  # Limiting to first 5 videos for demonstration
    
#     for video in data:
#         comments = get_comments(video['video_url'], driver)
#         video_data.append(comments)
#         print(video_data)
#     item = data

        
#     for video in item:
#         print("Title:", video['title'])
#         print("Views:", video['views'])
#         print("Posted Time:", video['date_time'])
#         print("Thumbnail URL:", video['video_url'])
#         print("\n" + "="*80 + "\n")
#         print("\n")
#     print(len(item))

#     driver.quit()
#     return item

# if __name__ == '__main__':
#     # Example usage
#     channel_url = 'https://www.youtube.com/c/bayyinah'
#     data = scrape_channel(channel_url)

#     for video in data:
#         print("Title:", video['title'])
#         print("Views:", video['views'])
#         print("Posted Time:", video['posted_time'])
#         print("Thumbnail URL:", video['thumbnail_url'])
#         print("Comments:", video['comments'])
#         print("\n" + "="*80 + "\n")






from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


def get_comments(video_url, driver):
    driver.get(video_url)
    
    # Scroll down to load comments
    driver.execute_script("window.scrollBy(0, 700);")
    time.sleep(2)
    
    comments = []
    comment_elements = driver.find_elements(By.XPATH, """//*[@id="content-text"]""")
    
    for elem in comment_elements:
        comments.append(elem.text)
    
    return comments


def scrape_channel(channel_url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(channel_url + '/videos')

    video_data = []

    try:
        video_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#details'))
        )
        
        for element in video_elements:
            title = element.find_element(By.CSS_SELECTOR, 'a#video-title-link').get_attribute('title')
            video_url = element.find_element(By.CSS_SELECTOR, 'a#video-title-link').get_attribute('href')
            views = element.find_element(By.XPATH, './/*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][1]').text
            date_time = element.find_element(By.XPATH, './/*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][2]').text

            video_data.append({
                'video_url': video_url,
                'title': title,
                'date_time': date_time,
                'views': views
            })
    except Exception as e:
        print(f"Error occurred: {e}")
    
    # Extract comments for each video
    for video in video_data[:5]:  # Limiting to the first 5 videos for demonstration
        comments = get_comments(video['video_url'], driver)
        video['comments'] = comments

    driver.quit()
    return video_data


def save_to_excel(data, filename):
    # Flatten the data for better Excel representation
    flattened_data = []
    for video in data:
        base_info = {
            'Title': video['title'],
            'Views': video['views'],
            'Posted Time': video['date_time'],
            'Video URL': video['video_url'],
        }
        comments = video.get('comments', [])
        if not comments:
            # Add a row with an empty comment if there are no comments
            row = base_info.copy()
            row['Comment'] = ''
            flattened_data.append(row)
        else:
            for comment in comments:
                row = base_info.copy()
                row['Comment'] = comment
                flattened_data.append(row)
    
    df = pd.DataFrame(flattened_data)
    df.to_excel(filename, index=False)



if __name__ == '__main__':
    # Example usage
    channel_url = 'https://www.youtube.com/c/bayyinah'
    data = scrape_channel(channel_url)

    save_to_excel(data, 'youtube_data.xlsx')

    for video in data:
        print("Title:", video['title'])
        print("Views:", video['views'])
        print("Posted Time:", video['date_time'])
        print("Video URL:", video['video_url'])
        print("Comments:", video.get('comments', 'No comments found'))
        print("\n" + "="*80 + "\n")
