rules = [
    ("S1", "B1S"),
    ("1SD", "RD"),
    ("B1", "1B"),
    ("BRD", "RDB"),
    ("_RD", "_"),
    ("_R", "_S"),
    ("_B", "1_"),
    ("1_", "1"),
    ("1R", "R1"),
]

def is_terminal(s):
    return all(c == "1" for c in s)

def derive_to_terminal(s, max_steps=1000):
    derivation = [s]
    step = 0

    while step < max_steps:
        if is_terminal(s):
            break
        applied = False
        for lhs, rhs in rules:
            idx = s.find(lhs)
            if idx != -1:
                s = s[:idx] + rhs + s[idx+len(lhs):]
                derivation.append(s)
                print(f"Step {step+1}: {lhs} -> {rhs} => {s}")
                step += 1
                applied = True
                break 
        if not applied:
            print("Fail!")
            break

    return derivation

input_string = "_S"
user_input = input("Enter input: ")
input_string += user_input
input_string += "D"
print("Starting input:", input_string)
derivation_sequence = derive_to_terminal(input_string)

print("\nOutput:", derivation_sequence[-1])
print(f'In decimal: ', len(derivation_sequence[-1]))