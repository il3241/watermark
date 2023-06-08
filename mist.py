from PIL import Image, ImageFilter
import extract

def save_img(
		image : Image,
		name : str):
	image.save("out_img/" + name+".PNG", "PNG")


def to_list(matrix): 
	row = []
	for j in range(len(matrix)): 
		for i in range(len(matrix[0])): 
			if matrix[j][i] == 0.0 or matrix[j][i] == 0:
				row.append(0)
			else: 
				row.append(1)
	return row

def CHECK(
		inp_mes : list,
		ext_mes : list) -> float: 
	B_e = 0

	for i in range(len(inp_mes)):
		if inp_mes[i] != ext_mes[i]:
			B_e += 1
	BER = B_e / len(inp_mes)

	return BER



def blur_and_check(
		t_inp : int,
        input_bin : list,
        stego_img : Image) -> float: 
    stego_filtred_img = stego_img.filter(ImageFilter.BLUR)
    ext_mes_bin = extract.extraction(stego_filtred_img, t_inp)
    
    BER = CHECK(input_bin, ext_mes_bin)
    
    save_img(stego_filtred_img, "1")


    return BER

def sharpen_and_check(
		t_inp : int,
        input_bin : list,
        stego_img : Image) -> float: 
    stego_filtred_img = stego_img.filter(ImageFilter.SHARPEN)
    ext_mes_bin = extract.extraction(stego_filtred_img, t_inp)
    BER = CHECK(input_bin, ext_mes_bin)
    save_img(stego_filtred_img, "2")
    

    return BER

def smooth_and_check(
		t_inp : int,
        input_bin : list,
        stego_img : Image) -> float: 
    stego_filtred_img = stego_img.filter(ImageFilter.SMOOTH)
    ext_mes_bin = extract.extraction(stego_filtred_img, t_inp)
    
    BER = CHECK(input_bin, ext_mes_bin)
    save_img(stego_filtred_img , "4")
    
    return BER

def contour_and_check(
        t_inp        : int,
        input_bin : list,
        stego_img : Image) -> float: 
    stego_filtred_img = stego_img.filter(ImageFilter.CONTOUR)
    ext_mes_bin = extract.extraction(stego_filtred_img, t_inp)
    
    BER = CHECK(input_bin, ext_mes_bin)
    save_img(stego_filtred_img , '3')
    
    return BER

def jpg_scale_90( 
		t_inp : int,
		input_bin : list,
        stego_img : Image) -> float: 
	stego_img.save("out_img/compressed_image_90.jpg", format="JPEG", quality=90)
	stego_filtred_img = Image.open("out_img/compressed_image_90.jpg")
	ext_mes_bin = extract.extraction(stego_filtred_img, t_inp)
	BER = CHECK(input_bin, ext_mes_bin)
	return BER


def jpg_scale_60( 
		t_inp : int,
		input_bin : list,
        stego_img : Image) -> float: 
	stego_img.save("out_img/compressed_image_60.jpg", format="JPEG", quality=60)
	stego_filtred_img = Image.open("out_img/compressed_image_60.jpg")
	ext_mes_bin = extract.extraction(stego_filtred_img, t_inp)
	
	BER = CHECK(input_bin, ext_mes_bin)
	return BER

def jpg_scale_20( 
		t_inp : int,
		input_bin : list,
        stego_img : Image) -> float: 
	stego_img.save("out_img/compressed_image_20.jpg", format="JPEG", quality=20)
	stego_filtred_img = Image.open("out_img/compressed_image_20.jpg")
	ext_mes_bin = extract.extraction(stego_filtred_img, t_inp)
	BER = CHECK(input_bin, ext_mes_bin)
	return BER
