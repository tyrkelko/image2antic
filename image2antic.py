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
from pathlib import Path

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

def find_pal_color(r,g,b):
    Hue_Dictionary = {11:135,12:112.5,13:90,14:67.5,15:45,1:22.5,2:337.5,3:315,4:292.5,5:270,6:225,7:202.5,8:180,9:157.5,10:135}
    R = float(r/255)
    G = float(g/255)
    B = float(b/255)
    mn = R
    if (mn > G):
        mn = G
    if (mn > B):
        mn = B
    if (R == B) and (R == G):
        Hue = 0
        h = 0
    else:
        if (R>=G) and (R>=B):
            Hue = (G-B)/(R-mn)
        elif (G>=R) and (G>=B):
            Hue = 2.0+(B-R)/(G-mn)
        else:
            Hue = 4.0+(R-G)/(B-mn)
        Hue = Hue * 60.0
        while (Hue < 0):
            Hue += 360
        while (Hue > 360):
            Hue -= 360
        closest_h_index = 1
        closest_h_distance = abs(Hue - Hue_Dictionary[1])
        for h in Hue_Dictionary:
            if (closest_h_distance > abs(Hue - Hue_Dictionary[h])):
                closest_h_index = h
                closest_h_distance = abs(Hue - Hue_Dictionary[h])
    Lum = pow( 0.299*R*R + 0.587*G*G + 0.114*B*B , 0.5 )
    Lum = round(16 * Lum)
    if Lum % 2 == 1:
        Lum = Lum - 1
    
    global Lum_A8
    Lum_A8 = Lum
    global Hue_A8
    if (h == 0):
        Hue_A8 = 0
    else:
        Hue_A8 = closest_h_index

