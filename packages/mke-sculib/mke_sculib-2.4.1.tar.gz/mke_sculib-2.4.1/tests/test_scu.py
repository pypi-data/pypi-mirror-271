import unittest
import astropy.units as u
from astropy.time import Time
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


import os, inspect, sys
# path was needed for local testing
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
print(parent_dir)
sys.path.insert(0, parent_dir + '/src')
print(sys.path)



from mke_sculib.scu import scu


class TestScu(unittest.TestCase):
    def test_construct(self):


        mpi = scu('10.98.76.45', '8997')
        self.assertEqual(mpi.ip, '10.98.76.45')
        self.assertEqual(mpi.port, '8997')

        mpi = scu('10.98.76.45', 8997)
        self.assertEqual(mpi.ip, '10.98.76.45')
        self.assertEqual(mpi.port, '8997')

        mpi = scu('10.98.76.45', port='8997')
        self.assertEqual(mpi.ip, '10.98.76.45')
        self.assertEqual(mpi.port, '8997')

        mpi = scu('10.98.76.45')
        self.assertEqual(mpi.ip, '10.98.76.45')
        self.assertEqual(mpi.port, '8080')

        mpi = scu(ip='10.98.76.45:8081')
        self.assertEqual(mpi.ip, '10.98.76.45')
        self.assertEqual(mpi.port, '8081')

        mpi = scu('http://134.104.22.44:8080/')
        self.assertEqual(mpi.ip, '134.104.22.44')
        self.assertEqual(mpi.port, '8080')
        
        mpi = scu('http://134.104.22.44:1234/')
        self.assertEqual(mpi.ip, '134.104.22.44')
        self.assertEqual(mpi.port, '1234')

        mpi = scu('http://134.104.22.44/')
        self.assertEqual(mpi.ip, '134.104.22.44')
        self.assertEqual(mpi.port, '8080')

        mpi = scu('http://localhost:1234')
        self.assertEqual(mpi.ip, 'localhost')
        self.assertEqual(mpi.port, '1234')

        mpi = scu('http://localhost/')
        self.assertEqual(mpi.ip, 'localhost')
        self.assertEqual(mpi.port, '8080')

    def test_export_session(self):
        api = scu('http://10.98.76.45:8997/')
        api.export_session()
    
    # def test_get_session_as_df():
    #     api = scu('http://10.98.76.45:8997/')
    #     api.get_session_as_df()

if __name__ == "__main__":
    # sim = TestAcuSim()
    # sim.test_unstow()

    unittest.main()
