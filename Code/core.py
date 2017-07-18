'''
	title	: PDF Text Watermarking Using Line Shifting 
	author	: Albert Mario G64130101
	desc	: core file include shifting line and detect watermark
'''

#!/usr/bin/env python
#-*- coding:utf-8 -*-

from colorama import Fore, Back, Style
from progressbar import *
from util import *
import ImageDraw
import Image
import PyPDF2
import glob
import sys
global REV_SEQUENCE	
global SEQUENCE
global PUTIH

PUTIH = (255, 255, 255)
SEQUENCE = generateSequenceShift(4)
REV_SEQUENCE = dict([(v, k) for k, v in SEQUENCE.iteritems()])

def lineShift(fileName, spreadSpectrum):
	fileNameInputs = sorted(glob.glob(fileName + '*.png'))
	ori = []
	bantuShift = -4
	merger = PyPDF2.PdfFileMerger()

	print Fore.CYAN + '[+]'+ Style.RESET_ALL +' Counting space and shifting line'
	
	for fileNameInput in fileNameInputs:
		im = Image.open(fileNameInput)
		am = Image.new(im.mode, im.size, 'white')
		draw = ImageDraw.Draw(am)

		lebar, tinggi = im.size
		
		patokan = 0
		hitungPutih = 0
		hitungSpasi = 0
		masukHitam = 0
		saatnya = 0

	    #hitung jumlah spasinya
		for i in range(tinggi):
			if hitungPutih == lebar:
				if patokan:
					if masukHitam:
						hitungSpasi += 1
						saatnya = 1
					else:
						patokan = 0

				else:
					pass # patokan = 0

			hitungPutih = 0

			for j in range(lebar):
				if im.getpixel((j, i)) == PUTIH:
					hitungPutih += 1
				else:
					if patokan:
						if masukHitam:
							if saatnya:
								ori.append(hitungSpasi)
								hitungSpasi = 0
								masukHitam = 0
								saatnya = 0
					else:
						patokan = 1
						masukHitam = 1

		#geser
		lineSpacing = 0
		cekSpasi = 0
		patokan = 1
		bantuSpasi = 0
			
		bantu_stop = 0
		tanda = ''
		x = 0


		for i in range(tinggi):
			if bantuSpasi == lebar:
				cekSpasi += 1
				
			if lineSpacing == 0:
				if cekSpasi > 8:
					lineSpacing = 1
				
					if patokan:
						patokan = 0
						bantuShift += 4
						
						if bantuShift >= len(spreadSpectrum):
							bantu_stop = 1
							
					else:
						patokan = 1
				
			bantuSpasi = 0
 			
			for j in range(lebar):
				if im.getpixel((j, i)) == PUTIH:
					bantuSpasi += 1
				else:
					cekSpasi = 0
					lineSpacing = 0
					if patokan == 0 and bantu_stop == 0: #kalo bukan patokan, digeser, tapi kalo patokan jangan digeser (diem aja di tempat)
						tanda = spreadSpectrum[bantuShift : bantuShift + 4]
						geser = SEQUENCE[tanda]
						draw.point((j, i + geser), im.getpixel((j, i))) #geser
					else:
						draw.point((j, i), im.getpixel((j, i)))

		bantuShift -= 4
		
		file_save = fileNameInput
		am.save(file_save, 'png')
		file_save_pdf = file_save.split('.')[0] + '.pdf'
		png2pdf(file_save, file_save_pdf)
		merger.append(open(file_save_pdf,'rb'))

	print Fore.CYAN + '[+]'+ Style.RESET_ALL +' Done'
	print Fore.CYAN + '[+]'+ Style.RESET_ALL +' Save watermarked file'
	fileName = raw_input(Fore.CYAN + '[+]'+ Style.RESET_ALL +' Save location : ')
	with open(fileName, 'wb') as fout:
		merger.write(fout)

	print Fore.CYAN + '[+]'+ Style.RESET_ALL +' Done'
	print Fore.CYAN + '[+]'+ Style.RESET_ALL +' Save info file '
	fileInfoLocation = raw_input(Fore.CYAN + '[+]'+ Style.RESET_ALL +' Save location : ')
	open(fileInfoLocation, 'w').write(' '.join(str(x) for x in ori))
	print Fore.CYAN + '[+]'+ Style.RESET_ALL +' Done'

def watermarkDetect(watermarkFile, seed, fileInfo):
	watermark = ''
	watermarkFiles = sorted(glob.glob(watermarkFile + '*.png'))
	wat = []

	print Fore.CYAN + '[+]' + Style.RESET_ALL+' Detecting watermark'

	for watermarkFile in watermarkFiles:
		imWat = Image.open(watermarkFile)

		lebar, tinggi = imWat.size
						
		#wat
		patokan = 0
		hitungPutih = 0
		hitungSpasi = 0
		masukHitam = 0
		saatnya = 0

		x = 0

	    #hitung jumlah spasinya
		for i in range(tinggi):
			if hitungPutih == lebar:
				if patokan:
					if masukHitam:
						hitungSpasi += 1
						saatnya = 1
					else:
						patokan = 0

				else:
					pass # patokan = 0

			hitungPutih = 0

			for j in range(lebar):
				x += 1
				
				if imWat.getpixel((j, i)) == PUTIH:
					hitungPutih += 1
				else:
					if patokan:
						if masukHitam:
							if saatnya:
								wat.append(hitungSpasi)
								hitungSpasi = 0
								masukHitam = 0
								saatnya = 0
					else:
						patokan = 1
						masukHitam = 1
		
	ss = ''
	count = 0
	ori = open(fileInfo, 'r').read().split()

	for i in range(len(wat)):
		temp = int(ori[i]) - wat[i]
		if temp:
			ss += REV_SEQUENCE[temp]
			count += 1

	pin = generatePin(seed, count * 4)
	keyBiner = generateSpreadSpectrum(pin, ss)

	x = 0
	for i in range(count / 2):
		watermark += chr(int(keyBiner[x : x + 8], 2))
		x += 8

		
	print Fore.CYAN + '[+]'+ Style.RESET_ALL + ' Done'
	print Fore.CYAN + '[+]' +  Style.RESET_ALL + ' Watermark :', watermark

def countPSNR(ori, wat):
	MSE = 0

	fileOri = sorted(glob.glob(pdf2png(ori) + '*.png'))
	fileWat = sorted(glob.glob(pdf2png(wat) + '*.png'))

	print fileOri
	print fileWat






	# PSNR = 20 * log(MAX / math.sqrt(MSE))