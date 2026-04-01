class PID:
	def __init__(self,KP,KI,KD, target, time_step):
		self.kp = KP
		self.ki = KI
		self.kd = KD 
		self.target = target
		self.time_step = time_step
		self.setpoint = target
		self.error = 0
		self.integral_error = 0
		self.error_last = 0
		self.derivative_error = 0
		self.output = 0
		
	def compute(self, pos):
		self.error = self.setpoint - pos
		self.integral_error += self.error * self.time_step
		self.derivative_error = self.error - self.error_last
		self.error_last = self.error
		self.output = -(self.kp*self.error + self.ki*self.integral_error + self.kd*self.derivative_error)
		print("PID: ", self.output, ", kp: ", self.kp*self.error, ", ki: ", self.ki*self.integral_error, ", kd: ", self.kd*self.derivative_error)
		return self.output 