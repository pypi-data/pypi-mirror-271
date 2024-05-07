from serial import Serial as _Serial
from typing import List as _List


class GPP4323Exception(IOError):
	pass


class GPP4323(_Serial):
	"""
	为访问、控制固纬 GPP 系列多通道程控直流电源提供便利。
	"""
	def __init__(self, port: str, baudrate: int = 115200):
		_Serial.__init__(self, port=port, baudrate=baudrate, timeout=0.5)
		self.__last_sent = ''
		self.__last_recv = ''

	def write_command(self, command: str):
		cmd = command.encode('ascii')
		if not command.endswith('\n'):
			cmd = f'{cmd}\n'
		self.__last_sent = cmd
		self.write(cmd)

	def read_feedback(self) -> str:
		fb = self.read_until()
		try:
			feedback = fb.decode('ascii')
		except UnicodeDecodeError:
			feedback = fb.decode('latin')
			self.__last_recv = feedback
			raise IOError(f'GPP 仪器返回数据编码异常：[{feedback}]')
		self.__last_recv = feedback
		if not feedback.endswith('\n'):
			raise GPP4323Exception(f'GPP仪器数据接收超时')

		return feedback.strip()

	def query(self, command: str) -> str:
		self.write_command(command)
		return self.read_feedback()

	def set_voltage(self, channel: int, voltage: float):
		"""
		设置输出电压值，单位：伏特
		"""
		cmd = f':source{channel}:voltage {voltage}\n'
		self.write_command(cmd)

	def set_current(self, channel: int, current: float):
		"""
		设置输出电流限制值，单位：安培
		"""
		cmd = f':source{channel}:current {current}\n'
		self.write_command(cmd)

	def get_voltage(self, channel: int) -> float:
		"""
		获取当前的输出电压设定值，单位：伏特
		"""
		feedback = self.query(f':source{channel}:voltage?\n')
		voltage = float(feedback)
		return voltage

	def get_current(self, channel: int) -> float:
		"""
		获取当前的输出电流限值设定值，单位：安培
		"""
		feedback = self.query(f':source{channel}:current?\n')
		current = float(feedback)
		return current

	def turn_off(self, channel: int):
		cmd = f':output{channel}:off\n'
		self.write_command(cmd)

	def turn_on(self, channel: int):
		cmd = f':output{channel}:on\n'
		self.write_command(cmd)

	def turn_off_all(self):
		cmd = ':alloutoff\n'
		self.write_command(cmd)

	def turn_on_all(self):
		self.write_command(':allouton\n')

	def measure_current(self, channel: int) -> float:
		"""
		测量指定通道的输出电流实际值，单位：安培
		"""
		feedback = self.query(f':measure{channel}:current?\n')
		current = float(feedback)
		return current

	def measure_voltage(self, channel: int) -> float:
		"""
		测量指定通道的输出电压实际值，单位：伏特
		"""
		feedback = self.query(f':measure{channel}:voltage?\n')
		voltage = float(feedback)
		return voltage

	def measure_power(self, channel: int) -> float:
		"""
		测量指定通道的输出功率实际值，单位：瓦特
		"""
		feedback = self.query(f':measure{channel}:power?\n')
		power = float(feedback)
		return power

	def measure_all_currents(self) -> _List[float]:
		"""
		测量所有通道的输出电流实际值，单位：安培
		"""
		feedback = self.query(f':measure:current:all?\n')
		tokens = feedback.split(',')
		currents = [float(token) for token in tokens]
		return currents
