def load_season(year):
    from pathlib import Path
    import json
    with open(Path(__file__).parent / 'seasons' / f'{year}.json', encoding='utf-8') as file:
        return json.load(file)


def build_drivers(season):
    drivers = {}
    for team in season["teams"]:
        for driver in season["teams"][team]:
            drivers[driver] = {'team_name': team, 'total_score': 0, "pace": season['skills'][driver]["pace"],
                               "consistency": season['skills'][driver]["consistency"],
                               "aggression": season['skills'][driver]["aggression"],
                               "skill": season['skills'][driver]["skill"]}
    return drivers
