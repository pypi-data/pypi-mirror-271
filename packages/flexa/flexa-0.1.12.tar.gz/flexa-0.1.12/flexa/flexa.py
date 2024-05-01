from typing import TypeVar, Generic
from dataclasses import dataclass


Output = TypeVar("Output")
Input = TypeVar("Input")


@dataclass
class Pair(Generic[Output, Input]):
    output: Output
    input: Input

class Flexa(Generic[Output, Input]):
    def __init__(self):
        self.pairs: list[Pair[Output, Input]] = []

    def contains_input(self, input: Input) -> bool:
        return input in [pair.input for pair in self.pairs]

    def set(self, output: Output, input: Input):
        if self.contains_input(input):
            raise ValueError("Invalid input value, input already exists")
        self.pairs.append(Pair(output, input))

    def result(self, input: Input) -> Output:
        for pair in self.pairs:
            if pair.input == input:
                return pair.output
        raise ValueError("Invalid input value, no match found")
