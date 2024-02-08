import sys

debug = False

class Machine:
	def __init__(self, program, tape=" "*600):
		self.program = program
		self.tape = [char for char in (tape+"$")]
		self.head = 0
		self.crash = False
		self.halt = False
	def run(self):
		global debug
		while not self.crash and not self.halt:
			self.program.advance(self, self.tape[self.head])
			if debug:
				print(self.tape, self.head)
		print(self.tape)
		if self.crash:
			print("CRASHED")
		else:
			print("HALTED")
	def write(self, cell):
		self.tape[self.head] = cell
	def move(self, amt):
		self.head += amt

class Transition:
	def __init__(self, key, write, action, nextState):
		self.key = key
		self.write = write
		self.action = action
		self.nextState = nextState

class State:
	def __init__(self, halt=False):
		self.HALT = halt
		self.transitions = {}
	def addTransition(self, t):
		self.transitions[t.key] = t

class Program:
	def __init__(self, states=None):
		self.state = 0
		self.states = states or []
	def advance(self, machine, cell):
		if cell not in self.states[self.state].transitions:
			machine.crash = True
			return
		t = self.states[self.state].transitions[cell]
		print(self.state, t.nextState, cell)
		machine.write(t.write)
		machine.move(t.action)
		self.state = t.nextState
		if self.states[self.state].HALT:
			machine.halt = True

if __name__ == "__main__":
	state1 = State()
	state1.addTransition(Transition('a', 'A', 1, 1))
	state1.addTransition(Transition('$', '$', 1, 5))
	state2 = State()
	state2.addTransition(Transition('a', 'a', 1, 1))
	state2.addTransition(Transition('B', 'B', 1, 1))
	state2.addTransition(Transition('b', 'B', -1, 2))
	state3 = State()
	state3.addTransition(Transition('B', 'B', -1, 2))
	state3.addTransition(Transition('a', 'a', -1, 3))
	state3.addTransition(Transition('A', 'A', 1, 4))
	state4 = State()
	state4.addTransition(Transition('a', 'a', -1, 3))
	state4.addTransition(Transition('A', 'A', 1, 0))
	state5 = State()
	state5.addTransition(Transition('B', 'B', 1, 4))
	state5.addTransition(Transition('$', '$', 1, 5))
	state6 = State(halt=True)
	
	tape = ""
	if len(sys.argv) > 1:
		tape = sys.argv[1]
	if len(sys.argv) > 2 and sys.argv[2] == '-d':
		debug = True
	x = Program([state1, state2, state3, state4, state5, state6])
	tm = Machine(x, tape)
	tm.run()
