import mmap
import sys

from collections import defaultdict

# The data array that will represent the
data_array = defaultdict(int)
instruction_pointer = 0
data_pointer = 0


class NoMoreInstructionsException(Exception):
    pass


def read_instruction(instructions):
    if instruction_pointer >= instructions.size():
        raise NoMoreInstructionsException()
    return chr(instructions[instruction_pointer])


def start_interpreting(instructions):
    global data_array
    global instruction_pointer
    global data_pointer

    # Program ends when instruction pointer falls off program
    while not (instruction_pointer >= instructions.size()):

        # Read instruction and execute it
        instruction = chr(instructions[instruction_pointer])
        if instruction == ">":
            data_pointer += 1
        elif instruction == "<":
            data_pointer -= 1
        elif instruction == "+":
            data_array[data_pointer] += 1
        elif instruction == '-':
            data_array[data_pointer] -= 1
        elif instruction == ',':
            #TODO: figure out better way to read bytes from either pipe or user input (issues with sys.stdin.read and \n)
            user_input = input()
            data_array[data_pointer] = int(user_input)
        elif instruction == '.':
            print(chr(data_array[data_pointer]), end='')

        elif instruction == '[':
            # if the byte at the data pointer is zero, then jump forward to the command after the matching ]
            if data_array[data_pointer] == 0:
                # TODO: support nested loops
                while read_instruction(instructions) != ']':
                    instruction_pointer += 1
        elif instruction == ']':
            # TODO: support nested loops
            # if the byte at the data pointer is nonzero, then jump back to the command after the matching [
            if data_array[data_pointer] != 0:
                while read_instruction(instructions) != '[':
                    instruction_pointer -= 1
        else:
            # Ignore anything that is not an instruction
            pass
        # print("%s ==> (%s) %s" % (instruction, data_pointer, dict(data_array)))
        instruction_pointer += 1


def main():
    input_path = sys.argv[1]
    with open(input_path, 'r') as input_file:
        memfile = mmap.mmap(input_file.fileno(), length=0, access=mmap.ACCESS_READ)
        start_interpreting(memfile)


if __name__ == '__main__':
    main()
