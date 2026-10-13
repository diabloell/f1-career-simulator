import random

from season_loader import load_season, build_drivers

race_history = {}
championship_history = {}
qualifying_history = {}
weather_history = {}
race_events_history = {}


def simulate_race(drivers, car_performance, qualifying_results, name_of_track, is_rainy):
    race_results = {}
    race_events_history[name_of_track] = {}
    starting_grid = {
        pilot: position
        for position, pilot in enumerate(qualifying_results, 1)
    }

    overtaking = tracks[name_of_track]["overtaking"]
    overtaking_coefficient = 0.75 - overtaking * 0.005
    skill_importance = tracks[name_of_track]['skill_importance']

    for pilot in drivers:
        race_events_history[name_of_track][pilot] = {"mistake": False, "dnf_reason": None}
        car_power = car_performance[drivers[pilot]["team_name"]]
        start_position = starting_grid[pilot]
        qualifying_bonus = ((len(drivers) + 1) / 2 - start_position) * overtaking_coefficient
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
            race_events_history[name_of_track][pilot]["mistake"] = True

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
            race_events_history[name_of_track][pilot]["dnf_reason"] = dnf_reason

            if dnf_reason == "technical":
                pilot_stats[pilot]["technical_dnfs"] += 1
            elif dnf_reason == "crash":
                pilot_stats[pilot]["crash_dnfs"] += 1

        race_results[pilot] = result

    race_results = dict(sorted(race_results.items(), key=lambda item: item[1], reverse=True))

    award_points(race_results, drivers, race_points_list)

    return race_results


def award_points(race_results, drivers, race_points_list):
    for place, pilot in enumerate(race_results):
        if place < len(race_points_list) and race_results[pilot] > 0:
            drivers[pilot]["total_score"] += race_points_list[place]


def constructor_standings(teams, drivers):
    teams_total_score = {x: 0 for x in teams}
    for team in teams:
        for pilot in teams[team]:
            teams_total_score[team] += drivers[pilot]['total_score']
    return dict(sorted(teams_total_score.items(), key=lambda item: item[1], reverse=True))


def podiums_of_each_race(race_history):
    if not race_history:
        print('No race results yet.')
        return

    race_width = max(18, max(len(race.removesuffix(' Grand Prix')) for race in race_history))
    driver_width = max(20, max(len(pilot) for results in race_history.values() for pilot in list(results)[:3]))

    header = f'{"#":>2}  {"GRAND PRIX":<{race_width}} │ {"1ST PLACE":<{driver_width}} │ {"2ND PLACE":<{driver_width}} │ {"3RD PLACE":<{driver_width}}'
    print('─' * len(header))
    print(header)
    print('─' * len(header))

    for number, (race, results) in enumerate(race_history.items(), 1):
        race_name = race.removesuffix(' Grand Prix')
        podium = list(results)[:3]
        print(
            f'{number:>2}  {race_name:<{race_width}} │ {podium[0]:<{driver_width}} │ {podium[1]:<{driver_width}} │ {podium[2]:<{driver_width}}')

    print('─' * len(header))
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
    print(f'==================== SEASON {season["year"]} ====================')
    print()
    print(f'--- The World Champion {season["year"]} is {championship[0][0]} ---')
    print()
    print(
        f'--- The Winner of Constructor Standings {season["year"]} is {list(constructor_standings(teams, drivers))[0]} ---')

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


