from turing import state, Turing
#Function to convert the file data structure
def load_tm(filename):
    #Hold information about the machine 
    transitions = {}
    start_state = None
    accepting_state = None
    states_list = []
    #Open file
    with open(filename, "r") as f:
        #Parse each line in the file 
        for line in f:
            line = line.strip()
            if not line:
                continue
            #Case for the states 
            if line.startswith("States:"):
                states_list = line.split(":", 1)[1].strip().split()
            #Case for the start states 
            elif line.startswith("Start_state:"):
                start_state = line.split(":", 1)[1].strip()
            #Case for the accepting states 
            elif line.startswith("Accepting_State:"):
                accepting_state = line.split(":", 1)[1].strip()
            #Case for the transitions 
            elif line.startswith("Transitions:"):
                #Remove lable 
                line = line.split(":", 1)[1].strip()
                #Split each transition into different strings 
                trans_strings = line.split()
                #Process the transitions 
                for tr_str in trans_strings:
                    #Remove the parentheses from the transition
                    tr_str = tr_str.strip("()")
                    #Break the transition into parts 
                    parts = [p.strip() for p in tr_str.strip("()").split(",")]
                    parts = [str(p) for p in parts]
                    #If the there are not 8 parts for each transition, something is wrong 
                    if len(parts) != 8:
                        raise ValueError(f"Invalid transition: {tr_str}")
                    #Get the transition data from the parts 
                    src, r1, r2, nxt, w1, w2, mv1, mv2 = parts
                    #Map each state to transitions using dictionary 
                    if src not in transitions:
                        transitions[src] = []
                    transitions[src].append((r1, r2, nxt, w1, w2, mv1, mv2))
    #Load the state data and transitions into the state object 
    states = [state(name, transitions.get(name, [])) for name in states_list]

    return states, start_state, accepting_state

def main():
    #Hard code in the file data structure 
    filename = "data_structure.txt"
    #Main loop
    while(True):
        #Ask the user for initial input 
        tape_input = input("Enter initial tape1 input string or (q)uit: ").strip()
        #Exit condition 
        if tape_input == 'q':
            break
        #Get the data from the file 
        states, start_state, accepting_state = load_tm(filename)
        #Initalize the class object 
        tm = Turing(start_state, states, tape_input)
        #Set the accepting state for the machine 
        tm.accepting = accepting_state
        #Run the machine on the input given
        result = tm.simulate()
        #Case for if the machine accepted the input 
        if result[0] == "ACCEPT":
            print("\nACCEPTED")
            output_tape = ''
            #Loop over the tape to print out a clean version 
            #Otherwise, it would have a bunch of 0s from the blanks
            for i in range(len(result[1])):
                if result[1][i] == '1':
                    output_tape += '1'
            #Print out the outpyt from the second tape 
            print("Output on Tape2: ", output_tape)
            print("Path of transitions:")
            print("Current state | Read tape 1 | Write tape 1 | Read tape 2 | Write tape 2 | New state")
            #Print out the path the input took through the machine 
            for p in result[2]:
                print(f"       {p[0]}           {p[1]}              {p[2]}              {p[3]}             {p[4]}            {p[5]}")
        #Otherwise, print that the input was rejected 
        else:
            print("\nREJECTED")

if __name__ == "__main__":
    main()