# import required modules
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename,asksaveasfilename
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps
import os
import numpy as np
from imageio import imread
import matplotlib.pyplot as plt

# contrast border thumbnail
root = Tk()
root.title("Simple Nevgative Photo Editor")
root.geometry("1280x640")
# create functions
def selected():
    global img_path, img ,height , width ,ench
    ench = [0,1,1,1,0,0,0]
    img_path = filedialog.askopenfilename(initialdir=os.getcwd()) 
    img = Image.open(img_path)
    img.thumbnail((400, 400))
    #img_enh = img.filter(ImageFilter.BoxBlur(0))
    img_enh = ImageTk.PhotoImage(img)
    canvas2.create_image(600, 210, image=img_enh)
    canvas2.image=img_enh                                                                                                                                                                                                                


#brightness adj
def brightness_choose(x):
    global ench
    ench[1] += x
    if ench[1] > 5:
        ench[1] = 5
    if ench[1] < 0:
        ench[1] = 0
    re_canvas()

#contrast adj       
def contrast_choose(x):
    global ench
    ench[2] += x
    if ench[2] > 5:
        ench[2] = 5
    if ench[2] < 0:
        ench[2] = 0
    re_canvas()

#color adj
def color_choose(x):
    global ench
    ench[3] += x
    if ench[3] > 5:
        ench[3] = 5
    if ench[3] < 0:
        ench[3] = 0
    re_canvas()

#rotate adj
def rotate_choose(x):
    global ench
    ench[4] += x
    re_canvas()


#flip adj
def flip_h():
    global ench
    if ench[5] == 1:
        ench[5] = 0
    elif ench[5] == 0:
        ench[5] = 1
    re_canvas()

#flip adj
def flip_v():
    global ench
    if ench[6] == 1:
        ench[6] = 0
    elif ench[6] == 0:
        ench[6] = 1
    re_canvas()

#filter adj

def filter_choose(x):
    global ench
    if ench[0] != x:
        ench[0] = x
        re_canvas()

#refresh img in canvas when something is changeing
def re_canvas():
    global img ,ench

    img = Image.open(img_path)
    img.thumbnail((400, 400))
    a = np.asarray(img)
    if ench[0] == 0 :
        pass
    elif ench[0] == 1:
        a = image_nevTopos(a, 0.6 , 0.8 , 0.9)
        a = (a * 255 / np.max(a)).astype('uint8')
    elif ench[0] == 2:
        a = image_nevTopos(a, 0.65 , 0.8 , 0.9)
        a = (a * 255 / np.max(a)).astype('uint8')
    elif ench[0] == 3:
        a = image_nevTopos(a, 0.6 , 0.85 , 0.9)
        a = (a * 255 / np.max(a)).astype('uint8')
    elif ench[0] == 4:
        a = image_nevTopos(a, 0.6 , 0.8 , 0.95)
        a = (a * 255 / np.max(a)).astype('uint8')
    elif ench[0] == 5:
        a = image_nevTopos(a, 0.55 , 0.8 , 0.9)
        a = (a * 255 / np.max(a)).astype('uint8')
    elif ench[0] == 6:
        a = image_nevTopos(a, 0.6 , 0.75 , 0.8)
        a = (a * 255 / np.max(a)).astype('uint8')
    elif ench[0] == 7:
        a = image_nevTopos(a, 0.6 , 0.8 , 0.75)
        a = (a * 255 / np.max(a)).astype('uint8')
    #print(a.as_integer_ratio())
    img = Image.fromarray(a, mode="RGB")


    img_enh = ImageEnhance.Brightness(img)
    img1 = img_enh.enhance(ench[1])

    img_enh = ImageEnhance.Contrast(img1)
    img2 = img_enh.enhance(ench[2])

    img_enh = ImageEnhance.Color(img2)
    img3 = img_enh.enhance(ench[3])
    
    img4 = img3.rotate(int(ench[4]), expand = 1)

    if ench[5] == 1:
        img5 = img4.transpose(Image.FLIP_LEFT_RIGHT)
    else:
        img5 = img4
    if ench[6] == 1:
        img6  = img5.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        img6  = img5


    imgg = ImageTk.PhotoImage(img6)
    canvas2.create_image(600, 210, image=imgg)
    canvas2.image=imgg
    print(ench)         

