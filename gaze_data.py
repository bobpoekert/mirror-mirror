import ctypes

dll = ctypes.CDLL('MinimalGazeDataStream.dll')

new_context = dll.GazeTrack
free_context = dll.FreeGazeTrackContext

callback_type = ctypes.CFUNCTYPE(None, ctypes.c_double, ctypes.c_double)


class DataStream(object):

	def __init__(self, on_point=None):
		self.on_point = on_point
		self.callback = callback_type(self._on_point)
		self.native_context = new_context(self.callback)
		print 'loaded context', self.native_context
		if self.native_context == 0:
			raise WindowsError('Failed to initialize native context')
		
	def _on_point(self, x, y):
		if self.on_point:
			self.on_point(x, y)
			
	def __del__(self):
		print 'unloading'
		if self.native_context != 0:
			free_context(self.native_context)