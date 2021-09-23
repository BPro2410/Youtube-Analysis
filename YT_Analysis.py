###########################################
########## Scrap YT Information  ##########
###########################################

### ---- Loading required libraries
import requests
import pandas as pd
import json
from selenium import webdriver
import matplotlib.pyplot as plt
import numpy as np
import time



### ---- YT download class
''' Downloads Information from various youtube channels using
selenium for web scraping data. This code only works for german
users because of the different html youtube popup window.
All you have to do is fill the class with the name of the 
youtuber for whom you want to retrieve information.
If you are based on any other country than Germany and want to scrap 
yt information with this code you might have to change code line 39-41 first.

In case if there are any questions feel free to contact me.
'''

class YTData:

    def __init__(self, channel, n = 10):

        ### ----- Calling Youtube
        url = "https://www.youtube.com/c/"
        url = url + channel + "/videos"
        self.channel = channel
        self.driver = webdriver.Chrome()
        self.driver.get(url)

        ### ----- Get rid of popup window (German only)
        if 'ICH STIMME ZU' in "ICH STIMME ZU" in self.driver.find_element_by_css_selector('*#yDmH0d').text:
            self.driver.find_element_by_xpath(
                '//*[@aria-label="In die Verwendung von Cookies und anderen Daten zu den beschriebenen Zwecken einwilligen"]').click()


    def Preprocess(self, n = 10, scroll = True):

        ### ----- Scroll to get more videos displayed
        if scroll == True:
            for i in range(0, 10000, 1000):
                self.driver.execute_script(f"window.scrollTo({str(i)}, {str(i + 1000)})")
                time.sleep(0.1)

                self.driver.execute_script("window.scrollTo(0, 0)")

        ### ----- Search Information about all videos
        videos = self.driver.find_elements_by_class_name('style-scope ytd-grid-video-renderer')

        # Create a list for later Pandas
        all_videos = list()

        # Loop through videos
        for video in videos:
            # Title
            title = video.find_element_by_xpath('.//*[@id = "video-title"]').text

            # Klicks (without string)
            views = video.find_element_by_xpath('.//*[@id = "metadata-line"]/span[1]').text
            view = views.split()
            view[0] = view[0].replace(".", "")
            if len(view) > 2:
                view[0] = view[0].replace(",", ".")
                view[0] = float(view[0])
                view[0] = view[0] * 1000000
            view = float(view[0])

            # Uploads
            uploads = video.find_element_by_xpath('.//*[@id = "metadata-line"]/span[2]').text

            # Store in dict & append list
            later_pandas = {
                'Title': title,
                'Views': view,
                'Upload': uploads
            }

            all_videos.append(later_pandas)

        ### ----- Create Pandas Data Frame
        self.df = pd.DataFrame(all_videos)  # Wrong order (new -> old)
        self.data = self.df.reindex(index = self.df.index[::-1])  # Right order (old -> new)
        self.data = self.data.reset_index()

        # Show top 10 clicked videos
        self.topvids = self.df.sort_values(by=["Views"], ascending=False)
        self.topvids = self.topvids[0:n]

        # Close driver
        self.driver.close()


    def PlotViews(self):

        ### ----- Plot Data
        plt.figure(figsize=(13, 7))
        plt.plot(self.data.Views, "orange",
                 alpha=.7,
                 linewidth=1)
        plt.title(f"Views: {self.channel} (last {len(self.data.Views)} videos)")
        plt.ylabel("Total views")
        plt.ticklabel_format(style='plain')
        plt.grid(True, alpha=0.3)
        plt.show()



###########################################
########## All possible commands ##########
###########################################

ytdata = YTData("spontanablack")            # Setup
ytdata.Preprocess(n = 10, scroll = True)    # Processing
ytdata.topvids                              # Top 10 clicked videos
c = ytdata.data                             # Show all scraped data
ytdata.PlotViews()                          # Plot video views


