# Python program to read 
# image using PIL module
# and prepare an atari
# antic5 charset and screen data

from tkinter import filedialog
from tkinter import ttk
import configparser
import os.path
from tkinter import *
from PIL import Image
import copy

a8_palette = [	( 45, 45, 45),( 59, 59, 59),( 73, 73, 73),( 87, 87, 87),(101,101,101),(115,115,115),(129,129,129),(143,143,143),
				(157,157,157),(171,171,171),(185,185,185),(199,199,199),(213,213,213),(227,227,227),(241,241,241),(255,255,255),
				( 92, 35,  0),(106, 49,  0),(120, 63,  0),(134, 77, 10),(148, 91, 24),(162,105, 38),(176,119, 52),(190,133, 66),
				(204,147, 80),(218,161, 94),(232,175,108),(246,189,122),(255,203,136),(255,217,150),(255,231,164),(255,245,178),
				(105, 20,  9),(119, 34, 23),(133, 48, 37),(147, 62, 51),(161, 76, 65),(175, 90, 79),(189,104, 93),(203,118,107),
				(217,132,121),(231,146,135),(245,160,149),(255,174,163),(255,188,177),(255,202,191),(255,216,205),(255,230,219),
				(108, 10, 56),(122, 24, 70),(136, 38, 84),(150, 52, 98),(164, 66,112),(178, 80,126),(192, 94,140),(206,108,154),
				(220,122,168),(234,136,182),(248,150,196),(255,164,210),(255,178,224),(255,192,238),(255,206,252),(255,220,255),
				(100,  5,101),(114, 19,115),(128, 33,129),(142, 47,143),(156, 61,157),(170, 75,171),(184, 89,185),(198,103,199),
				(212,117,213),(226,131,227),(240,145,241),(254,159,255),(255,173,255),(255,187,255),(255,201,255),(255,215,255),
				( 82,  7,137),( 96, 21,151),(110, 35,165),(124, 49,179),(138, 63,193),(152, 77,207),(166, 91,221),(180,105,235),
				(194,119,249),(208,133,255),(222,147,255),(236,161,255),(250,175,255),(255,189,255),(255,203,255),(255,217,255),
				( 58, 16,156),( 72, 30,170),( 86, 44,184),(100, 58,198),(114, 72,212),(128, 86,226),(142,100,240),(156,114,254),
				(170,128,255),(184,142,255),(198,156,255),(212,170,255),(226,184,255),(240,198,255),(254,212,255),(255,226,255),
				( 31, 30,156),( 45, 44,170),( 59, 58,184),( 73, 72,198),( 87, 86,212),(101,100,226),(115,114,240),(129,128,254),
				(143,142,255),(157,156,255),(171,170,255),(185,184,255),(199,198,255),(213,212,255),(227,226,255),(241,240,255),
				(  7, 46,137),( 21, 60,151),( 35, 74,165),( 49, 88,179),( 63,102,193),( 77,116,207),( 91,130,221),(105,144,235),
				(119,158,249),(133,172,255),(147,186,255),(161,200,255),(175,214,255),(189,228,255),(203,242,255),(217,255,255),
				(  0, 62,101),(  3, 76,115),( 17, 90,129),( 31,104,143),( 45,118,157),( 59,132,171),( 73,146,185),( 87,160,199),
				(101,174,213),(115,188,227),(129,202,241),(143,216,255),(157,230,255),(171,244,255),(185,255,255),(199,255,255),
				(  0, 75, 56),(  0, 89, 70),(  9,103, 84),( 23,117, 98),( 37,131,112),( 51,145,126),( 65,159,140),( 79,173,154),
				( 93,187,168),(107,201,182),(121,215,196),(135,229,210),(149,243,224),(163,255,238),(177,255,252),(191,255,255),
				(  0, 82,  9),(  0, 96, 23),( 12,110, 37),( 26,124, 51),( 40,138, 65),( 54,152, 79),( 68,166, 93),( 82,180,107),
				( 96,194,121),(110,208,135),(124,222,149),(138,236,163),(152,250,177),(166,255,191),(180,255,205),(194,255,219),
				(  0, 83,  0),( 11, 97,  0),( 25,111,  0),( 39,125, 10),( 53,139, 24),( 67,153, 38),( 81,167, 52),( 95,181, 66),
				(109,195, 80),(123,209, 94),(137,223,108),(151,237,122),(165,251,136),(179,255,150),(193,255,164),(207,255,178),
				( 19, 78,  0),( 33, 92,  0),( 47,106,  0),( 61,120,  0),( 75,134,  0),( 89,148, 11),(103,162, 25),(117,176, 39),
				(131,190, 53),(145,204, 67),(159,218, 81),(173,232, 95),(187,246,109),(201,255,123),(215,255,137),(229,255,151),
				( 45, 67,  0),( 59, 81,  0),( 73, 95,  0),( 87,109,  0),(101,123,  0),(115,137,  1),(129,151, 15),(143,165, 29),
				(157,179, 43),(171,193, 57),(185,207, 71),(199,221, 85),(213,235, 99),(227,249,113),(241,255,127),(255,255,141),
				( 70, 51,  0),( 84, 65,  0),( 98, 79,  0),(112, 93,  0),(126,107,  0),(140,121, 11),(154,135, 25),(168,149, 39),
				(182,163, 53),(196,177, 67),(210,191, 81),(224,205, 95),(238,219,109),(252,233,123),(255,247,137),(255,255,151) ]

