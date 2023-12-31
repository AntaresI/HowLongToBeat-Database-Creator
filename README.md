# HowLongToBeat-Database-Creator
![hi](/png/howlongtobeat_website.png)

# Introduction
This is my project that involves creating a database `HowLongToBeat_Database.sql` from scraping data from website [HowLongToBeat](https://howlongtobeat.com/), which contains videogames and gaming statistics related to each videogame, such as the game's genre, developer, publisher, how long it takes to finish the game etc. 

The main motivation for me creating this project was my hobby, which is playing videogames and measuring the time it takes me to complete a videogame. I was curious about which game is considered to be the longest and found the HowLongToBeat website where players would upload how long it took them to complete a game in various modes, such as playing only the main story, getting all the achievements and others. The website does offer its own [statistics](https://howlongtobeat.com/stats) but I wanted to search for: 

1) the longest-to-complete offline game (the rankings contain both online and offline games with no option to filter)

2) the longest-to-complete offline game in the mode Main+Sides which is how I play all videogames - complete the main story and sidequests (the rankings use either All Styles mode or seemingly don't correspond to any displayed duration for each game at all).

So I decided to do it myself. This meant the need to setup a list of all the videogames and their durations (how long it takes, according to players who have finished it, to complete the videogame). And while I was at it - why not get all the available info for each game right with it? Therefore I opted for using `Python` and its `PostgreSQL` library `psycopg2` to create a database containing all the possible info for each videogame. 

# Scraping HowLongToBeat

The script `HowLongToBeat_Site_Crawler.py` contains a class `HowLongToBeat_Crawler` which performs the webscraping. It contains all possible and meaningful information from the [HowLongToBeat](https://howlongtobeat.com/) for each videogame. Here is an example of how the website looks like for the game Europa Universalis III and what information has been webscraped into the database.
![hi](/png/website_scraped_info.png)
And here is an example of the `game_info` dictionary which is the final output of the `.scrape` method of class implemented in `HowLongToBeat_Site_Crawler.py`
![hi](/png/python_scraped_info.png)
# Uploading videogame information into the database

The script `HowLongToBeat_Database_Creator.py` contains a class `HowLongToBeat_Games_Database` which creates the PostgreSQL database `HowLongToBeat_Database.sql` and its tables, and the class's method `.database_update` obtains the `game_info` dictionary from `HowLongToBeat_Site_Crawler.py` for each game and updates it into the database.

[HowLongToBeat](https://howlongtobeat.com/) can be used to search for a videogame. The http corresponding to a videogame contains just a number behind the main site like `https://howlongtobeat.com/game/11285`, meaning that it is possible to simply cycle through several tens of thousands of numbers starting from 1 and see whether there is a videogame information returned by the website or not. This was done, the number of url numbers was 120 000, as somewhere around the 100 000 mark the number of loaded sites containing videogames drastically diminished. Many url's didn't contain anything at all and the website returned was simply blank. This resulted in 37323 videogames found and their information scraped into the database.

# Loading the database
In order to load the load the database into postgresql or mysql database do:
1) With installed Git, enter command `git clone https://github.com/AntaresI/HowLongToBeat-Database-Creator.git`
2) Move the `HowLongToBeat_Database.sql` where you want to store it and then go to that directory in Windows Command Prompt or Linux Bash
3) If you have PostgreSQL installed, enter command `psql -U username databasename < HowLongToBeat_Database.sql` or if you have MySQL installed, enter command `mysql -U username databasename < HowLongToBeat_Database.sql`
# HowLongToBeat_Database

The database `HowLongToBeat_Database.sql` contains 9 tables - `games`, `genres`, `developers`, `publishers`, `platforms` and its connecting tables `game_developers`, `game_publishers`, `game_platforms`, `game_genres`. 
## Games table
`games` table contains 37323 videogames and consist of columns:

`game_id` - Primary Key

`title` - title of the videogame

`off_or_on` - whether it is mainly an online or offline videogame

`description` - brief description of the videogame 

`logging` - how many players are playing the videogame with intention to log the duration of playing

`backlogs` - how many players have uploaded their resulting duration of playthrough to the site

`replays` - how many players have opted to replay the game and upload another log

`retired_percent` - how many players have expressed intention in completing the game but then decided to abandon it

`rating_percent` - rating of the game by the players that have completed it

`beat` - how many players have beaten the game

`main_story` - the average duration of playthrough where you only complete the main story and nothing extra according to the logged durations (offline videogame)

`main_and_extras` - the average duration of playthrough where you complete the main story and all the sidequests according to the logged durations (offline videogame)

`completionist` - the average duration of playthrough where you complete all the achievements according to the logged durations  (offline videogame)

`all_styles` - should be an average of all logs according to the logged durations (but not always, there is no explanation for what all_styles really means)  (offline videogame)

`single_player` - the average duration of playthrough where you reach the maximum level solo according to the logged durations (online videogame)

`co_op` - the average duration of playthrough where you reach the maximum level with a friend according to the logged durations (online videogame)

`versus` - the average duration of playthrough where you reach all achievements possible by playing against other players according to the logged durations (online videogame)

`eu_release` - release date in Europe

`na_release` - release date in North America

`jp_release` - release date in Japan

## Platforms, Genres, Developers, Publishers tables
These tables contain respectively:

`platform_id` - Primary Key

`platform` - name of platform


`genre_id` - Primary Key

`genre` - name of genre


`developer_id` - Primary Key

`developer` - name of developer


`publisher_id` - Primary Key

`publisher` - name of publisher


### Connecting tables
The 4 tables listed above are connected to the `games` table via their respective connecting tables `game_platforms`, `game_genres`, `game_developers`, `game_publishers`, which contain `game_id` along with id of platform, genre, developer or publisher corresponding to it.

# What is the longest offline game?
Now finally SQL queries can be constructed to find out the longest offline game and all its other information. The script `HowLongToBeat_Longest_Game_Selector_Script.py` does exactly that. It loads and connects to the database using the library `psycopg2` and then displays the result. 



I was searching for the longest offline game played in main_and_extras mode where the amount of backlogs is greater than 600 for not skewed statistics. The query and its result is - 

![hi](/png/longest_game_games.png)

Therefore the longest game is Hearts of Iron IV with 361 hours of playtime!!!!!!!

All the additional information about Hearts of Iron IV from the secondary tables -

![hi](/png/longest_game_info.png)
