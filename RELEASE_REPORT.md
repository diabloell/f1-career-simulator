# v1.0 release report

Date: 2026-10-21

The console Python release and the Windows x64 executable are ready for the owner to review. No commit or tag was created. Existing uncommitted save/load work and the existing 2023, 2025 and 2026 presets were preserved.

## Work completed

Added seasons/1999.json, 2007.json, 2010.json, 2012.json, 2021.json and 2024.json using the existing schema. Each has two unique drivers per team, a completed-race calendar and the appropriate race points. There are 16, 17, 19, 20, 22 and 24 rounds respectively.

Fixed season setup leaving old race archives in memory, final standings ties being decided by dictionary order, a crash when every driver retired, retired drivers being counted as winners and division by zero in empty pole conversion statistics. Loading now prints a readable save name instead of three debug values.

Added a runnable standard-library test suite and balance.py, a short README, .gitignore and reference/results files. No new game mechanics or runtime dependencies were added.

## Actual simulation counts

96,200 balance championships were run through championship.simulate_championship. This excludes functional tests. The first exploratory run included a mistaken 1999 team-to-performance mapping, which was corrected before calibration. That run is counted, not presented as a valid final configuration.

- Initial exploration: 6 x 300 = 1,800, seed 42.
- Six calibration passes: 6 x 6 x 400 = 14,400, seed 42.
- Candidate review: 6 x 1,000 = 6,000, seed 31415.
- Manual rating review: 6 x 500 = 3,000, seed 42.
- Initial large check: 6 x 10,000 = 60,000, seed 8675309.
- 2007 teammate review: 1,000, seed 42.
- Replacement 2007 final check: 10,000, seed 8675309.

The final results below contain 60,000 championships, with the superseded 2007 sample replaced. balance_results.json has unrounded averages for every driver and team. balance_history.json records the sample counts and calibration summaries. No different mathematical simulator was used to speed up these runs. At 10,000 samples, an estimated 50% title rate has about +/- 1 percentage point of 95% sampling uncertainty. These percentages describe this game, not the real probability of historical outcomes.

Calibration considered championship contenders first, then team points shares and teammates. Points-driven fitting was reviewed manually to avoid treating a handful of midfield points as evidence of elite pace. Reliability was estimated from result statuses, with ambiguous retirements excluded, then limited to the existing rating scale. Some initial target totals counted replacement drivers across teams; the final manual review corrected the affected BAR and Toro Rosso settings. This is documented rather than treating the automated fit as historical truth.

## Main results

| Year | Final title chances | Leading teams by average points |
|---|---|---|
| 1999 | Mika Hakkinen 42.4%; Eddie Irvine 30.0%; Michael Schumacher 25.5% | Ferrari 148.9; McLaren 125.9; Jordan 53.6 |
| 2007 | Kimi Raikkonen 32.0%; Lewis Hamilton 31.9%; Fernando Alonso 30.2%; Felipe Massa 5.9% | McLaren 228.1; Ferrari 212.6; BMW Sauber 100.9 |
| 2010 | Sebastian Vettel 38.2%; Fernando Alonso 23.3%; Mark Webber 20.0%; Lewis Hamilton 15.3%; Jenson Button 3.1% | Red Bull 541.6; McLaren 480.4; Ferrari 406.8 |
| 2012 | Sebastian Vettel 51.5%; Fernando Alonso 45.6% | Red Bull 476.7; Ferrari 408.4; McLaren 401.8 |
| 2021 | Lewis Hamilton 51.7%; Max Verstappen 48.3% | Mercedes 634.5; Red Bull 597.7; Ferrari 325.7 |
| 2024 | Max Verstappen 64.2%; Lando Norris 25.2%; Charles Leclerc 9.7% | McLaren 643.4; Ferrari 609.8; Red Bull 527.9 |

## Historical comparison

Real points below are final championship points, including supported historical bonuses or sprints in the source. Model points use race_points_list only. Compare shares and ordering where those rules differ. Real constructor shares use official totals, except McLaren 2007 is discussed separately. Simulated constructor order is based on average points, not a guarantee for each season.

1999: Hakkinen and Irvine are the leading title contenders, but Schumacher also has a substantial chance because he races all 16 rounds. Ferrari scores too many points compared with the real year for this reason. The Williams/Stewart order is slightly reversed on average.

