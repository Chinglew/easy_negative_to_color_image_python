# import required modules
from cProfile import label
from doctest import master
from pydoc import text
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
from tkinter.filedialog import askopenfilename,asksaveasfilename
from turtle import screensize, width
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps
import os
import numpy as np
from imageio import imread
import matplotlib.pyplot as plt

# contrast border thumbnail
#tkinter
root = Tk()
root.title("Simple Nevgative Photo Editor")
#setting window size
width=1000
height=680
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
x = (screenwidth / 2) - (width / 2)
y = (screenheight / 2 ) - (height / 2)
root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
root.resizable(width=False,height=False)
root.configure(bg='#3E56B8')

#logo title
logo_title = PhotoImage(file='img/logo.png')
root.iconphoto(False,logo_title)
# create functions
def selected():
    global img_path, img ,height , width ,ench
    ench = [0,1,1,1,0,0,0]
    img_path = filedialog.askopenfilename(initialdir=os.getcwd()) 
    img = Image.open(img_path)
    img.thumbnail((480, 480))
    #img_enh = img.filter(ImageFilter.BoxBlur(0))
    img_enh = ImageTk.PhotoImage(img)
    canvas2.create_image(250, 280, image=img_enh)
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
    img.thumbnail((480, 480))
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
    canvas2.create_image(250, 280, image=imgg)
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
            

#-----------------------------------------------------#
Ui_blue = '#3E56B8'
#btn addfile , save , exit #
logo = ImageTk.PhotoImage(Image.open('img/logo.png'))
label = Label(root,image= logo,bg=Ui_blue)
label.place(x=50,y=20)

#------------------------------------------------------#
img_choose_btn = PhotoImage(file='img/choose_img.png')
btn_choose_img = Button(root,image=img_choose_btn,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue,command=selected)
btn_choose_img.place(x=52, y=180)

#------------------------------------------------------#




#-----------------------------------------------------#

# brightness
img_label_Brightness = ImageTk.PhotoImage(Image.open('img/label_bright.png'))
label_brightness = Label(root,image=img_label_Brightness,bg=Ui_blue)
label_brightness.place(x=52,y=240)

img_minus_btn = PhotoImage(file='img/minus_btn.png')
btn_minus1 = Button(root,image=img_minus_btn,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue, relief=GROOVE,command=lambda:brightness_choose(-0.1))
btn_minus1.place(x=200, y=240)

img_plus_btn = PhotoImage(file='img/plus_btn.png')
btn_plus1 = Button(root,image=img_plus_btn,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue, relief=GROOVE,command=lambda:brightness_choose(0.1))
btn_plus1.place(x=245, y=240)


#contrast
img_label_Contrast = ImageTk.PhotoImage(Image.open('img/label_Contrast.png'))
label_Contrast  = Label(root,image=img_label_Contrast,bg=Ui_blue)
label_Contrast.place(x=52,y=285)

img_minus_btn2 = PhotoImage(file='img/minus_btn.png')
btn_minus2 = Button(root,image=img_minus_btn2,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue, relief=GROOVE,command=lambda:contrast_choose(-0.1))
btn_minus2.place(x=200, y=285)

img_plus_btn2 = PhotoImage(file='img/plus_btn.png')
btn_plus2 = Button(root,image=img_plus_btn2,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue, relief=GROOVE,command=lambda:contrast_choose(0.1))
btn_plus2.place(x=245, y=285)


#color
img_label_Color = ImageTk.PhotoImage(Image.open('img/label_Color.png'))
label_Color = Label(root,image=img_label_Color,bg=Ui_blue)
label_Color.place(x=52,y=330)

img_minus_btn3 = PhotoImage(file='img/minus_btn.png')
btn_minus3 = Button(root,image=img_minus_btn3,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue, relief=GROOVE,command=lambda:color_choose(-0.1))
btn_minus3.place(x=200, y=330)

img_plus_btn3 = PhotoImage(file='img/plus_btn.png')
btn_plus3 = Button(root,image=img_plus_btn3,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue, relief=GROOVE,command=lambda:color_choose(0.1))
btn_plus3.place(x=245, y=330)



# filter
Fliter_logo = ImageTk.PhotoImage(Image.open('img/Filter.png'))
Filter = Label(root,image=Fliter_logo,bg=Ui_blue)
Filter.place(x=45,y=380)


