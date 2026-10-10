import random

from data import (
    drivers,
    teams,
    car_performance,
    race_points_list,
    GrandPrix_list,
    driver_names
)

race_history = {}
championship_history = {}
qualifying_history = {}


def test_championship():
    assert len(race_history) == len(GrandPrix_list)
    assert len(qualifying_history) == len(GrandPrix_list)
    assert len(championship_history) == len(GrandPrix_list)

    for race in GrandPrix_list:
        assert len(race_history[race]) == len(drivers)
        assert len(qualifying_history[race]) == len(drivers)
        assert len(championship_history[race]) == len(drivers)

    expected_points = sum(race_points_list) * len(GrandPrix_list)
    actual_points = sum(
        drivers[pilot]["total_score"]
        for pilot in drivers
    )

    assert actual_points == expected_points

    print("All tests passed!")


def simulate_race(drivers, car_performance, qualifying_results):
    race_results = {}
    starting_grid = {
        pilot: position
        for position, pilot in enumerate(qualifying_results, 1)
    }
    for pilot in drivers:
        car_power = car_performance[drivers[pilot]["team_name"]]

        start_position = starting_grid[pilot]
        qualifying_bonus = (11.5 - start_position) * 0.45

        result = (
                0.3 * drivers[pilot]["pace"]
                + 0.5 * car_power
                + random.uniform(-5, 5)
                + qualifying_bonus
        )

        race_results[pilot] = result
    race_results = dict(sorted(race_results.items(), key=lambda item: item[1], reverse=True))
    award_points(race_results, drivers, race_points_list)
    return race_results


def award_points(race_results, drivers, race_points_list):
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
            teams_total_score[team] += drivers[pilot]['total_score']
    return dict(sorted(teams_total_score.items(), key=lambda item: item[1], reverse=True))


def podiums_of_each_race(race_history):
    print('The Podium Of Each Race:')
    print()
    for race, pilots in race_history.items():
        print(f'{race}: first - {list(pilots)[0]}, second - {list(pilots)[1]}, third - {list(pilots)[2]}')
    print()


def winner_of_each_race(race_history):
    print('The Winner Of Each Race:')
    for race, pilots in race_history.items():
        print(f'{race}: first - {list(pilots)[0]}')


def show_championship_after_race(race_name, championship_history):
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


def simulate_championship(drivers, car_performance, GrandPrix_list):
    for name_of_track in GrandPrix_list:
        qualifying_results = simulate_qualifying(drivers, car_performance)
        qualifying_history[name_of_track] = qualifying_results

        current_race = simulate_race(drivers, car_performance, qualifying_results)
        race_history[name_of_track] = current_race

        championship_history[name_of_track] = {
            pilot: drivers[pilot]["total_score"]
            for pilot in drivers
        }

    championship = sorted(
        drivers.items(),
        key=lambda item: item[1]["total_score"],
        reverse=True
    )
    return championship


def show_championship(championship, teams, drivers, race_history, championship_history):
    print()
    print(f'--- The World Champion 2026 is {championship[0][0]} ---')
    print()
    print(f'--- The Winner of Constructor Standings 2026 is {list(constructor_standings(teams, drivers))[0]} ---')
    print()

    for place, (pilot, stats) in enumerate(championship, 1):
        print(f"{place:>2}. {pilot:<22}    {stats['total_score']:>3} pts")

    print()
    podiums_of_each_race(race_history)
    show_championship_after_race('Monaco Grand Prix', championship_history)


def simulate_qualifying(drivers, car_performance):
    qualifying_results = {}
    for pilot in drivers:
        car_power = car_performance[drivers[pilot]["team_name"]]
        qualifying_score = 0.35 * drivers[pilot]['pace'] + 0.65 * car_power + random.uniform(-3, 3)
        qualifying_results[pilot] = qualifying_score
    return dict(sorted(qualifying_results.items(), key=lambda item: item[1], reverse=True))


def show_race_results(name_of_race, qualifying_results, race_results):
    starting_grid = {
        pilot: position
        for position, pilot in enumerate(qualifying_results, 1)
    }

    print(f'\n{name_of_race}')
    print(f'Pos  Driver                   Grid   Change')

    for finish_position, r_name in enumerate(race_results, 1):
        start_position = starting_grid[r_name]
        change = start_position - finish_position

        print(f'{finish_position:>3}  {r_name:<24} {start_position:>3}    {change:+}')


def count_wins(race_history, driver_names):
    counter = {}
    for pilot in driver_names:
        wins = 0
        for race in race_history:
            if pilot == list(race_history[race])[0]:
                wins += 1
        counter[pilot] = wins
    return dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))


def count_poles(qualifying_history, driver_names):
    counter = {}
    for pilot in driver_names:
        poles = 0
        for race in qualifying_history:
            if pilot == list(qualifying_history[race])[0]:
                poles += 1
        counter[pilot] = poles
    return dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))


def count_pole_to_win(race_history, qualifying_history):
    counter = 0
    total_races = len(race_history)
    for race in race_history:
        if list(race_history[race])[0] == list(qualifying_history[race])[0]:
            counter += 1
    print(f'Pole-to-win conversions: {counter} / {total_races} ({round(counter * 100 / total_races, 1)}%)')


championship2026 = simulate_championship(drivers, car_performance, GrandPrix_list)

show_championship(championship2026, teams, drivers, race_history, championship_history)

print(qualifying_history['Monaco Grand Prix'])
show_race_results('Monaco Grand Prix', qualifying_history['Monaco Grand Prix'], race_history['Monaco Grand Prix'])
print(race_history)
print(count_wins(race_history, driver_names))
print(count_poles(qualifying_history, driver_names))
print(qualifying_history)
count_pole_to_win(race_history, qualifying_history)
test_championship()
