import mmap
import sys

from collections import defaultdict
from io import StringIO

# The data array that will represent the
data_array = defaultdict(int)
instruction_pointer = 0
data_pointer = 0
instructions = None


class NoMoreInstructionsException(Exception): pass


def current_instruction():
    if instruction_pointer >= instructions.size():
        raise NoMoreInstructionsException()
    return chr(instructions[instruction_pointer])


def forward_to_loop_end():
    global instruction_pointer

    while current_instruction() != ']':
        instruction_pointer += 1
        # Oh noes, a new loop has started, let's continue from the end of this one
        if current_instruction() == '[':
            instruction_pointer += 1
            forward_to_loop_end()
            instruction_pointer += 1


def rewind_to_loop_start():
    global instruction_pointer

    while current_instruction() != '[':
        instruction_pointer -= 1
        # Oh noes, another loop has ended, let's continue from the start of this one
        if current_instruction() == ']':
            instruction_pointer -= 1
            rewind_to_loop_start()
            instruction_pointer -= 1


def start_interpreting():
    global data_array
    global instruction_pointer
    global data_pointer

    output = StringIO()

    # Program ends when instruction pointer falls off program
    while not (instruction_pointer >= instructions.size()):

        # Read instruction and execute it
        instruction = current_instruction()
        if instruction == ">":
            data_pointer += 1
        elif instruction == "<":
            data_pointer -= 1
        elif instruction == "+":
            data_array[data_pointer] += 1
        elif instruction == '-':
            data_array[data_pointer] -= 1
        elif instruction == ',':
            user_input = input()
            data_array[data_pointer] = int(user_input)
        elif instruction == '.':
            print(chr(data_array[data_pointer]), end='')

        elif instruction == '[':
            # if the byte at the data pointer is zero, then jump forward to the command after the matching ]
            if data_array[data_pointer] == 0:
                forward_to_loop_end()
        elif instruction == ']':
            # if the byte at the data pointer is nonzero, then jump back to the command after the matching [
            if data_array[data_pointer] != 0:
                rewind_to_loop_start()
        else:
            # Ignore anything that is not an instruction
            pass
        print("%s ==> (%s) %s" % (instruction, data_pointer, dict(data_array)))
        instruction_pointer += 1

    print(output.getvalue())


def main():
    global instructions
    input_path = sys.argv[1]
    with open(input_path, 'r') as input_file:
        instructions = mmap.mmap(input_file.fileno(), length=0, access=mmap.ACCESS_READ)
        start_interpreting()

if __name__ == '__main__':
    main()