#convert img from nevgative to color  
def image_nevTopos(nev_img,R,G,B):
    image = nev_img
    edge_color = np.mean(np.percentile(image, 99.5, axis=0), axis=0)
    # divide entire image by edge color
    image = np.divide(image, edge_color)

    min_px = np.percentile(image, 0.7)
    image = image - min_px
    image[image<0] = 0

    max_px = np.percentile(image, 99.7)
    image /= max_px
    image[image>1] = 1
    image = 1 - image

    # image corrections
    image[:, :, 0] /= R
    image[:, :, 1] /= G
    image[:, :, 2] /= B

    '''
    original value
    image[:, :, 0] /= 0.6
    image[:, :, 1] /= 0.8
    image[:, :, 2] /= 0.9
    '''
    # auto gamma correction

    x = np.mean(image)
    gamma = np.log(1/2)/np.log(x)
    image = image**gamma

    min_px = np.percentile(image, 0.7)
    image = image - min_px
    image[image<0] = 0
    max_px = np.percentile(image, 99.7)
    image /= max_px
    image[image>1] = 1

    return image

img1 = None
img2 = None
img3 = None
img4 = None
img5 = None
img6 = None
global ench
ench = [0,1,1,1,0,0,0]
    # filter , brightness , contrat ,color,rotate , filp_h , filp_v


def save():
    global img_path, img_enh, img1, img2, img3, img4, img5, img6 ,ench

    #file=None
    ext = img_path.split(".")[-1]
    file=asksaveasfilename(defaultextension =f".{ext}",filetypes=[("jpg file","*.jpg"),("PNG file","*.png"),("All Files","*.*")])
    if file: 
            img = Image.open(img_path)
            a = np.asarray(img)
            if ench[0] == 0 :
                pass
            elif ench[0] == 1:
                a = image_nevTopos(a, 0.6 , 0.8 , 0.9)
                a = (a * 255 / np.max(a)).astype('uint8')
            elif ench[0] == 2:
                a = image_nevTopos(a, 0.65 , 0.8 , 0.9)
                a = (a * 255 / np.max(a)).astype('uint8')
            elif ench[0] == 3:
                a = image_nevTopos(a, 0.6 , 0.85 , 0.9)
                a = (a * 255 / np.max(a)).astype('uint8')
            elif ench[0] == 4:
                a = image_nevTopos(a, 0.6 , 0.8 , 0.95)
                a = (a * 255 / np.max(a)).astype('uint8')
            elif ench[0] == 5:
                a = image_nevTopos(a, 0.55 , 0.8 , 0.9)
                a = (a * 255 / np.max(a)).astype('uint8')
            elif ench[0] == 6:
                a = image_nevTopos(a, 0.6 , 0.75 , 0.8)
                a = (a * 255 / np.max(a)).astype('uint8')
            elif ench[0] == 7:
                a = image_nevTopos(a, 0.6 , 0.8 , 0.75)
                a = (a * 255 / np.max(a)).astype('uint8')
            #print(a.as_integer_ratio())
            img = Image.fromarray(a, mode="RGB")

            img_enh = ImageEnhance.Brightness(img)
            img1 = img_enh.enhance(ench[1])

            img_enh = ImageEnhance.Contrast(img1)
            img2 = img_enh.enhance(ench[2])

            img_enh = ImageEnhance.Color(img2)
            img3 = img_enh.enhance(ench[3])
            
            img4 = img3.rotate(int(ench[4]), expand = 1)

            if ench[5] == 1:
                img5 = img4.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                img5 = img4
            if ench[6] == 1:
                img6 = img5.transpose(Image.FLIP_TOP_BOTTOM)
            else:
                img6 = img5

            img6.save(file)
            print('save done')
            

        
# brightness

bright = Label(root, text="Brightness:", font=("ariel 17 bold"))
bright.place(x=8, y=8)
br_nev = Button(root, text="-", width=3 ,font=('ariel 15 bold'), relief=GROOVE, command= lambda:brightness_choose(-0.1))
br_nev.place(x=150, y=8)
br_pos = Button(root, text="+", width=3, font=('ariel 15 bold'), relief=GROOVE, command= lambda:brightness_choose(0.1))
br_pos.place(x=200, y=8)

