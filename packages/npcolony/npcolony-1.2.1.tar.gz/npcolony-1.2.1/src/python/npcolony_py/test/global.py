#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

import npcolony

class GlobalTest(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(type(npcolony.VERSION), str)
        self.assertEqual(npcolony.VERSION, "1.2.1")

        self.assertEqual(type(npcolony.get_devices()), list)
