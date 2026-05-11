import pandas as pd

pd.set_option('display.max_columns', None)

video_list = ["video"]
def ranker(tournament):
    nan = pd.isna(tournament)
    if nan: 
        return 10
    t = tournament.lower().strip()
    if not t:
        return 10
    m = t.strip("-. ")
    if not m:
        return 10
    if t.startswith("showdown"):
        return 50
    elif t in video_list:
        return 25
    else:
        return 100

def load_champions_data(format_tag="Champions"):
    
    # data = pd.read_excel("VGCPastes_Repository.xlsx", 
    #                         sheet_name="Champions M-A",
    #                         header=2)
    data = pd.read_csv("https://docs.google.com/spreadsheets/d/1axlwmzPA49rYkqXh7zHvAtSP-TKbM0ijGYBPRflLSWw/gviz/tq?tqx=out:csv&gid=791705272",
                            header=2)



    vgc_data = data[["Team ID", "Full Name", "Pokepaste", "Tournament / Event", "Rank"]].copy()

    vgc_data["Point System"] = vgc_data["Tournament / Event"].apply(ranker)

    scrapper = vgc_data.to_dict(orient="records")

    for record in scrapper:
        record["format"] = format_tag
    
    return scrapper

def load_SV_data(format_tag="Scarlet/Violet"):
    data_sv = pd.read_csv("https://docs.google.com/spreadsheets/d/1axlwmzPA49rYkqXh7zHvAtSP-TKbM0ijGYBPRflLSWw/gviz/tq?tqx=out:csv&gid=972834435",
                            header=2)

    sv_data = data_sv[["Team ID", "Full Name", "Pokepaste", "Tournament / Event", "Rank"]].copy()

    sv_data["Point System"] = sv_data["Tournament / Event"].apply(ranker)

    scrapper_sv = sv_data.to_dict(orient="records")

    for record in scrapper_sv:
        record["format"] = format_tag
    
    return scrapper_sv

def load_Reg_data(format_tag="Scarlet/Violet"):
    data_reg = pd.read_csv("https://docs.google.com/spreadsheets/d/1axlwmzPA49rYkqXh7zHvAtSP-TKbM0ijGYBPRflLSWw/gviz/tq?tqx=out:csv&gid=1863148622",
                            header=2)

    reg_data = data_reg[["Team ID", "Full Name", "Pokepaste", "Tournament / Event", "Rank"]].copy()

    reg_data["Point System"] = reg_data["Tournament / Event"].apply(ranker)

    scrapper_reg = reg_data.to_dict(orient="records")

    for record in scrapper_reg:
        record["format"] = format_tag
    
    return scrapper_reg