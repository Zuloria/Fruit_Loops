from src.grid import Grid
from src.player import Player
from src import pickups


class GameState:
    """Samla spelets variabler i en klass."""
    def __init__(self):
        self.player = Player(16, 5)
        self.score = 0
        self.inventory = []

        self.g = Grid()
        self.g.set_player(self.player)
        self.g.make_walls()
        for i in range(2):
            self.g.random_walls_x()
            self.g.random_walls_y()
        pickups.randomize(self.g)


def print_status(game_grid, state):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have {state.score} points.")
    print(game_grid)


def start(state):
    command = "a"
    # Loopa tills användaren trycker Q eller X.
    while not command.casefold() in ["q", "x"]:
        print_status(state.g, state)

        command = input("To see inventory, use I. \nUse WASD to move, Q/X to quit. ")
        command = command.casefold()[:1]

        if command == "w" and state.player.can_move(0, -1, state.g):  # move up
            maybe_item = state.g.get(state.player.pos_x, state.player.pos_y -1)
            state.player.move(0, -1)
            if state.score > 0:
                state.score -= 1

        elif command == "a" and state.player.can_move(-1, 0, state.g):  # move left
            maybe_item = state.g.get(state.player.pos_x - 1, state.player.pos_y)
            state.player.move(-1, 0)
            if state.score > 0:
                state.score -= 1

        elif command == "s" and state.player.can_move(0, 1, state.g):  # move down
            maybe_item = state.g.get(state.player.pos_x, state.player.pos_y + 1)
            state.player.move(0, 1)
            if state.score > 0:
                state.score -= 1

        elif command == "d" and state.player.can_move(1, 0, state.g):  # move right
            maybe_item = state.g.get(state.player.pos_x + 1, state.player.pos_y)
            state.player.move(1, 0)
            if state.score > 0:
                state.score -= 1 

        else:
            maybe_item = None 

        if isinstance(maybe_item, pickups.Item):
            # we found something
            state.score += maybe_item.value
            print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")
            state.inventory.append(maybe_item)
            state.g.clear(state.player.pos_x, state.player.pos_y)

        if command == "i" and len(state.inventory) > 0:
            print("--------------------------------------")
            print(f"You have the following items:")
            for item in state.inventory:
                print(f"A {item.name} worth {item.value} ")

        elif command == "i" and len(state.inventory) == 0:
            print(f"You currently have no items :( ")

        
            
            


    # Hit kommer vi när while-loopen slutar
    print("Thank you for playing!")


# __name__ skapas av Python och sätts till "__main__" om man startar game.py
# direkt. Detta är för att undvika att start-funktionen körs om man importerar
# saker från game.py i en annan fil, till exempel vid testning.
if __name__ == "__main__":
    game_state = GameState()
    start(game_state)
