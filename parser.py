import sys
from machine import State, Transition, Program

keywords = {
	"L": "LEFT",
	"R": "RIGHT",
	"input": "INPUT",
	"HALT": "HALT"
}

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
		return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')

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
	for t in p.tokens:
		print(t.type, t.value)
