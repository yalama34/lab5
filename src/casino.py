import random
from typing import Optional
from wsgiref.util import request_uri

from .collection import PlayerCollection, GooseCollection, CasinoBalance
from .chip import Chip
from faker import Faker
from .constants import PlayerType, GooseType, player_min_bets
from .goose import BaseGoose, WarGoose, HonkGoose, LeaderGoose, LenderGoose, MimicGoose, TraitorGoose
from .player import PoorPlayer, MiddlePlayer, RichPlayer

fake = Faker('ru_RU')

class Casino:
    def __init__(self):
        self.players = PlayerCollection()
        self.geese = GooseCollection()
        self.balances = CasinoBalance()

        self.player_objects = {
            PlayerType.poor: PoorPlayer,
            PlayerType.middle: MiddlePlayer,
            PlayerType.rich: RichPlayer
        }

        self.goose_objects = {
            GooseType.base: BaseGoose,
            GooseType.war: WarGoose,
            GooseType.honk: HonkGoose,
            GooseType.leader: LeaderGoose,
            GooseType.lender: LenderGoose,
            GooseType.mimic: MimicGoose,
            GooseType.traitor: TraitorGoose,
        }

    def register_player(self, name: Optional[str] = None, social_class: Optional[str] = None):
        if name is None:
            name = fake.first_name()

        social_class_list = [soc.value for soc in PlayerType]
        if social_class is None:
            social_class = random.choice(social_class_list)
        elif social_class not in social_class_list:
            raise ValueError(f"Invalid social class {social_class}")

        player_class = self.player_objects[PlayerType(social_class)]
        player = player_class(name=name, social_class=social_class)
        self.balances[player.name] = player.balance
        self.players.append(player)
        print(f"На арене появляется новый игрок:\n{player}")

    def register_goose(self, name: Optional[str] = None, goose_type: Optional[str] = None):
        if name is None:
            name = fake.first_name()

        goose_type_list = [goose.value for goose in GooseType]
        if goose_type is None:
            goose_type = random.choice(goose_type_list)
        elif goose_type not in goose_type_list:
            raise ValueError(f"Invalid goose type {goose_type}")

        goose_class = self.goose_objects[GooseType(goose_type)]
        goose = goose_class(name=name, social_class=goose_type)
        self.geese.append(goose)
        print(f"В игру влетает новый гусь:\n{goose}")

    def remove_bankrupt_players(self):
        bankrupts = [player for player in self.players if player.balance.value <= 0]
        for player in bankrupts:
            self.players.remove_player(player)
            print(f"Игрок {player.name} обанкротился и покинул казино!")

    def event_bet(self):
        if not self.players:
            return None
        try:
            player = random.choice(self.players)
            goose = random.choice(self.geese)
        except IndexError:
            return None

        if random.random() <= 0.1 and goose and goose.balance > 0:
            bet = goose.balance
            if random.random() < 0.45:
                goose.balance += bet
                print(f"Гусь {goose.name} зачем-то решил депнуть. Ну и ладно, он выиграл. Выиграно фишек: {bet}")
            else:
                goose.balance -= bet
                print(f"Гусь {goose.name} зачем-то решил депнуть. Он проиграл, но и зачем ему эти фишки... Проиграно фишек: {bet}")
        bet = min(player_min_bets[player.social_class], player.balance)
        if bet <= 0:
            return f"Игрок {player.name} не может ставить"

        if random.random() < player.win_chance:
            player.balance += bet
            self.balances[player.name] = player.balance
            return f"Игрок {player.name} депнул и не прогадал. Выиграно фишек: {bet}"

        else:
            player.balance -= bet
            self.balances[player.name] = player.balance
            return f"Игрок {player.name} проиграл деньги системе и теперь плачет. Проиграно фишек: {bet}"

    def event_war_goose_attack(self):
        war_geese = [goose for goose in self.geese if goose.social_class == "war"]
        if not war_geese:
            return None
        goose = random.choice(war_geese)
        player = random.choice(self.players)
        if player.social_class == "rich":
            if random.random() < 0.6:
                return f"Гусь {goose.name} попытался атаковать игрока {player.name}, однако он богатый дядя и ходит с личной охраной. Атака провалена!"
        stolen = goose.steal_value + random.randint(0, 20)
        player.balance -= stolen
        goose.balance += stolen
        self.balances[player.name] = player.balance
        return f"Средь бела дня гусь {goose.name} атакует игрока {player.name} и крадёт у него {stolen} фишек!"

    def event_honk(self):
        honk_geese = [g for g in self.geese if g.social_class == "honk"]
        leader_geese = [g for g in self.geese if g.social_class == "leader"]
        war_geese = [g for g in self.geese if g.social_class == "war"]

        if not honk_geese and not leader_geese:
            goose = random.choice(self.geese)
            return f"Гусь {goose.name} крикнул с громкостью {goose.honk_volume}"

        if honk_geese and leader_geese:
            if random.random() < 0.8:
                goose = random.choice(honk_geese)
                goose()
            else:
                leader = random.choice(leader_geese)
                leader()
                if war_geese:
                    war_goose = random.choice(war_geese)
                    war_goose.steal_value += 5
                    return f"Лидер {leader.name} воодушевил гуся {war_goose.name}! Сила кражи увеличена на 5 и теперь равняется {war_goose.steal_value}"
                else:
                    return "Однако настоящих воинов среди гусей не нашлось..."

        elif honk_geese:
            goose = random.choice(honk_geese)
            goose()

        elif leader_geese:
            leader = random.choice(leader_geese)
            leader()
            if war_geese:
                war_goose = random.choice(war_geese)
                war_goose.steal_value += 5
                return f"Лидер {leader.name} воодушевил гуся {war_goose.name}! Сила кражи увеличена на 5 и теперь равняется {war_goose.steal_value}"
            else:
                return "Однако настоящих воинов среди гусей не нашлось..."

    def event_panic(self):
        poor_players = [p for p in self.players if p.social_class == "poor"]
        if not poor_players:
            return None
        if random.random() < 0.2:
            player = random.choice(poor_players)
            lost = player.balance
            player.balance = Chip(0)
            self.balances[player.name] = player.balance

            return f"Игрок {player.name} впал в панику и потерял все свои сбережения ({lost} фишек)!"

        return "Игры происходят как обычно, никто не паникует"

    def event_lender_loan(self):
        lenders = [g for g in self.geese if g.social_class == "lender"]
        if not lenders or not self.players:
            return None
        lender = random.choice(lenders)
        player = random.choice(self.players)

        if player.balance > 25:
            return f"Гусь {lender.name} предлагает игроку {player.name} взять фишки в долг, но тот отказался"

        loan_dict = {"poor": Chip(50), "middle": Chip(100), "rich": Chip(200)}
        interest_dict = {"poor": Chip(5), "middle": Chip(3), "rich": Chip(2)}

        amount = loan_dict[player.social_class]
        interest = interest_dict[player.social_class]

        player.debt.append({"amount": amount, "interest": interest, "remaining": amount})
        player.balance += amount
        self.balances[player.name] = player.balance

        return f"Гусь {lender.name} одолжил {player.name} {amount} фишек. Проценты: {interest}/ход"

    def event_traitor_goose_mercy(self):
        traitor_geese = [goose for goose in self.geese if goose.social_class == "traitor"]
        if not traitor_geese:
            return None
        goose = random.choice(traitor_geese)
        player = random.choice(self.players)
        given = goose.steal_value + random.randint(0, 20)
        player.balance += given
        goose.balance -= given
        self.balances[player.name] = player.balance
        return f"Гусь {goose.name} проявил милосердие к игру {player.name} и отсыпал ему {given} фишек!"

    def event_mimic(self):
        mimics = [goose for goose in self.geese if isinstance(goose, MimicGoose)]
        if not mimics:
            return None
        mimic = random.choice(mimics)

        targets = [goose for goose in self.geese if not isinstance(goose, MimicGoose)]
        if not targets:
            return f"Гусь {mimic.name} пытался имитировать, но вокруг лишь одни мимики"
        target = random.choice(targets)
        if mimic.imitating is None:
            mimic.start_imitating(target, duration=3)
        return f"Гусь {mimic.name} начал имитировать {target.__class__.__name__} на 3 шага!"

    def run_simulation(self, steps: int = 10, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
        print("=== НАЧАЛО СИМУЛЯЦИИ === \n")

        for step in range(1, steps + 1):
            if len(self.players) == 0:
                break
            print(f"--- ШАГ {step} ---")

            for goose in self.geese:
                if isinstance(goose, MimicGoose):
                    if goose.imitation_steps_left > 0:
                        if goose.imitation_steps_left == 0:
                            goose.end_imitating()
                            print(f"Гусь {goose.name} закончил имитацию!")

            self.remove_bankrupt_players()

            for player in self.players:
                if hasattr(player, 'debt') and player.debt:
                    debt_msg = player.pay_debt()
                    if debt_msg:
                        print(f"{player.name}: {debt_msg}")
                        self.balances[player.name] = player.balance

            possible_events = []

            if self.players:
                possible_events.append(self.event_bet)

            if any(g.social_class == "war" for g in self.geese):
                possible_events.append(self.event_war_goose_attack)

            honk_or_leader = any(g.social_class in ("honk", "leader") for g in self.geese)
            if honk_or_leader:
                possible_events.append(self.event_honk)

            if any(p.social_class == "poor" for p in self.players):
                possible_events.append(self.event_panic)

            if any(g.social_class == "lender" for g in self.geese) and self.players:
                possible_events.append(self.event_lender_loan)

            if len(self.players) < 10 and random.random() < 0.3:
                possible_events.append(lambda: self.register_player())

            if len(self.geese) < 15 and random.random() < 0.3:
                possible_events.append(lambda: self.register_goose())

            if any(g.social_class == "mimic" for g in self.geese):
                possible_events.append(self.event_mimic)

            if possible_events:
                chosen_event = random.choice(possible_events)
                result = chosen_event()
                if result:
                    print(f"{result}")
            else:
                print("Ничего не произошло...")

        print("СИМУЛЯЦИЯ ЗАВЕРШЕНА")
        print("=" * 70)
        print("ФИНАЛЬНЫЕ БАЛАНСЫ:")
        if len(self.players) == 0:
            print("Все игроки обанкротились!")
        else:
            for player in self.players:
                print(f"  {player.name}: {player.balance} фишек")




