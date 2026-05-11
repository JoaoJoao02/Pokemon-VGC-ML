import requests as rq
import time
import json
from itertools import chain
from Scraper import load_champions_data, load_Reg_data, load_SV_data

champ = load_champions_data()
reg = load_Reg_data()
sv = load_SV_data()

teams = list(chain(champ, reg, sv))


def identifier(line):

    if " @ " in line:
        return "name_item"
    elif line.startswith("Ability:"):
        return "ability"
    elif line.startswith("Tera Type:"):
        return "Tera Type"
    elif line.startswith("-"):
        return "moves"
    elif line.startswith("EVs:"):
        return "EVs"
    elif line.startswith("IVs:"):
        return "IVs"
    elif line.endswith("Nature"):
        return "nature"
    elif line.startswith("Level:"):
        return "level"
    elif line.startswith("Shiny:"):
        return "shiny"
    else:
        return "unknown"

def pokemon_parser(block, team_id, unknown_lines):

    lines = block.split('\r\n')

    name = None
    item = None
    ability = None
    tera_type = None
    moves = []
    IVS = {}
    EVS = {}
    nature = None

    # Handle the problem of Pokemons with no items
    if " @ " in lines[0]:
        name = lines[0].split(" @ ")[0]
        item = lines[0].split(" @ ")[1].strip()
    else:
        name = lines[0]


    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        line_type = identifier(line)
        if line_type == "ability":
            ability = line.split(": ")[1]
        elif line_type == "Tera Type":
            tera_type = line.split(": ")[1]
        elif line_type == "moves":
            split = line.split("- ")[1]
            moves.append(split)
        elif line_type == "IVs":
            iv = line.split(": ")[1]
            iv_split = iv.split(" / ")
            for i in iv_split:
                number = i.split(" ")[0]
                stat = i.split(" ")[1]
                try:
                    IVS[stat] = int(number)
                except:
                    print("IVs not parsed correctly")
                    continue
        elif line_type == "EVs":
            ev = line.split(": ")[1]
            ev_split = ev.split(" / ")
            for e in ev_split:
                number = e.split(" ")[0]
                stat = e.split(" ")[1]
                try:
                    EVS[stat] = int(number)
                except:
                    print("EVs not parsed correctly")
                    continue
        elif line_type == "nature":
            nature = line.split(" Nature")[0]
        elif line_type == "level":
            pass
        elif line_type == "shiny":
            pass
        else:
            unknown_lines.append({
            "team_id": team_id,
            "line": line
            })
        

    P1_dict = {
        "Pokemon": name,
        "Item": item,
        "Ability": ability,
        "Tera Type": tera_type,
        "EVs": EVS,
        "IVs": IVS,
        "Nature": nature,
        "Moves": moves
        }
        
    return P1_dict

seen_pokelinks = set()
unique_teams = []
for record in teams:
    pokelink = record["Pokepaste"]
    if pokelink not in seen_pokelinks:
        seen_pokelinks.add(pokelink)
        unique_teams.append(record)

teams = unique_teams

unknown_lines = []
all_teams = []
for record in teams:
    pokelink = record["Pokepaste"]
    if not pokelink.endswith("/json"):
        pokelink = pokelink.rstrip("/") + "/json"
    team = rq.get(pokelink, timeout=10)
    try:
        dic_team = team.json()
    except:
        print(f"Failed: {pokelink}")
        continue

    clean_team = dic_team["paste"].split('\r\n\r\n')

    pokemon_team = []
    for i in clean_team:
        if i:
            pokemon_team.append(pokemon_parser(i, record["Team ID"], unknown_lines))
    final_record = {
        "team_id": record["Team ID"],
        "player": record["Full Name"],
        "tournament": record["Tournament / Event"],
        "points": record["Point System"],
        "format": record["format"],
        "pokemon": pokemon_team
    }
    all_teams.append(final_record)
    time.sleep(1)

with open("teams.json", "w", encoding="utf-8") as f:
    json.dump(all_teams, f, indent=2, ensure_ascii=False)
print(f"Saved {len(all_teams)} teams")

with open("unknown_lines.json", "w", encoding="utf-8") as f:
    json.dump(unknown_lines, f, indent=2, ensure_ascii=False)
print(f"{len(unknown_lines)} unknown lines logged")

