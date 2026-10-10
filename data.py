race_points_list = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
GrandPrix_list = [
    'Australian Grand Prix',
    'Chinese Grand Prix',
    'Japanese Grand Prix',
    'Miami Grand Prix',
    'Canadian Grand Prix',
    'Monaco Grand Prix',
    'Barcelona Grand Prix',
    'Austrian Grand Prix',
    'British Grand Prix',
    'Belgian Grand Prix',
    'Hungarian Grand Prix',
    'Dutch Grand Prix',
    'Italian Grand Prix',
    'Spanish Grand Prix',
    'Azerbaijan Grand Prix',
    'Bahrain Grand Prix',
    'Singapore Grand Prix',
    'United States Grand Prix',
    'Mexico City Grand Prix',
    'Brazilian Grand Prix',
    'Las Vegas Grand Prix',
    'Qatar Grand Prix',
    'Abu Dhabi Grand Prix',
]

driver_names = [
    "George Russell",
    "Kimi Antonelli",
    "Charles Leclerc",
    "Lewis Hamilton",
    "Lando Norris",
    "Oscar Piastri",
    "Max Verstappen",
    "Isack Hadjar",
    "Liam Lawson",
    "Arvid Lindblad",
    "Pierre Gasly",
    "Franco Colapinto",
    "Esteban Ocon",
    "Oliver Bearman",
    "Nico Hulkenberg",
    "Gabriel Bortoleto",
    "Carlos Sainz",
    "Alexander Albon",
    "Fernando Alonso",
    "Lance Stroll",
    "Sergio Perez",
    "Valtteri Bottas"
]
teams = {
    "Mercedes": ["George Russell", "Kimi Antonelli"],
    "Ferrari": ["Charles Leclerc", "Lewis Hamilton"],
    "McLaren": ["Lando Norris", "Oscar Piastri"],
    "Red Bull": ["Max Verstappen", "Isack Hadjar"],
    "Racing Bulls": ["Liam Lawson", "Arvid Lindblad"],
    "Alpine": ["Pierre Gasly", "Franco Colapinto"],
    "Haas": ["Esteban Ocon", "Oliver Bearman"],
    "Audi": ["Nico Hulkenberg", "Gabriel Bortoleto"],
    "Williams": ["Carlos Sainz", "Alexander Albon"],
    "Aston Martin": ["Fernando Alonso", "Lance Stroll"],
    "Cadillac": ["Sergio Perez", "Valtteri Bottas"]
}
skills = {"George Russell": {"pace": 94, "consistency": 94, "aggression": 76},
          "Kimi Antonelli": {"pace": 97, "consistency": 87, "aggression": 86},

          "Charles Leclerc": {"pace": 94, "consistency": 89, "aggression": 82},
          "Lewis Hamilton": {"pace": 96, "consistency": 91, "aggression": 79},

          "Lando Norris": {"pace": 96, "consistency": 93, "aggression": 74},
          "Oscar Piastri": {"pace": 94, "consistency": 91, "aggression": 81},

          "Max Verstappen": {"pace": 99, "consistency": 96, "aggression": 94},
          "Isack Hadjar": {"pace": 88, "consistency": 82, "aggression": 88},

          "Liam Lawson": {"pace": 83, "consistency": 80, "aggression": 86},
          "Arvid Lindblad": {"pace": 84, "consistency": 74, "aggression": 84},

          "Pierre Gasly": {"pace": 89, "consistency": 88, "aggression": 81},
          "Franco Colapinto": {"pace": 82, "consistency": 77, "aggression": 87},

          "Esteban Ocon": {"pace": 85, "consistency": 84, "aggression": 88},
          "Oliver Bearman": {"pace": 87, "consistency": 82, "aggression": 85},

          "Nico Hulkenberg": {"pace": 87, "consistency": 91, "aggression": 73},
          "Gabriel Bortoleto": {"pace": 86, "consistency": 84, "aggression": 79},

          "Carlos Sainz": {"pace": 91, "consistency": 93, "aggression": 77},
          "Alexander Albon": {"pace": 88, "consistency": 88, "aggression": 78},

          "Fernando Alonso": {"pace": 93, "consistency": 95, "aggression": 90},
          "Lance Stroll": {"pace": 79, "consistency": 76, "aggression": 75},

          "Sergio Perez": {"pace": 83, "consistency": 82, "aggression": 75},
          "Valtteri Bottas": {"pace": 85, "consistency": 89, "aggression": 69}}
car_performance = {
    "Mercedes": 98,
    "Ferrari": 96,
    "McLaren": 94,
    "Red Bull": 95,
    "Racing Bulls": 90,
    "Alpine": 86,
    "Haas": 80,
    "Audi": 80,
    "Williams": 78,
    "Aston Martin": 73,
    "Cadillac": 70
}

drivers = {
    name: {
        "team_name": None,
        "total_score": 0,
        "pace": skills[name]['pace'],
        "consistency": skills[name]['consistency'],
        "aggression": skills[name]['aggression']
    }
    for name in driver_names
}

for team, players in teams.items():
    for player in players:
        drivers[player]["team_name"] = team
