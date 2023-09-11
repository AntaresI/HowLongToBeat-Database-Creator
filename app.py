
from flask import Flask, request, jsonify
import psycopg2 as pg2
import os

app = Flask(__name__)
url = os.getenv("DATABASE_URL")

conn = pg2.connect(url)

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
                     (SELECT TO_DATE(%s,'Month DD, YYYY')),(SELECT TO_DATE(%s,'Month DD, YYYY')))\
                        RETURNING game_id''',(game_info['title'], game_info['description'],\
                       game_info['off_or_on'], game_info['logging'],\
                       game_info['backlogs'], game_info['replays'], \
                       game_info['retired_percent'],\
                       game_info['rating_percent'], game_info['beat'], \
                       game_info['main_story'],\
                       game_info['main_and_extras'], game_info['completionist'],\
                       game_info['all_styles'], game_info['single_player'],\
                       game_info['co_op'], game_info['versus'], 
                       game_info['eu_release'], game_info['na_release'], game_info['jp_release']))
            game_id = cursor.fetchone()[0]
    return {"id": game_id, "Title": title, "message": f"Game {title} added."}, 201

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
                return jsonify({"error": "Games not found."}), 404

@app.route("/api/game/<int:game_id>", methods=["GET"])
def get_game(game_id):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM games WHERE game_id = %s", (game_id,)) 
            game = cursor.fetchone()
            if game:
                return jsonify({"game_id": game[0], "title": game[1], "off_or_on": game[2], "description": game[3]\
                               , "logging": game[4], "backlogs": game[5], "replays": game[6], "retired_percent": game[7]\
                               , "rating_percent": game[8], "beat": game[9], "main_story": game[10],\
                                "main_and_extras": game[11]\
                               , "completionist": game[12], "all_styles": game[13],\
                                   "single_player": game[14], "co_op": game[15]\
                                , "versus": game[16], "eu_release": game[17], "na_release": game[18],\
                                    "jp_release": game[19]
                                })
            else:
                return jsonify({"error": f"Game with ID {game_id} not found."}), 404
            
   
@app.route("/api/game/<int:game_id>", methods=["PUT"])
def update_game(game_id):
    game_info = request.get_json()
    UPDATE_GAME_BY_ID = '''UPDATE games SET {} WHERE game_id = %s'''.format(', '.join('{}=%s'.format(k) \
                    for k in game_info))     
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(UPDATE_GAME_BY_ID, (game_id,*game_info.values()))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Game with ID {game_id} not found."}), 404
    return jsonify({"id": game_id, "message": f"Game with ID {game_id} updated."})            



@app.route("/api/game/<int:game_id>", methods=["DELETE"])
def delete_game(game_id):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM games WHERE game_id = %s;", (game_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Game with ID {game_id} not found."}), 404
    return jsonify({"message": f"Game with ID {game_id} deleted."})            