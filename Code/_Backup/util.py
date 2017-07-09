'''
	title : PDF Text Watermarking Using Line Shifting 
	author : Albert Mario G64130101
	desc : utilility for convert, generate, and check
'''

#!/usr/bin/env python
#-*- coding:utf-8 -*-

from colorama import Fore, Back, Style
import commands
import Image
import os

def pdf2png(file_name_input):
	# file_name_output = raw_input(Fore.CYAN + '[+]' + Style.RESET_ALL + ' Location to save the PNG : ')
	print Fore.CYAN + '[+]'+ Style.RESET_ALL+' Convert PDF to PNG'
	file_name_output = file_name_input.split('.')[0]
	cmd = 'gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -r500 -sOutputFile=' + file_name_output + '%d.png '+ file_name_input #png 500 dpi
	try:
		os.system(cmd)
	except:
		print Fore.Cyan + '[+]' + Style.RESET_ALL + 'Error on converting PDF to PNG'
		exit(0)

	return file_name_output

	print Fore.CYAN + '[+]' + Style.RESET_ALL + ' Done'
	
def png2pdf(file_name_input, file_name_output):
	cmd = 'convert '+file_name_input+' -quality 100 -density 500 '+ file_name_output
	try:
		os.system(cmd)
	except:
		print Fore.Cyan + '[+]' + Style.RESET_ALL + 'Error on converting PNG to PDF'
		exit(0)

def generate_pin(seed, len_key):
	#pin ini menggunakan LFSR 6
	#akan diputar sesuai dengan panjang key
	
	list_seed = [int(i) for i in seed]
	hasil = str(list_seed[-1])
	
	for i in range(len_key - 1):
		temp = [list_seed[-1] ^ list_seed[3] ^ list_seed[1] ^ list_seed[0]]
		list_seed = temp + list_seed[:-1]
		hasil += str(list_seed[-1])
	
	return hasil

def generate_spread_spectrum(key, pin):
	hasil = ''
	for i in range(len(key)):
		hasil += str(int(key[i]) ^ int(pin[i]))
	
	return hasil

def generate_sequence_shift(length):
	shift_pixel = {}
	shift = 0
	shift2 = 0
	selisih = 1

	for i in range(2 ** length):
		temp = ''.join('{0:04b}'.format(i))
		if i < 2 ** length / 2:
			shift += selisih
			shift_pixel[temp] = shift
		else:
			shift2 -= selisih
			shift_pixel[temp] = shift2	

	# print shift_pixel
	return shift_pixel

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

	open('hasil1', 'w').write(hasil)

def check_line(file_name_input, key): # cek apakah jumlah baris > panjang key
	a = commands.getstatusoutput('pdftotext -layout ' + file_name_input + ' - | wc -l')

	jum_baris = int(a[1])
	len_key = len(key) * 8
	
	if jum_baris / 2 >= len_key / 4:
		return True
	else:
		return False

def check_key_body(pin): #cek apakah pin hanya mengandung 0 dan 1
	list_key = ['0', '1']
	
	for i in pin:
		if i not in list_key:
			return False
	
	return True

def check_file(file):
	try:
		open(file)
	except:
		return False

def hitung_PSNR(ori, wat):
	pass
