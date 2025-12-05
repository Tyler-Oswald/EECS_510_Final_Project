from Simulator.turing import state, Turing

def load_tm(filename):
    transitions = {}
    start_state = None
    accepting_state = None
    states_list = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("States:"):
                states_list = line.split(":", 1)[1].strip().split()
            elif line.startswith("Start_state:"):
                start_state = line.split(":", 1)[1].strip()
            elif line.startswith("Accepting_State:"):
                accepting_state = line.split(":", 1)[1].strip()
            elif line.startswith("Transitions:"):
                line = line.split(":", 1)[1].strip()
                trans_strings = line.split()
                for tr_str in trans_strings:
                    tr_str = tr_str.strip("()")
                    parts = [p.strip() for p in tr_str.strip("()").split(",")]
                    parts = [str(p) for p in parts]
                    if len(parts) != 8:
                        raise ValueError(f"Invalid transition: {tr_str}")
                    src, r1, r2, nxt, w1, w2, mv1, mv2 = parts
                    if src not in transitions:
                        transitions[src] = []
                    transitions[src].append((r1, r2, nxt, w1, w2, mv1, mv2))

    states = [state(name, transitions.get(name, [])) for name in states_list]

    return states, start_state, accepting_state

def main():
    filename = "data_structure.txt"
    while(True):
        tape_input = input("Enter initial tape1 input string or (q)uit: ").strip()
        if tape_input == 'q':
            break

        states, start_state, accepting_state = load_tm(filename)
        tm = Turing(start_state, states, tape_input)
        tm.accepting = accepting_state

        result = tm.simulate()

        if result[0] == "ACCEPT":
            print("\nACCEPTED")
            output_tape = ''
            for i in range(len(result[1])):
                if result[1][i] == '1':
                    output_tape += '1'
            print("Output on Tape2: ", output_tape)
            print("Path of transitions:")
            print("Current state | Read tape 1 | Write tape 1 | Read tape 2 | Write tape 2 | New state")
            for p in result[2]:
                print(f"       {p[0]}           {p[1]}              {p[2]}              {p[3]}             {p[4]}            {p[5]}")
        else:
            print("\nREJECTED")

if __name__ == "__main__":
    main()