# instruction sets

LOADW = 0x01  # LOAD R ADDR -- Load the value in the address  to register
STORE = 0x02  # STORE R ADDR -- Store the value in the register to address
ADD = 0x03  # ADD R1 R2 -- R1 = R1 + R2
SUB = 0x04  # SUB R1 R2 -- R1 = R1 - R2
HALT = 0xff  # STOP


def cpu(program_in_memory):
    """
    Given a list representing a 20 "byte" array of memory, run the stored
    program to completion, mutating the list in place.

    The memory format is:

    00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 11 12 13
    __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __
    INSTRUCTIONS ---------------------------^ OUT-^ IN-1^ IN-2^

    R1 and R2 size is 2 bytes because the input allocation for each is 1 Bytes.
    PC size is 1 byte because "address location identifier" size  is 1 byte. 
    In this particular model the registers are being identified by their position in a list.
    """

    registers = [
        0x00,  # PC
        0x0000,  # R1
        0x0000,  # R2
    ]

    while True:
        pc_value = registers[0x00]  # address of the current instruction
        op_code = program_in_memory[pc_value]

        if op_code == HALT:
            return

        oparg_1, oparg_2 = program_in_memory[pc_value + 0x01], program_in_memory[pc_value + 0x02]

        if op_code == LOADW:
            R, ADDR = oparg_1, oparg_2

            # The first component is the first byte and the second component is the second byte (see little endian concept)
            registers[R] = program_in_memory[ADDR] + program_in_memory[ADDR + 0x01] * 256

        if op_code == STORE:
            R, ADDR = oparg_1, oparg_2

            # Deconstruct the value into 2 bytes (see little endian concept)
            program_in_memory[ADDR] = registers[R] % 256
            program_in_memory[ADDR + 0x01] = registers[R] // 256

        if op_code == ADD:
            R1, R2 = oparg_1, oparg_2
            registers[R1] = registers[R1] + registers[R2]

        if op_code == SUB:
            R1, R2 = oparg_1, oparg_2
            registers[R1] = registers[R1] - registers[R2]

        registers[0x00] += 0x03 # Point to the next instruction in this case 3 because an instruction takes 3 slots


if __name__ == '__main__':
    # Program: 10 + 12
    program_in_memory = [
        0x01, 0x01, 0x10,  # LOAD R1 0x10 -- Load the value in the input address 0x10 to R1
        0x01, 0x02, 0x12,  # LOAD R2 0x12 -- Load the value in the input address 0x12 to R2,
        0x03, 0x01, 0x02,  # ADD R1 R2
        0x02, 0x01, 0x0e,  # STORE R1 0x0e -- Store the result value in R1 to the memory address output 0x0e
        0xff,  # halt
        0x00,  # unused
        0x00, 0x00,  # initial output -- not yet mutated
        0x0a, 0x00,  # input 1 -- only first byte is used
        0x0c, 0x00
    ]

    cpu(program_in_memory)
    print("Testing 10 + 22")
    print(program_in_memory)
    assert program_in_memory[0x0e] == 22


    # Program: 500 + 200
    program_in_memory = [
        0x01, 0x01, 0x10,  # LOAD R1 0x10 -- Load the value in the input address 0x10 to R1
        0x01, 0x02, 0x12,  # LOAD R2 0x12 -- Load the value in the input address 0x12 to R2,
        0x03, 0x01, 0x02,  # ADD R1 R2
        0x02, 0x01, 0x0e,  # STORE R1 0x0e -- Store the result value in R1 to the memory address output 0x0e
        0xff,  # halt
        0x00,  # unused
        0x00, 0x00,  # initial output -- not yet mutated
        0xf4, 0x01,  # input 1 -- used little endian concept for encoding since we're using 2 bytes
        0xc8, 0x00,  # input 2 -- used little endian concept for encoding since we're using 2 bytes
    ]

    cpu(program_in_memory)
    print("testing 200 + 500")
    print(program_in_memory)
    assert program_in_memory[0x0e] == 188
    assert program_in_memory[0x0f] == 2


    # Program: 400 - 155
    program_in_memory = [
        0x01, 0x01, 0x10,  # LOAD R1 0x10 -- Load the value in the input address 0x10 to R1
        0x01, 0x02, 0x12,  # LOAD R2 0x12 -- Load the value in the input address 0x12 to R2,
        0x04, 0x01, 0x02,  # SUB R1 R2
        0x02, 0x01, 0x0e,  # STORE R1 0x0e -- Store the result value in R1 to the memory address output 0x0e
        0xff,  # halt
        0x00,  # unused
        0x00, 0x00,  # initial output -- not yet mutated
        0x90, 0x01,  # input 1 -- used little endian concept for encoding since we're using 2 bytes
        0x9B, 0x00,  # input 2 -- used little endian concept for encoding since we're using 2 bytes
    ]

    cpu(program_in_memory)
    print("testing 400 - 155")
    print(program_in_memory)
    assert program_in_memory[0x0e] == 245
