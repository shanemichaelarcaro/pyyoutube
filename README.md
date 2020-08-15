# PyYoutube
### Automatic YouTube Music Download
This script was designed to take the name of a song and artist and download an mp3 version automatically. The intended purpose of this project was to replace the countless hours spent manually downloading music from YouTube using online converters. 

### Usage
Parameter | Default Value | Description | Required
------ | ------------- | ----------- | --------
`file_path` | `./names.txt` | Text file to read in names of song requests | Yes
`output_folder` | `.` | Video download location | Yes

### Project Specificatoins
* Search for YouTube videos using headless selenium
* Download mp4 version of the targeted video
* Convert file name into a useable state for terminal calls
* Convert video to mp3
* Revert file name to original state

### Dependencies
* [Selenium](https://selenium-python.readthedocs.io/) `pip3 install selenium`
* [PyTube](https://pypi.org/project/pytube/) `pip3 install pytube`
* [FFMPEG](https://ffmpeg.org/) `sudo apt-get install ffmpeg`
* [Firefox](https://www.mozilla.org/en-US/exp/firefox/) or any other web browser

### Bugs
This project was tested heavily on `Ubuntu Linux` but was designed to work on `Windows 10` as well. Although the testing on `Windows` was not as rigorous, initial test cases reported `0` bugs. 
