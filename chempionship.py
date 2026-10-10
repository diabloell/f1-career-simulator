import random


def simulate_race(drivers, car_performance):
    race_results = {}
    for pilot in drivers:
        car_power = car_performance[drivers[pilot]["team_name"]]
        result = 0.3*drivers[pilot]["pace"] + 0.7*car_power + random.uniform(-5, 5)
        race_results[pilot] = result
    race_results = dict(sorted(race_results.items(), key=lambda item: item[1], reverse=True))
    award_points(race_results, drivers)
    return race_results

def award_points(race_results, drivers):
    for place, pilot in enumerate(race_results):
        if place < len(race_points):
            drivers[pilot]['total_score'] += race_points[place]



race_points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
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
    "Ferrari": 94,
    "McLaren": 92,
    "Red Bull": 92,
    "Racing Bulls": 83,
    "Alpine": 81,
    "Haas": 76,
    "Audi": 74,
    "Williams": 72,
    "Aston Martin": 69,
    "Cadillac": 65
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

for _ in range(23):
    simulate_race(drivers, car_performance)
championship = sorted(
    drivers.items(),
    key=lambda item: item[1]["total_score"],
    reverse=True
)
print(f'--- The World Chempion of 2026 is {championship[0][0]} ---')
for place, (pilot, stats) in enumerate(championship, 1):
    print(f"{place}. {pilot} — {stats['total_score']} points")