def show_race_weekend(name_of_track, player_name=None):
    qualifying = qualifying_history[name_of_track]
    race = race_history[name_of_track]
    events = race_events_history[name_of_track]

    starting_grid = {pilot: position for position, pilot in enumerate(qualifying, 1)}

    print(f'\n==================== {name_of_track.upper()} ====================')
    print(f'Weather: {weather_history[name_of_track]}')

    print('\n========== QUALIFYING ==========\n')

    for place, pilot in enumerate(qualifying, 1):
        print(f'{place:>2}. {pilot}')

    print('\n========== RACE RESULTS ==========\n')
    print(f'{"Pos":<5} {"Driver":<23} {"Grid":<6} {"Change":<8} {"Events"}')

    for place, pilot in enumerate(race, 1):
        start = starting_grid[pilot]
        mistake = events[pilot]["mistake"]
        dnf_reason = events[pilot]["dnf_reason"]

        if race[pilot] == 0:
            position = "DNF"
            change = "-"
        else:
            position = str(place)
            change = f'{start - place:+}'

        event_info = []

        if mistake: event_info.append("Mistake")
        if dnf_reason: event_info.append(dnf_reason.capitalize())

        print(f'{position:<5} {pilot:<23} {start:<6} {change:<8} {", ".join(event_info) or "-"}')

    print('\n========== RACE NEWS ==========\n')

    winner = next(iter(race))
    pole = next(iter(qualifying))

    print(f'{winner} wins the {name_of_track}!')

    if winner == pole:
        print(f'{winner} converts pole position into victory!')
    else:
        print(f'{pole} fails to convert pole position into victory.')

    position_gains = {
        pilot: starting_grid[pilot] - place
        for place, pilot in enumerate(race, 1)
        if race[pilot] > 0
    }

    best_driver = max(position_gains, key=position_gains.get)
    best_gain = position_gains[best_driver]

    if best_gain > 0:
        print(f'{best_driver} gains {best_gain} positions!')

    for pilot in events:
        if events[pilot]["dnf_reason"] == "technical":
            print(f'{pilot} retires due to a technical failure!')
        elif events[pilot]["dnf_reason"] == "crash":
            print(f'{pilot} crashes out of the race!')

    if player_name:
        print('\n========== YOUR DRIVER NEWS ==========\n')
        show_player_race_news(name_of_track, player_name)

    print('\n========== CHAMPIONSHIP AFTER RACE ==========\n')

    show_championship_after_race(name_of_track, championship_history)


def race_archive(player_name=None):
    while True:
        print('\n========== RACE ARCHIVE ==========\n')

        for number, race in enumerate(GrandPrix_list, 1):
            print(f'{number:>2}. {race}')

        print('\n0. Back')

        choice = input('\nSelect Grand Prix: ')

        if choice == '0':
            return

        if choice.isdigit() and 1 <= int(choice) <= len(GrandPrix_list):
            name_of_track = GrandPrix_list[int(choice) - 1]
            show_race_weekend(name_of_track, player_name)
            input('\nPress Enter to return to archive...')
        else:
            print('Invalid option. Try again.')


def post_season_menu(player_name=None):
    while True:
        print('\n========== SEASON COMPLETED ==========')
        print('1. Race Archive')

        if player_name:
            print('2. My Driver Statistics')
            print('3. Exit')
        else:
            print('2. Exit')

        choice = input('\n> ')

        if choice == '1':
            race_archive(player_name)
        elif choice == '2' and player_name:
            show_player_statistics(player_name)
        elif (choice == '3' and player_name) or (choice == '2' and not player_name):
            return
        else:
            print('Invalid option. Try again.')


def show_player_race_news(name_of_track, player_name):
    qualifying = qualifying_history[name_of_track]
    race = race_history[name_of_track]
    events = race_events_history[name_of_track][player_name]

    start_position = list(qualifying).index(player_name) + 1

    if race[player_name] == 0:
        reason = events["dnf_reason"]

        if reason == "crash":
            print(f'{player_name} crashes out of the {name_of_track}!')
        elif reason == "technical":
            print(f'{player_name} retires due to a technical failure!')

    else:
        finish_position = list(race).index(player_name) + 1
        change = start_position - finish_position

        if finish_position == 1:
            print(f'{player_name} wins the {name_of_track}!')
        elif finish_position <= 3:
            print(f'{player_name} finishes on the podium in P{finish_position}!')
        elif finish_position <= len(race_points_list):
            print(f'{player_name} scores points with a P{finish_position} finish!')
        else:
            print(f'{player_name} finishes P{finish_position}.')

        if change > 0:
            print(f'{player_name} gains {change} positions from P{start_position}!')
        elif change < 0:
            print(f'{player_name} loses {abs(change)} positions from P{start_position}.')
        else:
            print(f'{player_name} finishes in the same position as qualifying.')

    if events["mistake"]:
        print(f'{player_name} makes a mistake during the race!')


