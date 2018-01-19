import random
from json import dump

import gui
from validate import *


def generate_strike_pattern(seed, width, height):
    # Implemented according to map.rst, so should work.
    validated = False
    seed_plus = 0
    while not validated:
        random.seed(seed + seed_plus)
        astrd_list = []
        karb_possibilities = list(range(ASTEROID_KARB_MIN, ASTEROID_KARB_MAX + 1))
        round_possibilities = list(range(ASTEROID_ROUND_MIN, ASTEROID_ROUND_MAX + 1))
        x_possibilities = list(range(0, width))
        y_possibilities = list(range(0, height))
        rounds = 0
        while True:
            round_plus = random.choice(round_possibilities)
            rounds += round_plus
            if rounds >= ROUND_LIMIT:
                break
            karb = random.choice(karb_possibilities)
            x = random.choice(x_possibilities)
            y = random.choice(y_possibilities)
            astrd_list.append([rounds, karb, x, y])
        validated = validate_asteroid_pattern(astrd_list)
        if not validated:
            seed_plus += 1
    return astrd_list


def json_bot_list(bots, earth_height):
    bot_list = []
    for x, i in enumerate(bots):
        bot_dict = {
                "ability_cooldown": 500,
                "ability_heat": 0,
                "ability_range": 2,
                "attack_cooldown": 0,
                "attack_heat": 0,
                "attack_range": 0,
                "blast_damage": 50,
                "build_health": 5,
                "cannot_attack_range": 10,
                "countdown": 0,
                "damage": 0,
                "defense": 5,
                "factory_max_rounds_left": 5,
                "factory_rounds_left": None,
                "factory_unit_type": None,
                "garrison": [],
                "harvest_amount": 3,
                "has_worker_acted": False,
                "health": 100,
                "id": x,
                "is_ability_unlocked": True,
                "is_built": False,
                "is_used": False,
                "level": 0,
                "location": {
                    "OnMap": {
                        "planet": "Earth",
                        "x": i[1],
                        "y": i[0]
                    }
                },
                "max_capacity": 8,
                "max_countdown": 5,
                "max_health": 100,
                "movement_cooldown": 20,
                "movement_heat": 0,
                "repair_health": 10,
                "self_heal_amount": 1,
                "target_location": None,
                "team": "Red" if i[2] == 0 else "Blue",
                "travel_time_decrease": 0,
                "unit_type": "Worker",
                "vision_range": 50
            }
        bot_list.append(bot_dict)
    return bot_list


def json_random_asteroid_strikes(asteroid_list):
    asteroid_dict = {}
    for i in asteroid_list:
        asteroid_dict[i[0]] = {
            "karbonite": i[1],
            "location": {
                "planet": "Mars",
                "x": i[2],
                "y": i[3],
            }
        }
    return asteroid_dict


def json_orbit(amplitude, period, center):
    return {
        "amplitude": amplitude,
        "period": period,
        "center": center,
        "amplitude_s": amplitude,
        "period_s": period,
        "center_s": center
    }


def create_json(seed, earth_height, earth_width, earth_terrain, earth_karb, bots, mars_width, mars_height, mars_terrain,
                mars_karb, asteroids, orbit):
    return {
        "seed": seed,
        "earth_map": {
            "planet": "Earth",
            "height": earth_height,
            "width": earth_width,
            "initial_units": bots,
            "is_passable_terrain": earth_terrain[::-1],
            "initial_karbonite": earth_karb[::-1],
        },
        "mars_map": {
            "planet": "Mars",
            "height": mars_height,
            "width": mars_width,
            "initial_units": [],
            "is_passable_terrain": mars_terrain[::-1],
            "initial_karbonite": mars_karb[::-1],
        },
        "asteroids": {
            "pattern": asteroids
        },
        "orbit": orbit
    }

if __name__ == "__main__":
	try:
		seed = random.randint(0,10000)
		earth_width, earth_height, *_ = [int(i) for i in input("Enter Earth dimensions. Minimum 20x20, maximum 50x50. e.g 25 25: ").strip().split(" ")]
		
		print("""
Instructions:
LMB: obstacle, RMB: clear
Hold [0-9] + LMB: Karbonite
Hold W + LMB: Worker""")
		
		earth_terrain, earth_karbonite, robot_pos = gui.create_pygame_earth_editor(earth_height, earth_width,"Earth")
		
		mars_width, mars_height, *_ = [int(i) for i in input("Enter Mars dimensions. Minimum 20x20, maximum 50x50. e.g 25 25: ").strip().split(" ")]
		
		mars_terrain, mars_karbonite, discardme = gui.create_pygame_earth_editor(mars_height, mars_width,"Mars")
		
		asteroid_list = generate_strike_pattern(seed, mars_height, mars_width)
		
		amplitude=50
		period=200
		center=125
		
		bots = json_bot_list(robot_pos, earth_height)
		orbit_params = json_orbit(amplitude, period, center)
		asteroids = json_random_asteroid_strikes(asteroid_list)
		
		filename = input("Enter Map Name:")
		filename += ".bc18map"
		print("Creating json...")
		json_struct = create_json(seed, earth_height, earth_width, earth_terrain, earth_karbonite, bots, mars_width,
                                  mars_height, mars_terrain, mars_karbonite, asteroids, orbit_params)
		print("Created json!")
		dump(json_struct, open(filename, "w"))

	except KeyboardInterrupt:
		print("Exiting. File will not be created.")
