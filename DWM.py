import numpy as np
from PIL import Image

def get_watermark(type_w):

	if type_w == '1': 
		watermark_3= Image.open('in_watermark/32.png').convert('L')
		# Преобразование изображения в двумерный массив
		array3 = np.array(watermark_3)
		return array3
	elif type_w == '2': 
		watermark2 = Image.open('in_watermark/16x16.PNG').convert('L')
		# Преобразование изображения в двумерный массив
		array2 = np.array(watermark2)
		return array2
	elif type_w == '3': 
		watermark1= Image.open('in_watermark/watermark2.PNG').convert('L')
		# Преобразование изображения в двумерный массив
		array1 = np.array(watermark1)
		return array1
	else: 
		try: 
			watermark_custom= Image.open(f'in_watermark/{type_w}').convert('L')
			# Преобразование изображения в двумерный массив
			arrayc = np.array(watermark_custom)
			return arrayc
		except: 
			return 0