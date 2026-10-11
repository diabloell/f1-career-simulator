import random

from data import (
    drivers,
    teams,
    car_performance,
    race_points_list,
    GrandPrix_list,
    driver_names,
    pilot_stats,
    car_reliability,
    tracks
)

race_history = {}
championship_history = {}
qualifying_history = {}
weather_history = {}


def simulate_race(drivers, car_performance, qualifying_results, name_of_track, is_rainy):
    race_results = {}

    starting_grid = {
        pilot: position
        for position, pilot in enumerate(qualifying_results, 1)
    }

    overtaking = tracks[name_of_track]["overtaking"]
    overtaking_coefficient = 0.75 - overtaking * 0.005
    skill_importance = tracks[name_of_track]['skill_importance']

    for pilot in drivers:
        car_power = car_performance[drivers[pilot]["team_name"]]
        start_position = starting_grid[pilot]
        qualifying_bonus = (11.5 - start_position) * overtaking_coefficient
        skill_bonus = (drivers[pilot]["skill"] - 85) * (skill_importance - 50) * 0.003

        result = (0.3 * drivers[pilot]["pace"] + 0.5 * car_power + random.uniform(-5,
                                                                                  5) + qualifying_bonus + skill_bonus)

        if is_rainy:
            result += rain_bonus(
                drivers[pilot]["skill"],
                drivers[pilot]["consistency"],
                drivers[pilot]["aggression"]
            )

        if driver_mistake(
                drivers[pilot]["consistency"],
                drivers[pilot]["skill"],
                name_of_track,
                is_rainy
        ):
            result -= random.uniform(2, 5)
            pilot_stats[pilot]["mistakes"] += 1

        dnf_reason = get_dnf_reason(
            drivers[pilot]["aggression"],
            car_reliability[drivers[pilot]["team_name"]],
            drivers[pilot]["skill"],
            name_of_track,
            is_rainy
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
        is_rainy = generate_weather(name_of_track)
        weather_history[name_of_track] = "Rain" if is_rainy else "Dry"

        qualifying_results = simulate_qualifying(drivers, car_performance, is_rainy)
        qualifying_history[name_of_track] = qualifying_results

        current_race = simulate_race(drivers, car_performance, qualifying_results, name_of_track, is_rainy)
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
    print('==================== SEASON 2026 ====================')
    print()
    print(f'--- The World Champion 2026 is {championship[0][0]} ---')
    print()
    print(f'--- The Winner of Constructor Standings 2026 is {list(constructor_standings(teams, drivers))[0]} ---')

    print('\n==================== DRIVER STANDINGS ====================\n')

    for place, (pilot, stats) in enumerate(championship, 1):
        print(f"{place:>2}. {pilot:<22}    {stats['total_score']:>3} pts")

    print('\n==================== CONSTRUCTOR STANDINGS ====================\n')

    for place, (team, score) in enumerate(constructor_standings(teams, drivers).items(), 1):
        print(f"{place:>2}. {team:<22}    {score:>3} pts")

    print('\n==================== SEASON STATISTICS ====================\n')

    print('WINS:')
    print(count_wins(race_history, driver_names))
    print()
    print('POLES:')
    print(count_poles(qualifying_history, driver_names))
    print()
    count_pole_to_win(race_history, qualifying_history)
    print()
    print(f'{sum(weather == "Rain" for weather in weather_history.values())} - rainy weekends')

    print('\n==================== DRIVER MISTAKES ====================\n')

    print(f'{sum(stats["mistakes"] for stats in pilot_stats.values())} - mistakes')
    show_pilots_mistakes()

    print('\n==================== DRIVER DNFS ====================\n')

    print(f'{sum(stats["dnfs"] for stats in pilot_stats.values())} - dnfs')
    show_pilots_dnf_details()

    print('\n==================== RACE RESULTS ====================\n')

    podiums_of_each_race(race_history)

    print('\n==================== MONACO GRAND PRIX ====================\n')

    print(f"Weather: {weather_history['Monaco Grand Prix']}")

    print('QUALIFYING:')
    for place, pilot in enumerate(qualifying_history['Monaco Grand Prix'], 1):
        print(f'{place:>2}. {pilot}')

    print()
    show_race_results('Monaco Grand Prix', qualifying_history['Monaco Grand Prix'], race_history['Monaco Grand Prix'])

    print('\nCHAMPIONSHIP STANDINGS AFTER MONACO:\n')
    show_championship_after_race('Monaco Grand Prix', championship_history)

    print('\n==================== END OF SEASON ====================')


def simulate_qualifying(drivers, car_performance, is_rainy):
    qualifying_results = {}
    for pilot in drivers:
        car_power = car_performance[drivers[pilot]["team_name"]]
        qualifying_score = 0.35 * drivers[pilot]['pace'] + 0.65 * car_power + random.uniform(-3, 3)
        if is_rainy:
            qualifying_score += rain_bonus(drivers[pilot]["skill"], drivers[pilot]["consistency"],
                                           drivers[pilot]["aggression"]) * 0.6
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


def driver_mistake(consistency, skill, name_of_track, is_rainy):
    mistake_chance = (100 - consistency) / 200
    skill_modifier = 1 - max(0, skill - 75) * 0.01
    mistake_chance *= skill_modifier

    difficulty_modifier = 1 + (tracks[name_of_track]['difficulty'] - 80) * 0.015
    mistake_chance *= difficulty_modifier

    if is_rainy:
        mistake_chance *= 1.5

    return random.random() < mistake_chance


def technical_dnf(reliability):
    technical_chance = 0.028 + (100 - reliability) * 0.002
    return random.random() < technical_chance


def crash_dnf(aggression, skill, name_of_track, is_rainy):
    crash_base = 0.018 + max(0, aggression - 70) * 0.0018

    skill_modifier = 1 - max(0, skill - 75) * 0.012
    skill_modifier = max(0.55, skill_modifier)

    crash_chance = crash_base * skill_modifier

    crash_modifier = 1 + (tracks[name_of_track]["crash_risk"] - 70) * 0.015
    crash_chance *= crash_modifier

    if is_rainy:
        rain_crash_modifier = 1.4 + max(0, aggression - 80) * 0.01
        crash_chance *= rain_crash_modifier

    return random.random() < crash_chance


def get_dnf_reason(aggression, reliability, skill, name_of_track, is_rainy):
    if technical_dnf(reliability):
        return "technical"
    if crash_dnf(aggression, skill, name_of_track, is_rainy):
        return "crash"
    return None


def show_pilots_mistakes():
    srt_pilot_stats = dict(sorted(pilot_stats.items(), key=lambda item: item[1]["mistakes"], reverse=True))
    for pilot in srt_pilot_stats: print(
        f"{pilot:<20}  "f"{srt_pilot_stats[pilot]['mistakes']} mistakes  "f"with {drivers[pilot]['consistency']} of consistency")
    print()


def show_pilots_dnfs():
    srt_pilot_stats = dict(sorted(pilot_stats.items(), key=lambda item: item[1]["dnfs"], reverse=True))
    for pilot in srt_pilot_stats: print(f"{pilot:<20}  {srt_pilot_stats[pilot]['dnfs']} dnfs  in season")
    print()


def show_pilots_dnf_details():
    srt_pilot_stats = dict(sorted(pilot_stats.items(), key=lambda item: item[1]["dnfs"], reverse=True))

    for pilot in srt_pilot_stats: print(
        f"{pilot:<20}  "f"{srt_pilot_stats[pilot]['dnfs']} total dnfs | "f"{srt_pilot_stats[pilot]['technical_dnfs']} technical | "f"{srt_pilot_stats[pilot]['crash_dnfs']} crash")
    print()


def generate_weather(name_of_track):
    return random.random() < tracks[name_of_track]["rain_chance"]


def rain_bonus(skill, consistency, aggression):
    return (skill - 85) * 0.16 + (consistency - 85) * 0.10 - max(0, aggression - 80) * 0.05


def choose_option(options, title):
    print(f'\n{title}')

    for number, (label, value) in enumerate(options, 1):
        print(f'{number}. {label}')

    while True:
        choice = input('> ')

        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1][1]

        print('Invalid option. Try again.')


