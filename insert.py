from PIL import Image
import numpy as np
from cprint import *

def read_to_matrix(container : Image, h_image : int, w_image : int): 
	
	container_mx = []

	for row in range(h_image):
		b_row = []
		for col in range(w_image): 
			pos = (col,row)
			# Получваем значения RGB пикселя
			r, g, b = container.getpixel(pos)
			b -= 128
			b_row.append(b)

		container_mx.append(b_row)
	container_mx = np.array(container_mx)
	return container_mx


def dct_forming(): 
	# Заполняем матрицу ДКП
	f_r_item = 0.354 # Для первой строки
	first_row = []
	dct_matrix = []
	# Заполняем первую строку 0.354
	for i in range(8): 
		first_row.append(f_r_item)
	dct_matrix.append(first_row)

	# Заполняем остальную матрицу ДКП
	for i in range(1, 8):
		row = []
		for j in range(0, 8): 
			val = ((2*j + 1)*i*np.pi) / 16
			item = 0.5 * np.cos(val) # Переменная хранящая подкосинусное значение, просто для читаемости
			row.append(round(item, 3))
		dct_matrix.append(row)
		
	# Преобразовываем из обычного питоновского списка в np.array
	dct_matrix = np.array(dct_matrix) 
	
	return dct_matrix

def dct(sector): 
	dct_mx = dct_forming()
	return np.matmul(np.matmul(dct_mx, sector), dct_mx.T)
def inv_dct(sector): 
	dct_mx = dct_forming()
	return np.matmul(np.matmul(dct_mx.T, sector), dct_mx)

def slicing(cantainer): 
	subarrays = []
	h, w = cantainer.shape
	for i in range(0, h, 8):
		for j in range(0, h, 8):
			subarray = [row[j:j+8] for row in cantainer[i:i+8]]
			subarrays.append(subarray)
	slice_array = np.array(subarrays) 

	return slice_array


def combine_slices(slice_matrix, start, end):
	main_matrix = []

	for j in range(8):
		row = []
		for h in range(start, end):
			for ind in range(8):
				row.append(slice_matrix[h][j][ind])
		main_matrix.append(row)
		
	
	return main_matrix


def get_med(sector): 
	items = []
	# добавляем первые девять элементов блока
	items.append(sector[0][1])
	items.append(sector[0][2])
	items.append(sector[0][3])
	items.append(sector[1][0])
	items.append(sector[1][1])
	items.append(sector[2][0])
	items.append(sector[2][1])
	items.append(sector[3][0])

	items = np.array(items)

	sorted_items = np.sort(items)
	
	MED = sorted_items[4]
	
	return MED

def get_force(dc, med, z): 
	if (abs(dc) > 1000) or (abs(dc) < 1): 
		return abs(z * med)
	else: 
		return abs(z * ((dc - med) / dc))


def insertion(b1, b2, delta, m, bit): 
	t = 80
	k = 12
	if bit:
		if delta > (t - k): 
			while delta > (t - k): 
				b1 = b1 - m
				delta = b1 - b2
		elif k > delta and delta > (-t/2): 
			while delta < k: 
				b1 = b1 + m
				delta = b1 - b2
		elif delta < (-t/2): 
			while delta > (-t - k): 
				b1 = b1 - m
				delta = b1 - b2
	else: 
		if delta > t/2: 
			while delta <= (t + k): 
				b1 = b1 + m
				delta = b1 - b2
		elif -k < delta and delta < t/2: 
			while delta >= -k: 
				b1 = b1 - m
				delta = b1 - b2
		elif delta < k - t: 
			while delta <= (k - t): 
				b1 = b1 + m
				delta = b1 - b2
	return b1
	

def conv_DWM(dwm): 
	row = []
	for i in range(len(dwm)): 
		for j in range(len(dwm[i])):
			row.append(dwm[i][j])
	return row


def INSERT(container : Image, watermark : np.array, h_image : int, w_image : int, h_dwm : int, w_dwm : int): 
	np.set_printoptions(suppress=True)
	container = container.convert('RGB')
	container_matrix = read_to_matrix(container, h_image, w_image)
	container_matrix = slicing(container_matrix)
	k=0
	bits = conv_DWM(watermark) 
	first_sector = container_matrix[0]
	first_sector_DCT = dct(first_sector)

	for i in range(len(container_matrix)-1): 
		sector_default = container_matrix[i]
		sector_DCT = dct(sector_default)
		#print(sector_DCT)
		dc = sector_DCT[0][0]
		med = get_med(sector_DCT)
		z = 2
		m = get_force(dc, med, z)

		next_sector_default = container_matrix[i+1]
		next_sector_DCT = dct(next_sector_default)
		bit = bits[k]
		k += 1
		if i % 2 == 0: 
			x_0 = 0
			y_0 = 4

			b1 = sector_DCT[y_0][x_0]
			b2 = next_sector_DCT[y_0][x_0]
		
			delta_LR = b1 - b2

			b1_mod = insertion(b1, b2, delta_LR, m, bit)
			sector_DCT[y_0][x_0] = b1_mod
		elif i % 2 == 1: 
			x_0 = 0
			y_0 = 5

			b1 = sector_DCT[y_0][x_0]
			b2 = next_sector_DCT[y_0][x_0]
		
			delta_LR = b1 - b2

			b1_mod = insertion(b1, b2, delta_LR, m, bit)
			sector_DCT[y_0][x_0] = b1_mod
		sector_inv_DCT = inv_dct(sector_DCT)
		tp = []
		for r in range(len(sector_inv_DCT)): 
			row = []
			for c in range(len(sector_inv_DCT[r])): 
				row.append(round(sector_inv_DCT[r][c]) + 128)
			tp.append(row)
	

		container_matrix[i] = tp
		"""if i == 1:
			rprint("container_matrix[i] после")
			for ttttt in container_matrix[i]: rprint(ttttt)"""
		#print(sector_DCT)
		
	#######################################
	#######################################
	# последний блок
	#######################################
	#######################################
	last = len(container_matrix)-1

	sector_default = container_matrix[last]
	sector_DCT = dct(sector_default)
	
	dc = sector_DCT[0][0]
	med = get_med(sector_DCT)
	z = 2
	m = get_force(dc, med, z)

	next_sector_DCT = first_sector_DCT
	bit = bits[k]
	k += 1
	x_0 = 0
	y_0 = 6

	b1 = sector_DCT[y_0][x_0]
	b2 = next_sector_DCT[y_0][x_0]

	delta_LR = b1 - b2

	b1_mod = insertion(b1, b2, delta_LR, m, bit)
	sector_DCT[y_0][x_0] = b1_mod
	sector_inv_DCT = inv_dct(sector_DCT)
	tp = []
	for i in range(len(sector_inv_DCT)): 
		row = []
		for j in range(len(sector_inv_DCT[i])): 
			row.append(round(sector_inv_DCT[i][j]) + 128)
		tp.append(row)
	container_matrix[last] = tp
	#for el in container_matrix: bprint(el) 

	container_out = []
	tp = []
	for i in range(0, len(container_matrix), 8): 
		tp = combine_slices(container_matrix, i,i+8)
		#print(i, i+8)
		for elem in tp: container_out.append(elem)
		tp = []

	#print(len(container_out), len(container_out[0]))
	return container_out
	#######################################
	#######################################
	#######################################
	