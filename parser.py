import sys
from machine import Machine, State, Transition, Program

keywords = {
	"L": "LEFT",
	"R": "RIGHT",
	"input": "INPUT",
	"HALT": "HALT"
}

debug = False

class Token:
	def __init__(self, t_type, t_value=None):
		self.type = t_type
		self.value = t_value

class Parser:
	def __init__(self, source):
		self.tokens = []
		self.source = source or ""
		self.start = 0
		self.current = 0
		self.line = 1
		self.cT = 0
		self.states = []
		self.lookup = {}
		self.transitions = []
		self.tape = ""

	def is_at_end(self):
		return self.current >= len(self.source)
	
	def advance(self):
		self.current += 1
		return self.source[self.current-1]
	
	def add_token(self, t_type):
		text = self.source[self.start: self.current]
		self.tokens.append(Token(t_type, text))

	def scan_tokens(self):
		while not self.is_at_end():
			self.start = self.current
			self.scan_token()
		self.tokens.append(Token("EOF"))

	def peek(self):
		if self.is_at_end():
			return False
		return self.source[self.current]

	def is_alpha(self, c):
		return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '$' or (c >= '0' and c <= '9')

	def idendifier(self):
		global keywords
		while self.is_alpha(self.peek()):
			self.advance();
		text = self.source[self.start:self.current]
		if text not in keywords:
			self.add_token("IDENT")
			return
		self.add_token(keywords[text])

	def scan_token(self):
		c = self.advance()
		match c:
			case ':':
				self.tokens.append(Token(":"))
			case '.':
				self.tokens.append(Token("."))
			case '#':
				while self.peek() != '\n' and not self.is_at_end():
					self.advance()
			case '\n':
				self.tokens.append(Token("NEWLINE"))
			case ' ':
				pass
			case _:
				if self.is_alpha(c):
					self.idendifier()
				else:
					raise BaseException("Weird tokens man")

	def match_ahead(self, t_type, n):
		if self.cT + n > len(self.tokens):
			return False
		return self.tokens[self.cT+n].type == t_type
	
	def token_to_action(self, value):
		if value == "RIGHT":
			return 1
		if value == "LEFT":
			return -1

	def parse(self):
		self.cT = 0
		state_index = 0
		if len(self.tokens) == 0:
			print("No Tokens Found")
			return
		while self.cT < len(self.tokens) and self.tokens[self.cT].type != "EOF":
			#print(self.tokens[self.cT].type)
			match self.tokens[self.cT].type:
				case "EOF":
					return
				case "INPUT":
					if self.match_ahead(":", 1) and self.match_ahead("IDENT", 2):
						self.tape = self.tokens[self.cT+2].value
						self.cT += 3
					else:
						raise BaseException("Expected Well Formed Input Define")
				case ".":
					if self.match_ahead("IDENT", 1):
						name = self.tokens[self.cT+1].value
						halts = False
						self.cT += 1
						if self.match_ahead("HALT", 1):
							halts = True
							self.cT += 2
						self.states.append(State(halt=halts, name=name))
						self.lookup[name] = state_index
						state_index += 1
				case "IDENT":
					if self.match_ahead("IDENT", 1) and (self.match_ahead("LEFT",2) or self.match_ahead("RIGHT",2)) and self.match_ahead("IDENT",3):
						if len(self.states) == 0:
							raise BaseException("Transition declared before state")
						transition = (state_index-1, self.tokens[self.cT].value, self.tokens[self.cT+1].value, self.token_to_action(self.tokens[self.cT+2].type), self.tokens[self.cT+3].value)
						self.transitions.append(transition)
						self.cT += 4
					else:
						raise BaseException("Malformed Transition")
			self.cT += 1
		for t in self.transitions:
			if t[0] == -1:
				raise BaseException("Transition declared before state")
			self.states[t[0]].addTransition(Transition(t[1],t[2],t[3],self.lookup[t[4]]))
		if debug:
			for s in self.states:
				print(s.name, s.HALT)
				for ti in s.transitions:
					t = s.transitions[ti]
					print("\t", t.key, t.write, t.action, t.nextState)
	def run(self):
		prog = Program(self.states)
		machine = Machine(prog, self.tape)
		machine.run()

if __name__ == "__main__":
	filename = ""
	if len(sys.argv) == 1:
		print(f"Usage: {sys.argv[0]} program.tasm")
		sys.exit(1)
	filename = sys.argv[1]
	file = open(filename)
	
	body = file.read()
	
	
	p = Parser(body)
	p.scan_tokens()
	p.parse()
	p.run()