def show_player_statistics(player_name):
    wins = 0
    podiums = 0
    poles = 0
    points_finishes = 0
    finishes = 0
    best_finish = None
    best_race = None
    biggest_gain = 0
    biggest_gain_race = None

    for name_of_track in race_history:
        qualifying = qualifying_history[name_of_track]
        race = race_history[name_of_track]

        start_position = list(qualifying).index(player_name) + 1

        if start_position == 1:
            poles += 1

        if race[player_name] == 0:
            continue

        finish_position = list(race).index(player_name) + 1
        finishes += 1

        if finish_position == 1: wins += 1
        if finish_position <= 3: podiums += 1
        if finish_position <= len(race_points_list): points_finishes += 1

        if best_finish is None or finish_position < best_finish:
            best_finish = finish_position
            best_race = name_of_track

        change = start_position - finish_position

        if change > biggest_gain:
            biggest_gain = change
            biggest_gain_race = name_of_track

    championship_position = sorted(
        drivers,
        key=lambda pilot: drivers[pilot]["total_score"],
        reverse=True
    ).index(player_name) + 1

    stats = pilot_stats[player_name]
    team = drivers[player_name]["team_name"]

    print('\n========== MY DRIVER STATISTICS ==========\n')
    print(f'Name: {player_name}')
    print(f'Team: {team}')
    print(f'Championship position: P{championship_position}')
    print(f'Championship points: {drivers[player_name]["total_score"]}')

    print('\n========== SEASON RESULTS ==========\n')
    print(f'Grand Prix entered: {len(race_history)}')
    print(f'Race finishes: {finishes}')
    print(f'Wins: {wins}')
    print(f'Podiums: {podiums}')
    print(f'Poles: {poles}')
    print(f'Points finishes: {points_finishes}')

    print('\n========== RACE HIGHLIGHTS ==========\n')

    if best_race:
        print(f'Best finish: P{best_finish} - {best_race}')

    if biggest_gain_race:
        print(f'Biggest position gain: +{biggest_gain} - {biggest_gain_race}')

    print('\n========== INCIDENTS ==========\n')
    print(f'Mistakes: {stats["mistakes"]}')
    print(f'Total DNFs: {stats["dnfs"]}')
    print(f'Technical DNFs: {stats["technical_dnfs"]}')
    print(f'Crash DNFs: {stats["crash_dnfs"]}')
    show_teammate_comparison(player_name)


