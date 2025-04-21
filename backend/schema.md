Schema format : Table(columns) — Table description

drivers(driverid, driverref, number, code, forename, surname, dob, nationality, url) — Information about F1 drivers.

driver_standings(driverstandingsid, raceid, driverid, points, position, positiontext, wins) — Driver championship standings for each race.

races(raceid, year, round, circuitid, name, date, time, url, fp1_date, fp1_time, fp2_date, fp2_time, fp3_date, fp3_time, quali_date, quali_time, sprint_date, sprint_time) — Information about each race and session timings.

results(resultid, raceid, driverid, constructorid, number, grid, position, positiontext, positionorder, points, laps, time, milliseconds, fastestlap, rank, fastestlaptime, fastestlapspeed, statusid) — Main race results for each driver in each race.

constructors(constructorid, constructorref, name, nationality, url) — Information about constructors (teams).

constructor_results(constructorresultsid, raceid, constructorid, points, status) — Constructor (team) race result per event.

constructor_standings(constructorstandingsid, raceid, constructorid, points, position, positiontext, wins) — Constructor (team) championship standings per race.

lap_times(raceid, driverid, lap, position, time, milliseconds) — Lap-by-lap times per driver per race.

pit_stops(raceid, driverid, stop, lap, time, duration, milliseconds) — Pit stop details for each driver.

qualifying(qualifyid, raceid, driverid, constructorid, number, position, q1, q2, q3) — Qualifying session results.

seasons(year, url) — Available F1 seasons.

sprint_results(resultid, raceid, driverid, constructorid, number, grid, position, positiontext, positionorder, points, laps, time, milliseconds, fastestlap, fastestlaptime, statusid) — Sprint race results per driver.

status(statusid, status) — Status codes used in race results (e.g., "Finished", "DNF").

circuits(circuitid, circuitref, name, location, country, lat, lng, alt, url) — Circuit information including location and coordinates.
