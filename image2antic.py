# Python program to read 
# image using PIL module
# and prepare an atari
# antic5 charset and screen data

from tkinter import filedialog
from tkinter import ttk
from tkinter import StringVar
from tkinter import colorchooser
import configparser
import os.path
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
#from ScrollableImage import ScrollableImage 
import copy
from pathlib import Path
import shlex, subprocess

#############################################################################################################################################################################
# Atari 800XL PAL palette and color management functions

a8_palette = [  (  0,  0,  0),( 33, 33, 33),( 75, 75, 75),(107,107,107),(132,132,132),(164,164,164),(206,206,206),(255,255,255), # black   0 -  15
		( 68,  0,  0),(104, 23,  0),(134, 55,  0),(173, 91, 00),(196,116, 31),(230,157, 62),(250,191,101),(255,222,140), # brown  16 -  31
		( 79,  0,  0),(118,  0,  0),(152, 40, 26),(184, 74, 59),(217, 97, 83),(243,142,124),(253,174,157),(255,206,189), # red    32 -  47
		( 91,  0,  0),(205,  0, 44),(158, 24, 75),(192, 65,108),(220, 87,132),(255,125,175),(253,155,206),(251,198,240), # pink   48 -  63
                                
                ( 85,  0, 51),(118,  0, 90),(144, 14,123),(188, 58,156),(213, 81,183),(247,116,222),(255,144,255),(255,186,255), # purple 64 -  79
		( 56,  0,103),(103,  0,138),(133, 16,172),(162, 62,214),(184, 88,238),(235,112,252),(252,150,249),(255,186,255), # purple 80 -  95
                ( 36,  0,103),( 67,  0,176),( 99, 24,205),(137, 69,244),(166, 89,253),(198,121,251),(224,157,250),(255,197,255), # Pur-Bl 96 - 111
  		(  0,  0,144),(  0, 32, 44),( 36, 55,209),( 71, 97,242),(100,124,255),(134,158,255),(163,188,255),(206,232,249), #       112 - 127
                                
		(  0,  0,103),(  0, 51,128),(  0, 84,176),( 45,113,214),( 70,148,233),(103,182,255),(134,217,255),(171,255,255),				
		(  0, 32, 47),(  0, 64, 83),(  0,104,128),( 30,139,159),( 49,165,178),( 95,195,218),(125,232,242),(163,251,253),                                
		(  0, 43,  0),(  0, 80, 32),(  0,128, 64),( 71, 97,242),( 51,172,128),( 86,212,165),(119,247,199),(206,251,238),
		(  0, 51,  0),(  0, 87,  0),(  0,124,  0),( 50,160,  0),( 50,160,  0),(103,220, 62),(139,255, 97),(184,255,128), # check middle of this line - color repeats
                                
		(  0, 42,  0),(  0, 80,  0),( 39,115,  0),( 80,142, 11),( 96,176,  0),(101,167, 15),(175,244, 76),(210,255,103),
		(  0, 26,  0),( 75, 99,  0),( 80, 96, 21),(103,132, 11),(132,156,  0),(172,198, 26),(206,229, 60),(237,255, 96),
		( 34,  0,  0),( 75, 40,  0),(111, 83, 11),(138,115, 11),(168,137, 12),(210,179, 37),(237,187, 70),(255,245,105),
		( 68,  0,  0),(104, 23,  0),(134, 55,  0),(173, 91, 00),(196,116, 31),(230,157, 62),(250,191,101),(255,222,140)]

def find_nearest_color(r,g,b):
	min = 255*255*255*255 # impossible max value
	min_index = -1
	for i in range(128):
		rp,gp,bp = a8_palette[i]
		distance = abs(pow(r-rp,2)+pow(g-gp,2)+pow(b-bp,2))
		if distance < min:
			min = distance
			min_index = i
	return min_index * 2

def find_pal_color(r,g,b):
        global Hue_A8
        global Lum_A8
        color_index = find_nearest_color(r,g,b)
        Hue_A8 = color_index >> 8
        Lum_A8 = color_index & 0x00FF

def find_rgb_color(Color_A8):
        return rgb_to_hex((a8_palette[int(Color_A8 / 2)]))

