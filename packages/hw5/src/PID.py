class PID:
    def __init__ (self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.c = 0
        self.i_error = 0
        self.error = 0
        self.I = 0
    def update_error(self, error):
        self.error = error.data
    def controller(self, dt):
        P = self.kp * self.error
        self.I = self.I + (self.ki * self.error*dt)
        D = self.kd * ((self.error - self.i_error)/dt)
        self.c = P + self.I + D
        self.i_error = self.error
        return self.c
