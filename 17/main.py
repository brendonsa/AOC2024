import re
from collections import defaultdict

data = open('input.txt', 'r').read()


re_register = re.compile('Register .: (\d+)')

re_instructions = re.compile('Program:\s*([\d,]+)')

class Register:
    def __init__(self, name, value=0):
        self.name = name
        self.value = int(value)
    
    def __str__(self) -> str:
        return f'Register {self.name}: {self.value}'
    
    def __repr__(self):
        return f'Register({self.name},{self.value})'
registers = dict()
for name,value in zip(['A','B','C'],re_register.findall(data)):
    registers[name] = Register(name,value)


instructions = []
OUTPUT = []
for instruction in re_instructions.findall(data)[0].split(','):
    instructions.append(int(instruction))

def find_combo_operand(op):
    if op <4:
        return op
    elif op == 4:
        return registers['A'].value
    elif op == 5:
        return registers['B'].value
    elif op == 6:
        return registers['C'].value 
    else:
        raise ValueError('Invalid program')


def adv(op,pointer):
    registers['A'].value = registers['A'].value // (2**find_combo_operand(op))
    return pointer+2

def bxl(op,pointer):
    registers['B'].value =  registers['B'].value ^ op
    return pointer+2

def bst(op,pointer):
    registers['B'].value = find_combo_operand(op) %8
    return pointer+2

def jnz(op,pointer):
    if registers['A'].value == 0:
        return pointer+2
    else:
        return op
    
def bxc(_,pointer):
    registers['B'].value = registers['B'].value ^ registers['C'].value
    return pointer+2

def out(op,pointer):
    OUTPUT.append(find_combo_operand(op)%8)
    return pointer+2

def bdv(op,pointer):
    registers['B'].value = registers['A'].value // (2**find_combo_operand(op))
    return pointer+2

def cdv(op,pointer):
    registers['C'].value = registers['A'].value // (2**find_combo_operand(op))
    return pointer+2

OPERATIONS = {0:adv,
              1:bxl,
              2:bst,
              3:jnz,
              4:bxc,
              5:out,
              6:bdv,
              7:cdv,
}

pointer = 0
while True:
    if pointer >= len(instructions):
        break
    else:
        operation, operand = OPERATIONS[instructions[pointer]], instructions[pointer+1]
        pointer = operation(operand,pointer)

print(','.join(map(str,OUTPUT)))

def reset_registers(A):
    registers['A'].value=A
    registers['B'].value=0
    registers['C'].value=0

pointer = 0
b = 0
for a in range(len(instructions)):
    b+=8**a

b = 8**(len(instructions)-1)

def regen_output(a):
    pointer = 0
    reset_registers(a)
    OUTPUT.clear()

    while True:
        if pointer >= len(instructions):
            break
        else:
            operation, operand = OPERATIONS[instructions[pointer]], instructions[pointer+1]
            pointer = operation(operand,pointer)

a = 0
OUTPUT.clear()
possible_vals = defaultdict()
for i in reversed(range(len(instructions))):
    for x in range(9):
        possible_a = a+(8**i)*x
        regen_output(possible_a)
        if len(OUTPUT)!= len(instructions):
            continue
        else:
            if OUTPUT[i] == instructions[i]:
                possible_vals.append(x)
                a = possible_a
                break
print(a)


print(','.join(map(str,OUTPUT)))

# pointer = 0
# OUTPUT.clear()
# while True:
#     if pointer >= len(instructions):
#         break
#     else:
#         operation, operand = OPERATIONS[instructions[pointer]], instructions[pointer+1]
#         pointer = operation(operand,pointer)

# print(','.join(map(str,OUTPUT)))


# reset_registers(potential_A)
# OUTPUT.clear()
# from collections import defaultdict
# POTENTIAL_NUMS = defaultdict(set)
# while True:
#     if potential_A == 10000000:
#         print(POTENTIAL_NUMS)
#         print(set.intersection(*POTENTIAL_NUMS.values()))
#     if pointer >= len(instructions):
#         if len(OUTPUT)!=len(instructions):
#             OUTPUT.clear()
#             potential_A+=1
#             reset_registers(potential_A)
#             pointer = 0
#             continue
#         if any(OUTPUT!=instructions):
#             pointer = 0
#             potential_A+=1
#             OUTPUT.clear()
#             reset_registers(potential_A)
#             continue
#         break
#     else:
#         operation, operand = OPERATIONS[instructions[pointer]], instructions[pointer+1]
#         pointer = operation(operand,pointer)
#         for idx, o in enumerate(OUTPUT):
#             if instructions[idx] != o:
#                 pointer = 100000
#             if instructions[idx] == o:
#                 POTENTIAL_NUMS[idx].add(potential_A)

# print(potential_A)