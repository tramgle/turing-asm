# turing-asm
An assembly, parser and runtime for right infinite Turing machine.

Example Program
```
input: abababab

# Entry point
.entry
a A R entry
b B R detach

.detach HALT
```

The `input` directive gives the starting tape for the machine

`.entry` defines a new program state called, and any transition instructions are added to the state. The first state defined in the program will be used as the entry point

Transitions are defined as a 4 part instruction:
`{tape symbol} {write symbol} {move direction} {next state}`

A state can be defined as a halting state by adding the `HALT` keyword at the end of a state declaration: `.detach HALT`

## Another Example
```
input: aabb
.state1
a A R state2
$ $ R state6

.state2
a a R state2
B B R state2
b B L state3

.state3
B B L state3
a a L state4
A A R state5

.state4
a a L state4
A A R state1

.state5
B B R state5
$ $ R state6

.state6 HALT
```

# Usage
`python parser.py palindrome.tasm`