def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb

def popup_color_picker():
        win = tk.Toplevel()
        win.minsize(640, 400)
        win.resizable(width=True, height=True)
        win.wm_title("Atari 128 Colors - PAL")
        win.colorPickerFrame = ttk.LabelFrame(win, text = "Pick a Color", width = 640, height = 400)
        win.colorPickerFrame.grid(sticky = "NSEW", column = 1, row = 1, padx = 20, pady = 20)
        win.color_lbl = []
        win.color_name_lbl = []
        for j in range(4):
                for i in range(4):
                        for k in range(8):
                                win.color_lbl.append(ttk.Label(win.colorPickerFrame, background = find_rgb_color(2*(j*32+i*8+k)), width = 20))
                                win.color_lbl[j*32+i*8+k].grid(column = j*2, row = i*8+k)
                                win.color_name_lbl.append(ttk.Button(win.colorPickerFrame, text = str(2*(j*32+i*8+k)), width = 5))
                                win.color_name_lbl[j*32+i*8+k].grid(column = j*2 + 1, row = i*8+k)
                
class CustomDialog(tk.Toplevel):
        def __init__(self, parent, prompt):
                tk.Toplevel.__init__(self, parent)
                self.minsize(640, 400)
                self.resizable(width=True, height=True)
                self.wm_title("Atari 128 Colors - PAL")
                self.colorPickerFrame = ttk.LabelFrame(self, text = "Pick a Color", width = 640, height = 400)
                self.colorPickerFrame.grid(sticky = "NSEW", column = 1, row = 1, padx = 20, pady = 20)
                self.color_lbl = []
                self.color_name_lbl = []
                for j in range(4):
                        for i in range(4):
                                for k in range(8):
                                        self.color_lbl.append(ttk.Label(self.colorPickerFrame, background = find_rgb_color(2*(j*32+i*8+k)), width = 20))
                                        self.color_lbl[j*32+i*8+k].grid(column = j*2, row = i*8+k)
                                        self.color_name_lbl.append(ttk.Button(self.colorPickerFrame, text = str(2*(j*32+i*8+k)), width = 5, command = self.on_ok(color = 2*(j*32+i*8+k))))
                                        self.color_name_lbl[j*32+i*8+k].grid(column = j*2 + 1, row = i*8+k)

                self.var = tk.StringVar()
                self.label = tk.Label(self, text=prompt)
                self.entry = tk.Entry(self, textvariable=self.var)
                self.ok_button = tk.Button(self, text="OK", command=self.on_ok)

                self.label.grid(column = 0, row = 0)
                self.entry.grid(column = 1, row = 0)
                self.ok_button.grid(column = 2, row = 0)

                self.entry.bind("<Return>", self.on_ok)

        def on_ok(self, color, event=None):
                self.destroy()

        def show(self):
                self.wm_deiconify()
                self.entry.focus_force()
                self.wait_window()
                return self.var.get()

#############################################################################################################################################################################
# Configuration management
# get configuration with previous working directory and parameters
config = configparser.RawConfigParser()

def init():
        'Create a configuration file if does not exist'
        config.add_section('InputImage')
        config.set('InputImage', 'Directory', './')
        config.set('InputImage', 'Filename', '*.gif')
        config.add_section('Output')
        config.set('Output', 'AnticMode', '5')
        config.set('Output', 'skip_column', '0')
        config.set('Output', 'interleave', '0')
        with open('image2antic.cfg', 'w') as output:
                config.write(output)

# check if dataUpdate.cfg exist if not create it   
if not os.path.exists('image2antic.cfg'):
        print("Can't find 'image2antic.cfg', create a new configuration file") 
        init()

# Read configurations using section and key to get the value
config.read('image2antic.cfg')
input_directory = config.get('InputImage', 'Directory')
input_filename = config.get('InputImage', 'Filename')
global antic_mode
antic_mode = config.get('Output', 'AnticMode')
global skip_column
skip_column = config.get('Output', 'skip_column', fallback='0')
global interleave
interleave = str(config.get('Output', 'interleave', fallback='0'))


