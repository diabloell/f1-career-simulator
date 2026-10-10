import random

from data import (
    drivers,
    teams,
    car_performance,
    race_points_list,
    GrandPrix_list,
    race_history
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
    for race, pilots in race_history.items():
        print(f'{race}: first - {list(pilots)[0]}, second - {list(pilots)[1]}, third - {list(pilots)[2]}')

def winner_of_each_race():
    print('The Winner Of Each Race: ')
    for race, pilots in race_history.items():
        print(f'{race}: first - {list(pilots)[0]}')




for name_of_track in GrandPrix_list:
    current_race = simulate_race(drivers, car_performance)
    race_history[name_of_track] = current_race
championship = sorted(
    drivers.items(),
    key=lambda item: item[1]["total_score"],
    reverse=True)


print(f'--- The World Champion 2026 is {championship[0][0]} ---')
print(f'--- The Winner of Constructor Standings 2026 is {list(constructor_standings(teams, drivers))[0]}---')

for place, (pilot, stats) in enumerate(championship, 1):
    print(f"{place}. {pilot} — {stats['total_score']} points")

podiums_of_each_race()


