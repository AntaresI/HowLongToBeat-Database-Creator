import psycopg2 as pg2   #Python library for controlling PostGresSQL databases
from HowLongToBeat_Site_Crawler import HowLongToBeat_Crawler

class HowLongToBeat_Games_Database:
    
    def __init__(self):
        
        self._url = 0   #Initializing url number to keep track of what url the updater is scraping from
        
        """TRY/EXCEPT BLOCK TO CREATE DATABASE IF IT DOESN'T ALREADY EXIST ON THE USER'S COMPUTER"""
        try:
            self.conn = pg2.connect(
            
            user = "postgres",
            host = "localhost",
            password = "password"    
            )
            
            self.conn.autocommit = True
            
            self.cur = self.conn.cursor()
            
            self.cur.execute('CREATE database HowLongToBeat_Games_List')
            
        except pg2.errors.DuplicateDatabase:
            pass
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        
        """CREATE THE TABLES"""
        self.conn = pg2.connect(
        database = 'howlongtobeat_games_list',
        user = "postgres",
        host = "localhost",
        password = "password"    
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS games (game_id SERIAL PRIMARY KEY, title VARCHAR(500) UNIQUE, off_or_on VARCHAR(10), \
                    description VARCHAR(10000), logging INT, backlogs INT, replays INT, retired_percent DECIMAL(4,1),\
                    rating_percent INT, beat INT, main_story DECIMAL(5,1), main_and_extras DECIMAL(5,1),\
                    completionist DECIMAL(5,1), all_styles DECIMAL(5,1), single_player DECIMAL(5,1), co_op DECIMAL(5,1),\
                    versus DECIMAL(5,1), eu_release DATE, na_release DATE, jp_release DATE)")
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS platforms (platform_id SERIAL PRIMARY KEY, platform VARCHAR(500) UNIQUE)")
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS game_platforms (platform_id INTEGER REFERENCES platforms(platform_id)\
                         ON UPDATE CASCADE ON DELETE CASCADE, game_id INTEGER REFERENCES games(game_id) ON UPDATE CASCADE ON\
                         DELETE CASCADE)")
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS genres (genre_id SERIAL PRIMARY KEY, genre VARCHAR(500) UNIQUE)")
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS game_genres (genre_id INTEGER REFERENCES genres(genre_id) ON UPDATE CASCADE \
                         ON DELETE CASCADE, game_id INTEGER REFERENCES games(game_id) ON UPDATE CASCADE\
                         ON DELETE CASCADE)")
        
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS developers (developer_id SERIAL PRIMARY KEY, developer VARCHAR(500) UNIQUE)")
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS game_developers (developer_id INTEGER REFERENCES developers(developer_id) ON UPDATE\
                         CASCADE ON DELETE CASCADE, game_id INTEGER REFERENCES games(game_id) ON UPDATE\
                         CASCADE ON DELETE CASCADE)")
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS publishers (publisher_id SERIAL PRIMARY KEY, publisher VARCHAR(500) UNIQUE)")
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS game_publishers (publisher_id INTEGER REFERENCES publishers(publisher_id) ON UPDATE\
                         CASCADE ON DELETE CASCADE, game_id INTEGER REFERENCES games(game_id) ON UPDATE \
                         CASCADE ON DELETE CASCADE)")
        """"""""""""""""""""""""   
        
    def database_update(self, start_url, end_url):
        
        """UPDATING DATABASE BY CRAWLING FROM START_URL NUMBER TO END_URL NUMBER"""
        for i in range(start_url, end_url+1):
            
            """UPDATE THE _URL NUMBER"""
            self._url = i
            print(f"URL number being processed is {i}")
            """"""""""""""""""""""""""""""
            
            """GET ALL THE SCRAPED INFO FROM THE IMPORTED CRAWLER"""
            crawler = HowLongToBeat_Crawler(i)
            game_info = crawler.scrape()
            if game_info == None:
                continue
            """"""""""""""""""""""""""""""""""""""""""""""""""""""
            
            """INSERTING THE INFORMATION INTO THE RESPECTIVE TABLES WITH TRY/EXCEPT BLOCK TO PREVENT STOPPAGE DUE TO UNIQUE INSERT VIOLATION"""
            try:
                self.cur.execute('''INSERT INTO games (title, description, off_or_on, logging, backlogs, replays, retired_percent,\
                        rating_percent, beat, main_story, main_and_extras, completionist, all_styles,\
                        single_player , co_op, versus, eu_release, na_release, jp_release) VALUES\
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,(SELECT TO_DATE(%s,'Month DD, YYYY')),\
                         (SELECT TO_DATE(%s,'Month DD, YYYY')),(SELECT TO_DATE(%s,'Month DD, YYYY')))
                            '''
                            ,(game_info['title'], game_info['description'], game_info['online'], game_info['log_statistics'][0],\
                              game_info['log_statistics'][1], game_info['log_statistics'][2], game_info['log_statistics'][3],\
                              game_info['log_statistics'][4], game_info['log_statistics'][5], game_info['durations']['Main Story'],\
                              game_info['durations']['Main + Extras'], game_info['durations']['Completionist'],\
                              game_info['durations']['All Styles'], game_info['durations']['Single-Player'],\
                              game_info['durations']['Co-Op'], game_info['durations']['Vs.'], 
                              game_info['releases']['EU'], game_info['releases']['NA'], game_info['releases']['JP']))
            except pg2.errors.UniqueViolation:
                print("THIS URL HAS ALREADY BEEN PROCESSED INTO THE DATABASE!")
                continue
            
            for j in range(len(game_info['platforms'])):
                try:
                    self.cur.execute('''INSERT INTO platforms (platform) VALUES (%s)''',(game_info['platforms'][j],))   
                except pg2.errors.UniqueViolation:
                    pass 
               
                self.cur.execute('''INSERT INTO game_platforms (platform_id, game_id) VALUES ((SELECT platform_id FROM platforms WHERE platform = %s),(SELECT game_id FROM games WHERE title = %s))''',(game_info['platforms'][j],game_info['title']))
                    
            for j in range(len(game_info['genres'])):
                try:
                    self.cur.execute('''INSERT INTO genres (genre) VALUES (%s)''',(game_info['genres'][j],))
                except pg2.errors.UniqueViolation:
                      pass
                
                self.cur.execute('''INSERT INTO game_genres (genre_id, game_id) VALUES ((SELECT genre_id FROM genres WHERE genre = %s),(SELECT game_id FROM games WHERE title = %s))''',(game_info['genres'][j],game_info['title']))   
           
            for j in range(len(game_info['developers'])):
                try:
                    self.cur.execute('''INSERT INTO developers (developer) VALUES (%s)''',(game_info['developers'][j],))
                except pg2.errors.UniqueViolation:
                    pass
                print("j")
                self.cur.execute('''INSERT INTO game_developers (developer_id, game_id) VALUES ((SELECT developer_id FROM developers WHERE developer = %s),(SELECT game_id FROM games WHERE title = %s))''',(game_info['developers'][j],game_info['title']))
                    
            for j in range(len(game_info['publishers'])):
                try:
                    self.cur.execute('''INSERT INTO publishers (publisher) VALUES (%s)''',(game_info['publishers'][j],))
                except pg2.errors.UniqueViolation:
                    pass
              
                self.cur.execute('''INSERT INTO game_publishers (publisher_id, game_id) VALUES ((SELECT publisher_id FROM publishers WHERE publisher = %s),(SELECT game_id FROM games WHERE title = %s))''',(game_info['publishers'][j],game_info['title']))
            """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""        
    def close_database(self):
         self.conn.close()   