def find_nearest_color(r,g,b):
    min = 255*255*255*255 # impossible max value
    min_index = -1
    for i in range(256):
        rp,gp,bp = a8_palette[i]
        distance = abs((r*r+g*g+b*b) - (rp*rp+gp*gp+bp*bp))
        if distance < min:
            min = distance
            min_index = i
    return min_index

# get configuration with previous working directory and parameters
config = configparser.RawConfigParser()

def init():
    'Create a configuration file if does not exist'
    config.add_section('InputImage')
    config.set('InputImage', 'Directory', './')
    config.set('InputImage', 'Filename', '*.gif')
    config.add_section('Output')
    config.set('Output', 'AnticMode', '5')
    with open('image2antic.cfg', 'w') as output:
        config.write(output)

#------------------------------------------------------------------------
# check if dataUpdate.cfg exist if not create it   
if not os.path.exists('image2antic.cfg'):
    print("Can't find 'image2antic.cfg', create a new configuration file") 
    init()

# Read configurations using section and key to get the value
config.read('image2antic.cfg')
input_directory = config.get('InputImage', 'Directory')
input_filename = config.get('InputImage', 'Filename')
input_directory = config.get('Output', 'AnticMode')

#------------------------------------------------------------------------




#------------------------------------------------------------
def update(section, key, value):
    #Update config using section key and the value to change
    #call this when you want to update a value in configuation file
    # with some changes you can save many values in many sections
    config.set(section, key, value )
    with open('image2antic.cfg', 'w') as output:
        config.write(output)
#------------------------------------------------------------

