
#
# Decompression application using adaptive arithmetic coding
#
# Usage: python adaptive-arithmetic-decompress.py InputFile OutputFile
# This decompresses files generated by the adaptive-arithmetic-compress.py application.
#
# Copyright (c) Project Nayuki
#
# https://www.nayuki.io/page/reference-arithmetic-coding
# https://github.com/nayuki/Reference-arithmetic-coding
#

import sys
import arithmetic_coding


# Command line main application function.
def main(args):
    # Handle command line arguments
    if len(args) != 2:
        sys.exit("Usage: python adaptive-arithmetic-decompress.py InputFile OutputFile")
    inputfile, outputfile = args

    # Perform file decompression
    with open(inputfile, "rb") as inp, open(outputfile, "wb") as out:
        bitin = arithmetic_coding.BitInputStream(inp)
        decompress(bitin, out)


def decompress(bitin, out):
    initfreqs = arithmetic_coding.FlatFrequencyTable(257)
    freqs = arithmetic_coding.SimpleFrequencyTable(initfreqs)
    dec = arithmetic_coding.ArithmeticDecoder(32, bitin)
    while True:
        # Decode and write one byte
        symbol = dec.read(freqs)
        if symbol == 256:  # EOF symbol
            break
        out.write(bytes((symbol,)))
        freqs.increment(symbol)


# Main launcher
if __name__ == "__main__":
    main(sys.argv[1:])
