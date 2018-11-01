from pymouse import PyMouseEvent

class Clickonacci(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):
        '''Print Fibonacci numbers when the left click is pressed.'''
        if button == 1:
		if press:
			print('Clicked!')
	else:
		self.stop

C = Clickonacci()
C.run()