#------------------------------------------------------------
def update(section, key, value):
    #Update config using section key and the value to change
    #call this when you want to update a value in configuation file
    # with some changes you can save many values in many sections
    config.set(section, key, value )
    with open('image2antic.cfg', 'w') as output:
        config.write(output)
#------------------------------------------------------------

#############################################################################################################################################################################
# compilation and emulation command line
def exec_emulator_with_build():
    global working_directory
    global antic_mode
    command_line = "wine /home/kobi/Altirra-3.10/Altirra.exe "+working_directory+".xex"
    print(command_line)
    # TODO: complete with configuration and execution accordingly


def exec_cc65_build():
    global working_directory
    command_line = "/home/kobi/cc65/bin/cl65 --debug-info -Wl --dbgfile,"+working_directory+".lab -m "+working_directory+".map -Ln "+working_directory+".lbl -t atari -Oi segments.s main.c -o "+working_directory+".xex -C atari.cfg"
    print(command_line)
    # TODO: complete with configuration and execution accordingly


#############################################################################################################################################################################
# process image to CC65 Atari 800 code
def process_cc65_code():
    global input_filename
    global antic_mode
    global interleave
    print("interleave = ", interleave)
    print("processing...")
    rgb_im = img.convert("RGB")
    global working_directory
    working_directory = input_filename.split(".")[0]
    Path(working_directory).mkdir(parents=True, exist_ok=True)

    screen_mem_start = 19456            # 0x4C00
    charset_base_mem_start= 12288       # 0x3000
    
    antic_target_modes = {
        "4" : {"colors" : 4, "display_mode" : "text", "columns" : 40, "lines" : 24, "char_width" : 4, "char_height" : 8, "dl" : "DL_CHR40x8x4"},
        "5" : {"colors" : 4, "display_mode" : "text", "columns" : 40, "lines" : 12, "char_width" : 4, "char_height" : 8, "dl" : "DL_CHR40x16x4"}
    }

    segments_file_text = ""
    atari_cfg_memory = ""
    atari_cfg_segments = ""
    atari_main_c_definitions = ""
    atari_main_c_dl_array = ""
    atari_main_c_update = ""
    atari_main_c_draw = ""
    atari_main_c_input = ""
    charsets_mem_list = []
    w, h = img.size
    if (skip_column == "1"):
        rgb_im = rgb_im.resize((int(w/2), h), resample = 0)
        w = int(w/2)
    mode_to_bpp = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}
    d = mode_to_bpp[img.mode]

    columns = antic_target_modes[antic_mode]["columns"]
    lines = round(h/8)

    # arrange an array of ANTIC COLOR TEXT mode 4x8 tiles
    tiles = {}
    for j in range(lines):
        for i in range (round(w / 4)):
            for y in range (8):
                tiles[i,j,y] = 0
                for x in range (4):
                    if ((i*4+x<w) and (j*8+y<h)):
                        r, g, b = rgb_im.getpixel((i*4+x, j*8+y))
                    else:
                        r, g, b = (0,0,0)  
                    pixel = round(((r*8+g*8+b*8)/640))
                    double_bit_pixel = 2 if (pixel == 5) else 1 if (pixel == 7) else pixel
                    tiles[i,j,y] = tiles[i,j,y] + (64 if x == 0 else 16 if x == 1 else 4 if x == 2 else 1) * double_bit_pixel
                # reduce byte size in case exceeded byte size due to additional colors.
                while (tiles[i,j,y] > 255):
                    tiles[i,j,y]-=256

    print("Actual rows and lines: (", i, ",", j, ")")
    if (int(interleave) > 0):
            columns = int(w/4)
            atari_main_c_definitions = atari_main_c_definitions + "#include <peekpoke.h>\n\n"
            atari_main_c_definitions = atari_main_c_definitions + "#define ROWS " + str(lines) + "\n"
            atari_main_c_definitions = atari_main_c_definitions + "#define COLS " + str(columns) + "\n"
            atari_main_c_definitions = atari_main_c_definitions + "#define SCREEN_RIGHT_BOUNDARY " + str(columns - antic_target_modes[antic_mode]["columns"]) + "\n"
            

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
    global charsets_size
    charset_dli_change = []
    charset_dli_change.append(0)
    global a8_palette
    for y in range(8):
        temp_char[y] = 0
    if (int(interleave) == 0):
            chars[charset_index, chars_index] = copy.deepcopy(temp_char)
            chars_index = chars_index + 1
    else:
            for charset in range(int(interleave)):
                    chars[charset, 0] = copy.deepcopy(temp_char)
                    
            
    for j in range(lines): #range(antic_target_modes[antic_mode]["lines"]): #range(round(h/8)):
        if (int(interleave) == 0):
                if (chars_index > 87):
                    charset_index = charset_index + 1
                    chars_index = 0
                    for y in range(8):
                        temp_char[y] = 0
                    chars[charset_index, chars_index] = copy.deepcopy(temp_char)
                    chars_index = chars_index + 1
                    charset_dli_change.append(j - 1)
        else:
                if (j > 0):
                        charset_dli_change.append(j)      
                charset_index = j % int(interleave)
                chars_index = 0
                for c_i in chars.keys():
                        if ((c_i[0] == charset_index) and (c_i[1] > chars_index)):
                                chars_index = c_i[1]
                chars_index = chars_index + 1

                
        for i in range (columns):
            if ((i < round(w/4)) and (j < round(h/8))):
                fifth_color = 0
                for y in range (8):
                    temp_char[y] = 0
                    for x in range (4):
                        if ((i*4+x < w) and (j*8+y < h)):
                                r, g, b = rgb_im.getpixel((i*4+x, j*8+y))
                        else:
                                r, g, b = (0,0,0)
                        pixel = rgb_colors.index((r,g,b))
                            
                        temp_char[y] = temp_char[y] + (min(pixel, 3) << (6-2*x))
                        if (pixel == 4):
                                fifth_color = 1

                char_exists = False
                for char in chars:
                    if char[0] == charset_index and chars[char] == temp_char:
                        char_exists = True
                        chars_reuse = chars_reuse + 1
                        screen[i,j] = char[1]
                        if (fifth_color == 1):
                            screen[i,j] += 128
                    
                if (not char_exists):
                    chars_count = chars_count + 1
                    chars[charset_index, chars_index] = copy.deepcopy(temp_char)
                    screen[i,j] = chars_index
                    if (fifth_color == 1):
                        screen[i,j] += 128
                    
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

    root.charsetSizeLabel.configure(text="Charsets Size " + str(charsets_size))
    
    print ("generate screen_data")
    for j in range(antic_target_modes[antic_mode]["lines"]):
        for i in range (columns):
            screenArray.append(screen[i,j])

    atari_cfg_memory = atari_cfg_memory + "# dlist load chunk (generated with image2antic.py)\n"
    atari_cfg_memory = atari_cfg_memory + "#    TODO DLIST_MEM: file = %O,               start = $1E00, size = $0018;\n"
    atari_cfg_memory = atari_cfg_memory + "# screen data load chunk (generated with image2antic.py)\n"
    atari_cfg_memory = atari_cfg_memory + "SCREEN_MEM: file = %O,               start = "+hex(screen_mem_start).upper().replace("0X", "$")+", size = "+str('0x%04x' % len(screenArray)).upper().replace("0X", "$")+";\n"
    atari_main_c_definitions = atari_main_c_definitions + "#define SCREEN_MEM\t"+hex(screen_mem_start).upper().replace("0X", "0x")+"\n"
    atari_main_c_definitions = atari_main_c_definitions + "#define DLIST_MEM		0x4800 //0x6C00	// aligned to 1K\n"
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
    atari_main_c_dl_array = atari_main_c_dl_array + "	DL_DLI(DL_BLK8),\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "	DL_BLK8,\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "	DL_BLK8,\n"
    if (int(interleave) > 0):
            atari_main_c_dl_array = atari_main_c_dl_array + "	DL_LMS(DL_DLI(DL_HSCROL("+antic_target_modes[antic_mode]["dl"]+"))),"
    else:
            atari_main_c_dl_array = atari_main_c_dl_array + "	DL_LMS("+antic_target_modes[antic_mode]["dl"]+"),"        
    atari_main_c_dl_array = atari_main_c_dl_array + "(SCREEN_MEM & 0x00FF),"
    atari_main_c_dl_array = atari_main_c_dl_array + "SCREEN_MEM >> 8,\n"
    for i in range(1,int(antic_target_modes[antic_mode]["lines"])):
        if i in charset_dli_change:
            if (int(interleave) == 0):
                    atari_main_c_dl_array = atari_main_c_dl_array + "	DL_DLI("+antic_target_modes[antic_mode]["dl"]+"),\n"
            else:
                    line_screen_mem_start = screen_mem_start + i * columns
                    print("line: ", i, "start address: ", hex(line_screen_mem_start), "columns: ", columns)
                    atari_main_c_dl_array = atari_main_c_dl_array + "	DL_LMS(DL_DLI(DL_HSCROL("+antic_target_modes[antic_mode]["dl"]+"))),"
                    atari_main_c_dl_array = atari_main_c_dl_array + "((SCREEN_MEM + "+ str(i * columns) +") & 0x00FF),"
                    atari_main_c_dl_array = atari_main_c_dl_array + "(SCREEN_MEM + "+ str(i * columns) +") >> 8,\n"
        else:
            atari_main_c_dl_array = atari_main_c_dl_array + "	"+antic_target_modes[antic_mode]["dl"]+",\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "	DL_JVB,0x00,DLIST_MEM>>8\n"
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


    if (int(interleave) > 0):
            charset_mem_str_tmp = charsets_mem_str
            for i in range(int(lines / int(interleave)) - 1):
                    charset_mem_str_tmp = charset_mem_str_tmp + ",\n" + charsets_mem_str
            charsets_mem_str = charset_mem_str_tmp
            atari_main_c_update = "if ((moving_type == MOVING_RIGHT) || (auto_scroll == 1))\n\t{\n\t\tif ((vblank_counter & 0x03) == 3)\n\t\t\tscreen_pos++;\n\t\tANTIC.hscrol = vblank_counter & 0x03;\n\t\tvblank_counter = vblank_counter & 0x03;\n\t}\n\tif (moving_type == MOVING_LEFT)\n\t{\n\t\tif ((vblank_counter & 0x03) == 0)\n\t\t\tif (screen_pos > 0)\n\t\t\t\tscreen_pos--;\n\t}\n\t\tif (screen_pos > SCREEN_RIGHT_BOUNDARY)\n\t\tscreen_pos = 0;"
            atari_main_c_draw = "i = ROWS;\n\trow_addr = SCREEN_MEM + screen_pos + 24 * COLS;\n\twhile (--i < 255)\n\t{\n\t\trow_addr = row_addr - COLS;\n\t\tPOKE(DLIST_MEM + 4 + 3 * i, row_addr & 0x00FF);\n\t\tPOKE(DLIST_MEM + 5 + 3 * i, row_addr >> 8);\n\t}"
            atari_main_c_input = "st = (PIA.porta & 0x0f);\n\tst = st ^ 0x0f;\n\tif (st == JOY_BIT_RIGHT)\n\t{\n\t\tmoving_type = MOVING_RIGHT;\n\t\tauto_scroll = 0;\n\t\treturn;\n\t}\n\tif (st == JOY_NO_MOVE)\n\t{\n\t\tmoving_type = MOVING_NONE;\n\t\treturn;\n\t}\n\tif (st == JOY_BIT_LEFT)\n\t{\n\t\tmoving_type = MOVING_LEFT;\n\t\tauto_scroll = 0;\n\t\treturn;\n\t}\n\tif (st == JOY_BIT_UP)\n\t{\n\t\tmoving_type = MOVING_UP;\n\t\tauto_scroll = 1;\n\t\treturn;\n\t}\n\tif (st == JOY_BIT_DOWN)\n\t{\n\t\n\t\tmoving_type = MOVING_DOWN;\n\t\n\t}"
    color4 = yet_another_a8_palette[0][0] * 16 + yet_another_a8_palette[0][1]
    color0 = yet_another_a8_palette[1][0] * 16 + yet_another_a8_palette[1][1]
    color1 = yet_another_a8_palette[2][0] * 16 + yet_another_a8_palette[2][1]
    color2 = yet_another_a8_palette[3][0] * 16 + yet_another_a8_palette[3][1]
    color3 = yet_another_a8_palette[4][0] * 16 + yet_another_a8_palette[4][1]
    print(color0, color1, color2, color3, color4)

    if (int(interleave) == 0):
            csi = 0
            charset_index = 1
    else:
            csi = 1
    mainCTemplateFile = open("sources_templates/main.c", "r")
    main_c_file = mainCTemplateFile.read().replace("##ATARI_MAIN_C_DEFINITIONS##", atari_main_c_definitions).replace("##ATARI_MAIN_C_DL_ARRAY##", atari_main_c_dl_array).replace("##CHARSETS_MEM##", str(charsets_mem_str)).replace("##COLOR0##", str(color0)).replace("##COLOR1##", str(color1)).replace("##COLOR2##", str(color2)).replace("##COLOR3##", str(color3)).replace("##COLOR4##", str(color4)).replace("##CHARSET_INDEX##", str(csi)).replace("##MAIN_C_UPDATE##", atari_main_c_update).replace("##MAIN_C_DRAW##", atari_main_c_draw).replace("##MAIN_C_INPUT##", atari_main_c_input)
    mainCFile = open(working_directory+"/main.c", "w+")
    mainCFile.write(main_c_file)
    exec_cc65_build()
    exec_emulator_with_build()
    
