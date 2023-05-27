import numpy as np
from PIL import Image

def get_watermark(type_w):

	watermark_big= Image.open('in_watermark/16x16.PNG').convert('L')
	# Преобразование изображения в двумерный массив
	array1 = np.array(watermark_big)

	watermark_circle = Image.open('in_watermark/watermark2.PNG').convert('L')
	# Преобразование изображения в двумерный массив
	array2 = np.array(watermark_circle)

	if type_w == 1: return array1
	if type_w == 2: return array2