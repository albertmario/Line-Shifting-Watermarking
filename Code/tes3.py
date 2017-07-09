#!/usr/bin/python

class Error(Exception):
	pass
class ValueTooSmall(Error):
	def __init__(self):
		self.msg = 'kekecilan'