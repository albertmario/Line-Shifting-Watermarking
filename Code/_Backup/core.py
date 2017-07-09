'''
	title : PDF Text Watermarking Using Line Shifting 
	author : Albert Mario G64130101
	desc : core file include shifting line and detect watermark
'''

#!/usr/bin/env python
#-*- coding:utf-8 -*-

from colorama import Fore, Back, Style
from progressbar import *
from util import *
import ImageDraw
import Image
import glob
global rev_sequence	
global sequence
global putih

putih = (255, 255, 255)
sequence = generate_sequence_shift(4)
rev_sequence = dict([(v, k) for k, v in sequence.iteritems()])

def line_shift(file_name, spread_spectrum):
	file_name_input = glob.glob(file_name + '*.png')[0]
	im = Image.open(file_name_input)
	am = Image.new(im.mode, im.size, 'white')
	draw = ImageDraw.Draw(am)
	
	ori = []
	lebar, tinggi = im.size
	
	patokan = 0
	hitung_putih = 0
	hitung_spasi = 0
	masuk_hitam = 0
	saatnya = 0

	print Fore.CYAN + '[+]'+ Style.RESET_ALL + ' Counting space on original file'
	widgets = [Fore.CYAN + '[+]'+ Style.RESET_ALL +' Progress: ', Percentage(), ' ', Bar(marker=u'\u2588',left='[',right=']'),
           ' ', ETA(), ' '] #see docs for other options

	pbar = ProgressBar(widgets=widgets, maxval=lebar*tinggi)
	x = 0
	pbar.start()
    #hitung jumlah spasinya
	for i in range(tinggi):
		if hitung_putih == lebar:
			if patokan:
				if masuk_hitam:
					hitung_spasi += 1
					saatnya = 1
				else:
					patokan = 0

			else:
				pass # patokan = 0

		hitung_putih = 0

		for j in range(lebar):
			x += 1
			pbar.update(x)
			if im.getpixel((j, i)) == putih:
				hitung_putih += 1
			else:
				if patokan:
					if masuk_hitam:
						if saatnya:
							ori.append(hitung_spasi)
							hitung_spasi = 0
							masuk_hitam = 0
							saatnya = 0
				else:
					patokan = 1
					masuk_hitam = 1
	pbar.finish()

	print Fore.CYAN + '[+]'+ Style.RESET_ALL +' Save info file '
	file_info_location = raw_input(Fore.CYAN + '[+]'+ Style.RESET_ALL +' Save location : ')
	open(file_info_location, 'w').write(' '.join(str(x) for x in ori))
	print Fore.CYAN + '[+]'+ Style.RESET_ALL +' Done'
	
	line_spacing = 0
	cek_spasi = 0
	patokan = 1
	bantu_spasi = 0
	bantu_shift = -4
	bantu_stop = 0
	tanda = ''
	x = 0

	print Fore.CYAN + '[+]'+ Style.RESET_ALL +' Shifting line'

	pbar = ProgressBar(widgets=widgets, maxval=lebar*tinggi)
	pbar.start()

	#geser
	for i in range(tinggi):
		if bantu_spasi == lebar:
			cek_spasi += 1
			
		if line_spacing == 0:
			if cek_spasi > 8:
				line_spacing = 1
			
				if patokan:
					patokan = 0
					bantu_shift += 4
					
					if bantu_shift >= len(spread_spectrum):
						bantu_stop = 1
						
				else:
					patokan = 1
			
		bantu_spasi = 0
		
		for j in range(lebar):
			x += 1
			pbar.update(x)
			if im.getpixel((j, i)) == putih:
				bantu_spasi += 1
			else:
				cek_spasi = 0
				line_spacing = 0
				if patokan == 0 and bantu_stop == 0: #kalo bukan patokan, digeser, tapi kalo patokan jangan digeser (diem aja di tempat)
					tanda = spread_spectrum[bantu_shift : bantu_shift + 4]
					geser = sequence[tanda]
					draw.point((j, i + geser), im.getpixel((j, i))) #geser
				else:
					draw.point((j, i), im.getpixel((j, i)))
	
	pbar.finish()
	print Fore.CYAN + '[+]'+ Style.RESET_ALL +' Save watermarked file'
	file_save = raw_input(Fore.CYAN + '[+]'+ Style.RESET_ALL +' Save location : ')
	am.save(file_save, 'png')
	print Fore.CYAN + '[+]'+ Style.RESET_ALL +' Convert back to PDF'
	file_save_pdf = file_save.split('.')[0] + '.pdf'
	png2pdf(file_save, file_save_pdf)
	print Fore.CYAN + '[+]'+ Style.RESET_ALL +' Done'

def watermark_detect(watermark_file, seed, file_info):
	watermark_file = glob.glob(watermark_file + '*.png')[0]
	im_wat = Image.open(watermark_file)

	wat = []
	res = []

	lebar, tinggi = im_wat.size
	widgets = [Fore.CYAN + '[+]'+ Style.RESET_ALL+ ' Progress: ', Percentage(), ' ', Bar(marker=u'\u2588',left='[',right=']'),
           ' ', ETA(), ' '] #see docs for other options

	print Fore.CYAN + '[+]' + Style.RESET_ALL+' Detecting watermark'
	pbar = ProgressBar(widgets=widgets, maxval=lebar*tinggi)
	pbar.start()
					
	#wat
	patokan = 0
	hitung_putih = 0
	hitung_spasi = 0
	masuk_hitam = 0
	saatnya = 0
	x = 0

	for i in range(tinggi):
		if hitung_putih == lebar:
			if patokan:
				if masuk_hitam:
					hitung_spasi += 1
					saatnya = 1
				else:
					patokan = 0

			else:
				pass # patokan = 0

		hitung_putih = 0

		for j in range(lebar):
			x += 1
			pbar.update(x)
			if im_wat.getpixel((j, i)) == putih:
				hitung_putih += 1
			else:
				if patokan:
					if masuk_hitam:
						if saatnya:
							wat.append(hitung_spasi)
							hitung_spasi = 0
							masuk_hitam = 0
							saatnya = 0
							# patokan = 0
				else:
					patokan = 1
					masuk_hitam = 1
	
	
	ss = ''
	count = 0
	ori = open(file_info, 'r').read().split()

	for i in range(len(wat)):
		temp = int(ori[i]) - wat[i]
		if temp:
			ss += rev_sequence[temp]
			count += 1

	pin = generate_pin(seed, count * 4)
	key_biner = generate_spread_spectrum(pin, ss)

	watermark = ''
	x = 0
	for i in range(count / 2):
		watermark += chr(int(key_biner[x : x + 8], 2))
		x += 8

	pbar.finish()
	print Fore.CYAN + '[+]'+ Style.RESET_ALL + ' Done'
	return watermark