*Online Data Mining*

Team know_how_to_google
Team members: Emmanuel Owusu Annim | Felicia Betten | Robin Kratschmayr | Baris Orman 

This repository contains several spiders to scrape information that is stored at www.funda.nl. The stakeholder asked for the following information as minimum requirements for this module: zipcode of the house, the asking price, the squared meters surface of living area, the squared meters of the whole property, the year of construction, whether it has a garden or not, the type of house, the house description, the energylabel and the number of rooms of bathrooms. 

Next to these minimum requirements, we have scraped (more) information on:
1) sold houses
2) brokers information
3) brokers reviews
4) images per house
5) object recognition

As the scraped csv files are big, we decide to upload the full versions to OneDrive (https://onedrive.live.com/?authkey=%21AgmmjLDD31MuXX0&id=37D8990536FAED09%21110&cid=37D8990536FAED09) and to Brightspace. On GitHub we have uploaded subsets.

If you want to run the objectrecognition on your machine, another file, which exceeds the github storage limit needs to be downloaded and stored in the following folder 'Object recognition analysis/yolo' the file 'yolov3.weights' can be downloaded in our drive here: https://1drv.ms/u/s!Agnt-jYFmdg3oncRRGd0i_ZTwzVM?e=yHaVPB

An overview on the scraped data can be found in the Scraped_data_ERD.jpg file.

Please note the following before checking the Code.
1. In the folder Final scraping logic/funda you will first find several .csv files with the output of the scraping.
2. In that folder you will also find the funda.py file where all spiders are put together, including the teammember that was responsible for that part.
3. The scraping was done through Luminati Proxy Manager (LPM).
4. The log files of scrapy are also stored in the repo.
5. The workflow.md file shows our Git workflow.
6. Each team member has his/her own folder to try out stuff, but all the final codes are added to the funda.py.
7. Finally, you will also see the final version of our ERD including the scraped data.
8. There are two versions of the subset of the scraping with images. (1) where only the galery picture of a listed house was scraped (15000 houses) and (2) where all images of a house are scraped (1500 houses).
9. some sample images are in this git_repo but more are also on the onedrive.

