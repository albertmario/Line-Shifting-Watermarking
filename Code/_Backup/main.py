'''
	title : PDF Text Watermarking Using Line Shifting 
	author : Albert Mario G64130101
	desc : main file
'''

#!/usr/bin/env python
#-*- coding:utf-8 -*-

from colorama import Fore, Back, Style
from core import *
from util import *
import sys

def manual():
	print 'SYNOPSIS'
	print '\t python main.py [OPTIONS] [ARGS]\n'
	print 'DESCRIPTION'
	print '\t PDF Text Watermarking Using Line Shifting\n'
	print 'OPTIONS'
	print '\t-S, --shift\n\t\tShifting line with key and pin.'
	print '\t-D, --detect\n\t\tDetect the watermark.'
	print '\t-P, --psnr\n\t\tPeak Signal to Noise Ratio'
	print '\t-H, --help\n\t\tShow this manual.'

def start():
	cek = 0
	if len(sys.argv) < 2:
		print 'python ' + sys.argv[0] + ' --help to see manual.'
		exit(0)
	else:	
		if sys.argv[1] == '-S' or sys.argv[1] == '--shift': 
			if len(sys.argv) != 5:
				print 'Usage: python ' + sys.argv[0] + ' --shift [/path/to/file] [key] [pin]'
				exit(0)
			elif check_file(sys.argv[2]) == False:
				print sys.argv[2] + ': No such file or directory'
				exit(0)
			elif len(sys.argv[4]) != 6 or check_key_body(sys.argv[4]) == False:
				print 'pin must be 6 characters long consist of 1 and 0'
				exit(0)
			elif check_line(sys.argv[2], sys.argv[3]) == False:
				print 'the key is too long'
				exit(0)

		elif sys.argv[1] == '-D' or sys.argv[1] == '--detect':
			if len(sys.argv) != 5:
				print 'Usage: python ' + sys.argv[0] + ' --detect [/path/to/file] [pin] [/path/to/info]'
				exit(0)
			elif check_file(sys.argv[2]) == False:
				print sys.argv[2] + ': No such file or directory'
				exit(0)
			elif len(sys.argv[3]) != 6 or check_key_body(sys.argv[3]) == False:
				print 'pin must be 6 characters long consist of 1 and 0'
				exit(0)
			elif check_file(sys.argv[4]) == False:
				print sys.argv[4] + ': No such file or directory'
				exit(0)
			cek = 1

		elif sys.argv[1] == '--psnr' or sys.argv[1] == '-P':
			if len(sys.argv) != 4:
				print 'Usage: python ' + sys.argv[0] + ' --psnr [/path/to/original/file/png] [/path/to/watermarked/file/png]'
				exit(0)
			cek = 2

		elif sys.argv[1] == '-H' or sys.argv[1] == '--help':
			manual()
			exit(0)

		else:
			print 'Invalid argument'
			print 'python ' + sys.argv[0] + ' --help to see manual.'
			exit(0)

	if cek == 0:
		file_name_input = sys.argv[2]
		key = sys.argv[3]
		seed = sys.argv[4]
		pin = generate_pin(seed, len(key) * 8)
		key_biner = ''.join('{0:08b}'.format(ord(x), 'b') for x in key)
		spread_spectrum = generate_spread_spectrum(key_biner, pin)
		file_name = pdf2png(file_name_input)
		# line_shift(file_name, spread_spectrum)
	elif cek == 1:
		watermark_file_input = sys.argv[2]
		file_name = pdf2png(watermark_file_input)
		seed = sys.argv[3]
		file_info = sys.argv[4]
		watermark = watermark_detect(file_name, seed, file_info)
		print Fore.CYAN + '[+]' +  Style.RESET_ALL + ' Watermark :', watermark
	else:
		hitung_PSNR(sys.argv[2], sys.argv[3])
		

if __name__ == '__main__':
	start()