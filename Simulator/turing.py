#This class pairs a state name with all the transitions from that state 
class state:
    def __init__(self,name, transitions):
        self.name = name
        self.trans = transitions
#Class for the turing machine   
class Turing:
    #We take in the start state, states, and the inital input on tape 1
    def __init__(self, start, states, input):
        #Track the current state 
        self.current_state = start
        self.states = states
        self.accepting = None
        #Track the head positions on the tape 
        self.head1 = 2
        self.head2 = 2
        #Pad the tapes with 0s to act as blanks 
        self.tape1 = ['0', '0'] + list(input) + ['0', '0']
        #Using 0 as a blank 
        self.tape2 = ['0'] * (len(input)+4)
        self.path = []
    #Method that performs a transition 
    def transition(self):
        #For every state in the states list
        for st in self.states:
            #Look for the current state in the list
            if st.name == self.current_state:
                #Loop over every transitions that is valid for this state 
                for tr in st.trans:
                    #Get data from transition
                    read1, read2, next_state, write1, write2, mv1, mv2 = tr

                    #We need to dynamically expand the tapes as they grow 
                    #This avoids list indexing errors 
                    if self.head1 < 0:
                        self.tape1.insert(0, '0')
                        self.head1 = 0
                    elif self.head1 >= len(self.tape1):
                        self.tape1.append('0')

                    # Expand tape2 if needed
                    if self.head2 < 0:
                        self.tape2.insert(0, '0')
                        self.head2 = 0
                    elif self.head2 >= len(self.tape2):
                        self.tape2.append('0')
                    #Check if the current input on the tape matchs the transition 
                    if self.tape1[self.head1] == read1 and self.tape2[self.head2] == read2:
                        #If it does match, we can overwrite the data at this position on the tape
                        #with the new write values from the transition 
                        self.tape1[self.head1] = write1
                        self.tape2[self.head2] = write2
                        #Save the state we are exiting in a temp var
                        #This is so it can be used for the path 
                        old_state = self.current_state
                        #Update the current state 
                        self.current_state = next_state
                        
                        #Adjust the head positions depending on the transition
                        if mv1 == 'R': self.head1 += 1
                        elif mv1 == 'L': self.head1 -= 1
                        #Head 2 position 
                        if mv2 == 'R': self.head2 += 1
                        elif mv2 == 'L': self.head2 -= 1
                        #Add this new transition data to the path 
                        self.path.append((old_state, read1, write1, read2, write2, next_state))
                        #We return F to keep going 
                        return "F"
        #If there is no valid transition for the input 
        #We can halt the machine 
        return "HALT"
    #This method simulates the machine by repeatedly running the transition method
    #And checking for acceptance 
    def simulate(self):
        #Loop until the machine halts 
        while True:
            #If the machine hits an accepting state, we can terminate
            if self.current_state == self.accepting:
                return ("ACCEPT", self.tape2, self.path)
            #Check for transitions 
            result = self.transition()
            #If we run out of transitions to take, we can halt and reject input
            if result == "HALT":
                return ("REJECT", None)