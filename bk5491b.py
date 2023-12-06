import pyvisa
import time

class bk5491b():

	def __init__(self, pyvisa_instr, baud_rate=9600):
		self.instr = pyvisa_instr # this is the pyvisa instrument, rm.open_resource('ASRL/dev/ttyUSB0::INSTR')
		self.instr.baud_rate  = baud_rate # the default BK5491b baud rate is 9600, but can be manually changed to 38400, or 19200
		self.function_list    = ['VOLTage:AC', 'VOLTage:DC', 'CURRent:AC', 'CURRent:DC', 'RESistance', 'FREQuency', 'PERiod','DIODe', 'CONTinuity']
		self.nplc_list        = [0.1, 1, 10] # 1 PCL = 16.7ms
		self.volt_rng_list    = [0.5,   5,    50,  500, 1000, 'AUTO'] # V
		self.ac_volt_rng_list = [0.5,   5,    50,  500, 750,  'AUTO'] # V
		self.curr_rng_list    = [0.005, 0.05, 0.5, 5,   20,   'AUTO'] # A
		self.res_rng_list     = [500, 5000, 50000, 500000, 5000000, 'AUTO'] # Ohm
		
			
	def reset(self):
		self.instr.write('*RST')
		time.sleep(3)
	
	def measure(self, function='', rng_list = [], nplc=1, rng='AUTO', samples=1):
		if (function not in self.function_list):
			print("Please select one of the following nplc values")
			print(self.function_list)
			return 'ERROR'
		if (nplc not in self.nplc_list):
			print("Please select one of the following nplc values")
			print(self.nplc_list)
			return 'ERROR'
		else:
			self.instr.write('function ' + function)
			time.sleep(0.3)
			if (function not in ['FREQuency', 'PERiod']):
				self.instr.write(function + ':NPLCycles ' + str(nplc))
				time.sleep(0.5)
			else:
				self.instr.write('VOLTage:AC:NPLCycles 1')
				time.sleep(0.5)
		if (rng not in rng_list):
			print("Please select one of the following rng values")
			print(rng_list)
			return 'ERROR'
		elif (rng == 'AUTO' and function in ['FREQuency', 'PERiod']):
			self.instr.write('VOLTage:AC:RANGe:AUTO 1')
		elif (rng == 'AUTO'):
			self.instr.write(function + ':RANGe:AUTO 1')
		elif (function in ['FREQuency', 'PERiod']):
			self.instr.write('VOLTage:AC:RANGe ' + str(rng))
		else:
			self.instr.write(function + ':RANGe ' + str(rng))
		time.sleep(1)
		value = 0.0
		self.instr.query('FETCH?') # this fetch removes the previous write echo
		for i in range(0,samples):
			value_str = self.instr.query('FETCH?')
			if (nplc == 10):
				time.sleep(0.25) # 1 PCL = 16.7ms, 10 PCL = 0.167s
			value = value + float(value_str[7:-1]) # the first 7 characters are the fetch command, last character is line feed
		return value/samples

	def meas_v(self, nplc=1, rng='AUTO', samples=1):
		return self.measure(function='VOLTage:DC', rng_list = self.volt_rng_list, nplc=nplc, rng=rng, samples=samples) 

	
	def meas_i(self, nplc=1, rng='AUTO', samples=1):
		return self.measure(function='CURRent:DC', rng_list = self.curr_rng_list, nplc=nplc, rng=rng, samples=samples) 
	

	def meas_r(self, nplc=1, rng='AUTO', samples=1):
		return self.measure(function='RESistance', rng_list = self.res_rng_list, nplc=nplc, rng=rng, samples=samples) 

	
	def meas_acv(self, nplc=1, rng='AUTO', samples=1):
		return self.measure(function='VOLTage:AC', rng_list = self.ac_volt_rng_list, nplc=nplc, rng=rng, samples=samples)

	def meas_aci(self, nplc=1, rng='AUTO', samples=1):
		return self.measure(function='CURRent:AC', rng_list = self.curr_rng_list, nplc=nplc, rng=rng, samples=samples)

	def meas_freq(self, nplc=1, rng='AUTO', samples=1):
		return self.measure(function='FREQuency', rng_list = self.ac_volt_rng_list, nplc=nplc, rng=rng, samples=samples)

	def meas_period(self, nplc=1, rng='AUTO', samples=1):
		return self.measure(function='PERiod', rng_list = self.ac_volt_rng_list, nplc=nplc, rng=rng, samples=samples)