2007: Raikkonen, Hamilton and Alonso have almost equal title chances. McLaren can win the constructors championship because its real exclusion was an administrative sanction. Real driver points sum to 218 for McLaren; this is not the official constructor score and also includes the drivers' Hungary points that McLaren was separately barred from scoring. The simulator applies neither penalty. Speed has the majority Toro Rosso seat (10 starts versus Vettel's 7); Albers has the Spyker seat (9 versus Yamamoto's 7 and Winkelhock's 1).

2010: Vettel, Alonso, Webber and Hamilton remain contenders. The first five teams have the historical order. The model gives too much of the total points to the leading teams, particularly Red Bull and McLaren, and too little to Mercedes and Renault.

2012: Vettel and Alonso are close favorites. Other winners are possible, but Hamilton and Button win less often than in reality while Alonso wins more. Ferrari and McLaren are close in average team points. Mercedes and Sauber are slightly reversed. A single fixed pace rating cannot independently reproduce qualifying pace, race pace, reliability, development and isolated surprise results.

2021: Hamilton and Verstappen are almost level; Mercedes is the stronger constructor. Belgium is a normal full-points game race rather than the real shortened event. Sprint and fastest-lap points are omitted.

2024: Verstappen is the favorite and McLaren leads Ferrari and Red Bull in average team points. The model does not reproduce the early Red Bull advantage and later McLaren improvement. Verstappen averages about eight wins rather than nine, while Norris and Leclerc win more than in reality. Sargeant has 14 starts versus Colapinto's 9; Ricciardo has 18 versus Lawson's 6.

## Detailed results

### 1999 (16 races)

| Driver | Real pts | Model pts | Title % | Real wins | Model wins | Real podiums | Model podiums | Real poles | Model poles |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Mika Hakkinen | 76 | 78.7 | 42.4 | 5 | 4.90 | 10 | 9.53 | 11 | 6.30 |
| Eddie Irvine | 74 | 75.2 | 30.0 | 4 | 3.57 | 9 | 9.41 | 0 | 2.43 |
| Michael Schumacher | 44 | 73.7 | 25.5 | 2 | 3.51 | 6 | 9.17 | 3 | 4.57 |
| Heinz-Harald Frentzen | 54 | 48.2 | 1.1 | 2 | 1.60 | 6 | 6.03 | 1 | 0.70 |
| David Coulthard | 48 | 47.1 | 1.0 | 2 | 1.57 | 6 | 5.85 | 0 | 1.92 |
| Ralf Schumacher | 35 | 31.8 | 0.0 | 0 | 0.59 | 3 | 3.74 | 0 | 0.08 |
| Rubens Barrichello | 21 | 17.6 | 0.0 | 0 | 0.14 | 3 | 1.68 | 1 | 0.00 |
| Johnny Herbert | 15 | 12.4 | 0.0 | 1 | 0.06 | 1 | 0.99 | 0 | 0.00 |
| Giancarlo Fisichella | 13 | 10.6 | 0.0 | 0 | 0.04 | 1 | 0.78 | 0 | 0.00 |
| Jarno Trulli | 7 | 6.3 | 0.0 | 0 | 0.01 | 1 | 0.34 | 0 | 0.00 |
| Damon Hill | 7 | 5.3 | 0.0 | 0 | 0.01 | 0 | 0.26 | 0 | 0.00 |
| Pedro Diniz | 3 | 2.6 | 0.0 | 0 | 0.00 | 0 | 0.07 | 0 | 0.00 |
| Alexander Wurz | 3 | 1.9 | 0.0 | 0 | 0.00 | 0 | 0.05 | 0 | 0.00 |
| Alessandro Zanardi | 0 | 1.7 | 0.0 | 0 | 0.00 | 0 | 0.04 | 0 | 0.00 |
| Jean Alesi | 2 | 1.4 | 0.0 | 0 | 0.00 | 0 | 0.03 | 0 | 0.00 |
| Olivier Panis | 2 | 1.0 | 0.0 | 0 | 0.00 | 0 | 0.02 | 0 | 0.00 |
| Pedro de la Rosa | 1 | 0.2 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Jacques Villeneuve | 0 | 0.1 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Marc Gene | 1 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Toranosuke Takagi | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Luca Badoer | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Ricardo Zonta | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |

