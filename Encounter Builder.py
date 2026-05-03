# D&D Encounter Generator

#Imports
import json, re, random

#Global variables
party_size = 0
party_level = 0
desired_difficulty = 0
party_xp_threshold = 0

def load_monsters(): #Load monsters list from JSON file
    with open("monsters.json") as monsters_file:
         return json.load(monsters_file)

def load_difficulty_table(): #Load difficulty table from JSON file
    with open("difficulty_table.json") as difficulty_table_file:
        return json.load(difficulty_table_file)

def get_party_info(): # Define party size variable for encounter
    try:
        global party_size
        global party_level
        global desired_difficulty

        print("Define Party Info")
        party_size = int(input("\tEnter the size of the party (1-10): "))
        party_level = int(input("\tEnter the average level of the party (rounded down) (1-20): "))
        desired_difficulty = int(input("\tEnter the desired difficulty (1-4): "))

        if party_size <= 0 or party_level <= 0 or desired_difficulty <= 0:
            raise ValueError("One or more inputs contained a number that is less than or equal to 0")

        if party_size > 10 or party_level > 20 or desired_difficulty > 4:
            raise ValueError("One or more inputs contained a number that is greater than the allowed maximum")

        print("\n")
    except ValueError as e:
        print("Input was invalid.")
        print(e)
        exit()

def filter_monsters(monsters): #Extract XP value and filter based on party threshold value
    global party_xp_threshold
    min_xp = party_xp_threshold * .9
    max_xp = party_xp_threshold * 1.1
    monsters_filtered = []

    def get_xp(monster): #Regex search for XP embedded in Challenge field
        challenge = monster["Challenge"]
        xp = re.search(r"\(([\d,]+)\s*XP\)", challenge)
        return int(xp.group(1).replace(",", ""))

    while len(monsters_filtered) == 0:
        for m in monsters:
            if min_xp <= get_xp(m) <= max_xp:
                monsters_filtered.append(m)

        min_xp = min_xp * .9 #First pass is the closest match, this expands search criteria to match a lower CR creature if needed.

    return monsters_filtered

def calculate_difficulty(difficulty_table): #Calc difficulty using party size and difficulty table
    global party_xp_threshold

    party_xp_threshold = party_size * difficulty_table[party_level - 1][desired_difficulty - 1]

def generate_encounter(monsters): # Randomly select encounter from filtered list
    max_range = len(monsters)

    if max_range > 1:
        i = random.randint(1, max_range)
    else:
        i = 1

    return monsters[i - 1]

def display_encounter_details(selected_monster): # Print monster details
    print("Generated Encounter Details")

    print(f"\n\t{'Party Size':<10}: {party_size}")
    print(f"\t{'Party Level (Avg)':<10}: {party_level}")
    print(f"\t{'Desired Difficulty':<10}: {desired_difficulty}")
    print(f"\t{'XP Range':<10}: {round(party_xp_threshold * .9)} - {round(party_xp_threshold * 1.1)}\n\t *An expanded XP range may be used if no suitable combatant is found*")

    print(f"\n\t{'Name:':<20} {selected_monster['name']}")
    print(f"\t{'Race/Alignment:':<20} {selected_monster['meta']}")
    print(f"\t{'Armor Class:':<20} {selected_monster['Armor Class']}")
    print(f"\t{'Hit Points:':<20} {selected_monster['Hit Points']}")
    print(f"\t{'Challenge:':<20} {selected_monster['Challenge']}")

    print("\n\tStats:")
    print(f"\t\tSTR: {selected_monster['STR']:<5} {selected_monster['STR_mod']}")
    print(f"\t\tDEX: {selected_monster['DEX']:<5} {selected_monster['DEX_mod']}")
    print(f"\t\tCON: {selected_monster['CON']:<5} {selected_monster['CON_mod']}")
    print(f"\t\tINT: {selected_monster['INT']:<5} {selected_monster['INT_mod']}")
    print(f"\t\tWIS: {selected_monster['WIS']:<5} {selected_monster['WIS_mod']}")
    print(f"\t\tCHA: {selected_monster['CHA']:<5} {selected_monster['CHA_mod']}")

    print("\n\tDetails:")
    print(f"\t\t{'Skills:':<15} {selected_monster.get('Skills', 'None')}")
    print(f"\t\t{'Senses:':<15} {selected_monster.get('Senses', 'None')}")
    print(f"\t\t{'Languages:':<15} {selected_monster.get('Languages', 'None')}")
    print(f"\t\t{'Resistances:':<15} {selected_monster.get('Damage Resistances', 'None')}")
    print(f"\t\t{'Immunities:':<15} {selected_monster.get('Damage Immunities', 'None')}")

