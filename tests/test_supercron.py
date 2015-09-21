#!/usr/bin/env python3

import sys
import os
import unittest


class RunTests(unittest.TestCase):
	"""class that tests supercron for behavior correctness"""

	def setUp(self):
		ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
		sys.path.append(ROOT_DIR)
		import supercron

	def test_midnight(self):
		SuperCron.add_job("ls", "ls", SuperCron.parse_repetition("midnight"))


if __name__ == "__main__":
	unittest.main()