def process_cc65_code():
    print("processing...")
    antic_target_modes = {
        "4" : {"colors" : 4, "display_mode" : "text", "columns" : 40, "lines" : 24, "char_width" : 4, "char_height" : 8},
        "5" : {"colors" : 4, "display_mode" : "text", "columns" : 40, "lines" : 12, "char_width" : 4, "char_height" : 8}
    }
    antic_target = "5"
    # img.show() 
    print("/************************************************")
    print("** Generated with image2antic.py               **")
    print("** Kobi Tyrkel                                 **")
    print("** April 23, 2020                              **")
    print("** " + img.format) 
    print("** " + img.mode)
    # prints image size and channel
    w, h = img.size
    print('** width:  ', w)
    print('** height: ', h)
    mode_to_bpp = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}
    d = mode_to_bpp[img.mode]
    print('** depth: ' + str(d))
    print("************************************************/")
    print("#include <atari.h>")
    print("#include <string.h>")
    print("")
    print("#define SCREEN_MEM		0x7000")
    print("#define DLIST_MEM		0x6C00	// aligned to 1K")
    print("#define CHARSET0_MEM 	0x5000	// aligned to 1K")
    print("#define CHARSET1_MEM 	0x5400	// aligned to 1K")
    print("#define CHARSET2_MEM 	0x5800	// aligned to 1K")
    print("#define CHARSET3_MEM 	0x5C00	// aligned to 1K")
    print("#define CHARSET4_MEM 	0x6000	// aligned to 1K")
    
    print("")
    # display the image pixel colors on the screen
    rgb_im = img.convert('RGB')
    for y in range(h):
        for x in range(w):
            r, g, b = rgb_im.getpixel((x, y))
            ch = round(((r*512+g*64+b*8)/8))
            ch = " " if (ch == 0) else ch
            #print(ch, end = "")
        #print(" ")

    # arrange an array of ANTIC 4 COLOR TEXT mode 4x8 tiles
    tiles = {}
    for j in range(round(h/8)):
        for i in range (round(w / 4)):
            for y in range (8):
                tiles[i,j,y] = 0
                for x in range (4):
                    r, g, b = rgb_im.getpixel((i*4+x, j*8+y))
                    pixel = round(((r*8+g*8+b*8)/640))
                    double_bit_pixel = 2 if (pixel == 5) else 1 if (pixel == 7) else pixel
                    tiles[i,j,y] = tiles[i,j,y] + (64 if x == 0 else 16 if x == 1 else 4 if x == 2 else 1) * double_bit_pixel
    # group distinct chars and create screen char map                
    chars = {}
    screen = {}
    temp_char = {}
    charset_index = 0
    chars_index = 0
    chars_count = 0
    chars_reuse = 0
    global charset_dli_change
    charset_dli_change = []
    charset_dli_change.append(0)
    global a8_palette
    for y in range(8):
        temp_char[y] = 0
    chars[charset_index, chars_index] = copy.deepcopy(temp_char)
    chars_index = chars_index + 1
    for j in range(round(h/8)): 
        if (chars_index > 87):
            charset_index = charset_index + 1
            chars_index = 0
            for y in range(8):
                temp_char[y] = 0
            chars[charset_index, chars_index] = copy.deepcopy(temp_char)
            chars_index = chars_index + 1
            charset_dli_change.append(j - 1)
        for i in range (antic_target_modes[antic_target]["columns"]):
            if (i < round(w/4)):
                for y in range (8):
                    temp_char[y] = 0
                    for x in range (4):
                        r, g, b = rgb_im.getpixel((i*4+x, j*8+y))
                        #if (r,g,b in rgb_colors):
                        pixel = rgb_colors.index((r,g,b))
                            
                        double_bit_pixel = 2 if (pixel == 5) else 1 if (pixel == 7) else pixel
                        temp_char[y] = temp_char[y] + (64 if x == 0 else 16 if x == 1 else 4 if x == 2 else 1) * pixel #double_bit_pixel
                char_exists = False
                for char in chars:
                    if char[0] == charset_index and chars[char] == temp_char:
                        char_exists = True
                        chars_reuse = chars_reuse + 1
                        screen[i,j] = char[1]
                if (not char_exists):
                    chars_count = chars_count + 1
                    chars[charset_index, chars_index] = copy.deepcopy(temp_char)
                    screen[i,j] = chars_index
                    chars_index = chars_index + 1
            else:
                screen[i,j] = 0
    # print the charsets and screen data formatted for cc65
    charsets_size = []
    for charset_number in range(charset_index + 1):
        chars_in_set = 0
        for char in chars:
            if (char[0] == charset_number):
                chars_in_set = chars_in_set + 1
        print ("// antic 5 chars data")
        print ("unsigned char charset_"+str(charset_number)+"_data[] = {")
        for char in range(chars_in_set):
            for byte in range(8): #chars[charset_number, char]:
                print (chars[charset_number, char][byte], end = ", ")
            print ("")
        print ("}; // chars in set:", chars_in_set)
        charsets_size.append(chars_in_set)
    print ("// antic 5 screen data")
    print ("unsigned char screen_data[] = {")
    for j in range(antic_target_modes[antic_target]["lines"]):
        for i in range (antic_target_modes[antic_target]["columns"]):
            print(screen[i, j], end=", ")
        print("")
    print("};")
    print("")
    print("// CHARSET DLI CHANGES IN LINES: " + str(charset_dli_change))
    print("unsigned char antic4_display_list[] = {")
    print("	DL_BLK8,")
    print("	DL_BLK8,")
    print("	DL_DLI(DL_BLK8),")
    print("	DL_LMS(DL_CHR40x16x4),")
    print("	0x00,")
    print("	SCREEN_MEM >> 8,")
    for i in range(1,12):
        if i in charset_dli_change:
            print("	DL_DLI(DL_CHR40x16x4),")
        else:
            print("	DL_CHR40x16x4,")
    print("	DL_JVB,")
    print("	0x00,")
    print("};")
    print("")
    print("")
    print("void erase_sprite(void);")
    print("void update_sprite(void);")
    print("void draw_sprite(void);")
    print("void handle_input (void);")
    print("")
    print("void init_strings_length(void);")
    print("void string_index_to_mem(unsigned char, unsigned int);")
    print("void wait_for_vblank(void);")
    print("void setup_dli(void);")
    global dli_count
    
    dli_count = len(charset_dli_change)
    for i in range(0,dli_count):
        print('void dli_routine_'+str(i)+'(void);')
    print("")
    print("void main(void)")
    print("{")
    print("	// CREATE SCREEN")
    print("	memcpy((void*) DLIST_MEM,antic4_display_list,sizeof(antic4_display_list));")
    print("	OS.sdlst=(void*)DLIST_MEM;")
    print("")
    print("	// CREATE CHARSET")
    #print("	//memcpy((void*)CHARSET_MEM, 0xE000, 0x400);")
    for i in range(charset_index+1):
        print("	memcpy((void*)(CHARSET"+str(i)+"_MEM), charset_"+str(i)+"_data, 8*"+str(charsets_size[i])+");")
    #print("	memcpy((void*)(CHARSET0_MEM), charset_0_data, 8*97);")
    #print("	memcpy((void*)(CHARSET1_MEM), charset_1_data, 8*50);")
    #print("	//memcpy((void*)(CHARSET1_MEM + 8 * 97), my_chars, 26*8);")
    print("	OS.chbas = CHARSET0_MEM >> 8;")
    print("	memcpy((void*)(SCREEN_MEM), screen_data, 40*12);")
    print("")
    print("	// SET COLORS")
    print("	OS.color1 = " + str(my_a8_palette[0]) + ";") #0xEA;")
    print("	OS.color2 = " + str(my_a8_palette[1]) + ";") # = 0x22;")
    print("	OS.color3 = " + str(my_a8_palette[2]) + ";") #0xFF;")
    print("	OS.color4 = " + str(my_a8_palette[3]) + ";") #0x00;")
    print("")
    print("	setup_dli();")
    print("	wait_for_vblank();")
    print("	ANTIC.nmien = NMIEN_DLI | NMIEN_VBI; ")
    print("")
    print("    OS.sdmctl = 0x3E;")
    print("	// GAME LOOP")
    print("	while (1) {")
    print("		wait_for_vblank();")
    print("		erase_sprite();")
    print("		handle_input();")
    print("		update_sprite();")
    print("		draw_sprite();")
    print("	};")
    print("}")
    print("")
    print('void wait_for_vblank(void)')
    print('{')
    print('    asm("lda $14");')
    print('wvb:')
    print('    asm("cmp $14");')
    print('    asm("beq %g", wvb);')
    print('} ')

    for i in range(0,dli_count):
        print('void dli_routine_'+str(i)+'(void)')
        print('{')
        print('    asm("pha");')
        print('    asm("tya");')
        print('    asm("pha");')
        print('    asm("tya");')
        print('    asm("pha");')
        print('    ANTIC.wsync = 1;')
        print('    ANTIC.chbase = CHARSET'+str(i)+'_MEM >> 8;')
        if (i < dli_count-1):
            dli_update = i+1
        else:
            dli_update = 0
        print('    OS.vdslst = &dli_routine_'+str(dli_update)+';')
        print('    asm("pla");')
        print('    asm("tay");')
        print('    asm("pla");')
        print('    asm("tax");')
        print('    asm("pla");')
        print('    asm("rti");')
        print('}')

    print('void setup_dli(void)')
    print('{')
    print('	wait_for_vblank();')
    print('    OS.vdslst = &dli_routine_0;')
    print('}')
    print('void erase_sprite() {')
    print('	// ERASE SPRITE')
    print('}')
    print('void update_sprite() {')
    print('	// TODO: UPDATE SPRITE')
    print('}')
    print('void draw_sprite() {')
    print('	// TODO: DRAW SPRITE')
    print('}')
    print('void handle_input (void)')
    print('{')
    print(' // TODO: HANDLE INPUT')
    print('}')

