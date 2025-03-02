class Character:
    def __init__(self, name, hp, mp, arm, dmg):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.arm = arm
        self.dmg = dmg

    def take_damage(self, damage):
        actual_damage = max(0, damage - self.arm)
        self.hp -= actual_damage
        return actual_damage

    def is_alive(self):
        return self.hp > 0


class Game:
    def __init__(self):
        self.map = None
        self.player = None
        self.enemy = None
        self.inventory = []

    def create_map(self, width, height):
        self.map = [['.' for _ in range(width)] for _ in range(height)]
        self.map[height // 2][width // 2] = 'P'  # Изначальная позиция игрока
        self.enemy = Character("Enemy", hp=20, mp=0, arm=1, dmg=5)
        self.map[height // 2][(width // 2) + 2] = 'E'  # Позиция врага рядом с игроком

    def render_map(self):
        for row in self.map:
            print(' '.join(row))
        print(f"HP Игрока: {self.player.hp}, HP Противника: {self.enemy.hp}")

    def move_player(self, direction):
        px, py = self.find_player()
        new_x, new_y = px, py
        
        if direction == 'w' and px > 0:  # вверх
            new_x = px - 1
        elif direction == 's' and px < len(self.map) - 1:  # вниз
            new_x = px + 1
        elif direction == 'a' and py > 0:  # влево
            new_y = py - 1
        elif direction == 'd' and py < len(self.map[0]) - 1:  # вправо
            new_y = py + 1

        # Проверяем, не будет ли игрок перемещаться на позицию врага
        if self.map[new_x][new_y] != 'E':
            self.map[px][py] = '.'  # Стереть старую позицию
            self.map[new_x][new_y] = 'P'  # Обозначить новую позицию игрока

    def find_player(self):
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == 'P':
                    return y, x
        return None

    def attack_enemy(self):
        damage = self.player.dmg
        actual_damage = self.enemy.take_damage(damage)
        print(f"{self.player.name} атаковал {self.enemy.name}, нанес ему {actual_damage} урона!")

    def check_attack(self):
        px, py = self.find_player()
        ex, ey = self.get_enemy_position()

        # Проверяем, находится ли враг рядом с игроком (не на одной позиции)
        if (abs(px - ex) + abs(py - ey) == 1) and (px != ex or py != ey):
            self.attack_enemy()
        else:
            print("Враг находися далко, чтобы атаковать.")

    def get_enemy_position(self):
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == 'E':
                    return y, x
        return None
        
    def show_inventory(self):
        print("Инвентарь:")
        print("1. Нож (z) - Урон: 9")
        print("2. Зелье (x) - Урон: 5")
        print("3. Топорик (c) - Урон: 11")
        print("4. Ничего (v)")
        choice = input("Выберите предмет (z/x/c/v): ")
        if choice == 'z':
            self.selected_item = 'knife'
            self.player.dmg = 10
        elif choice == 'x':
            self.selected_item = 'potion'
            self.player.dmg = 6
        elif choice == 'c':
            self.selected_item = 'axe'
            self.player.dmg = 12
        elif choice == 'v':
            self.selected_item = 'nothing'
            self.player.dmg = 4
        else:
            print("Неправильный выбор предмета")

    def game_loop(self):
        while self.player.is_alive() and self.enemy.is_alive():
            self.render_map()
            action = input("Выберите действие (w/a/s/d для передвижения, e для атаки, r для просмотра инвентаря)")
            if action in ['w', 'a', 's', 'd']:
                self.move_player(action)
            elif action == 'e':
                self.check_attack()  # Проверка атаки при нажатии "e"
            elif action == "r":
                self.show_inventory()

        if not self.player.is_alive():
            print("Game Over!")
        if not self.enemy.is_alive():
            print("Враг повержен!")


def main():
    print("Добро пожаловать в игру!")
    game = Game()
    player_name = input("Введите имя вашего персонажа: ")
    game.player = Character(player_name, hp=30, mp=0, arm=2, dmg=4)
    
    map_type = input("Выберете тип карты (стандарт/генерация): ")
    if map_type == 'генерация':
        width = int(input("Введите ширину: "))
        height = int(input("Введите высоту: "))
        game.create_map(width, height)
    else:
        game.create_map(5, 5)  # Стандартная карта 5x5

    game.game_loop()


if __name__ == "__main__":
    main()