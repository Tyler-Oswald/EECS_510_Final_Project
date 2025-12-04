class state:
    def __init__(self,name, transitions):
        self.name = name
        self.trans = transitions
    
class Turing:
    def __init__(self, start, states, input):
        self.current_state = start
        self.states = states
        self.accepting = None
        self.head1 = 2
        self.head2 = 2
        self.tape1 = ['0', '0'] + list(input) + ['0', '0']
        #Using 0 as a blank 
        self.tape2 = ['0'] * (len(input)+4)
        self.path = []
    
    def transition(self):
        for st in self.states:
            if st.name == self.current_state:
                for tr in st.trans:
                    read1, read2, next_state, write1, write2, mv1, mv2 = tr

                    # Expand tape1 if needed
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

                    if self.tape1[self.head1] == read1 and self.tape2[self.head2] == read2:

                        self.tape1[self.head1] = write1
                        self.tape2[self.head2] = write2
                        
                        old_state = self.current_state
                        self.current_state = next_state

                        if mv1 == 'R': self.head1 += 1
                        elif mv1 == 'L': self.head1 -= 1

                        if mv2 == 'R': self.head2 += 1
                        elif mv2 == 'L': self.head2 -= 1

                        self.path.append((old_state, read1, write1, read2, write2, next_state))
                        return "F"
        return "HALT"

    def simulate(self):
        while True:
            if self.current_state == self.accepting:
                return ("ACCEPT", self.tape2, self.path)

            result = self.transition()
            if result == "HALT":
                return ("REJECT", None)