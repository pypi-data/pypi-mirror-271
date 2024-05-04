import sys


def output_stdout(outputValue):
    r"""Outputs to stdout

    Outputs the given outputValue to stdout and flushes the stream after

    Parameters
    ----------
    outputValue: Any
        The value that's written to stdout
    """

    sys.stdout.write(str(outputValue) + "\n")
    sys.stdout.flush()