from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from pytube import YouTube
import platform, subprocess, os

class YTDownload:
    def __init__(self, file_path, output_folder):
        # Making selenium headless
        options = Options()
        options.headless = True
        self.windows_system = platform.system() == 'Windows'
        self.driver = webdriver.Firefox(options=options)
        self.data = [text[:-1] for text in self.read(file_path)]
        self.output_folder = output_folder
        self.loadbar = 0
        self.current_video = None
        self.last_progress = -1
        self.links = []
        print("Browser opened.")

    def read(self, file_path):
        with open(file_path) as f:
            data = f.readlines()
        return data

    def search(self):
        print("Starting Video Search")
        driver = self.driver
        redirect = "https://www.youtube.com/"
        # For every title in data search youtube and find the link
        for title in self.data:
            driver.get(redirect)
            # Send title to youtube and search
            driver.find_element_by_xpath('//input[@id="search"]').send_keys(title)
            driver.find_element_by_xpath('//button[@id="search-icon-legacy"]').click()
            # Record first video's watch link   
            self.links.append(driver.find_element_by_xpath('//a[@id="video-title"]').get_attribute("href"))
            print(f"{title} link grabbed: {self.links[-1]}")
        driver.quit()
        print("Browser closed.")

    def progress_func(self, stream, chunk, bytes_remaining):
        progress = int(round((1 - bytes_remaining / self.current_video.filesize) * 100))
        if progress != self.last_progress:
            for _ in range(0, progress, 5):
                print("|", end="")
            print(str(progress) + "%")
        self.last_progress = progress
        
    def download(self):
        """
        Edit the name of the file so it can be easily used in the file system
        Download the video as mp4 in the lowest resolution possible (using audio only so resolution doesn't matter)
        """
        print("Download video files")
        # Creates and downloads youtube objects for every link found using search
        for index, link in enumerate(self.links):
            #Converting title to useable state for terminal call
            print(f"Downloading {self.data[index]}")
            file_name = "".join([letter for letter in self.data[index].replace(' ', '_') if 48 <= ord(letter) \
                >= 57 or 65 <= ord(letter) <= 90 or 97 <= ord(letter) <= 122 or ord(letter) == 94])
            yt = YouTube(link, on_progress_callback=self.progress_func)
            video = yt.streams.filter(file_extension='mp4').get_lowest_resolution()
            self.current_video = video
            video.download(filename=file_name, output_path=self.output_folder, skip_existing=True)
        print("Download finished.")

    def convert(self):
        """
        Takes a mp4 file and first edits the name so it can be easily used in the file system
        After the name is correct the video is converted to a mp3 file using ffmpeg
        After the video is converted, delete the original mp4 and change the name to the original
        """
        print("Starting conversion")
        for title in self.data:
            # Converting title to useable state for terminal call
            title = title.replace(' ', '_')
            file_name = "".join([letter for letter in title if 48 <= ord(letter) \
                 >= 57 or 65 <= ord(letter) <= 90 or 97 <= ord(letter) <= 122 or ord(letter) == 94])

            print(f"Converting {title}")
            # Creating file path
            base_path = os.path.join(os.path.abspath(self.output_folder), file_name)
            input_path, output_path = base_path + '.mp4', base_path + '.mp3'

            print(f"Input Path: {input_path}")

            if not self.windows_system:
                # Linux or MacOs using terminal
                # Terminal call of ffmpeg to convert mp4 to mp3 file
                subprocess.call(['ffmpeg', '-i', input_path, output_path])
                # Remove original .mp4 file
                subprocess.call(['rm', input_path])
                # FFMPEG doesn't work with spaces in name so they have to be changed to a different character then reverted back
                subprocess.call(['mv', output_path, output_path.replace('_', ' ')])
            else:
                # Windows using command line
                # Terminal call of ffmpeg to convert mp4 to mp3 file
                subprocess.call(['ffmpeg', '-i', input_path, output_path])
                # Remove original .mp4 file
                subprocess.call(['del', input_path])
                # FFMPEG doesn't work with spaces in name so they have to be changed to a different character then reverted back
                subprocess.call(['rename', output_path, output_path.replace('_', ' ')])
        print("Conversion finished.")

yt = YTDownload("./names.txt", ".")
yt.search()
yt.download()
yt.convert()


