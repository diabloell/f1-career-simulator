"""Run reproducible balance checks using the actual game functions."""
import argparse
import json
import random
from collections import Counter
from pathlib import Path
import championship as game


def test_balance(year, number_of_seasons=1000, seed=42):
    if number_of_seasons < 1:
        raise ValueError('Number of seasons must be positive')
    random.seed(seed)
    game.setup_season(year)
    titles, team_titles = Counter(), Counter()
    points, wins, podiums, poles, team_points, dnfs = (Counter() for _ in range(6))
    for _ in range(number_of_seasons):
        for driver in game.drivers.values():
            driver['total_score'] = 0
        for stats in game.pilot_stats.values():
            for key in stats:
                stats[key] = 0
        for history in (game.race_history, game.qualifying_history, game.championship_history,
                        game.weather_history, game.race_events_history):
            history.clear()
        standings = game.simulate_championship(game.drivers, game.car_performance, game.GrandPrix_list)
        titles[standings[0][0]] += 1
        constructors = game.constructor_standings(game.teams, game.drivers)
        team_titles[next(iter(constructors))] += 1
        team_points.update(constructors)
        for name, driver in game.drivers.items():
            points[name] += driver['total_score']
            dnfs[name] += game.pilot_stats[name]['dnfs']
        for race, results in game.race_history.items():
            finishers = [name for name, score in results.items() if score > 0]
            wins.update(finishers[:1])
            podiums.update(finishers[:3])
            poles.update(list(game.qualifying_history[race])[:1])
    return dict(year=year, simulations=number_of_seasons, seed=seed,
                drivers={name:dict(title_percent=100*titles[name]/number_of_seasons,
                                  points=points[name]/number_of_seasons,
                                  wins=wins[name]/number_of_seasons,
                                  podiums=podiums[name]/number_of_seasons,
                                  poles=poles[name]/number_of_seasons,
                                  dnfs=dnfs[name]/number_of_seasons) for name in game.drivers},
                teams={name:dict(title_percent=100*team_titles[name]/number_of_seasons,
                                points=team_points[name]/number_of_seasons,
                                points_share=100*team_points[name]/sum(team_points.values())) for name in game.teams})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--years', nargs='+', type=int, default=[1999,2007,2010,2012,2021,2024])
    parser.add_argument('--seasons', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    results = []
    for year in args.years:
        result = test_balance(year, args.seasons, args.seed)
        results.append(result)
        print(year, sorted(((n,round(d['title_percent'],1),round(d['points'],1),round(d['wins'],1))
                            for n,d in result['drivers'].items()), key=lambda x:x[2], reverse=True)[:6], flush=True)
        print('Teams:', sorted(((n,round(d['points'],1)) for n,d in result['teams'].items()), key=lambda x:x[1], reverse=True), flush=True)
    if args.output:
        args.output.write_text(json.dumps(results, indent=2)+'\n', encoding='utf-8')