#for i in range(0,255,64):
#    for j in range(0,255,64):
#        for k in range(0,255,64):
#            find_pal_color(i,j,k)
#            print("RGB(",str(i),str(j),str(k),") is A8(",str(Hue_A8), str(Lum_A8),")")

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
    global input_filename
    print("processing...")
    rgb_im = img.convert("RGB")
    working_directory = input_filename.split(".")[0]
    Path(working_directory).mkdir(parents=True, exist_ok=True)

    screen_mem_start = 28672 # 0x7000
    charset_base_mem_start= 20480 # 0x5000
    
    #define SCREEN_MEM		0x7000
    #define DLIST_MEM		0x6C00	// aligned to 1K
    #define CHARSET0_MEM 	0x5000	// aligned to 1K
    #define CHARSET1_MEM 	0x5400	// aligned to 1K
    #define CHARSET2_MEM 	0x5800	// aligned to 1K
    #define CHARSET3_MEM 	0x5C00	// aligned to 1K
    #define CHARSET4_MEM 	0x6000	// aligned to 1K

    antic_target_modes = {
        "4" : {"colors" : 4, "display_mode" : "text", "columns" : 40, "lines" : 24, "char_width" : 4, "char_height" : 8},
        "5" : {"colors" : 4, "display_mode" : "text", "columns" : 40, "lines" : 12, "char_width" : 4, "char_height" : 8}
    }
    antic_target = "5"
    segments_file_text = ""
    atari_cfg_memory = ""
    atari_cfg_segments = ""
    atari_main_c_definitions = ""
    atari_main_c_dl_array = ""
    charsets_mem_list = []
    w, h = img.size
    mode_to_bpp = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}
    d = mode_to_bpp[img.mode]

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
    screenArray = []
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
    # generate the charsets and screen data formatted for cc65
    atari_cfg_memory = atari_cfg_memory + "# charsets load chunk (generated with image2antic.py)\n"
    atari_cfg_segments = atari_cfg_segments + "# segments declaration (generated with image2antic.py)\n"
    
    charsets_size = []
    for charset_number in range(charset_index + 1):
        chars_in_set = 0
        for char in chars:
            if (char[0] == charset_number):
                chars_in_set = chars_in_set + 1
        print ("generate charset_"+str(charset_number)+"_data")
        charsetArray = []
        for char in range(chars_in_set):
            for byte in range(8): 
                charsetArray.append(chars[charset_number, char][byte])
        print ("chars in set:", chars_in_set)
        for i in range(chars_in_set * 8, 128 * 8):
            charsetArray.append(0)
        print ("filled blanks to 128 chars")
        
        charsetByteArray = bytearray(charsetArray)
        charsetBinaryFile = open(working_directory+"/charset_"+str(charset_number)+"_data.bin", "wb")
        charsetBinaryFile.write(charsetByteArray)

        charsets_mem_list.append("CHARSET"+str(charset_number)+"_MEM")

        atari_cfg_memory = atari_cfg_memory + "CHARSET_"+str(charset_number)+"_MEM: file = %O,               start = "+hex(charset_base_mem_start+charset_number*1024).upper().replace("0X", "$")+", size = $0400;\n"
        atari_cfg_segments = atari_cfg_segments + "    CHARSET_"+str(charset_number)+":       load = CHARSET_"+str(charset_number)+"_MEM,       type = rw, define = yes;\n"
        atari_main_c_definitions = atari_main_c_definitions + "#define CHARSET"+str(charset_number)+"_MEM\t"+hex(charset_base_mem_start + charset_number*1024).upper().replace("0X", "0x")+"\n"
        
        segments_file_text = segments_file_text + '.segment "CHARSET_'+str(charset_number)+'"\n'
        segments_file_text = segments_file_text + '_L_CHARSET_'+str(charset_number)+':\n'
        segments_file_text = segments_file_text + '.incbin "charset_'+str(charset_number)+'_data.bin"\n'
        segments_file_text = segments_file_text + '.export _L_CHARSET_'+str(charset_number)+'\n\n'
        charsets_size.append(chars_in_set)

    print ("generate screen_data")
    for j in range(antic_target_modes[antic_target]["lines"]):
        for i in range (antic_target_modes[antic_target]["columns"]):
            screenArray.append(screen[i,j])

    atari_cfg_memory = atari_cfg_memory + "# dlist load chunk (generated with image2antic.py)\n"
    atari_cfg_memory = atari_cfg_memory + "#    TODO DLIST_MEM: file = %O,               start = $1E00, size = $0018;\n"
    atari_cfg_memory = atari_cfg_memory + "# screen data load chunk (generated with image2antic.py)\n"
    atari_cfg_memory = atari_cfg_memory + "SCREEN_MEM: file = %O,               start = "+hex(screen_mem_start).upper().replace("0X", "$")+", size = "+str('0x%04x' % len(screenArray)).upper().replace("0X", "$")+";\n"
    atari_main_c_definitions = atari_main_c_definitions + "#define SCREEN_MEM\t"+hex(screen_mem_start).upper().replace("0X", "0x")+"\n"
    atari_main_c_definitions = atari_main_c_definitions + "#define DLIST_MEM		0x6C00	// aligned to 1K\n"
    atari_main_c_definitions = atari_main_c_definitions + "//extern unsigned char *L_DLIST_MEM;\n"
    atari_main_c_definitions = atari_main_c_definitions + "extern unsigned char *L_SCREEN_MEM;\n"
    atari_main_c_definitions = atari_main_c_definitions + "extern unsigned char *L_CHARSET0_MEM;\n"
    atari_main_c_definitions = atari_main_c_definitions + "extern unsigned char *L_CHARSET1_MEM;\n"
        
    atari_cfg_segments = atari_cfg_segments + "#   TODO DLIST:    load = DLIST_MEM,    type = rw, define = yes;\n"
    atari_cfg_segments = atari_cfg_segments + "    SCREEN:       load = SCREEN_MEM,       type = rw, define = yes;\n"
        
    segments_file_text = segments_file_text + '.segment "SCREEN"\n'
    segments_file_text = segments_file_text + '_L_SCREEN:\n'
    segments_file_text = segments_file_text + '.incbin "screen_data.bin"\n'
    segments_file_text = segments_file_text + '.export _L_SCREEN\n\n'

    atari_main_c_dl_array = atari_main_c_dl_array + "// CHARSET DLI CHANGES IN LINES: " + str(charset_dli_change)+"\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "unsigned char antic4_display_list[] = {\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "	DL_BLK8,\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "	DL_BLK8,\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "	DL_DLI(DL_BLK8),\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "	DL_LMS(DL_CHR40x16x4),\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "	0x00,\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "	SCREEN_MEM >> 8,\n"
    for i in range(1,12):
        if i in charset_dli_change:
            atari_main_c_dl_array = atari_main_c_dl_array + "	DL_DLI(DL_CHR40x16x4),\n"
        else:
            atari_main_c_dl_array = atari_main_c_dl_array + "	DL_CHR40x16x4,\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "	DL_JVB,\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "	0x00,\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "};\n"

    screenByteArray = bytearray(screenArray)
    screenBinaryFile = open(working_directory+"/screen_data.bin", "wb")
    screenBinaryFile.write(screenByteArray)

    segmentsFile = open(working_directory+"/segments.s", "w+")
    segmentsFile.write(segments_file_text)

    configurationTemplateFile = open("sources_templates/atari.cfg", "r")
    cfg_file_str = configurationTemplateFile.read().replace("##atari_cfg_memory##", atari_cfg_memory).replace("##atari_cfg_segments##", atari_cfg_segments)
    cfgFile = open(working_directory+"/atari.cfg", "w+")
    cfgFile.write(cfg_file_str)

    charsets_mem_str = ""
    i = 0
    for s in charsets_mem_list:
        if (i > 0):
            charsets_mem_str = charsets_mem_str + ", "
        charsets_mem_str = charsets_mem_str + s + " >> 8"
        i = i + 1

    color4 = yet_another_a8_palette[0][0] * 16 + yet_another_a8_palette[0][1]
    color0 = yet_another_a8_palette[1][0] * 16 + yet_another_a8_palette[1][1]
    color1 = yet_another_a8_palette[2][0] * 16 + yet_another_a8_palette[2][1]
    color2 = yet_another_a8_palette[3][0] * 16 + yet_another_a8_palette[3][1]
    color3 = color4 #255-color0 #yet_another_a8_palette[4][0] << 4 + yet_another_a8_palette[4][1]
    print(color0, color1, color2, color3, color4)
    
    mainCTemplateFile = open("sources_templates/main.c", "r")
    main_c_file = mainCTemplateFile.read().replace("##ATARI_MAIN_C_DEFINITIONS##", atari_main_c_definitions).replace("##ATARI_MAIN_C_DL_ARRAY##", atari_main_c_dl_array).replace("##CHARSETS_MEM##", str(charsets_mem_str)).replace("##COLOR0##", str(color0)).replace("##COLOR1##", str(color1)).replace("##COLOR2##", str(color2)).replace("##COLOR3##", str(color3)).replace("##COLOR4##", str(color4))
    mainCFile = open(working_directory+"/main.c", "w+")
    mainCFile.write(main_c_file)
    
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
        global yet_another_a8_palette
        yet_another_a8_palette = []
        for j in range(h):
            for i in range(w):
                r, g, b = rgb_im.getpixel((i, j))
                if ((r,g,b) not in rgb_colors):
                    rgb_colors.append((r,g,b))
                    my_a8_palette.append(find_nearest_color(r,g,b))
                    find_pal_color(r,g,b)
                    yet_another_a8_palette.append((Hue_A8, Lum_A8))
        print(rgb_colors)
        self.imageParamsLabel.configure(text = "Image Format: "+ img.format+"\nwidth:  "+str( w) + "\nheight: "+str(h)+"\ndepth: "+str(d) + "\nNumber of colors: " + str(len(colors)) + str(colors) + "\nPalette (RGB): " + str(rgb_colors) + "\nPalette (A8): " + str(my_a8_palette) + "\nPalette (A8c)" + str(yet_another_a8_palette))
        if (len(my_a8_palette) < 5):
            for i in range (len(my_a8_palette), 5):
                my_a8_palette.append(0)
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