# main loop handler class
class Root(Tk):
    # show working dialog with a file browse button
    def __init__(self):
        super(Root, self).__init__()
        self.title("Image2Antic")

        self.minsize(640, 400)
        #self.wm_iconbitmap('icon.ico')
 
    # label frame for input file settings
        self.labelFrame = ttk.LabelFrame(self, text = "Input File")
        self.labelFrame.grid(column = 1, row = 3, padx = 20, pady = 20)
        self.button()
        self.imageParamsLabel = ttk.Label(self.labelFrame, text = "")
        self.imageParamsLabel.grid(column = 1, row = 1)
 
    # label frame for output file settings
        self.labelFrame1 = ttk.LabelFrame(self, text = "Output File")
        self.labelFrame1.grid(column = 1, row = 10, padx = 20, pady = 20)
        self.button1()
        self.imageParamsLabel1 = ttk.Label(self.labelFrame1, text = "")
        self.imageParamsLabel1.grid(column = 1, row = 1)
 
    # browse button to open a file browser on click
    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Browse",command = self.fileDialog)
        self.button.grid(column = 2, row = 1)
        
    # browse button to begin output process
    def button1(self):
        self.button1 = ttk.Button(self.labelFrame1, text = "Process",command = process_cc65_code)
        self.button1.grid(column = 2, row = 1)
        
    # when invoked, open the image and extract information on it
    def imageViewer(self):
        global input_directory
        global input_filename
        global img
        global my_a8_palette
        global rgb_colors
        
        img = Image.open(input_directory+'/'+input_filename) 
        w, h = img.size
        mode_to_bpp = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}
        d = mode_to_bpp[img.mode]
        px = img.load()
        colors = []
        for j in range(h):
            for i in range(w):
                if (px[i, j] not in colors):
                    colors.append(px[i,j])
        rgb_im = img.convert('RGB')
        rgb_colors = []
        my_a8_palette = []
        for j in range(h):
            for i in range(w):
                r, g, b = rgb_im.getpixel((i, j))
                if ((r,g,b) not in rgb_colors):
                    rgb_colors.append((r,g,b))
                    my_a8_palette.append(find_nearest_color(r,g,b))
        print(rgb_colors)
        self.imageParamsLabel.configure(text = "Image Format: "+ img.format+"\nwidth:  "+str( w) + "\nheight: "+str(h)+"\ndepth: "+str(d) + "\nNumber of colors: " + str(len(colors)) + str(colors) + "\nPalette (RGB): " + str(rgb_colors) + "\nPalette (A8): " + str(my_a8_palette))
        img.show()
        
    # file dialog for choosing our image 2 antic file
    def fileDialog(self):
        global input_directory
        global input_filename
        self.filename =  filedialog.askopenfilename(initialdir = input_directory,title = "Select file",filetypes = (("GIF files","*.gif"),("PNG files","*.png"),("all files","*.*")))
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        input_directory = self.filename.split('/')
        input_filename = input_directory.pop()
        input_directory = '/'.join(input_directory)
        print(input_directory)
        print(input_filename)
        update("InputImage", "Directory", input_directory)
        update("InputImage", "Filename", input_filename)
        self.title("Image2Antic :: "+input_filename)
        self.imageViewer()

root = Root()
root.mainloop()
