from src.casino import Casino

if __name__ == "__main__":
    casino = Casino()
    try:
        simulation_steps = int(input("Введите количество шагов симуляции (дефолтное значение - 10): "))
    except AttributeError:
        simulation_steps = 10
    seed = input("Введите сид (если не хотите устанавливать сид введите -): ")
    if seed == '-':
        seed = None
    else:
        try:
            seed = int(seed)
        except ValueError:
            print("Некорректное значение сида. Используется случайный сид.")
            seed = None
    players_count = int(input("Введите изначальное количество игроков: "))
    geese_count = int(input("Введите изначальное количество гусей: "))
    for i in range(players_count):
        casino.register_player()

    for i in range(geese_count):
        casino.register_goose()

    casino.run_simulation(steps=simulation_steps, seed=seed)