#contrast
contra = Label(root, text="Contrast:", font=("ariel 17 bold"))
contra.place(x=35, y=58)
con_nev = Button(root, text="-", width=3 ,font=('ariel 15 bold'), relief=GROOVE, command= lambda:contrast_choose(-0.1))
con_nev.place(x=150, y=58)
con_pos = Button(root, text="+", width=3, font=('ariel 15 bold'), relief=GROOVE, command= lambda:contrast_choose(0.1))
con_pos.place(x=200, y=58)

#color
col = Label(root, text="Color:", font=("ariel 17 bold"))
col.place(x=70, y=108)
col_nev = Button(root, text="-", width=3 ,font=('ariel 15 bold'), relief=GROOVE, command= lambda:color_choose(-0.1))
col_nev.place(x=150, y=108)
col_pos = Button(root, text="+", width=3, font=('ariel 15 bold'), relief=GROOVE, command= lambda:color_choose(0.1))
col_pos.place(x=200, y=108)


# rotate
rotate = Label(root, text="Rotate:", font=("ariel 17 bold"))
rotate.place(x=370, y=8)
rotate_nev = Button(root, text="<<", width=3 ,font=('ariel 15 bold'), relief=GROOVE, command= lambda:rotate_choose(90))
rotate_nev.place(x=460, y=8)
rotate_pos = Button(root, text=">>", width=3, font=('ariel 15 bold'), relief=GROOVE, command= lambda:rotate_choose(-90))
rotate_pos.place(x=510, y=8)


#flip
flip = Label(root, text="Flip:", font=("ariel 17 bold"))
flip.place(x=400, y=50)
rotate_nev = Button(root, text="H", width=3 ,font=('ariel 15 bold'), relief=GROOVE, command= flip_h)
rotate_nev.place(x=460, y=50)
rotate_pos = Button(root, text="V", width=3, font=('ariel 15 bold'), relief=GROOVE, command= flip_v)
rotate_pos.place(x=510, y=50)

# filter
fil = Label(root, text="Filter:", font=("ariel 17 bold"))
fil.place(x=385, y=108)
filter_none = Button(root, text="None", width=3 ,font=('ariel 15 bold'), relief=GROOVE, command= lambda:filter_choose(0))
filter_none.place(x=460, y=108)
filter_1 = Button(root, text="1", width=3, font=('ariel 15 bold'), relief=GROOVE, command= lambda:filter_choose(1))
filter_1.place(x=510, y=108)
filter_2 = Button(root, text="2", width=3, font=('ariel 15 bold'), relief=GROOVE, command= lambda:filter_choose(2))
filter_2.place(x=560, y=108)
filter_3 = Button(root, text="3", width=3, font=('ariel 15 bold'), relief=GROOVE, command= lambda:filter_choose(3))
filter_3.place(x=610, y=108)
filter_4 = Button(root, text="4", width=3, font=('ariel 15 bold'), relief=GROOVE, command= lambda:filter_choose(4))
filter_4.place(x=660, y=108)
filter_5 = Button(root, text="5", width=3, font=('ariel 15 bold'), relief=GROOVE, command= lambda:filter_choose(5))
filter_5.place(x=710, y=108)
filter_6 = Button(root, text="6", width=3, font=('ariel 15 bold'), relief=GROOVE, command= lambda:filter_choose(6))
filter_6.place(x=760, y=108)
filter_7 = Button(root, text="7", width=3, font=('ariel 15 bold'), relief=GROOVE, command= lambda:filter_choose(7))
filter_7.place(x=810, y=108)


# create canvas to display image
canvas2 = Canvas(root, width="1240", height="420", relief=RIDGE, bd=2)
canvas2.place(x=15, y=150)
# create buttons


btn1 = Button(root, text="Select Image", font=('ariel 15 bold'), relief=GROOVE, command=selected)
btn1.place(x=100, y=595)
btn2 = Button(root, text="Save", width=12, font=('ariel 15 bold'), relief=GROOVE, command=save)
btn2.place(x=280, y=595)
btn3 = Button(root, text="Exit", width=12, font=('ariel 15 bold'), relief=GROOVE, command=root.destroy)
btn3.place(x=460, y=595)
root.mainloop()