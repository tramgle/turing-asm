# turing-asm
An assembly, parser and runtime for right infinite Turing machine.

```
input: abababab

# Entry point
.entry
a A R entry
b B R detach

.detach HALT
```

The `input` directive gives the starting tape for the machine

`.entry` defines a new program state called, and any transition instructions are added to the state

Transitions are defined as a 4 part instruction:
`{tape symbol} {write symbol} {move direction} {next state}`