img_label_default = ImageTk.PhotoImage(Image.open('img/label_Default.png'))
btn_default = Button(root,image=img_label_default,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue,relief=GROOVE, command= lambda:filter_choose(0))
btn_default.place(x=52,y=450)

img_btn_num1 = ImageTk.PhotoImage(Image.open('img/btn_num1.png'))
btn_num1 = Button(root,image=img_btn_num1,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue,relief=GROOVE, command= lambda:filter_choose(1))
btn_num1.place(x=200,y=450)

img_btn_num2 = ImageTk.PhotoImage(Image.open('img/btn_num2.png'))
btn_num2 = Button(root,image=img_btn_num2,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue,relief=GROOVE, command= lambda:filter_choose(2))
btn_num2.place(x=245,y=450)

img_btn_num3 = ImageTk.PhotoImage(Image.open('img/btn_num3.png'))
btn_num3 = Button(root,image=img_btn_num3,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue,relief=GROOVE, command= lambda:filter_choose(3))
btn_num3.place(x=290,y=450)

img_btn_num4 = ImageTk.PhotoImage(Image.open('img/btn_num4.png'))
btn_num4 = Button(root,image=img_btn_num4,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue,relief=GROOVE, command= lambda:filter_choose(4))
btn_num4.place(x=335,y=450)

img_btn_num5= ImageTk.PhotoImage(Image.open('img/btn_num5.png'))
btn_num5 = Button(root,image=img_btn_num5,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue,relief=GROOVE, command= lambda:filter_choose(5))
btn_num5.place(x=200,y=500)

img_btn_num6= ImageTk.PhotoImage(Image.open('img/btn_num6.png'))
btn_num6 = Button(root,image=img_btn_num6,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue,relief=GROOVE, command= lambda:filter_choose(6))
btn_num6.place(x=245,y=500)

img_btn_num7= ImageTk.PhotoImage(Image.open('img/btn_num7.png'))
btn_num7 = Button(root,image=img_btn_num7,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue,relief=GROOVE, command= lambda:filter_choose(7))
btn_num7.place(x=290,y=500)



#export btn
img_export_btn = PhotoImage(file='img/export_img.png')
btn_export_img = Button(root,image=img_export_btn,borderwidth=0,bg=Ui_blue,relief=GROOVE,activebackground=Ui_blue,command=save)
btn_export_img.place(x=52, y=560)

#exit btn
img_exit_btn = PhotoImage(file='img/exit_img.png')
btn_exit_img = Button(root,image=img_exit_btn,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue,relief=GROOVE, command=root.destroy)
btn_exit_img.place(x=180, y=560)



# create canvas to display image
text_preview = Label(root, text='Preview',font=('arial 17 bold'),bg='#3E56B8',fg='#FFFFFF')
text_preview.place(x=448, y=20)
canvas2 = Canvas(root, width="500", height="550", relief=RIDGE)
canvas2.place(x=450, y=60)


# rotate

img_rotate1_btn = PhotoImage(file='img/btn_rotate_left.png')
rotate1_btn = Button(root,image=img_rotate1_btn,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue,relief=GROOVE, command= lambda:rotate_choose(90))
rotate1_btn.place(x=720, y=620)

img_rotate2_btn = PhotoImage(file='img/btn_rotate_right.png')
rotate2_btn = Button(root,image=img_rotate2_btn,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue,relief=GROOVE, command= lambda:rotate_choose(-90))
rotate2_btn.place(x=760, y=620)



#flip
img_flip1_btn = PhotoImage(file='img/btn_flip_left.png')
flip1_btn = Button(root,image=img_flip1_btn,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue,relief=GROOVE, command= flip_h)
flip1_btn.place(x=620, y=620)


img_flip2_btn = PhotoImage(file='img/btn_flip_right.png')
flip2_btn = Button(root,image=img_flip2_btn,borderwidth=0,bg=Ui_blue,activebackground=Ui_blue,relief=GROOVE, command= flip_v)
flip2_btn.place(x=660, y=620)
#rotate_pos = Button(root, text="V", width=3, font=('ariel 15 bold'), relief=GROOVE, command= flip_v)
#rotate_pos.place(x=510, y=50)


root.mainloop()