# main loop handler class
class Root(Tk):
    # show working dialog with a file browse button
    def __init__(self):
        super(Root, self).__init__()
        self.title("Image2Antic")

        self.minsize(640, 400)
        self.resizable(width=True, height=True)
        self.grid_columnconfigure(index = 1, minsize = 1280)
        self.grid_rowconfigure(index = 1, minsize = 768)
        #self.wm_iconbitmap('icon.ico')
 
        self.previewFrame = ttk.LabelFrame(self, text = "Convert An Image To Atari 800XL CC65 Source", width = 1260, height = 220)
        self.previewFrame.grid(sticky = "NSEW", column = 1, row = 1, padx = 20, pady = 20)

        self.imageRGBColorTitle = ttk.Label(self.previewFrame, text = "RGB Color")
        self.imageRGBColorTitle.grid(column = 0, rowspan = 2, row = 1)

        self.imageRGBColorTitle = ttk.Label(self.previewFrame, text = "A8 PAL Color")
        self.imageRGBColorTitle.grid(column = 2, rowspan = 2, row = 1)


        self.imageSize = ttk.Label(self.previewFrame)
        self.imageSize.grid(column = 5, row = 2, padx = 20)
        self.browseButton()

        self.previewCanvasFrame = ttk.LabelFrame(self.previewFrame, text = "Image Preview Pane", width = 1220, height = 200)
        self.previewCanvasFrame.grid(sticky = "NSEW", column = 0, row = 0, columnspan = 10)
        self.previewCanvas = Canvas(self.previewCanvasFrame, width = 1220, height = 192, scrollregion=(0,0,2048,2048))
        self.previewCanvas.grid(column = 0, row = 0, padx = 20, pady = 10)
        #self.previewA8Canvas = Canvas(self.previewCanvasFrame, width = 1220, height = 192, scrollregion=(0,0,2048,2048))
        #self.previewA8Canvas.grid(column = 0, row = 2, padx = 20, pady = 10)

        self.canvasHbar = Scrollbar(self.previewCanvasFrame, orient=HORIZONTAL)
        self.canvasHbar.grid(sticky="ew") 
        self.canvasHbar.config(command = self.previewCanvas.xview)
        self.previewCanvas.config(xscrollcommand=self.canvasHbar.set)
        #self.previewA8Canvas.config(xscrollcommand=self.canvasHbar.set)

        global antic_modes
        antic_modes = [("Text 4 (40x24,4 colors)", 1, "4"), ("Text 5 (40x12,4 colors)", 2, "5")]
        antic_mode_options = ["Antic 4", "Antic 5"]
        
        global antic_mode
        self.rb_antic_mode = StringVar(None, str(antic_mode))        

        print(antic_mode)
        # antic_mode_changed - update config file and global variable
        def antic_mode_changed(*args):
            global antic_mode
            global antic_modes
            print("antic mode changed")
            print(self.rb_antic_mode.get())
            antic_mode = str(self.rb_antic_mode.get())
            print("on save:",antic_mode)
            update("Output", "anticmode", antic_mode)
    
        self.rb_antic_mode.trace("w", antic_mode_changed)
       
        for text, num, mode in antic_modes:
            self.anticRadioButtons = ttk.Radiobutton(self.previewFrame, text=text, variable=self.rb_antic_mode, value=mode)
            self.anticRadioButtons.grid(sticky = "W", column = 5, row = num + 3)

        

        
        # skip odd columns for processing images designed for Antic 4 with 2x1 pixel ratio.
        def skip_column_changed(*args):
            global skip_column
            skip_column = self.rb_skip_column.get()
            update("Output", "skip_column", skip_column)
            
        global skip_column
        self.rb_skip_column = StringVar()
        self.rb_skip_column.set(str(skip_column))
        
        self.rb_skip_column.trace("w", skip_column_changed)
        
        self.skipColumnCheckBox = ttk.Checkbutton(self.previewFrame, text = "Skip column (Antic 4 compatibility)", variable = self.rb_skip_column)
        self.skipColumnCheckBox.grid(column = 5, row = 6, sticky = "W")

        # allow user select if the screen has horizontal scroll and if so, how to rotate the charsets between display lines
        global interleaveOptions
        interleaveOptions = ["No Scroll", "Single Charset Scroll", "Two Charset Scroll", "Three Charset Scroll", "Four Charset Scroll", "Five Charset Scroll", "Six Charset Scroll"]
        print(interleaveOptions)
        global interleave
        def interleave_changed(*args):
            global interleaveOptions
            global interleave
            interleave = interleaveOptions.index(self.rb_interleave.get())
            update("Output", "interleave", interleave)
            
        
        self.rb_interleave = StringVar()
        
        
        self.interleaveDropdown = ttk.OptionMenu(self.previewFrame, self.rb_interleave, interleaveOptions[0], *interleaveOptions)
        self.interleaveDropdown.grid(column = 5, row = 8, sticky = "W")
        self.rb_interleave.set(interleaveOptions[int(interleave)])

        self.rb_interleave.trace("w", interleave_changed)

        #charsets_size              
        self.charsetSizeLabel = ttk.Label(self.previewFrame, text="Charsets Size []")
        self.charsetSizeLabel.grid(column = 5, row = 10, sticky = "W")

        self.processButton()


        # UI color list variables
        self.imageRGBColors = []
        self.imageRGBColorsLabel = []
        self.imageA8Colors = []
        self.imageA8ColorsLabel = []
        self.imageA8ColorsButton = []
        self.yet_another_a8_palette = []
        self.rgb_colors = []
        
    # browse button to open a file browser on click
    def browseButton(self):
        self.browseButton = ttk.Button(self, text = "Browse for an image to work on",command = self.fileDialog)
        self.browseButton.grid(column = 1, row = 0, padx = 20)
        
    # browse button to begin output process
    def processButton(self):
        global charsets_size
        charsets_size = []
        self.processButton = ttk.Button(self, text = "Process",command = process_cc65_code)
        self.processButton.grid(column = 1, row =2, sticky="E", padx = 20)
        
    def showImg(self, img):
        self.render = ImageTk.PhotoImage(img)

        self.previewCanvas.create_image(0, 0, image = self.render, anchor=NW)
        self.previewCanvas.configure(scrollregion=(0,0,img.size[0], img.size[1]))
        
    def choose_bg_color(self):
                color = self.buttons['bg_color'].configure()['background'][4]
                color = askcolor(color=color)[1]
                if not color:
                        return
                self.buttons['bg_color'].configure(background=color)
                the_queue.put('background {}'.format(color))
                
    # when invoked, open the image and extract information on it
    def imageViewer(self):
        global input_directory
        global input_filename
        global img
        global rgb_colors
        global yet_another_a8_palette
        global skip_column
        self.yet_another_a8_palette.clear()
        del self.yet_another_a8_palette[:]
        self.rgb_colors.clear()
        del self.rgb_colors[:]
        self.imageRGBColors.clear()
        del self.imageRGBColors[:]
        self.imageRGBColorsLabel.clear()
        del self.imageRGBColorsLabel[:]
        self.imageA8Colors.clear()
        del self.imageA8Colors[:]
        self.imageA8ColorsLabel.clear()
        del self.imageA8ColorsLabel[:]
        self.imageA8ColorsButton.clear()
        del self.imageA8ColorsButton[:]
        self.imageA8ColorsButton = []
        del self.imageA8ColorsButton[:]
        self.yet_another_a8_palette = []
        yet_another_a8_palette = []
        del self.yet_another_a8_palette[:]
        self.rgb_colors = []
        rgb_colors = []
        del self.rgb_colors[:]
        colors = []
        img = Image.open(input_directory+'/'+input_filename) 
        w, h = img.size
        mode_to_bpp = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}
        d = mode_to_bpp[img.mode]
        px = img.load()
        
        for j in range(h):
            for i in range(w):
                if (px[i, j] not in colors):
                    colors.append(px[i,j])
        rgb_im = img.convert('RGB')
        
        
        
        for j in range(h):
            for i in range(w):
                r, g, b = rgb_im.getpixel((i, j))
                if ((r,g,b) not in self.rgb_colors):
                    self.rgb_colors.append((r,g,b))
                    rgb_colors.append((r,g,b))
                    find_pal_color(r,g,b)
                    self.yet_another_a8_palette.append((Hue_A8, Lum_A8))
                    yet_another_a8_palette.append((Hue_A8, Lum_A8))
        
        number_of_colors = len(self.yet_another_a8_palette)
        
        if (number_of_colors < 6):
            for i in range (len(self.yet_another_a8_palette), 6):
                self.rgb_colors.append((0,0,0))
                rgb_colors.append((0,0,0))
                self.yet_another_a8_palette.append((0, 0))
                yet_another_a8_palette.append((0, 0))
        
        for i in range(number_of_colors):
                atari_color = self.yet_another_a8_palette[i][0]*16+self.yet_another_a8_palette[i][1]
                self.imageA8Colors.append(ttk.Label(self.previewFrame, background = find_rgb_color(atari_color), text = str(atari_color), width = 10))
                self.imageA8Colors[i].grid(column = 2, row = i+3)
                self.imageA8ColorsButton.append(ttk.Button(self.previewFrame, text = "< Adjust", width = 10, command = self.pick_color))
                self.imageA8ColorsButton[i].grid(column = 4, row = i+3)
                self.imageRGBColors.append(ttk.Label(self.previewFrame, background = rgb_to_hex(self.rgb_colors[i]), text = rgb_to_hex(self.rgb_colors[i]), width = 10))
                self.imageRGBColors[i].grid(column = 0, row = i+3)

        self.a8_img = Image.new( rgb_im.mode, rgb_im.size)
        pixelMap = rgb_im.load()
        pixelsNew = self.a8_img.load()
        for i in range(img.size[0]):
                for j in range(img.size[1]):
                        r,g,b = rgb_im.getpixel((i,j))
                        a8c = yet_another_a8_palette[rgb_colors.index((rgb_im.getpixel((i, j))))][0]*16+yet_another_a8_palette[rgb_colors.index((rgb_im.getpixel((i, j))))][1]
                        pixelsNew[i,j] = a8_palette[int(a8c/2)]

        # now create the ImageTk PhotoImage:
        self.showImg(self.a8_img)

        self.imageSize.configure(text = "Size: " + str(w)+", "+str(h))

    def pick_color(self):
                my_color = popup_color_picker()

                
    # file dialog for choosing our image 2 antic file
    def fileDialog(self):
        global input_directory
        global input_filename
        self.filename =  filedialog.askopenfilename(initialdir = input_directory,title = "Select file",filetypes = (("all files","*.*"),("GIF files","*.gif"),("PNG files","*.png")))
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
