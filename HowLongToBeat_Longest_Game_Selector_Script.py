
import psycopg2 as pg2

conn = pg2.connect(
database = 'howlongtobeat_games_list',
user = "postgres",
host = "localhost",
password = "password"    
)
conn.autocommit = True
cur = conn.cursor()

cur.execute("SELECT * FROM games WHERE backlogs>600 AND main_and_extras IS NOT NULL \
            ORDER BY main_and_extras DESC LIMIT 1")
            
longest_game = cur.fetchall()            
colnames = [desc[0] for desc in cur.description]      
for i in range(len(longest_game[0])):
    print(f"{colnames[i]}: {longest_game[0][i]}")      
    
    
cur.execute('''SELECT title, developer, publisher, genre, platform FROM game_developers JOIN \
developers ON game_developers.developer_id = developers.developer_id JOIN games ON \
game_developers.game_id = games.game_id JOIN game_publishers ON \
game_publishers.game_id = games.game_id JOIN publishers ON game_publishers.publisher_id\
= publishers.publisher_id JOIN game_genres ON \
game_genres.game_id = games.game_id JOIN genres ON game_genres.genre_id\
= genres.genre_id JOIN game_platforms ON \
game_platforms.game_id = games.game_id JOIN platforms ON game_platforms.platform_id\
= platforms.platform_id  WHERE title = (%s)''',(longest_game[0][colnames.index('title')],))
    
print("""""""""""""""""""")
longest_game_info = cur.fetchall()
colnames = [desc[0] for desc in cur.description]      
for i in range(len(longest_game_info[0])):
    print(f"{colnames[i]}: {longest_game_info[0][i]}")    
         