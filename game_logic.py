class Game:
    def __init__(self):
        self.world = {
            'dark_cave': {
                'description': 'You are in a dark, damp cave. The air is heavy. There is a faint light coming from a passage to the north.',
                'exits': {'north': 'lit_room'},
                'image': 'images/dark_cave.png'
            },
            'lit_room': {
                'description': 'You have entered a larger room, lit by a hole in the ceiling. You see an old wooden chest in one corner and a passage to the east.',
                'exits': {'east': 'narrow_corridor', 'south': 'dark_cave'},
                'image': 'images/lit_room.png'
            },
            'narrow_corridor': {
                'description': 'You are in a narrow corridor. Ahead of you is a large stone door with an inscription. It seems to be locked. The only way back is west.',
                'exits': {'west': 'lit_room'},
                'image': 'images/narrow_corridor.png'
            },
            'cave_exit': {
                'description': 'You found the exit and see the sunlight! Congratulations!',
                'exits': {},
                'image': 'images/exit.png' 
            }
        }
        self.current_room_key = 'dark_cave'
        self.is_door_locked = True

    def get_current_room_data(self):
        return self.world[self.current_room_key]

    def process_movement(self, direction):
        valid_exits = self.get_current_room_data()['exits']
        if direction in valid_exits:
            self.current_room_key = valid_exits[direction]
            return True
        return False

    def process_action(self, action, value=None):
        if action == 'read':
            if self.current_room_key == 'narrow_corridor':
                return "The inscription reads: 'I have no voice, but I speak. I have no body, but I come alive with wind. What am I?'"
            else:
                return "There is nothing to read here."

        elif action == 'answer':
            if self.current_room_key == 'narrow_corridor':
                if self.is_door_locked and value.lower() == 'an echo':
                    self.is_door_locked = False
                    self.world['narrow_corridor']['exits']['east'] = 'cave_exit'
                    return "With a loud GRIND, the stone door slowly opens... The way east is now clear!"
                elif not self.is_door_locked:
                    return "The door is already open."
                else:
                    return "Nothing happens."
            else:
                return "There is nothing to answer here."