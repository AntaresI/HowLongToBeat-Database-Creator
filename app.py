

from flask import Flask, request, jsonify
import psycopg2 as pg2
app = Flask(__name__)


conn = pg2.connect(
database = 'howlongtobeat_games_list',
user = "postgres",
host = "localhost",
password = "password"    
)

@app.get("/")
def home():
    return "Connected"


@app.route("/api/game", methods=["POST"])
def add_game():
    game_info = request.get_json()
    title = game_info["title"]
    with conn:
        with conn.cursor() as cursor:
            cursor.execute('''INSERT INTO games (title, description, off_or_on, logging, backlogs, replays, retired_percent,\
                    rating_percent, beat, main_story, main_and_extras, completionist, all_styles,\
                    single_player , co_op, versus, eu_release, na_release, jp_release) VALUES\
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,(SELECT TO_DATE(%s,'Month DD, YYYY')),\
                     (SELECT TO_DATE(%s,'Month DD, YYYY')),(SELECT TO_DATE(%s,'Month DD, YYYY'))) RETURNING game_id''',(game_info['title'], game_info['description'], game_info['online'], game_info['log_statistics'][0],\
                       game_info['log_statistics'][1], game_info['log_statistics'][2], \
                       game_info['log_statistics'][3],\
                       game_info['log_statistics'][4], game_info['log_statistics'][5], \
                       game_info['durations']['Main Story'],\
                       game_info['durations']['Main + Extras'], game_info['durations']['Completionist'],\
                       game_info['durations']['All Styles'], game_info['durations']['Single-Player'],\
                       game_info['durations']['Co-Op'], game_info['durations']['Vs.'], 
                       game_info['releases']['EU'], game_info['releases']['NA'], game_info['releases']['JP']))
            game_id = cursor.fetchone()[0]
    return {"id": game_id, "Title": title, "message": f"Game {title} added."}, 201


SELECT_ALL_USERS = "SELECT * FROM users;"


@app.route("/api/game", methods=["GET"])
def get_all_games():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM games")
            games = cursor.fetchall()
            if games:
                result = []
                for game in games:
                    result.append({"game_id": game[0], "title": game[1], "off_or_on": game[2], "description": game[3]\
                                   , "logging": game[4], "backlogs": game[5], "replays": game[6], "retired_percent": game[7]\
                                   , "rating_percent": game[8], "beat": game[9], "main_story": game[10],\
                                    "main_and_extras": game[11]\
                                   , "completionist": game[12], "all_styles": game[13],\
                                       "single_player": game[14], "co_op": game[15]\
                                    , "versus": game[16], "eu_release": game[17], "na_release": game[18],\
                                        "jp_release": game[19]
                                    })
                return jsonify(result)
            else:
                return jsonify({"error": f"Games not found."}), 404

@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,)) 
            user = cursor.fetchone()
            if user:
                return jsonify({"id": user[0], "name": user[1]})
            else:
                return jsonify({"error": f"User with ID {user_id} not found."}), 404