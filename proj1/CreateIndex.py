
# Authors: Filipe Pires [85122] & João Alegria [85048]

import sys

import FileParser
import Tokenizer
import PersistIndex
import Indexer

# Main class for Project 1


def main(args):

    HELP = """USAGE:\n
           python3 Indexer.py [-h] [-o outputFile] [-l limit] [-t tokenizer] inputFile1 [inputFile2]+ \n
        OPTIONS:\n
           h - shows this help\n
           o - define output file's name\n
           l - define limit for the number of lines to be processed in each input file\n
           t - define the tokenizer used for the program\n
        ARGUMENTS:\n
           outputFile - actual name for the output file\n
           limit - value for the number of lines limit\n
           tokenizer - must be simple(for the simple 2.1 tokenizer) or complex(for the more advanced 2.2 tokenizer)\n
           inputFile - names of the input files to be processed\n"""

    ERROR = "Please execute this command with the correct argument(s) or add the option '-h' to learn about its usage.\n"

    if len(args) < 1:
        print(HELP)
        return 1

    for i in range(0, len(args)-1):
        if args[i] == "-h" or args[i] == "-help" or args[i] == "--help":
            print(HELP)
            return 2

    inputFiles = args.copy()
    outputFile = "out.txt"
    limit = None
    tokenizer = "simple"

    for i in range(0, len(args)-1):
        if args[i] == "-o":
            assert not args[i +
                            1].startswith("-"), "This option must have the value indicated."
            outputFile = args[i+1]
            inputFiles.remove(args[i])
            inputFiles.remove(args[i+1])
        if args[i] == "-l":
            assert not args[i +
                            1].startswith("-"), "This option must have the value indicated."
            limit = int(args[i+1])
            inputFiles.remove(args[i])
            inputFiles.remove(args[i+1])
        if args[i] == "-t":
            assert not args[i +
                            1].startswith("-"), "This option must have the value indicated."
            assert args[i+1] == "simple" or args[i +
                                                 1] == "complex", "Tokenizer option must be either \"simple\" or \"complex\""
            tokenizer = args[i+1]
            inputFiles.remove(args[i])
            inputFiles.remove(args[i+1])

    if tokenizer == "simple":
        PersistIndex.PersistCSV(
            outputFile,
            indexer=Indexer.FileIndexer(
                FileParser.GZipFileParser(inputFiles, limit),
                Tokenizer.SimpleTokenizer()
            )
        ).persist()
    else:
        PersistIndex.PersistCSV(
            outputFile,
            indexer=Indexer.FileIndexer(
                FileParser.GZipFileParser(inputFiles, limit),
                Tokenizer.ComplexTokenizer()
            )
        ).persist()

    return 0


main(sys.argv[1:])
