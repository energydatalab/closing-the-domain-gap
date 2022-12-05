class Dataset():
    def __init__(self, img_txt, lbl_txt, out_dir, img_txt_val, lbl_txt_val, img_txt_supplement=None, lbl_txt_supplement=None):
        self.img_txt = img_txt
        self.lbl_txt = lbl_txt
        self.out_dir = out_dir
        self.img_txt_val = img_txt_val
        self.lbl_txt_val = lbl_txt_val
        self.img_txt_supplement = img_txt_supplement
        self.lbl_txt_supplement = lbl_txt_supplement


    def get_img_txt(self):
        return self.img_txt
    
    def get_lbl_txt(self):
        return self.lbl_txt
    
    def get_out_dir(self):
        return self.out_dir
    
    def get_img_txt_val(self):
        return self.img_txt_val
    
    def get_lbl_txt_val(self):
        return self.lbl_txt_val
    
    def get_img_txt_supplement(self):
        return self.img_txt_supplement
    
    def get_lbl_txt_supplement(self):
        return self.lbl_txt_supplement