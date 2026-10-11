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
skills = {
    "George Russell": {"pace": 94, "consistency": 94, "aggression": 76, "skill": 94},
    "Kimi Antonelli": {"pace": 95, "consistency": 87, "aggression": 86, "skill": 89},

    "Charles Leclerc": {"pace": 95, "consistency": 89, "aggression": 82, "skill": 95},
    "Lewis Hamilton": {"pace": 96, "consistency": 91, "aggression": 79, "skill": 97},

    "Lando Norris": {"pace": 95.7, "consistency": 93, "aggression": 74, "skill": 94},
    "Oscar Piastri": {"pace": 94, "consistency": 91, "aggression": 81, "skill": 93},

    "Max Verstappen": {"pace": 96.3, "consistency": 96,"aggression": 94,"skill": 99},
    "Isack Hadjar": {"pace": 90, "consistency": 82, "aggression": 88, "skill": 86},

    "Liam Lawson": {"pace": 83, "consistency": 80, "aggression": 86, "skill": 83},
    "Arvid Lindblad": {"pace": 84, "consistency": 74, "aggression": 84, "skill": 78},

    "Pierre Gasly": {"pace": 89, "consistency": 88, "aggression": 81, "skill": 90},
    "Franco Colapinto": {"pace": 82, "consistency": 77, "aggression": 87, "skill": 81},

    "Esteban Ocon": {"pace": 85, "consistency": 84, "aggression": 88, "skill": 86},
    "Oliver Bearman": {"pace": 87, "consistency": 82, "aggression": 85, "skill": 86},

    "Nico Hulkenberg": {"pace": 87, "consistency": 91, "aggression": 73, "skill": 91},
    "Gabriel Bortoleto": {"pace": 86, "consistency": 84, "aggression": 79, "skill": 85},

    "Carlos Sainz": {"pace": 91, "consistency": 93, "aggression": 77, "skill": 93},
    "Alexander Albon": {"pace": 88, "consistency": 88, "aggression": 78, "skill": 90},

    "Fernando Alonso": {"pace": 93, "consistency": 95, "aggression": 90, "skill": 98},
    "Lance Stroll": {"pace": 79, "consistency": 76, "aggression": 75, "skill": 76},

    "Sergio Perez": {"pace": 83, "consistency": 82, "aggression": 75, "skill": 87},
    "Valtteri Bottas": {"pace": 85, "consistency": 89, "aggression": 69, "skill": 91}
}
car_performance = {
    "Mercedes": 96.8,
    "Ferrari": 96,
    "McLaren": 96,
    "Red Bull": 96,
    "Racing Bulls": 90,
    "Alpine": 86,
    "Haas": 80,
    "Audi": 80,
    "Williams": 78,
    "Aston Martin": 73,
    "Cadillac": 70
}
car_reliability = {
    "Mercedes": 97,
    "Ferrari": 95,
    "McLaren": 96,
    "Red Bull": 95,
    "Racing Bulls": 91,
    "Alpine": 89,
    "Haas": 88,
    "Audi": 87,
    "Williams": 89,
    "Aston Martin": 86,
    "Cadillac": 82
}
drivers = {
    name: {
        "team_name": None,
        "total_score": 0,
        "pace": skills[name]['pace'],
        "consistency": skills[name]['consistency'],
        "aggression": skills[name]['aggression'],
        "skill": skills[name]['skill']
    }
    for name in driver_names
}

for team, players in teams.items():
    for player in players:
        drivers[player]["team_name"] = team
pilot_stats = {pilot: {
    "wins": 0,
    "poles": 0,
    "podiums": 0,
    "mistakes": 0,
    "dnfs": 0,
    "technical_dnfs": 0,
    "crash_dnfs": 0
} for pilot in driver_names}