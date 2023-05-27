def check(h_img, w_img, h_wat, w_wat): 
    if h_img != w_img:    return False
    if h_wat != w_wat:    return False
    if h_img != h_wat//8: return False
    return True
