import os

class logger():
	def __init__(self, logfile=None, default_log_level='INFO'):
		self.DATA_DIR = os.path.join(os.path.expanduser("~"), '.nv')
		if logfile is None:
			self.LOG_FILE = os.path.join(self.DATA_DIR, 'nv.log')
		else:
			self.LOG_FILE = logfile
		self.LOG_LEVEL = default_log_level

	def log(self, data, printlogs=True):
		if printlogs is not None:
			self.PRINT_LOGS = printlogs
		f = open(self.LOG_FILE, 'a')
		f.write(f"\n{data}\n")
		f.close()
		if self.PRINT_LOGS:
			print(data)

	
		
