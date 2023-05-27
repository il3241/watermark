from PIL import Image
import numpy as np

from cprint import *
import DWM
import insert
import extract
import proc

def main(): 
	image_path = proc.get_image_path()
	try: 
		image_cont = Image.open(image_path)
	except FileNotFoundError: 
		rprint("Файл изображения не найден. Обратите внимание, что входной файл должен находиться в папке /in_image")
		return
	# Получаем ширину и высоту изображения
	w_img, h_img = image_cont.size
	
	# Целевое действие
	todo_main = proc.task()

	while todo_main != "exit": 
		if todo_main == 1:
			todo_main == "exit"
			# Получаем ЦВЗ
			type_w = proc.get_watermark_type()

			while  type_w != "exit": 
				if type_w != 1 and type_w != 2: 
					rprint("Введите либо 1, либо 2")
					type_w = int(input())
				else: 

					watermark = DWM.get_watermark(type_w)
					type_w = "exit"

					
			h_wat, w_wat = watermark.shape
			if proc.check(h_img, w_img, h_wat, w_wat):
				bprint("Необходимо применить преобразование Арнольда?")
				bprint("1 - Да;")
				bprint("2 - Нет.")
				arn = int(input())
				while arn != "exit": 
					if arn == 1: 
						gprint("Введите кол-во итераций")
						iter = int(input())
						watermark = proc.arnold_transformation(watermark, h_wat, iter)
						for row in watermark: rprint(row)
						arn = "exit"
					elif arn == 2: 			
						arn = "exit"
					else: 
						rprint("Введите либо 1, либо 2")
						arn = int(input())
				
				out_matrix = insert.INSERT(image_cont, watermark, h_img, w_img, h_wat, w_wat)
				#for row in out_matrix: rprint(row)
				new_image = proc.insert_to_start(image_cont, h_img, w_img, out_matrix)
				new_image.save("output.PNG")
				new_image.show

				return 0
				
			
			
		elif todo_main == 2:
			
			ext_mes = extract.extraction(image_cont)
			ext_mes_dwm = proc.to_watermark_matrix(ext_mes)
			bprint("При встраивании было применено преобразование Арнольда?")
			bprint("1 - Да;")
			bprint("2 - Нет.")
			inv_arn = int(input())
			if inv_arn == 1: 
				gprint("Введите кол-во итераций:")
				iter = int(input())
				h_wat, w_wat = ext_mes_dwm.shape
				ext_mes_dwm = proc.inv_arnold_transformation(ext_mes_dwm, h_wat, iter)
			for row in ext_mes_dwm: bprint(row)
			image = Image.fromarray((ext_mes_dwm * 255).astype(np.uint8), 'L')
			# Отображение изображения
			image.save(f"out_watermark/watermark.PNG")
			todo_main == "exit"
			return 0
		else: 
			bprint("Что необходимо сделать с входным файлом:")
			bprint("1 - встроить ЦВЗ;")
			bprint("2 - извлечь ЦВЗ.")
			bprint("Введите либо 1, либо 2!")
			todo_main = int(input())

if __name__ == "__main__": 
	main()
	


