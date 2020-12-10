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

Please note the following before checking the Code.
1. In the folder Final scraping logic/funda you will first find several .csv files with the output of the scraping.
2. In that folder you will also find the funda.py file where all spiders are put together, including the teammember that was responsible for that part.
3. The scraping was done through Luminati Proxy Manager (LPM).
4. The log files of scrapy are also stored in the repo.
5. The workflow.md file shows our Git workflow.
6. Each team member has his/her own folder to try out stuff, but all the final codes are added to the funda.py.
7. Finally, you will also see the final version of our ERD including the scraped data.
