from functools import lru_cache

data = open('input.txt').read()
data = data.split('\n')



def is_over_none_position(from_coord, directions, none_coord):
    current_pos = from_coord
    for direction in directions:
        for move in direction:
            if move == '<':
                current_pos = (current_pos[0], current_pos[1] - 1)
            elif move == '>':
                current_pos = (current_pos[0], current_pos[1] + 1)
            elif move == 'v':
                current_pos = (current_pos[0] + 1, current_pos[1])
            elif move == '^':
                current_pos = (current_pos[0] - 1, current_pos[1])
            if current_pos == none_coord:
                return True
    return False


def calculate_directions(from_coord, to_coord, none_coord):
    directions = []
    delta_row = to_coord[0] - from_coord[0]
    delta_col = to_coord[1] - from_coord[1]

    if delta_col < 0:
        directions.append('<' * abs(delta_col))
    if delta_row > 0:
        directions.append('v' * abs(delta_row))
    
    if delta_row < 0:
        directions.append('^' * abs(delta_row))
    if delta_col > 0:
        directions.append('>' * delta_col)

    if is_over_none_position(from_coord, directions, none_coord):
        directions.reverse()

    
    directions.append('A')
    
    return ''.join(directions)

def generate_keypad_mapping(keypad, none_coord):
    mapping = {}

    for from_key, from_coord in keypad.items():
        mapping[from_key] = {}
        for to_key, to_coord in keypad.items():
            if from_key != to_key:  # No need to map a key to itself
                mapping[from_key][to_key] = calculate_directions(from_coord, to_coord,none_coord)

    return mapping

keypad = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
    '0': (3, 1), 'A': (3, 2)
}

KEY_MAP = generate_keypad_mapping(keypad, (3,0))

directional_keyboard = {
            '^':(0,1),'A':(0,2),
    '<':(1,0),'>':(1,2),'v':(1,1)
}
DIRECTIONAL_MAP = generate_keypad_mapping(directional_keyboard, (0,0))

# Get the needed keypresses
curr_button = 'A'
presses = []
for d in data:
    press = ''
    for elem in d:
        press += KEY_MAP[curr_button][elem]
        curr_button=elem
    presses.append(press)

presses_copy = presses.copy()

for _ in (range(2)):
    for idx, press in enumerate(presses):
        curr_button = 'A'

        new_press = ''
        for elem in press:
            try:
                new_press += DIRECTIONAL_MAP[curr_button][elem]
            except KeyError:
                new_press += 'A'
            curr_button = elem

        presses[idx] = new_press


a = 0
for d,p in zip(data,presses):
    d = d.lstrip('0').rstrip('A')
    d = int(d)
    print(d, len(p))
    a+= d*(len(p))
print(a)




presses = presses_copy

# Need to reverse the first solution. Go in Depth first.
# Memoization is crucial here
@lru_cache(maxsize=None)
def get_keypresses(depth,curr_button,elem):
    if depth == 1:
        try:
            # Length would be too wild to handle. Return only a number of presses.
            # Presses themselves would be analysed in the upper layers.
            return len(DIRECTIONAL_MAP[curr_button][elem])
        except KeyError:
            return 1
    else:
        try:
            key_press = DIRECTIONAL_MAP[curr_button][elem]
        except KeyError:
            key_press = 'A'
        to_ret = 0
        curr_button = 'A'
        for k in key_press:
            to_ret += get_keypresses(depth-1,curr_button,k)
            curr_button=k
        return to_ret


presses_new = []    
for p in presses:
    p_new = 0
    curr_button = 'A'
    for p_ in p:
        p_new += get_keypresses(25,curr_button,p_)
        curr_button = p_
    presses_new.append(p_new)



a = 0
for d,p in zip(data,presses_new):
    d = d.lstrip('0').rstrip('A')
    d = int(d)
    print(d, p)
    a+= d*(p)
print(a)