def show_teammate_comparison(player_name):
    team = drivers[player_name]["team_name"]
    teammate = next(pilot for pilot in teams[team] if pilot != player_name)

    player_qualifying_wins = 0
    teammate_qualifying_wins = 0

    player_race_wins = 0
    teammate_race_wins = 0
    both_dnfs = 0

    player_wins = 0
    teammate_wins = 0
    player_podiums = 0
    teammate_podiums = 0

    for name_of_track in race_history:
        qualifying = list(qualifying_history[name_of_track])
        race_results = race_history[name_of_track]
        race = list(race_results)

        if qualifying.index(player_name) < qualifying.index(teammate):
            player_qualifying_wins += 1
        else:
            teammate_qualifying_wins += 1

        if race_results[player_name] == 0 and race_results[teammate] == 0:
            both_dnfs += 1
        elif race_results[teammate] == 0 or (
                race_results[player_name] > 0 and race.index(player_name) < race.index(teammate)):
            player_race_wins += 1
        else:
            teammate_race_wins += 1

        if race_results[player_name] > 0:
            position = race.index(player_name) + 1
            if position == 1: player_wins += 1
            if position <= 3: player_podiums += 1

        if race_results[teammate] > 0:
            position = race.index(teammate) + 1
            if position == 1: teammate_wins += 1
            if position <= 3: teammate_podiums += 1

    print('\n========== TEAMMATE COMPARISON ==========\n')
    print(f'Team: {team}')
    print(f'Your driver: {player_name}')
    print(f'Teammate: {teammate}')

    print()
    print(f'{"Statistic":<25} {player_name:>18} {teammate:>18}')
    print('-' * 65)
    print(
        f'{"Championship points":<25} {drivers[player_name]["total_score"]:>18} {drivers[teammate]["total_score"]:>18}')
    print(f'{"Qualifying H2H":<25} {player_qualifying_wins:>18} {teammate_qualifying_wins:>18}')
    print(f'{"Race H2H":<25} {player_race_wins:>18} {teammate_race_wins:>18}')
    print(f'{"Race wins":<25} {player_wins:>18} {teammate_wins:>18}')
    print(f'{"Podiums":<25} {player_podiums:>18} {teammate_podiums:>18}')
    print(f'{"DNFs":<25} {pilot_stats[player_name]["dnfs"]:>18} {pilot_stats[teammate]["dnfs"]:>18}')

    if both_dnfs:
        print(f'\nBoth drivers retired in {both_dnfs} races (excluded from Race H2H).')


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
    print(f'\nAvailable season: {season["year"]}')

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

    new_driver = {
        "team_name": team,
        "total_score": 0
    }

    for stat in ["pace", "consistency", "aggression", "skill"]:
        options = [(f'{pilot} — {drivers[pilot][stat]}', drivers[pilot][stat]) for pilot in drivers]
        options.append(("Enter custom value (0-100)", None))

        value = choose_option(options, f'Choose your {stat.upper()}:')

        if value is None:
            while True:
                try:
                    value = float(input(f'Enter {stat.upper()} (0-100): ').replace(",", "."))
                    if 0 <= value <= 100:
                        break
                    print('Value must be between 0 and 100.')
                except ValueError:
                    print('Invalid number. Try again.')

        new_driver[stat] = value

    teams[team][teams[team].index(replaced)] = name

    driver_names[driver_names.index(replaced)] = name

    del drivers[replaced]

    drivers[name] = new_driver

    pilot_stats[name] = {stat: 0 for stat in pilot_stats[replaced]}
    del pilot_stats[replaced]

    print('\n========== DRIVER CREATED ==========')
    print(f'Name: {name}')
    print(f'Team: {team}')
    print(f'Replaced: {replaced}')

    for stat in ["pace", "consistency", "aggression", "skill"]:
        print(f'{stat.upper()}: {new_driver[stat]}')

    return name


def choose_season():
    from pathlib import Path
    seasons_folder = Path(__file__).parent / "seasons"
    presets = sorted(seasons_folder.glob("*.json"))
    print('\n========== CHOOSE THE SEASON ==========')
    for pos, el in enumerate(presets):
        print(f'{pos + 1}. {el.stem}')
    preset = input('\n> ')
    while not preset.isdigit() or int(preset) not in range(1, len(presets) + 1):
        preset = input('Invalid option. Try again: ')
    year_of_season = int(presets[int(preset) - 1].stem)
    return year_of_season


def setup_season(year):
    global season, teams, GrandPrix_list, tracks
    global car_performance, car_reliability, race_points_list
    global drivers, driver_names, pilot_stats

    season = load_season(year)
    teams = season["teams"]
    race_points_list = season["race_points_list"]
    GrandPrix_list = season["GrandPrix_list"]
    tracks = season["tracks"]
    car_performance = season["car_performance"]
    car_reliability = season["car_reliability"]
    drivers = build_drivers(season)
    driver_names = list(drivers)
    pilot_stats = {pilot: {"wins": 0,
                           "poles": 0,
                           "podiums": 0,
                           "mistakes": 0,
                           "dnfs": 0,
                           "technical_dnfs": 0,
                           "crash_dnfs": 0} for pilot in driver_names}


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
    year = choose_season()
    setup_season(year)
    player_name = None
    if mode == '2':
        player_name = create_driver()
    championship = simulate_championship(drivers, car_performance, GrandPrix_list)
    show_championship(championship, teams, drivers, race_history, championship_history)
    if player_name:
        position = next(
            place for place, (pilot, stats) in enumerate(championship, 1)
            if pilot == player_name
        )

        print('\n========== YOUR RESULTS ==========')
        print(f'Position: P{position}')
        print(f'Points: {drivers[player_name]["total_score"]}')
        print(f'Team: {drivers[player_name]["team_name"]}')
        print(f'DNFs: {pilot_stats[player_name]["dnfs"]}')
    post_season_menu(player_name)


if __name__ == '__main__':
    main()
