from PIL import Image
import numpy as np

from cprint import *
import DWM
import insert
import extract
import proc
import mist
import histograms


def main(): 
	image_path = proc.get_image_path()
	try: 
		image_cont = Image.open(image_path)
		start_img = image_cont
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
				tp = DWM.get_watermark(type_w)
				if len(tp) == 0: 
					rprint("Введите либо номер от 1 до 3, либо название существубщего файла в папке in_watermark/")
					type_w = int(input())
				else: 
					watermark = tp
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
						
						arn = "exit"
					elif arn == 2: 			
						arn = "exit"
					else: 
						rprint("Введите либо 1, либо 2")
						arn = int(input())
				gprint("Введите значениие параметра алгоритма (значение по умолчанию 2):")
				z_inp = int(input())
				gprint("Введите значениие параметров T и K (значения по умолчанию 80 и 12):")
				t_inp = int(input())
				k_inp = int(input())
				out_matrix = insert.INSERT(image_cont, watermark, h_img, w_img, h_wat, w_wat, z_inp, t_inp, k_inp)
				#for row in out_matrix: rprint(row)
				new_image = proc.insert_to_start(image_cont, h_img, w_img, out_matrix)
				new_image.save("output.PNG")
				bprint("Оценить качество встраивания?")
				bprint("1 - Да;")
				bprint("2 - Нет.")
				obs = int(input())
				while obs != "exit": 
					if obs == 1: 
						
						mse = proc.get_mse(start_img, new_image)
						rmse = proc.get_rmse(mse)
						psnr = proc.get_psnr(mse)
						ssim = proc.get_ssim(start_img, new_image)
						bprint("=====================")
						bprint("MSE")
						gprint(round(mse, 3))
						bprint("---------------------")
						bprint("RMSE")
						gprint(round(rmse, 3))
						bprint("---------------------")
						bprint("PSNR")
						gprint(round(psnr, 3))
						bprint("---------------------")
						bprint("SSIM")
						gprint(round(ssim, 3))
						bprint("=====================")
						obs = "exit"
					elif obs == 2: 
						obs = "exit"
					else: 
						rprint("Введите либо 1 (Да), либо 2 (Нет).")
						obs = int(input())
				bprint("Оценить устойчивость встраивания к деструктивным воздействиям?")
				bprint("Да  - 1")
				bprint("Нет - 2")
				destr = int(input())
				while destr != "exit": 
					if destr == 1: 
						ext_mes = extract.extraction(new_image, t_inp)
						
						watermark_l = mist.to_list(watermark)
						
						bprint("=====================")
						bprint("BER_0") 
						BER_0 = mist.CHECK(watermark_l, ext_mes)
						gprint(BER_0)
						bprint("---------------------")
						bprint("BER_blur") 
						BER_blur = mist.blur_and_check(t_inp, watermark_l, new_image)
						gprint(round(BER_blur, 3))
						bprint("---------------------")
						bprint("BER_sharpen") 
						BER_sharpen = mist.sharpen_and_check(t_inp, watermark_l, new_image)
						gprint(round(BER_sharpen, 3))
						bprint("---------------------")
						bprint("BER_contour") 
						BER_contour = mist.contour_and_check(t_inp, watermark_l, new_image)
						gprint(round(BER_contour, 3))
						bprint("---------------------")
						bprint("BER_smooth") 
						BER_smooth = mist.smooth_and_check(t_inp, watermark_l, new_image)
						gprint(round(BER_smooth, 3))
						bprint("---------------------")
						bprint("BER_jpeg_90") 
						BER_jpeg_90 = mist.jpg_scale_90(t_inp, watermark_l, new_image)
						gprint(round(BER_jpeg_90, 3))
						bprint("---------------------")
						bprint("BER_jpeg_60") 
						BER_jpeg_60 = mist.jpg_scale_60(t_inp, watermark_l, new_image)
						gprint(round(BER_jpeg_60, 3))
						bprint("---------------------")
						bprint("BER_jpeg_20") 
						BER_jpeg_20 = mist.jpg_scale_20(t_inp, watermark_l, new_image)
						gprint(round(BER_jpeg_20, 3))
						bprint("=====================")

						destr = "exit"
					elif destr == 2: 
						destr = "exit"
					else: 
						rprint("Введите либо 1 (Да), либо 2 (Нет).")
						destr = int(input())
				bprint("Построить гистограммы?")
				bprint("Да  - 1")
				bprint("Нет - 2")
				hist = int(input())
				while hist != "exit": 
					if hist == 1: 
						histograms.show_histograms(start_img, new_image)

						hist = "exit"
					elif hist == 2: 
						hist = "exit"
					else: 
						rprint("Введите либо 1 (Да), либо 2 (Нет).")
						hist = int(input())
				

				return 0
				
			
			
		elif todo_main == 2:
			gprint("Введите значениие параметра T (значения по умолчанию 80):")
			t_inp = int(input())
			ext_mes = extract.extraction(image_cont, t_inp)
			step = h_img // 8
			ext_mes_dwm = proc.to_watermark_matrix(ext_mes, step)
			bprint("При встраивании было применено преобразование Арнольда?")
			bprint("1 - Да;")
			bprint("2 - Нет.")
			inv_arn = int(input())
			if inv_arn == 1: 
				gprint("Введите кол-во итераций:")
				iter = int(input())
				h_wat, w_wat = ext_mes_dwm.shape
				ext_mes_dwm = proc.inv_arnold_transformation(ext_mes_dwm, h_wat, iter)
			#for row in ext_mes_dwm: bprint(row)
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
	


