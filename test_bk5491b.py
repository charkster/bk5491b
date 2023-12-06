import pyvisa
from bk5491b import bk5491b
import time

rm = pyvisa.ResourceManager('@py')

dmm1 = bk5491b(pyvisa_instr=rm.open_resource('ASRL/dev/ttyUSB0::INSTR'),baud_rate=19200)
dmm1.reset()
print(dmm1.meas_i(nplc=10,rng=20,samples=4))
print(dmm1.meas_v(nplc=0.1,samples=5))
print(dmm1.meas_i(rng=0.005,samples=3))
print(dmm1.meas_v())
print(dmm1.meas_r(rng='AUTO',samples=5,nplc=10))
print(dmm1.meas_freq())
print(dmm1.meas_period())
