'''
	title	: PDF Text Watermarking Using Line Shifting 
	author	: Albert Mario G64130101
	desc	: utilility for convert, generate, and check
'''

#!/usr/bin/env python
#-*- coding:utf-8 -*-

from colorama import Fore, Back, Style
import commands
import Image
import os

#===============================Custom Error Exception=====================
class Error(Exception):
	'''Base class for other exception'''
	pass
class SeedError(Error):
	'''Exception for pin error'''
	def __init__(self):
		self.msg = 'seed of pin must be 1 character only'
class KeyError(Error):
	'''Exception for key error'''
	def __init__(self):
		self.msg = 'the secret key is too long'
class FileError(Error):
	'''Exception for file error'''
	def __init__(self):
		self.msg = 'no such file'
class SumError(Error):
	'''Exception for Sum error'''
	def __init__(self):
		self.msg = 'md5sum is different'

#==============================Utility=====================================
def pdf2png(fileNameInput):
	print Fore.CYAN + '[+]'+ Style.RESET_ALL+' Convert PDF to PNG'
	fileNameOutput = fileNameInput.split('.')[0]
	cmd = 'gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -r500 -sOutputFile=' + fileNameOutput + '%d.png '+ fileNameInput #png 500 dpi
	os.system(cmd)
	return fileNameOutput
	
def png2pdf(fileNameInput, fileNameOutput):
	cmd = 'convert '+fileNameInput+' -quality 100 -density 500 '+ fileNameOutput
	os.system(cmd)

def generatePin(seed, lenKey):
	#pin ini menggunakan LSFR 8 bit
	#akan diputar sesuai dengan panjang key
	
	listSeed = [int(i) for i in seed]
	hasil = str(listSeed[-1])
	
	for i in range(lenKey - 1):
		temp = [listSeed[-1] ^ listSeed[3] ^ listSeed[1] ^ listSeed[0]]
		listSeed = temp + listSeed[:-1]
		hasil += str(listSeed[-1])
	
	return hasil

def generateSpreadSpectrum(key, pin):
	hasil = ''
	for i in range(len(key)):
		hasil += str(int(key[i]) ^ int(pin[i]))
	
	return hasil

def generateSequenceShift(length):
	shiftPixel = {}
	shift = 0
	shift2 = 0
	selisih = 1

	for i in range(2 ** length):
		temp = ''.join('{0:04b}'.format(i))
		if i < 2 ** length / 2:
			shift += selisih
			shiftPixel[temp] = shift
		else:
			shift2 -= selisih
			shiftPixel[temp] = shift2	

	return shiftPixel

def pixels(file_name):
	im = Image.open(file_name)
	print im.format, im.size, im.mode

	lebar, tinggi = im.size
	
	hasil = ''
	temp = 0
	
	for i in range(tinggi):
		for j in range(lebar):
			r,g,b = im.getpixel((j, i))
			if r == g == b == 255:
				temp = 0
			else:
				temp = 1
			
			if j == lebar - 1:
				hasil += str(temp) + "\n"
			else:
				hasil += str(temp)

	open('hasil2', 'w').write(hasil)

def checkLine(fileNameInput, key): # cek apakah jumlah baris > panjang key
	try:
		a = commands.getstatusoutput('pdftotext -layout ' + fileNameInput + ' - | wc -l')

		jumBaris = int(a[1])
		lenKey = len(key) * 8
		
		if jumBaris / 2 >= lenKey / 4:
			return True
		else:
			raise KeyError
	except KeyError, err:
		print err.msg
		return False

def checkSeedBody(seed): #cek apakah seed hanya mengandung 0 dan 1
	try:

		if len(seed) > 1:
			raise SeedError

		return True
	except SeedError, err:
		print err.msg
		return False

def checkFile(file):
	try:
		if os.path.isfile(file) == False:
			raise FileError
	except FileError, err:
		print err.msg
		return False