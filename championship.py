import random

from data import (
    drivers,
    teams,
    car_performance,
    race_points_list,
    GrandPrix_list,
    driver_names,
    pilot_stats,
    car_reliability
)

race_history = {}
championship_history = {}
qualifying_history = {}


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

        if driver_mistake(
            drivers[pilot]["consistency"],
            drivers[pilot]["skill"]
        ):
            result -= random.uniform(2, 5)
            pilot_stats[pilot]["mistakes"] += 1

        dnf_reason = get_dnf_reason(
            drivers[pilot]["aggression"],
            car_reliability[drivers[pilot]["team_name"]],
            drivers[pilot]["skill"]
        )

        if dnf_reason is not None:
            result = 0
            pilot_stats[pilot]["dnfs"] += 1

            if dnf_reason == "technical":
                pilot_stats[pilot]["technical_dnfs"] += 1
            elif dnf_reason == "crash":
                pilot_stats[pilot]["crash_dnfs"] += 1

        race_results[pilot] = result

    race_results = dict(sorted(
        race_results.items(),
        key=lambda item: item[1],
        reverse=True
    ))

    award_points(race_results, drivers, race_points_list)

    return race_results


def award_points(race_results, drivers, race_points_list):
    for place, pilot in enumerate(race_results):
        if place < len(race_points_list) and race_results[pilot] > 0:
            drivers[pilot]["total_score"] += race_points_list[place]


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
    print(qualifying_history['Monaco Grand Prix'])
    show_race_results('Monaco Grand Prix', qualifying_history['Monaco Grand Prix'], race_history['Monaco Grand Prix'])
    print()
    print(count_wins(race_history, driver_names))
    print(count_poles(qualifying_history, driver_names))
    count_pole_to_win(race_history, qualifying_history)
    print()
    print(f'{sum(stats["mistakes"] for stats in pilot_stats.values())} - mistakes')
    show_pilots_mistakes()
    print(f'{sum(stats["dnfs"] for stats in pilot_stats.values())} - dnfs')
    show_pilots_dnfs()
    show_pilots_dnf_details()


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

        if race_results[r_name] == 0:
            print(f'DNF  {r_name:<24} {start_position:>3}    -')
        else:
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


def driver_mistake(consistency, skill):
    mistake_chance = (100 - consistency) / 200
    skill_modifier = 1 - max(0, skill - 75) * 0.01
    mistake_chance *= skill_modifier
    return random.random() < mistake_chance


def technical_dnf(reliability):
    technical_chance = 0.028 + (100 - reliability) * 0.002
    return random.random() < technical_chance


def crash_dnf(aggression, skill):
    crash_base = 0.018 + max(0, aggression - 70) * 0.0018

    skill_modifier = 1 - max(0, skill - 75) * 0.012
    skill_modifier = max(0.55, skill_modifier)

    crash_chance = crash_base * skill_modifier

    return random.random() < crash_chance


def get_dnf_reason(aggression, reliability, skill):
    if technical_dnf(reliability):
        return "technical"
    if crash_dnf(aggression, skill):
        return "crash"
    return None


def show_pilots_mistakes():
    srt_pilot_stats = dict(sorted(pilot_stats.items(),key=lambda item: item[1]["mistakes"],reverse=True))
    for pilot in srt_pilot_stats:print(f"{pilot:<20}  "f"{srt_pilot_stats[pilot]['mistakes']} mistakes  "f"with {drivers[pilot]['consistency']} of consistency")
    print()


def show_pilots_dnfs():
    srt_pilot_stats = dict(sorted(pilot_stats.items(),key=lambda item: item[1]["dnfs"],reverse=True))
    for pilot in srt_pilot_stats:print(f"{pilot:<20}  {srt_pilot_stats[pilot]['dnfs']} dnfs  in season")
    print()


def show_pilots_dnf_details():
    srt_pilot_stats = dict(sorted(pilot_stats.items(),key=lambda item: item[1]["dnfs"],reverse=True))

    for pilot in srt_pilot_stats:print(f"{pilot:<20}  "f"{srt_pilot_stats[pilot]['dnfs']} total dnfs | "f"{srt_pilot_stats[pilot]['technical_dnfs']} technical | "f"{srt_pilot_stats[pilot]['crash_dnfs']} crash")
    print()

championship2026 = simulate_championship(drivers, car_performance, GrandPrix_list)

show_championship(championship2026, teams, drivers, race_history, championship_history)
