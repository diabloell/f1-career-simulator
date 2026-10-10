import random

from data import (
    drivers,
    teams,
    car_performance,
    race_points_list,
    GrandPrix_list,
)


def simulate_race(drivers, car_performance):
    race_results = {}
    for pilot in drivers:
        car_power = car_performance[drivers[pilot]["team_name"]]
        result = 0.3*drivers[pilot]["pace"] + 0.5*car_power + random.uniform(-5, 5)
        race_results[pilot] = result
    race_results = dict(sorted(race_results.items(), key=lambda item: item[1], reverse=True))
    award_points(race_results, drivers)
    return race_results

def award_points(race_results, drivers):
    for place, pilot in enumerate(race_results):
        if place < len(race_points_list):
            drivers[pilot]['total_score'] += race_points_list[place]


def constructor_standings(teams, drivers):
    teams_total_score = {"Mercedes": 0,
    "Ferrari": 0,
    "McLaren": 0,
    "Red Bull": 0,
    "Racing Bulls": 0,
    "Alpine": 0,
    "Haas": 0,
    "Audi": 0,
    "Williams": 0,
    "Aston Martin": 0,
    "Cadillac": 0}
    for team in teams:
        for pilot in teams[team]:
            teams_total_score[team]+=drivers[pilot]['total_score']
    return dict(sorted(teams_total_score.items(), key = lambda item: item[1], reverse = True))

def podiums_of_each_race():
    print('The Podium Of Each Race: ')
    print()
    for race, pilots in race_history.items():
        print(f'{race}: first - {list(pilots)[0]}, second - {list(pilots)[1]}, third - {list(pilots)[2]}')
    print()

def winner_of_each_race():
    print('The Winner Of Each Race: ')
    for race, pilots in race_history.items():
        print(f'{race}: first - {list(pilots)[0]}')

def show_championship_after_race(race_name):
    for race in championship_history:
        if race_name == race:
            print(f'Championship after {race}')
            print()
            standings = sorted(
                championship_history[race].items(),
                key=lambda item: item[1],
                reverse=True
            )
            for place, (pilot, score) in enumerate(standings, 1):
                print(f'{place:>2}. {pilot:<22}    {score:>3} pts')

race_history = {}
championship_history = {}

for name_of_track in GrandPrix_list:
    current_race = simulate_race(drivers, car_performance)
    race_history[name_of_track] = current_race
    championship_history[name_of_track] = {pilot: drivers[pilot]["total_score"]
    for pilot in drivers}

championship = sorted(
    drivers.items(),
    key=lambda item: item[1]["total_score"],
    reverse=True)

print()
print(f'--- The World Champion 2026 is {championship[0][0]} ---')
print()
print(f'--- The Winner of Constructor Standings 2026 is {list(constructor_standings(teams, drivers))[0]}---')
print()

for place, (pilot, stats) in enumerate(championship, 1):
    print(f"{place:>2}. {pilot:<22}    {stats['total_score']:>3} pts")
print()
podiums_of_each_race()
show_championship_after_race('Monaco Grand Prix')


