import requests as rq
from bs4 import BeautifulSoup  


URL = "https://limitlessvgc.com/teams/"

def sparser(id):
    current_url = URL + str(id)
    try:
        link = rq.get(current_url, timeout=10)
        link.raise_for_status()
    except rq.exceptions.RequestException as exc:
        print(f"Request failed for {current_url}: {exc}")
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

    for t in div_tournament:
        tournament = t.find('ul')
        tournament_entries = []
        for li in tournament.find_all('li'):
            links = li.find_all('a')
            tournament_name = "Unknown"
            player_name = "Unknown"
            
            for link in links:
                href = link.get('href', '')
                if href.startswith('/tournaments/'):
                    tournament_name = link.text.strip()
                elif href.startswith('/players/'):
                    player_name = link.text.strip()
            
            tournament_entries.append({
                "tournament": tournament_name,
                "player": player_name
            })

        
    return {
        "Url": current_url,
        "Team": team,
        "Tournament Info": tournament_entries or ["No tournament data"],
    }

print(sparser(253))