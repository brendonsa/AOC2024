data = open('input_values.txt').read().split('\n')
input_vals = dict()
for d in data:
    k,v = (d.split(':'))
    input_vals[k] = int(v[1:])

rules = open('input_rules.txt').read().split('\n')

for r in rules:
    v,k = r.split(' -> ')
    v = v.split(' ')
    input_vals[k] = v


def op_and(a,b):
    return a and b

def op_or(a,b):
    return a or b

def op_xor(a,b):
    return a!=b

# Extract z rules

z = []
for k in input_vals.keys():
    if k[0] == 'z':
        z.append(k)

OPERATIONS = {
    'AND': op_and,
    'OR': op_or,
    'XOR': op_xor
}

def solve(val):
    val1 = input_vals[val[0]]
    if isinstance(val1,list):
        val1 = solve(val1)
        # input_vals[val[0]] = val1
    val2 = input_vals[val[2]]
    if isinstance(val2,list):
        val2 = solve(val2)
        # input_vals[val[2]] = val2
    return OPERATIONS[val[1]](val1,val2)
    
binary_number = ''
for z_ in reversed(sorted(z)):
    print(z_)
    binary_number += str(int(solve(input_vals[z_])))

print(int(binary_number,2))
    
