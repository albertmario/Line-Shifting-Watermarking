'''
	title	: PDF Text Watermarking Using Line Shifting 
	author	: Albert Mario G64130101
	desc	: core file include shifting line and detect watermark
'''

#!/usr/bin/env python
#-*- coding:utf-8 -*-

from colorama import Fore, Back, Style
from util import *
from PIL import ImageDraw
from PIL import Image
import PyPDF2
import glob
import sys
import math
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
						draw.point((j, i + geser), im.getpixel((j, i))) #geser posisi baris ganjil
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

def watermarkDetect(watermarkFile, fileInfo, seed):
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
			try:
				ss += REV_SEQUENCE[temp]
			except:
				pass
				
			count += 1

	seedBiner = ''.join('{0:08b}'.format(ord(x), 'b') for x in seed)
	pin = generatePin(seedBiner, count * 4)
	keyBiner = generateSpreadSpectrum(pin, ss)

	x = 0
	for i in range(count / 2):
		watermark += chr(int(keyBiner[x : x + 8], 2))
		x += 8

		
	print Fore.CYAN + '[+]'+ Style.RESET_ALL + ' Done'
	print Fore.CYAN + '[+]' +  Style.RESET_ALL + ' Watermark :', watermark

def countPSNR(ori, wat):
	#perhitungan PSNR didasarkan pada masing2 channel R, G, B

	fileOri = sorted(glob.glob(pdf2png(ori) + '*.png'))
	fileWat = sorted(glob.glob(pdf2png(wat) + '*.png'))

	maxR = maxG = maxB = 0
	mseR = mseG = mseB = 0

	for i in range(len(fileOri)):
		im = Image.open(fileOri[i])
		am = Image.open(fileWat[i])
		lebar, tinggi = im.size

		for j in range(tinggi):
			for k in range(lebar):
				ri,gi,bi = im.getpixel((k, j))
				if ri >= maxR:
					maxR = ri
				if gi >= maxG:
					maxG = gi
				if bi >= maxB:
					maxB = bi

				ra,ga,ba = am.getpixel((k, j))

				mseR += pow((ri - ra), 2)
				mseG += pow((gi - ga), 2)
				mseB += pow((bi - ba), 2)

	mseR = mseR * 1.0 / (lebar * tinggi)
	mseG = mseG * 1.0 / (lebar * tinggi)
	mseB = mseB * 1.0 / (lebar * tinggi)

	psnrR = 20 * math.log(maxR / math.sqrt(mseR))
	psnrG = 20 * math.log(maxG / math.sqrt(mseG))
	psnrB = 20 * math.log(maxB / math.sqrt(mseB))

	print Fore.CYAN + '[+]' + Style.RESET_ALL + ' PSNR on channel Red', psnrR
	print Fore.CYAN + '[+]' + Style.RESET_ALL + ' PSNR on channel Green', psnrG
	print Fore.CYAN + '[+]' + Style.RESET_ALL + ' PSNR on channel Blue', psnrB