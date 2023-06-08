from PIL import Image
from cprint import *
from math import log10
import numpy as np
from skimage.metrics import structural_similarity as ssim

def check(h_img, w_img, h_wat, w_wat): 
    if h_img != w_img:    print(1); return False
    if h_wat != w_wat:    print(2); return False
    if h_img//8 != h_wat: print(3); return False
    return True

def get_image_path(): 
	bprint("Введите название входного файла (файл должен быть сохранен в папке /in_image)")
	image_name = input()
	path_to_inp_image = "in_image/" + image_name
	
	return path_to_inp_image

def task():
	bprint("Что необходимо сделать с входным файлом:")
	bprint("1 - встроить ЦВЗ;")
	bprint("2 - извлечь ЦВЗ.")
	task = int(input())
	return task


def get_watermark_type(): 
	bprint("Выберите ЦВЗ")
	bprint("1 - ЦВЗ 32x32 (для изображений 256x256);")
	bprint("2 - ЦВЗ 16x16 (для изображений 128x128);")
	bprint("3 - ЦВЗ 8x8 (для изображений 64x64).")
	bprint("Либо введите название файла со своим ЦВЗ")
	typeW = input()
	return typeW


def insert_to_start(container : Image, h_image : int, w_image : int, matrix): 
	container = container.convert('RGB')
	#print(len(matrix), len(matrix[0]), h_image, w_image)
	for row in range(h_image):
		for col in range(w_image): 
			pos = (col,row)
			# Получваем значения RGB пикселя
			r, g, b = container.getpixel(pos)
			#print(row, col)
			b_mod = int(matrix[row][col])
			container.putpixel(pos, (r, g, b_mod))
	return container

def arnold_transformation(watermark_matrix : np.array, watermark_size : int, iter_val : int) -> np.array: 
	
	arnold_matrix = np.zeros((watermark_matrix.shape[0], watermark_matrix.shape[1]))
	
	
	multiplication_matrix = np.array([[1, 1],
				   					  [1, 2]])
	
	#print(watermark_size)
	for iter_counter in range(iter_val):
		for i in range(watermark_size):
			for j in range(watermark_size): 
				# Формируем новые координаты
				new_coord = np.matmul(multiplication_matrix, np.array([[i], [j]]))
				
				# Записываем их
				new_i = int(new_coord[0] % (watermark_size))
				new_j = int(new_coord[1] % (watermark_size))
				#print(new_i, new_j)
				#arnold_matrix.append(watermark_matrix[i][j])
				arnold_matrix[new_i][new_j] = watermark_matrix[i][j]
				#np.copyto(arnold_matrix[new_i:new_i + watermark_matrix.shape[0], new_j:new_j + watermark_matrix.shape[1]], watermark_matrix)
	#print("arnold", arnold_matrix)
	
	arnold_matrix = np.array(arnold_matrix)
	
	return arnold_matrix

def inv_arnold_transformation(arnold_watermark_matrix : np.array, watermark_size : int, iter_val : int) -> np.array: 
	"""Функция возвращающая обратную матрицу Арнольда

	Args:
		arnold_watermark_matrix (np.array): _description_
		watermark_size (int): _description_
		iter_val (int): _description_

	Returns:
		np.array: inv_arnold_matrix - обратная матрица Арнольда
	"""
	inv_arnold_matrix = np.zeros((arnold_watermark_matrix.shape[0], arnold_watermark_matrix.shape[1]))
	

	multiplication_matrix = np.array([[2, -1], [-1, 1]])
	#print(watermark_size)
	for iter_counter in range(iter_val):
		for i in range(watermark_size):
			for j in range(watermark_size): 
				# Формируем новые координаты
				new_coord = np.matmul(multiplication_matrix, np.array([[i], [j]]))
				
				# Записываем их
				new_i = int(new_coord[0] % (watermark_size))
				new_j = int(new_coord[1] % (watermark_size))
				#print(new_i, new_j)
				#arnold_matrix.append(watermark_matrix[i][j])
				inv_arnold_matrix[new_i][new_j] = arnold_watermark_matrix[i][j]
				#np.copyto(arnold_matrix[new_i:new_i + watermark_matrix.shape[0], new_j:new_j + watermark_matrix.shape[1]], watermark_matrix)
	#print("arnold", inv_arnold_matrix)
	inv_arnold_matrix = np.array(inv_arnold_matrix)


	return inv_arnold_matrix


def to_watermark_matrix(dwm, step): 
	matrix_dwm = []
	st = 0

	for i in range(step): 
		row = []
		for j in range(st, st+step): 
			row.append(dwm[j])
		matrix_dwm.append(row)
		st += step
	return np.array(matrix_dwm)



def get_mse(
        old_img : Image, 
        new_img : Image) -> float: 
	old_img = old_img.convert('RGB')
	new_img = new_img.convert('RGB')
	size_of_img = (old_img.size)
	size = size_of_img[0] * size_of_img[1]
	delta_sum = 0

	for y in range(size_of_img[1]):
		for x in range(size_of_img[0]):
			pos = (x,y)
			r_old, g_old, b_old = old_img.getpixel(pos)
			r_new, g_new, b_new = new_img.getpixel(pos)
			
			delta = b_old - b_new

			delta_sum += pow(delta,2)

	MSE = delta_sum / (size)

	return MSE

def get_psnr(
		MSE : float) -> float: 
	PSNR = 10 * log10((255*255)/MSE)

	return PSNR

def get_rmse(
		MSE : float) -> float: 
	RMSE = pow(MSE, 0.5)

	return RMSE


def get_ssim(
		old_img : Image, 
        new_img : Image): 
	
	old_arr = np.array(old_img)
	new_arr = np.array(new_img)

	b_old = old_arr[:, :, 2]
	b_new = new_arr[:, :, 2]

	SSIM = ssim(b_old, b_new)

	return SSIM


