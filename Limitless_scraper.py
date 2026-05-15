import requests as rq
from bs4 import BeautifulSoup  
import time
import json


URL_teams = "https://limitlessvgc.com/teams/"
URL_tournaments = "https://limitlessvgc.com/tournaments/"
format_cache = {}

def format_sparser(id):
    tournament_url = URL_tournaments + str(id)
    try:
        link = rq.get(tournament_url, timeout=10)
        link.raise_for_status()
    except rq.exceptions.RequestException as exc:
        print(f"Request failed for {tournament_url}: {exc}")
        return None
    
    soup = BeautifulSoup(link.text, "html.parser")
    div_format = soup.find_all('div', class_="infobox-line")
    format_name = "Unknown"
    for form in div_format:
        if form.a:
            format_name = form.a.text

    return format_name




def sparser(id):
    team_url = URL_teams + str(id)
    try:
        link = rq.get(team_url, timeout=10)
        link.raise_for_status()
    except rq.exceptions.RequestException as exc:
        print(f"Request failed for {team_url}: {exc}")
        return None

    soup = BeautifulSoup(link.text, "html.parser")
    div_pkmn = soup.find_all('div', class_ = "pkmn")
    div_tournament = soup.find_all('div', class_ = "teamlist-results")

    team = []
    for pokemon in div_pkmn:
        name = "Unknown"
        item = pokemon.find('div', class_="item")
        ability = pokemon.find('div', class_="ability")
        tera = pokemon.find('div', class_="tera")
        moves = pokemon.find('ul', class_="moves")

        name_div = pokemon.find('div', class_="name")
        name = name_div.a.text.strip() if name_div and name_div.a else "Unknown"

        item_text = item.text.strip() if item else "No Item"
        ability_text = ability.text.strip() if ability else "No Ability"
        a_split = ability_text.split("Ability: ")[1].strip() if "Ability: " in ability_text else ability_text
        tera_text = tera.text.strip() if tera else "No Tera"
        t_split = tera_text.split("Tera Type:")[1].strip() if "Tera Type: " in tera_text else tera_text
        move_list = [m.text.strip() for m in moves.find_all("li")] if moves else []

        team.append({
            "Pokemon": name,
            "Item": item_text,
            "Ability": a_split,
            "Tera Type": t_split,
            "Moves": move_list or ["No moves"]
        })

    tournament_entries = []
    for t in div_tournament:
        tournament = t.find('ul')
        for li in tournament.find_all('li'):
            links = li.find_all('a')
            tournament_name = "Unknown"
            player_name = "Unknown"
            
            
            for link in links:
                href = link.get('href', '')
                if href.startswith('/tournaments/'):
                    tournament_id = href.split('tournaments/')[1]
                    if tournament_id not in format_cache:
                        format_cache[tournament_id] = format_sparser(tournament_id)
                    format_name = format_cache[tournament_id]
                    if ',' in link.text.strip():
                        tournament_name = link.text.split(',')[0].strip()
                    else:
                        tournament_name = link.text.strip()
                elif href.startswith('/players/'):
                    player_name = link.text.strip()
            
            tournament_entries.append({
                "tournament": tournament_name,
                "player": player_name,
                "format": format_name,
                "Points": 100
            })

    records = []
    for entry in tournament_entries:
        records.append({
            "team_id": "L" + str(id),
            "player": entry["player"],
            "tournament": entry["tournament"],
            "format": entry["format"],
            "points": entry["Points"],
            "pokemon": team
        })

        
    return records

all_teams = []
wanted_format = ["S & V", "S / V", "S&V", "S/V", "Scarlet", "Champions"]
last_id_seen = 6285
new_id = 1
for team_id in range(new_id, last_id_seen + 1):
    record = sparser(team_id)
    if record != None: 
        for entry in record:
            if any(f in entry["format"] for f in wanted_format):
                all_teams.append(entry)

    if team_id % 100 == 0:
        print(f"Progress: {team_id}/{last_id_seen} - {len(all_teams)} teams collected")
 
    if team_id % 500 == 0:
        with open("limitless_teams.json", "w", encoding="utf-8") as f:
            json.dump(all_teams, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(all_teams)} teams")

    time.sleep(1)

with open("limitless_teams.json", "w", encoding="utf-8") as f:
    json.dump(all_teams, f, indent=2, ensure_ascii=False)
print(f"Saved {len(all_teams)} teams")