"""Release checks. Run with: python -m unittest tests -v"""
import contextlib
import io
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import championship as game

ROOT = Path(__file__).parent
YEARS = [1999, 2007, 2010, 2012, 2021, 2023, 2024, 2025, 2026]


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.output = io.StringIO()
        self.redirect = contextlib.redirect_stdout(self.output)
        self.redirect.__enter__()
        random.seed(12345)

    def tearDown(self):
        self.redirect.__exit__(None, None, None)

    def simulate(self, year):
        game.setup_season(year)
        return game.simulate_championship(game.drivers, game.car_performance, game.GrandPrix_list)

    def test_all_presets_and_race_invariants(self):
        for year in YEARS:
            with self.subTest(year=year):
                standings = self.simulate(year)
                names = [n for ns in game.teams.values() for n in ns]
                self.assertEqual(len(names), len(set(names)))
                self.assertTrue(all(len(ns) == 2 for ns in game.teams.values()))
                self.assertEqual(set(names), set(game.season['skills']))
                self.assertEqual(len(game.GrandPrix_list), len(set(game.GrandPrix_list)))
                self.assertEqual(set(game.GrandPrix_list), set(game.tracks))
                self.assertEqual(set(game.teams), set(game.car_performance))
                self.assertEqual(set(game.teams), set(game.car_reliability))
                for stats in game.season['skills'].values():
                    self.assertTrue(all(0 <= value <= 100 for value in stats.values()))
                for history in (game.race_history, game.qualifying_history, game.weather_history,
                                game.race_events_history, game.championship_history):
                    self.assertEqual(set(history), set(game.GrandPrix_list))
                expected = dict.fromkeys(names, 0)
                for race, results in game.race_history.items():
                    self.assertEqual(set(results), set(names))
                    self.assertEqual(set(game.qualifying_history[race]), set(names))
                    self.assertIn(game.weather_history[race], ['Rain', 'Dry'])
                    for place, (name, score) in enumerate(results.items()):
                        if score > 0 and place < len(game.race_points_list):
                            expected[name] += game.race_points_list[place]
                        event = game.race_events_history[race][name]
                        self.assertEqual(score == 0, event['dnf_reason'] is not None)
                    self.assertEqual(expected, game.championship_history[race])
                self.assertEqual(expected, {n:d['total_score'] for n,d in game.drivers.items()})
                self.assertEqual(sum(expected.values()), sum(game.constructor_standings(game.teams,game.drivers).values()))
                for name, stats in game.pilot_stats.items():
                    self.assertEqual(stats['dnfs'], stats['technical_dnfs'] + stats['crash_dnfs'])
                    self.assertEqual(stats['dnfs'], sum(r[name] == 0 for r in game.race_history.values()))
                game.show_championship(standings,game.teams,game.drivers,game.race_history,game.championship_history)
                for race in game.GrandPrix_list:
                    game.show_race_weekend(race)
                game.setup_season(year)
                self.assertFalse(game.race_history)
                with patch('builtins.input', return_value=str(YEARS.index(year)+1)):
                    self.assertEqual(game.choose_season(),year)

    def test_points_and_ties(self):
        self.simulate(1999)
        pilots = list(game.drivers)
        for points in ([10,6,4,3,2,1],[10,8,6,5,4,3,2,1],[25,18,15,12,10,8,6,4,2,1]):
            for d in game.drivers.values(): d['total_score'] = 0
            result = {n:100-i if i<4 else 0 for i,n in enumerate(pilots)}
            game.award_points(result,game.drivers,points)
            self.assertEqual([game.drivers[n]['total_score'] for n in pilots[:5]],points[:4]+[0])
        game.race_history.clear()
        game.race_history['test'] = {pilots[1]:100,pilots[0]:99}
        game.drivers[pilots[0]]['total_score']=10
        game.drivers[pilots[1]]['total_score']=10
        self.assertGreater(game.standings_key(pilots[1]),game.standings_key(pilots[0]))

    def test_custom_driver_and_save_roundtrip(self):
        for year in YEARS:
            with self.subTest(year=year), tempfile.TemporaryDirectory() as folder:
                game.setup_season(year)
                count = len(game.drivers)
                values=['',next(iter(game.drivers)),'Test Driver','0','1','1']
                for _ in range(4):values += [str(count+1),'bad','101','nan','95,5']
                with patch('builtins.input', side_effect=values):
                    name=game.create_driver()
                self.assertEqual(len(game.drivers),count)
                self.assertTrue(all(game.drivers[name][s] == 95.5 for s in ['pace','skill','consistency','aggression']))
                game.simulate_championship(game.drivers,game.car_performance,game.GrandPrix_list)
                game.show_player_statistics(name)
                game.show_race_weekend(game.GrandPrix_list[0],name)
                before=json.dumps(game.race_history)
                with patch.object(game,'__file__',str(Path(folder)/'championship.py')):
                    for title in ['My season','Another season','']:
                        with patch('builtins.input',return_value=title):game.save_championship(name)
                    files=sorted((Path(folder)/'saves').glob('*.json'))
                    self.assertEqual(len(files),3)
                    self.assertEqual(json.loads(files[0].read_text())['name'],'My season')
                    with patch('builtins.input',side_effect=['1','1','1','','0','2','3']):
                        game.load_championship()
                    self.assertEqual(json.dumps(game.race_history),before)
                    old=json.loads(files[0].read_text());del old['name'];files[0].write_text(json.dumps(old))
                    with patch('builtins.input',side_effect=['1','3']):game.load_championship()
                    self.assertIn('Championship '+str(year),self.output.getvalue())

    def test_existing_user_saves(self):
        files=sorted((ROOT/'saves').glob('*.json'))
        for index,path in enumerate(files,1):
            with self.subTest(file=path.name),patch('builtins.input',return_value=str(index)),patch.object(game,'post_season_menu'):
                game.load_championship()
                for race in game.race_history:game.show_race_weekend(race, json.loads(path.read_text()).get('player_name'))

    def test_weather_incidents_and_all_retired(self):
        game.setup_season(1999)
        race=game.GrandPrix_list[0]
        with patch.object(game.random,'random',return_value=0):
            self.assertTrue(game.generate_weather(race))
            self.assertTrue(game.driver_mistake(80,90,race,True))
            self.assertEqual(game.get_dnf_reason(80,80,90,race,True),'technical')
        with patch.object(game,'technical_dnf',return_value=False),patch.object(game,'crash_dnf',return_value=True):
            self.assertEqual(game.get_dnf_reason(80,80,90,race,False),'crash')
        with patch.object(game,'get_dnf_reason',return_value='technical'):
            game.simulate_championship(game.drivers,game.car_performance,game.GrandPrix_list)
        self.assertEqual(sum(game.count_wins(game.race_history,game.driver_names).values()),0)
        game.show_race_weekend(race)
        game.count_pole_to_win({}, {})

    def test_clean_cli(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)
            for name in ['championship.py','season_loader.py']:shutil.copy2(ROOT/name,target/name)
            shutil.copytree(ROOT/'seasons',target/'seasons')
            for i,year in enumerate(YEARS,1):
                with self.subTest(year=year):
                    completed=subprocess.run([sys.executable,'-E','-S','-X','utf8',str(target/'championship.py')],
                         input=f'1\n{i}\nCLI {year}\n1\n1\n\n0\n2\n',text=True,capture_output=True,encoding='utf-8',env={**__import__('os').environ,'PYTHONIOENCODING':'utf-8'},cwd=folder,timeout=20)
                    self.assertEqual(completed.returncode,0,completed.stderr)
                    self.assertIn('END OF SEASON',completed.stdout)
            self.assertEqual(len(list((target/'saves').glob('*.json'))),9)


if __name__ == '__main__':
    unittest.main()
