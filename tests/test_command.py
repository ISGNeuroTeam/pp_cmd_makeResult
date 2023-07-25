"""Module for testing makeresults command"""
import subprocess
import time
from unittest import TestCase

SAMPLE_HEAD = [["_time", "_raw", "host", "source", "sourcetype"]]
SAMPLE = [[1000000000, None, None, None, None]]


def capture(s):
    """Captures the output of postprocessing
     command s and turns it into a list"""
    x = subprocess.run(["pp", s],
                       check=False,
                       capture_output=True).stdout.decode()
    x = [n.split() for n in x[:-1].split("\n")]
    x = [x[0]] + [lst[1:] for lst in x[1:]]
    return x


class TestCommand(TestCase):
    """Class for testing makeresults command"""

    def test_n(self):
        for i in range(1, 10):
            for j in [True]:
                test_string = f"makeresults count={i}, annotate={j}"
                sample = [[int(time.time()), None, None, None, None]]
                sample = SAMPLE_HEAD + sample * i
                result = capture(test_string)
                # Checking if length of resulting dataframe is correct
                self.assertEqual(len(sample), len(result))

                for k in range(1, i):
                    if j:
                        for m in range(1, 4):
                            # Checking if non _time fields are None
                            self.assertEqual('None', result[k][m])

                    # Checking if _time is somewhere near actual value
                    self.assertTrue(sample[k][0] <= int(result[k][0]) <= sample[k][0]+100)

                    if k > 1:
                        # Checking if _time is the same throughout the whole dataframe
                        self.assertEqual(result[k][0], result[k-1][0])

