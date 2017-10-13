'''
	title	: PDF Text Watermarking Using Line Shifting 
	author	: Albert Mario G64130101
	desc 	: main file
'''

#!/usr/bin/env python
#-*- coding:utf-8 -*-

from core import *
from util import *
import optparse
import sys

def start():
	desc = '''
	PDF Text Watermarkng Using Line Shifting
	'''
	parser = optparse.OptionParser(description=desc, version='%prog version 1.0')
	parser.add_option('-s', '--shift', help='Shifting line with key and pin', action='store', dest='shi', nargs=3, metavar='[path/to/file] [key] [pin]')
	parser.add_option('-d', '--detect', help='Detecting watermark', action='store', dest='det', nargs=3, metavar='[/path/to/file] [pin] [/path/to/info_file]')
	parser.add_option('-p', '--psnr', help='count Peak Signal to Noise Ratio', action='store', dest='ps', nargs=2, metavar='[/path/to/original/file] [/path/to/watermarked/file]')
	(opts, args) = parser.parse_args()

	if opts.shi:
		if checkFile(opts.shi[0]) == False:
			sys.exit()
		elif checkSeedBody(opts.shi[2]) == False:
			sys.exit()
		elif checkLine(opts.shi[0], opts.shi[1]) == False:
			sys.exit()
		else:
			fileNameInput = opts.shi[0]
			key = opts.shi[1]
			seed = opts.shi[2]
			keyBiner = ''.join('{0:08b}'.format(ord(x), 'b') for x in key)
			seedBiner = ''.join('{0:08b}'.format(ord(x), 'b') for x in seed)
			pin = generatePin(seedBiner, len(keyBiner))
			spreadSpectrum = generateSpreadSpectrum(keyBiner, pin)
			fileName = pdf2png(fileNameInput)
			lineShift(fileName, spreadSpectrum)
			sys.exit()
	elif opts.det:
		if checkFile(opts.det[0]) == False or checkFile(opts.det[2]) == False:
			sys.exit()
		elif checkSeedBody(opts.det[1]) == False:
			sys.exit()
		else:
			watermarkFileInput = opts.det[0]
			seed = opts.det[1]
			fileInfo = opts.det[2]
			fileName = pdf2png(watermarkFileInput)
			watermarkDetect(fileName, fileInfo, seed)
			sys.exit()
	elif opts.ps:
		if checkFile(opts.ps[0]) == False or checkFile(opts.ps[0]) == False:
			sys.exit()
		else:
			countPSNR(opts.ps[0], opts.ps[1])
			sys.exit()

if __name__ == '__main__':
	start()