| Team | Real pts | Model pts | Real share % | Model share % | Constructor titles % |
|---|---:|---:|---:|---:|---:|
| Ferrari | 128 | 148.9 | 30.77 | 35.79 | 76.2 |
| McLaren | 124 | 125.9 | 29.81 | 30.25 | 23.8 |
| Jordan | 61 | 53.6 | 14.66 | 12.87 | 0.0 |
| Williams | 35 | 33.5 | 8.41 | 8.06 | 0.0 |
| Stewart | 36 | 30.0 | 8.65 | 7.21 | 0.0 |
| Benetton | 16 | 12.6 | 3.85 | 3.03 | 0.0 |
| Prost | 9 | 7.4 | 2.16 | 1.77 | 0.0 |
| Sauber | 5 | 3.9 | 1.20 | 0.94 | 0.0 |
| Arrows | 1 | 0.2 | 0.24 | 0.06 | 0.0 |
| BAR | 0 | 0.1 | 0.00 | 0.02 | 0.0 |
| Minardi | 1 | 0.0 | 0.24 | 0.00 | 0.0 |

Sources: [F1 drivers](https://www.formula1.com/en/results/1999/drivers), [F1 constructors](https://www.formula1.com/en/results/1999/team), [F1 calendar/results](https://www.formula1.com/en/results/1999/races), [Jolpica race records](https://api.jolpi.ca/ergast/f1/1999/results/), [F1 pole awards](https://www.formula1.com/en/results/1999/awards/pole-positions).

### 2007 (17 races)

| Driver | Real pts | Model pts | Title % | Real wins | Model wins | Real podiums | Model podiums | Real poles | Model poles |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Lewis Hamilton | 109 | 114.3 | 31.9 | 4 | 4.31 | 12 | 11.64 | 6 | 4.20 |
| Fernando Alonso | 109 | 113.9 | 30.2 | 4 | 4.23 | 12 | 11.58 | 2 | 4.04 |
| Kimi Raikkonen | 110 | 113.3 | 32.0 | 6 | 5.09 | 12 | 11.81 | 3 | 6.24 |
| Felipe Massa | 94 | 99.3 | 5.9 | 3 | 2.90 | 10 | 9.63 | 6 | 2.47 |
| Nick Heidfeld | 61 | 59.8 | 0.0 | 0 | 0.37 | 2 | 3.77 | 0 | 0.04 |
| Robert Kubica | 39 | 41.1 | 0.0 | 0 | 0.08 | 0 | 1.64 | 0 | 0.01 |
| Heikki Kovalainen | 30 | 26.9 | 0.0 | 0 | 0.01 | 1 | 0.42 | 0 | 0.00 |
| Giancarlo Fisichella | 21 | 17.9 | 0.0 | 0 | 0.00 | 0 | 0.16 | 0 | 0.00 |
| Nico Rosberg | 20 | 17.2 | 0.0 | 0 | 0.00 | 0 | 0.15 | 0 | 0.00 |
| David Coulthard | 14 | 11.7 | 0.0 | 0 | 0.00 | 0 | 0.07 | 0 | 0.00 |
| Alexander Wurz | 13 | 10.7 | 0.0 | 0 | 0.00 | 1 | 0.05 | 0 | 0.00 |
| Mark Webber | 10 | 8.2 | 0.0 | 0 | 0.00 | 1 | 0.03 | 0 | 0.00 |
| Vitantonio Liuzzi | 3 | 8.0 | 0.0 | 0 | 0.00 | 0 | 0.02 | 0 | 0.00 |
| Jarno Trulli | 8 | 6.5 | 0.0 | 0 | 0.00 | 0 | 0.01 | 0 | 0.00 |
| Jenson Button | 6 | 5.0 | 0.0 | 0 | 0.00 | 0 | 0.01 | 0 | 0.00 |
| Ralf Schumacher | 5 | 4.1 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Takuma Sato | 4 | 3.5 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Scott Speed | 0 | 1.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Adrian Sutil | 1 | 0.7 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Anthony Davidson | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Rubens Barrichello | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Christijan Albers | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |

| Team | Real pts | Model pts | Real share % | Model share % | Constructor titles % |
|---|---:|---:|---:|---:|---:|
| McLaren | 0 | 228.1 | 0.00 | 34.41 | 71.7 |
| Ferrari | 204 | 212.6 | 45.84 | 32.07 | 28.3 |
| BMW Sauber | 101 | 100.9 | 22.70 | 15.22 | 0.0 |
| Renault | 51 | 44.8 | 11.46 | 6.76 | 0.0 |
| Williams | 33 | 27.8 | 7.42 | 4.20 | 0.0 |
| Red Bull | 24 | 19.9 | 5.39 | 3.00 | 0.0 |
| Toyota | 13 | 10.7 | 2.92 | 1.61 | 0.0 |
| Toro Rosso | 8 | 8.9 | 1.80 | 1.35 | 0.0 |
| Honda | 6 | 5.0 | 1.35 | 0.76 | 0.0 |
| Super Aguri | 4 | 3.5 | 0.90 | 0.53 | 0.0 |
| Spyker | 1 | 0.7 | 0.22 | 0.10 | 0.0 |

Sources: [F1 drivers](https://www.formula1.com/en/results/2007/drivers), [F1 constructors](https://www.formula1.com/en/results/2007/team), [F1 calendar/results](https://www.formula1.com/en/results/2007/races), [Jolpica race records](https://api.jolpi.ca/ergast/f1/2007/results/), [F1 pole awards](https://www.formula1.com/en/results/2007/awards/pole-positions).

### 2010 (19 races)

| Driver | Real pts | Model pts | Title % | Real wins | Model wins | Real podiums | Model podiums | Real poles | Model poles |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sebastian Vettel | 256 | 279.2 | 38.2 | 5 | 4.56 | 10 | 10.72 | 10 | 5.19 |
| Fernando Alonso | 252 | 266.8 | 23.3 | 5 | 3.71 | 10 | 9.93 | 2 | 3.63 |
| Mark Webber | 242 | 262.3 | 20.0 | 4 | 3.72 | 10 | 9.81 | 5 | 3.96 |
| Lewis Hamilton | 240 | 254.8 | 15.3 | 3 | 3.60 | 9 | 9.51 | 1 | 3.78 |
| Jenson Button | 214 | 225.6 | 3.1 | 2 | 2.39 | 7 | 7.88 | 0 | 1.98 |
| Felipe Massa | 144 | 140.0 | 0.0 | 0 | 0.43 | 5 | 3.14 | 0 | 0.36 |
| Nico Rosberg | 142 | 127.2 | 0.0 | 0 | 0.30 | 3 | 2.66 | 0 | 0.05 |
| Robert Kubica | 136 | 117.4 | 0.0 | 0 | 0.26 | 3 | 2.40 | 0 | 0.05 |
| Michael Schumacher | 72 | 61.2 | 0.0 | 0 | 0.03 | 0 | 0.52 | 0 | 0.00 |
| Rubens Barrichello | 47 | 41.9 | 0.0 | 0 | 0.00 | 0 | 0.15 | 0 | 0.00 |
| Adrian Sutil | 47 | 40.0 | 0.0 | 0 | 0.00 | 0 | 0.15 | 0 | 0.00 |
| Kamui Kobayashi | 32 | 26.3 | 0.0 | 0 | 0.00 | 0 | 0.06 | 0 | 0.00 |
| Vitaly Petrov | 27 | 20.6 | 0.0 | 0 | 0.00 | 0 | 0.03 | 0 | 0.00 |
| Nico Hulkenberg | 22 | 20.0 | 0.0 | 0 | 0.00 | 0 | 0.02 | 1 | 0.00 |
| Vitantonio Liuzzi | 21 | 16.4 | 0.0 | 0 | 0.00 | 0 | 0.01 | 0 | 0.00 |
| Pedro de la Rosa | 6 | 9.5 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Sebastien Buemi | 8 | 6.2 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Jaime Alguersuari | 5 | 3.5 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Heikki Kovalainen | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Jarno Trulli | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Timo Glock | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Karun Chandhok | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Lucas di Grassi | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Bruno Senna | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |

| Team | Real pts | Model pts | Real share % | Model share % | Constructor titles % |
|---|---:|---:|---:|---:|---:|
| Red Bull | 498 | 541.6 | 25.95 | 28.22 | 80.0 |
| McLaren | 454 | 480.4 | 23.66 | 25.03 | 19.1 |
| Ferrari | 396 | 406.8 | 20.64 | 21.20 | 0.9 |
| Mercedes | 214 | 188.5 | 11.15 | 9.82 | 0.0 |
| Renault | 163 | 138.0 | 8.49 | 7.19 | 0.0 |
| Williams | 69 | 61.9 | 3.60 | 3.23 | 0.0 |
| Force India | 68 | 56.3 | 3.54 | 2.93 | 0.0 |
| Sauber | 44 | 35.8 | 2.29 | 1.87 | 0.0 |
| Toro Rosso | 13 | 9.7 | 0.68 | 0.51 | 0.0 |
| Lotus | 0 | 0.0 | 0.00 | 0.00 | 0.0 |
| Virgin | 0 | 0.0 | 0.00 | 0.00 | 0.0 |
| HRT | 0 | 0.0 | 0.00 | 0.00 | 0.0 |

Sources: [F1 drivers](https://www.formula1.com/en/results/2010/drivers), [F1 constructors](https://www.formula1.com/en/results/2010/team), [F1 calendar/results](https://www.formula1.com/en/results/2010/races), [Jolpica race records](https://api.jolpi.ca/ergast/f1/2010/results/), [F1 pole awards](https://www.formula1.com/en/results/2010/awards/pole-positions).

### 2012 (20 races)

| Driver | Real pts | Model pts | Title % | Real wins | Model wins | Real podiums | Model podiums | Real poles | Model poles |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sebastian Vettel | 281 | 296.4 | 51.5 | 5 | 6.02 | 10 | 11.76 | 6 | 7.59 |
| Fernando Alonso | 278 | 292.1 | 45.6 | 3 | 5.07 | 13 | 11.32 | 2 | 5.11 |
| Lewis Hamilton | 190 | 201.7 | 1.1 | 4 | 2.21 | 7 | 7.09 | 7 | 1.75 |
| Jenson Button | 188 | 200.1 | 0.9 | 3 | 2.18 | 6 | 7.00 | 1 | 1.72 |
| Kimi Raikkonen | 207 | 197.7 | 0.8 | 1 | 1.75 | 7 | 6.53 | 0 | 0.98 |
| Mark Webber | 179 | 180.3 | 0.2 | 2 | 1.63 | 4 | 5.93 | 2 | 2.41 |
| Felipe Massa | 122 | 116.3 | 0.0 | 0 | 0.45 | 2 | 2.84 | 0 | 0.31 |
| Romain Grosjean | 96 | 89.2 | 0.0 | 0 | 0.23 | 3 | 1.80 | 0 | 0.10 |
| Nico Rosberg | 93 | 86.9 | 0.0 | 1 | 0.21 | 2 | 1.76 | 1 | 0.02 |
| Sergio Perez | 66 | 61.7 | 0.0 | 0 | 0.06 | 3 | 0.85 | 0 | 0.00 |
| Nico Hulkenberg | 63 | 58.8 | 0.0 | 0 | 0.06 | 0 | 0.78 | 0 | 0.00 |
| Kamui Kobayashi | 60 | 55.9 | 0.0 | 0 | 0.05 | 1 | 0.70 | 0 | 0.00 |
| Michael Schumacher | 49 | 46.5 | 0.0 | 0 | 0.04 | 1 | 0.58 | 0 | 0.01 |
| Paul di Resta | 46 | 43.0 | 0.0 | 0 | 0.02 | 0 | 0.40 | 0 | 0.00 |
| Pastor Maldonado | 45 | 41.3 | 0.0 | 1 | 0.02 | 1 | 0.42 | 1 | 0.00 |
| Bruno Senna | 31 | 28.3 | 0.0 | 0 | 0.01 | 0 | 0.22 | 0 | 0.00 |
| Jean-Eric Vergne | 16 | 14.8 | 0.0 | 0 | 0.00 | 0 | 0.03 | 0 | 0.00 |
| Daniel Ricciardo | 10 | 9.1 | 0.0 | 0 | 0.00 | 0 | 0.01 | 0 | 0.00 |
| Heikki Kovalainen | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Vitaly Petrov | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Timo Glock | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Charles Pic | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Narain Karthikeyan | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Pedro de la Rosa | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |

| Team | Real pts | Model pts | Real share % | Model share % | Constructor titles % |
|---|---:|---:|---:|---:|---:|
| Red Bull | 460 | 476.7 | 22.77 | 23.60 | 72.6 |
| Ferrari | 400 | 408.4 | 19.80 | 20.22 | 14.5 |
| McLaren | 378 | 401.8 | 18.71 | 19.89 | 12.9 |
| Lotus | 303 | 286.9 | 15.00 | 14.20 | 0.1 |
| Mercedes | 142 | 133.4 | 7.03 | 6.60 | 0.0 |
| Sauber | 126 | 117.5 | 6.24 | 5.82 | 0.0 |
| Force India | 109 | 101.9 | 5.40 | 5.04 | 0.0 |
| Williams | 76 | 69.6 | 3.76 | 3.45 | 0.0 |
| Toro Rosso | 26 | 23.9 | 1.29 | 1.18 | 0.0 |
| Caterham | 0 | 0.0 | 0.00 | 0.00 | 0.0 |
| Marussia | 0 | 0.0 | 0.00 | 0.00 | 0.0 |
| HRT | 0 | 0.0 | 0.00 | 0.00 | 0.0 |

Sources: [F1 drivers](https://www.formula1.com/en/results/2012/drivers), [F1 constructors](https://www.formula1.com/en/results/2012/team), [F1 calendar/results](https://www.formula1.com/en/results/2012/races), [Jolpica race records](https://api.jolpi.ca/ergast/f1/2012/results/), [F1 pole awards](https://www.formula1.com/en/results/2012/awards/pole-positions).

### 2021 (22 races)

| Driver | Real pts | Model pts | Title % | Real wins | Model wins | Real podiums | Model podiums | Real poles | Model poles |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Lewis Hamilton | 387.5 | 398.9 | 51.7 | 8 | 9.24 | 17 | 17.11 | 5 | 10.74 |
| Max Verstappen | 395.5 | 396.1 | 48.3 | 10 | 8.63 | 18 | 16.95 | 10 | 9.10 |
| Valtteri Bottas | 226 | 235.7 | 0.0 | 1 | 1.65 | 11 | 8.14 | 4 | 1.49 |
| Sergio Perez | 190 | 201.6 | 0.0 | 1 | 0.94 | 5 | 6.14 | 0 | 0.62 |
| Carlos Sainz | 164.5 | 164.2 | 0.0 | 0 | 0.45 | 4 | 4.15 | 0 | 0.02 |
| Charles Leclerc | 159 | 161.5 | 0.0 | 0 | 0.40 | 1 | 4.00 | 2 | 0.02 |
| Lando Norris | 160 | 157.1 | 0.0 | 0 | 0.39 | 4 | 3.80 | 1 | 0.02 |
| Daniel Ricciardo | 115 | 108.7 | 0.0 | 1 | 0.10 | 1 | 1.75 | 0 | 0.00 |
| Pierre Gasly | 110 | 107.3 | 0.0 | 0 | 0.12 | 1 | 1.89 | 0 | 0.00 |
| Fernando Alonso | 81 | 78.5 | 0.0 | 0 | 0.04 | 1 | 0.91 | 0 | 0.00 |
| Esteban Ocon | 74 | 72.8 | 0.0 | 1 | 0.03 | 1 | 0.76 | 0 | 0.00 |
| Sebastian Vettel | 43 | 42.0 | 0.0 | 0 | 0.00 | 1 | 0.18 | 0 | 0.00 |
| Lance Stroll | 34 | 33.3 | 0.0 | 0 | 0.00 | 0 | 0.09 | 0 | 0.00 |
| Yuki Tsunoda | 32 | 30.5 | 0.0 | 0 | 0.00 | 0 | 0.10 | 0 | 0.00 |
| George Russell | 16 | 15.5 | 0.0 | 0 | 0.00 | 1 | 0.01 | 0 | 0.00 |
| Kimi Raikkonen | 10 | 9.8 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Nicholas Latifi | 7 | 6.2 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Antonio Giovinazzi | 3 | 2.5 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Mick Schumacher | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Nikita Mazepin | 0 | 0.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |

| Team | Real pts | Model pts | Real share % | Model share % | Constructor titles % |
|---|---:|---:|---:|---:|---:|
| Mercedes | 613.5 | 634.5 | 27.79 | 28.56 | 69.0 |
| Red Bull | 585.5 | 597.7 | 26.52 | 26.90 | 30.9 |
| Ferrari | 323.5 | 325.7 | 14.65 | 14.66 | 0.0 |
| McLaren | 275 | 265.8 | 12.46 | 11.96 | 0.0 |
| Alpine | 155 | 151.2 | 7.02 | 6.81 | 0.0 |
| AlphaTauri | 142 | 137.8 | 6.43 | 6.20 | 0.0 |
| Aston Martin | 77 | 75.3 | 3.49 | 3.39 | 0.0 |
| Williams | 23 | 21.7 | 1.04 | 0.97 | 0.0 |
| Alfa Romeo | 13 | 12.3 | 0.59 | 0.55 | 0.0 |
| Haas | 0 | 0.0 | 0.00 | 0.00 | 0.0 |

Sources: [F1 drivers](https://www.formula1.com/en/results/2021/drivers), [F1 constructors](https://www.formula1.com/en/results/2021/team), [F1 calendar/results](https://www.formula1.com/en/results/2021/races), [Jolpica race records](https://api.jolpi.ca/ergast/f1/2021/results/), [F1 pole awards](https://www.formula1.com/en/results/2021/awards/pole-positions).

### 2024 (24 races)

| Driver | Real pts | Model pts | Title % | Real wins | Model wins | Real podiums | Model podiums | Real poles | Model poles |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Max Verstappen | 437 | 389.6 | 64.2 | 9 | 8.04 | 14 | 15.54 | 8 | 10.71 |
| Lando Norris | 374 | 357.7 | 25.2 | 4 | 5.53 | 13 | 13.56 | 8 | 5.86 |
| Charles Leclerc | 356 | 333.9 | 9.7 | 3 | 4.32 | 13 | 12.17 | 3 | 3.97 |
| Oscar Piastri | 292 | 285.7 | 0.7 | 2 | 2.38 | 8 | 9.31 | 0 | 1.70 |
| Carlos Sainz | 290 | 275.9 | 0.3 | 2 | 2.07 | 9 | 8.74 | 1 | 1.30 |
| George Russell | 245 | 227.8 | 0.0 | 2 | 0.92 | 4 | 5.86 | 4 | 0.28 |
| Lewis Hamilton | 223 | 208.6 | 0.0 | 2 | 0.60 | 5 | 4.80 | 0 | 0.13 |
| Sergio Perez | 152 | 138.3 | 0.0 | 0 | 0.13 | 4 | 1.84 | 0 | 0.05 |
| Fernando Alonso | 70 | 55.7 | 0.0 | 0 | 0.00 | 0 | 0.14 | 0 | 0.00 |
| Nico Hulkenberg | 41 | 34.7 | 0.0 | 0 | 0.00 | 0 | 0.02 | 0 | 0.00 |
| Pierre Gasly | 42 | 31.7 | 0.0 | 0 | 0.00 | 1 | 0.02 | 0 | 0.00 |
| Yuki Tsunoda | 30 | 22.0 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Lance Stroll | 24 | 17.8 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Esteban Ocon | 23 | 17.5 | 0.0 | 0 | 0.00 | 1 | 0.00 | 0 | 0.00 |
| Alexander Albon | 12 | 9.3 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Daniel Ricciardo | 12 | 7.6 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Kevin Magnussen | 16 | 5.4 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Logan Sargeant | 0 | 2.9 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Valtteri Bottas | 0 | 1.1 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |
| Zhou Guanyu | 4 | 0.9 | 0.0 | 0 | 0.00 | 0 | 0.00 | 0 | 0.00 |

| Team | Real pts | Model pts | Real share % | Model share % | Constructor titles % |
|---|---:|---:|---:|---:|---:|
| McLaren | 666 | 643.4 | 25.05 | 26.54 | 66.6 |
| Ferrari | 652 | 609.8 | 24.52 | 25.16 | 31.1 |
| Red Bull | 589 | 527.9 | 22.15 | 21.78 | 2.4 |
| Mercedes | 468 | 436.4 | 17.60 | 18.00 | 0.0 |
| Aston Martin | 94 | 73.5 | 3.54 | 3.03 | 0.0 |
| Alpine | 65 | 49.1 | 2.44 | 2.03 | 0.0 |
| Haas | 58 | 40.0 | 2.18 | 1.65 | 0.0 |
| RB | 46 | 29.6 | 1.73 | 1.22 | 0.0 |
| Williams | 17 | 12.2 | 0.64 | 0.50 | 0.0 |
| Sauber | 4 | 2.0 | 0.15 | 0.08 | 0.0 |

Sources: [F1 drivers](https://www.formula1.com/en/results/2024/drivers), [F1 constructors](https://www.formula1.com/en/results/2024/team), [F1 calendar/results](https://www.formula1.com/en/results/2024/races), [Jolpica race records](https://api.jolpi.ca/ergast/f1/2024/results/), [F1 pole awards](https://www.formula1.com/en/results/2024/awards/pole-positions).

## Checks

`python -m unittest tests -v` passed all six test groups, including subcases for all nine presets. Checks include exact points reconstruction after every race, event/DNF consistency, complete archives, all nine menu selections, custom drivers with invalid input, statistics and teammate comparison, unique saves, custom/default names, save/load round trips, archives after loading, legacy saves without name and all six existing user saves. Tests use temporary directories for writes.

The command-line program was also run for each year from a temporary copy containing only source files and presets, with site-packages disabled and Python environment overrides ignored. All nine completed a season, saved it and opened the archive. This was tested on Python 3.14.5; the documented minimum 3.9 is based on the language features used and was not separately executed. All project Python source files compile and all project JSON files parse. Git diff and whitespace checks were reviewed.

## Limits

No sprints, fastest-lap bonus, half-points, penalties, mid-season replacements or car development. There are no individual driver-specific mechanical failure rates. The reliability formula has a 2.8% minimum technical failure probability and cannot represent the very high failure rate of some old cars within 0-100 ratings. Track weather probabilities and gameplay ratings are estimates, not reconstructed observations. There are no special exceptions for individual historical results. Pole counts can differ considerably because qualifying and race pace share a single pace rating. Existing 2023, 2025 and 2026 presets were functionally checked but not historically rebalanced.

## Cleanup and release scope

Deleted the empty README.txt and seasons/test_json.py, an unused experimental loader that requested input on import. Replaced the previously non-runnable tests.py with useful release checks. No saves were deleted or rewritten. .venv, .idea, the existing packaging spec, build, dist and Python cache were left in place. Automatic safety review rejected the bulk cleanup command; generated folders are now ignored by Git. The old executable in dist was subsequently replaced with a checked v1.0 build, as described below.

Historical presets, source, useful documentation and user data were kept. There are no temporary calibration scripts inside the project. The retained balance/reference JSON files are evidence for this release, not files required by the game.

Additional sources: [points systems](https://www.formula1points.com/psd), [Spyker appearances](https://gpracingstats.com/constructors/spyker/).

Final status: ready for a v1.0 source and Windows x64 release, with the statistical/model limits above. The owner still needs to review the diff and make the final commit/tag.

## Windows executable

Built with Python 3.14.5 and PyInstaller 6.22.3 using F1-Championship-Generator.spec. All nine season presets are bundled in the executable. Saves are stored next to the executable rather than in its temporary extraction directory. ASCII table separators avoid encoding errors on Windows consoles and redirected output.

The executable was copied alone into a temporary directory with spaces and Cyrillic characters. All PYTHON environment variables were removed and PATH was restricted to Windows System32. All nine seasons completed, saved and opened a race archive. Separate executable processes verified persistent saves, unique filenames, loading, custom driver statistics, teammate comparison and the archive after restart. No external source files, presets or Python installation were used by these runs. Testing was on this Windows 11 x64 computer, not a separate clean Windows virtual machine.

F1-Championship-Generator-v1.0-Windows-x64.zip in dist is the package to attach to a GitHub release. It has not been uploaded. Commit the packaging spec with the source changes; keep the generated dist/build folders out of Git.