def create_driver():
    print('\n========== CREATE YOUR DRIVER ==========')
    print('\nAvailable season: 2026')

    name = input('\nEnter your driver name: ').strip()

    while not name or name.casefold() in (pilot.casefold() for pilot in drivers):
        print('Invalid or already existing driver name.')
        name = input('Enter your driver name: ').strip()

    team = choose_option(
        [(team, team) for team in teams],
        'Select your team:'
    )

    replaced = choose_option(
        [(pilot, pilot) for pilot in teams[team]],
        'Select driver to replace:'
    )

    reference_drivers = [
        "Max Verstappen",
        "George Russell",
        "Kimi Antonelli",
        "Lewis Hamilton",
        "Charles Leclerc",
        "Lando Norris",
        "Oscar Piastri"
    ]

    new_driver = {
        "team_name": team,
        "total_score": 0
    }

    for stat in ["pace", "consistency", "aggression", "skill"]:
        options = [
            (f'{pilot} — {drivers[pilot][stat]}', drivers[pilot][stat])
            for pilot in reference_drivers
        ]

        new_driver[stat] = choose_option(options, f'Choose your {stat.upper()}:')

    # Заменяем пилота в составе команды
    teams[team][teams[team].index(replaced)] = name

    # Обновляем список участников
    driver_names[driver_names.index(replaced)] = name

    # Заменяем характеристики пилота
    del drivers[replaced]
    drivers[name] = new_driver

    # Создаём статистику нового пилота
    pilot_stats[name] = {stat: 0 for stat in pilot_stats[replaced]}
    del pilot_stats[replaced]

    print('\n========== DRIVER CREATED ==========')
    print(f'Name: {name}')
    print(f'Team: {team}')
    print(f'Replaced: {replaced}')

    for stat in ["pace", "consistency", "aggression", "skill"]:
        print(f'{stat.upper()}: {new_driver[stat]}')

    return name


def main():
    print('\n========== F1 CHAMPIONSHIP GENERATOR ==========')
    print('1. Generate Championship')
    print('2. Create Your Driver')
    print('3. Exit')

    mode = input('\n> ')

    while mode not in ('1', '2', '3'):
        mode = input('Invalid option. Try again: ')

    if mode == '3':
        return

    player_name = None

    if mode == '2':
        player_name = create_driver()

    championship2026 = simulate_championship(drivers, car_performance, GrandPrix_list)

    show_championship(championship2026, teams, drivers, race_history, championship_history)

    if player_name:
        position = next(
            place for place, (pilot, stats) in enumerate(championship2026, 1)
            if pilot == player_name
        )

        print('\n========== YOUR RESULTS ==========')
        print(f'Position: P{position}')
        print(f'Points: {drivers[player_name]["total_score"]}')
        print(f'Team: {drivers[player_name]["team_name"]}')
        print(f'DNFs: {pilot_stats[player_name]["dnfs"]}')


if __name__ == '__main__':
    main()
