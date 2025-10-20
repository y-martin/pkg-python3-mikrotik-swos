#!/usr/bin/env python3

from mikrotik_swos.mikrotik_system import Mikrotik_System
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


sys = Mikrotik_System("http://switch", "login", "password")
sys.show()
sys.set(identity="switch")