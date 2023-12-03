import requests
import json
import pandas as pd
import psycopg2
from configparser import ConfigParser

def fetch_monster_list():
    monster_list = []
    monster_df = pd.DataFrame()
    monster_json = []

    try:
        monsters_api_response = requests.get("https://www.dnd5eapi.co/api/monsters")
        monsters_api_root_data = monsters_api_response.content

        monsters_list = json.loads(monsters_api_root_data)
        monsters_index = monsters_list['results']

        for monster_index_item in monsters_index:
            monster_index_name = monster_index_item['name']
            monster_index_api_path = monster_index_item['url']

            try:

                print("Fetchng details for %s..." % monster_index_name)

                monster_details_response = requests.get("https://www.dnd5eapi.co%s" % monster_index_api_path)
                monster_details = json.loads(monster_details_response.content)
                
                monster_name = monster_details['name']
                monster_size = monster_details['size']
                monster_type = monster_details['type']
                monster_alignment = monster_details['alignment']
                monster_ac = monster_details['armor_class']
                monster_hp = monster_details['hit_points']
                monster_hp_roll = monster_details['hit_points_roll']
                monster_speed = monster_details['speed']
                monster_str = monster_details['strength']
                monster_dex = monster_details['dexterity']
                monster_con = monster_details['constitution']
                monster_int = monster_details['intelligence']
                monster_wis = monster_details['wisdom']
                monster_cha = monster_details['charisma']
                monster_proficiencies = monster_details['proficiencies']
                monster_dmg_vuln = monster_details['damage_vulnerabilities']
                monster_dmg_res = monster_details['damage_resistances']
                monster_dmg_imm = monster_details['damage_immunities']
                monster_cond_imm = monster_details['condition_immunities']
                monster_senses = monster_details['senses']
                monster_languages = monster_details['languages']
                monster_cr = monster_details['challenge_rating']
                monster_xp = monster_details['xp']
                monster_special_abilities = monster_details['special_abilities']
                monster_actions = monster_details['actions']

                try:
                    monster_json.append({
                        "name": monster_name,
                        "size": monster_size,
                        "type": monster_type,
                        "alignment": monster_alignment,
                        "ac": monster_alignment,
                        "hp": monster_hp,
                        "hp_roll": monster_hp_roll,
                        "speed": monster_speed,
                        "str": monster_str,
                        "dex": monster_dex,
                        "con": monster_con,
                        "int": monster_int,
                        "wis": monster_wis,
                        "cha": monster_cha,
                        "proficiencies": monster_proficiencies,
                        "dmg_vuln": monster_dmg_vuln,
                        "dmg_res": monster_dmg_res,
                        "dmg_imm": monster_dmg_imm,
                        "cond_imm": monster_cond_imm,
                        "senses": monster_senses,
                        "languages": monster_languages,
                        "cr": monster_cr,
                        "xp": monster_xp,
                        "special_abilities": monster_special_abilities,
                        "action": monster_actions
                    })

                except Exception as error:
                    print("Error importing JSON data: %s" % error)

            except:
                print("Error fetching details for %s" % monster_index_name)

    except:
        print("Error fetching monster list from the API.")

    return monster_json

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()

    parser.read(filename)

    db = {}

    if parser.has_section(section):
        params = parser.items(section)

        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    
    return db

def update_db(monster_json):
    conn = None
    monster_list = json.loads(monster_json)

    print(monster_json)

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        print('PostgreSQL database version:')

        cur.execute('SELECT version()')

        db_version = cur.fetchone()

        print(db_version)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

#fetch_monster_list()
update_db(fetch_monster_list())