def save_encounter(selected_monster): # Prompt user to save encounter character sheet
    save = ""

    while save.lower() != "y" and save.lower() != "n":
        save = input("\nWould you like to save this encounter? (y/n): ")
        if save.lower() != "y" and save.lower() != "n":
            print("Please enter 'y' or 'n'")

    if save.lower() == "y":
        print("Saving encounter details...")
        generate_html(selected_monster)

def generate_html(selected_monster): # Generate html character sheet of the selected monster
    content = \
    f"""
        <html>
            <head>
                <title>{selected_monster['name']}</title>
                <style>
                    body {{ font-family: Arial; margin: 20px; background: #F0e7d8}}
                    h1 {{ border-bottom: 2px solid black; }}
                    img {{ max-width: 300px; }}
                </style>
            </head>
            <body>
                <h1>{selected_monster['name']}</h1>
                <p><strong>{selected_monster['meta']}</strong></p>
                
                <img src="{selected_monster['img_url']}" alt="{selected_monster['name']}">
                
                <h2>Stats</h2>
                <p><strong>Armor Class:</strong> {selected_monster['Armor Class']}</p>
                <p><strong>Hit Points:</strong> {selected_monster['Hit Points']}</p>
                <p><strong>Speed:</strong> {selected_monster['Speed']}</p>
                
                <h2>Abilities</h2>
                <p>STR: {selected_monster['STR']} {selected_monster['STR_mod']}</p>
                <p>DEX: {selected_monster['DEX']} {selected_monster['DEX_mod']}</p>
                <p>CON: {selected_monster['CON']} {selected_monster['CON_mod']}</p>
                <p>INT: {selected_monster['INT']} {selected_monster['INT_mod']}</p>
                <p>WIS: {selected_monster['WIS']} {selected_monster['WIS_mod']}</p>
                <p>CHA: {selected_monster['CHA']} {selected_monster['CHA_mod']}</p>
                
                
                <h2>Details</h2>
                <p><strong>Saving Throws:</strong> {selected_monster.get('Saving Throws', 'None')}</p>
                <p><strong>Skills:</strong> {selected_monster.get('Skills', 'None')}</p>
                <p><strong>Senses:</strong> {selected_monster.get('Senses', 'None')}</p>
                <p><strong>Languages:</strong> {selected_monster.get('Languages', 'None')}</p>
                <p><strong>Challenge:</strong> {selected_monster.get('Challenge', 'None')}</p>
                <p><strong>Damage Resistances:</strong> {selected_monster.get('Damage Resistances', 'None')}</p>
                <p><strong>Damage Immunities:</strong> {selected_monster.get('Damage Immunities', 'None')}</p>
                <p><strong>Condition Immunities:</strong> {selected_monster.get('Condition Immunities', 'None')}</p>
                
                <h2>Traits</h2>
                {selected_monster['Traits']}
            
                <h2>Actions</h2>
                {selected_monster['Actions']}
            </body>
        </html>
    """

    with open(f"{selected_monster['name']}.html", "w", encoding="utf-8") as file:
        file.write(content)

def __main__():
    #Load JSON files
    monsters = load_monsters()
    difficulty_table = load_difficulty_table()

    # Main program flow
    get_party_info()
    calculate_difficulty(difficulty_table)
    monsters = filter_monsters(monsters)
    selected_monster = generate_encounter(monsters)
    display_encounter_details(selected_monster)
    save_encounter(selected_monster)

__main__()
