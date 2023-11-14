class FiniteAutomata:
    def __init__(self, in_file):
        self.in_file = in_file
        self.states = []
        self.initial_state = ''
        self.out_states = []
        self.alphabet = []
        self.transitions = []
        self.read_data()

    def read_data(self):
        with open(self.in_file, 'r') as f:
            data = f.read()

        states_data = data[data.find('states={') + len('states={'):data.find('}')]
        self.states = states_data.split(', ')

        self.initial_state = data[data.find('initial_state=') + len('initial_state='):data.find('\n', data.find(
            'initial_state='))].strip()

        out_states_data = data[
                          data.find('out_states={') + len('out_states={'):data.find('}', data.find('out_states={'))]
        self.out_states = out_states_data.split(', ')

        alphabet_data = data[data.find('alphabet={') + len('alphabet={'):data.find('}', data.find('alphabet={'))]
        self.alphabet = alphabet_data.split(', ')

        transitions_data = data[
                           data.find('transitions={') + len('transitions={'):data.find('}', data.find('transitions={'))]
        transitions = transitions_data.split('; ')
        for transition in transitions:
            transition = transition.strip()[1:-1].split(', ')
            self.transitions.append(tuple(transition))

    def __check_string(self, string, state):
        if not string:
            if state in self.out_states:
                return True
            else:
                return False
        for character in string:
            if character not in self.alphabet:
                return
            valid_transitions = [transition for transition in self.transitions if
                                 transition[0] == state and transition[2] == character]
            if not valid_transitions:
                return False
            for transition in valid_transitions:
                if self.__check_string(string[string.find(character) + 1:], transition[1]):
                    return True
            return False

    def is_dfa(self):
        for state in self.states:
            for symbol in self.alphabet:
                transitions = [t for t in self.transitions if t[1] == state and t[2] == symbol]
                if len(transitions) > 1:
                    return False
        return True

    def is_match(self, sequence):
        return self.__check_string(sequence, self.initial_state)

    def menu(self):
        while True:
            print("1. Print states")
            print("2. Print initial state")
            print("3. Print out states")
            print("4. Print alphabet")
            print("5. Print transitions")
            print("6. Quit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.print_states()
            elif choice == '2':
                self.print_initial_state()
            elif choice == '3':
                self.print_out_states()
            elif choice == '4':
                self.print_alphabet()
            elif choice == '5':
                self.print_transitions()
            elif choice == '6':
                print("Exiting menu.")
            elif choice == '7':
                print(self.is_match(input()))
            elif choice == '8':
                print(self.is_dfa())
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def print_states(self):
        print("States:", self.states)

    def print_initial_state(self):
        print("Initial State:", self.initial_state)

    def print_out_states(self):
        print("Out States:", self.out_states)

    def print_alphabet(self):
        print("Alphabet:", self.alphabet)

    def print_transitions(self):
        print("Transitions:", self.transitions)


fa = FiniteAutomata("id.in")

