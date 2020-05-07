# Python program to read 
# image using PIL module
# and prepare an atari
# antic5 charset and screen data

from tkinter import filedialog
from tkinter import ttk
from tkinter import StringVar
import configparser
import os.path
from tkinter import *
from PIL import Image, ImageTk
import copy
from pathlib import Path
import shlex, subprocess

#pal palette
a8_palette = [	                (  0,  0,  0),( 33, 33, 33),( 75, 75, 75),(107,107,107),(132,132,132),(164,164,164),(206,206,206),(255,255,255), # black   0 -  15
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
		#distance = abs((r*r+g*g+b*b) - (rp*rp+gp*gp+bp*bp))
		distance = abs(pow(r-rp,2)+pow(g-gp,2)+pow(b-bp,2))
		if distance < min:
			min = distance
			min_index = i
	return min_index * 2

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


def find_rgb_color(Color_A8):
    Hue_RGB = {0:"#000000",2:"#212121",4:"#4b4b4b",6:"#6b6b6b",8:"#848484",10:"#a4a4a4",12:"#cecece",14:"#efefef",
               16:"#440000",18:"#681700",20:"#863700",22:"#ad5b00",24:"#c4741f",26:"#e69d3e",28:"#fabf65",30:"#ffde8c",
               32:"#4f0000",34:"#760500",36:"#98281a",38:"#b84a3b",40:"#d96153",42:"#f38e7c",44:"#fdae9d",46:"#ffcebd",
               48:"#5b0000",50:"#85002c",52:"#9e184b",54:"#c0416c",56:"#dc5784",58:"#ff7daf",60:"#fd9bce",62:"#fbc6f0",
               64:"#550033",66:"#76015a",68:"#900e7b",70:"#bc3a9c",72:"#d551b7",74:"#f774de",76:"#ff91ff",78:"#ffbaff",
               80:"#380167",82:"#68028a",84:"#8510ac",86:"#a23ed6",88:"#b855ee",90:"#eb70fc",92:"#fc96f9",94:"#ffbaff",
               96:"#24008b",98:"#4300b0",100:"#6318cd",102:"#8945f4",104:"#a659fd",106:"#c679fb",108:"#e09dfa",110:"#ffc5ff",
               112:"#05008e",114:"#0119ad",116:"#2437d1",118:"#4761f2",120:"#647cff",122:"#869eff",124:"#a3bcfe",126:"#cee8f9",
               128:"#000067",130:"#003380",132:"#0554b0",134:"#2d71d6",136:"#4694e9",138:"#67b6ff",140:"#86d9ff",142:"#abffff",
               144:"#00202f",146:"#044153",148:"#006679",150:"#1e8b9f",152:"#31a5b2",154:"#5fc3da",156:"#7de8f2",158:"#a3fbfd",
               160:"#002b00",162:"#005020",164:"#007741",166:"#4761f2",168:"#33ac83",170:"#56d4a5",172:"#77f7c7",174:"#a5fbee",
               176:"#003300",178:"#005700",180:"#057c08",182:"#32a003",184:"#32a003",186:"#67dc3e",188:"#8bfe61",190:"#b8fe81",
               192:"#002a00",194:"#005000",196:"#277300",198:"#4f8e0b",200:"#60b000",202:"#65a70f",204:"#aff44c",206:"#d2fd67",
               208:"#001a00",210:"#4b6300",212:"#4f6115",214:"#68840b",216:"#849c00",218:"#acc61b",220:"#cee53b",222:"#edfe60",
               224:"#220000",226:"#4a2800",228:"#695300",230:"#8a730b",232:"#a8890c",234:"#d2b325",236:"#edd946",238:"#fff569",
               240:"#3e0000",242:"#651700",244:"#7e3a09",246:"#a95d00",248:"#c3761e",250:"#eb9936",252:"#febb62",254:"#fee185"}
    return (Hue_RGB[Color_A8])

def cga_quantize(image):
    
    pal_image= Image.new("P", (1,1))
    #pal_image.putpalette( (16,16,16, 32,32,32, 64,64,64, 128,128,128) + (0,0,0)*252)
    c0r=a8_palette[int(140/2)][0]
    c0g=a8_palette[int(140/2)][1]
    c0b=a8_palette[int(140/2)][2]
    c1r=a8_palette[int(92/2)][0]
    c1g=a8_palette[int(92/2)][1]
    c1b=a8_palette[int(92/2)][2]
    c2r=a8_palette[int(50/2)][0]
    c2g=a8_palette[int(50/2)][1]
    c2b=a8_palette[int(50/2)][2]
    c3r=a8_palette[int(24/2)][0]
    c3g=a8_palette[int(24/2)][1]
    c3b=a8_palette[int(24/2)][2]
    pal_image.putpalette((c0r, c0g, c0b, c1r, c1g, c1b, c2r, c2g, c2b, c3r, c3g, c3b ) + (0,0,0)*252)
    return image.convert("RGB").quantize(palette=pal_image)

# get configuration with previous working directory and parameters
config = configparser.RawConfigParser()

def init():
    'Create a configuration file if does not exist'
    config.add_section('InputImage')
    config.set('InputImage', 'Directory', './')
    config.set('InputImage', 'Filename', '*.gif')
    config.add_section('Output')
    config.set('Output', 'AnticMode', '5')
    config.set('Output', 'SkipColumn', '0')
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
global antic_mode
antic_mode = config.get('Output', 'AnticMode')
global skip_column
skip_column = config.get('Output', 'SkipColumn', fallback='0')
#------------------------------------------------------------------------

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


#------------------------------------------------------------
def update(section, key, value):
    #Update config using section key and the value to change
    #call this when you want to update a value in configuation file
    # with some changes you can save many values in many sections
    config.set(section, key, value )
    with open('image2antic.cfg', 'w') as output:
        config.write(output)
#------------------------------------------------------------

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
    
def process_cc65_code():
    global input_filename
    global antic_mode
    print("processing...")
    rgb_im = img.convert("RGB")
    global working_directory
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
        "4" : {"colors" : 4, "display_mode" : "text", "columns" : 40, "lines" : 24, "char_width" : 4, "char_height" : 8, "dl" : "DL_CHR40x8x4"},
        "5" : {"colors" : 4, "display_mode" : "text", "columns" : 40, "lines" : 12, "char_width" : 4, "char_height" : 8, "dl" : "DL_CHR40x16x4"}
    }
    segments_file_text = ""
    atari_cfg_memory = ""
    atari_cfg_segments = ""
    atari_main_c_definitions = ""
    atari_main_c_dl_array = ""
    charsets_mem_list = []
    w, h = img.size
    if (skip_column == "1"):
        rgb_im = rgb_im.resize((int(w/2), h), resample = 0)
        w = int(w/2)
        rgb_im.show()
    mode_to_bpp = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}
    d = mode_to_bpp[img.mode]

    # arrange an array of ANTIC COLOR TEXT mode 4x8 tiles
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
                # reduce byte size in case exceeded byte size due to additional colors.
                while (tiles[i,j,y] > 255):
                    tiles[i,j,y]-=256
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
    for j in range(antic_target_modes[antic_mode]["lines"]): #range(round(h/8)): 
        if (chars_index > 87):
            charset_index = charset_index + 1
            chars_index = 0
            for y in range(8):
                temp_char[y] = 0
            chars[charset_index, chars_index] = copy.deepcopy(temp_char)
            chars_index = chars_index + 1
            charset_dli_change.append(j - 1)
        for i in range (antic_target_modes[antic_mode]["columns"]):
            if ((i < round(w/4)) and (j < round(h/8))):
                fifth_color = 0
                for y in range (8):
                    temp_char[y] = 0
                    for x in range (4):
                        r, g, b = rgb_im.getpixel((i*4+x, j*8+y))
                        pixel = rgb_colors.index((r,g,b))
                            
                        temp_char[y] = temp_char[y] + (pixel << (6-2*x))
                    
                    while (temp_char[y] > 255):
                        fifth_color = 1
                        temp_char[y]-=256

                char_exists = False
                for char in chars:
                    if char[0] == charset_index and chars[char] == temp_char:
                        char_exists = True
                        chars_reuse = chars_reuse + 1
                        screen[i,j] = char[1]
                        if (fifth_color == 0):
                            screen[i,j] += 128
                    
                if (not char_exists):
                    chars_count = chars_count + 1
                    chars[charset_index, chars_index] = copy.deepcopy(temp_char)
                    screen[i,j] = chars_index
                    if (fifth_color == 0):
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

    print ("generate screen_data")
    print(screen)
    for j in range(antic_target_modes[antic_mode]["lines"]):
        for i in range (antic_target_modes[antic_mode]["columns"]):
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
    atari_main_c_dl_array = atari_main_c_dl_array + "	DL_LMS("+antic_target_modes[antic_mode]["dl"]+"),\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "	0x00,\n"
    atari_main_c_dl_array = atari_main_c_dl_array + "	SCREEN_MEM >> 8,\n"
    for i in range(1,int(antic_target_modes[antic_mode]["lines"])):
        if i in charset_dli_change:
            atari_main_c_dl_array = atari_main_c_dl_array + "	DL_DLI("+antic_target_modes[antic_mode]["dl"]+"),\n"
        else:
            atari_main_c_dl_array = atari_main_c_dl_array + "	"+antic_target_modes[antic_mode]["dl"]+",\n"
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
    color3 = yet_another_a8_palette[4][0] * 16 + yet_another_a8_palette[4][1]
    print(color0, color1, color2, color3, color4)
    
    mainCTemplateFile = open("sources_templates/main.c", "r")
    main_c_file = mainCTemplateFile.read().replace("##ATARI_MAIN_C_DEFINITIONS##", atari_main_c_definitions).replace("##ATARI_MAIN_C_DL_ARRAY##", atari_main_c_dl_array).replace("##CHARSETS_MEM##", str(charsets_mem_str)).replace("##COLOR0##", str(color0)).replace("##COLOR1##", str(color1)).replace("##COLOR2##", str(color2)).replace("##COLOR3##", str(color3)).replace("##COLOR4##", str(color4))
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
        self.resizable(width=False, height=False)
        self.grid_columnconfigure(index = 1, minsize = 640)
        #self.wm_iconbitmap('icon.ico')
 
        self.previewFrame = ttk.LabelFrame(self, text = "Convert An Image To Atari 800XL CC65 Source", width = 560, height = 192)
        self.previewFrame.grid(sticky = "NSEW", column = 1, row = 1, padx = 20, pady = 20)
        
        self.previewTopLabel = ttk.Label(self.previewFrame, text = "Source Image Preview", width = 25)
        self.previewTopLabel.grid(column = 1, row = 1, padx = 20, pady = 20)

        self.previewLabel = ttk.Label(self.previewFrame, text = "Browse to choose an image", width = 25, background = "white")
        self.previewLabel.grid(column = 1, row = 2, rowspan = 5, padx = 20, pady = 20)
        
        self.imageColors = ttk.Label(self.previewFrame, text = "RGB Colors")
        self.imageColors.grid(sticky = "W", column = 1, row = 1, columnspan = 2, padx = 20)
        self.imageColor0 = ttk.Label(self.previewFrame, background = "red", width = 3)
        self.imageColor0.grid(column = 2, row = 2, pady = 3, padx = 20)
        self.imageColor1 = ttk.Label(self.previewFrame, background = "green", width = 3)
        self.imageColor1.grid(column = 2, row = 3, pady = 3, padx = 20)
        self.imageColor2 = ttk.Label(self.previewFrame, background = "blue", width = 3)
        self.imageColor2.grid(column = 2, row = 4, pady = 3, padx = 20)
        self.imageColor3 = ttk.Label(self.previewFrame, background = "black", width = 3)
        self.imageColor3.grid(column = 2, row = 5, pady = 3, padx = 20)
        self.imageColor4 = ttk.Label(self.previewFrame, background = "black", width = 3)
        self.imageColor4.grid(column = 2, row = 6, pady = 3, padx = 20)
        self.imageColorValue0 = ttk.Label(self.previewFrame, text = "#FF0000")
        self.imageColorValue0.grid(column = 3, row = 2)
        self.imageColorValue1 = ttk.Label(self.previewFrame, text = "#00FF00")
        self.imageColorValue1.grid(column = 3, row = 3)
        self.imageColorValue2 = ttk.Label(self.previewFrame, text = "#0000FF")
        self.imageColorValue2.grid(column = 3, row = 4)
        self.imageColorValue3 = ttk.Label(self.previewFrame, text = "#000000")
        self.imageColorValue3.grid(column = 3, row = 5)
        self.imageColorValue4 = ttk.Label(self.previewFrame, text = "#000000")
        self.imageColorValue4.grid(column = 3, row = 6)

        self.imageSize = ttk.Label(self.previewFrame, text = "Size: 0, 0")
        self.imageSize.grid(sticky = "W", column = 4, row = 6, columnspan = 2, padx = 20, pady = 3)

        self.chooseImage = ttk.Label(self.previewFrame, text = "Choose Image")
        self.chooseImage.grid(sticky = "W", column = 4, row = 2, columnspan = 1, padx = 20, pady = 3)
        
        self.browseButton()
 
    # label frame for output file settings

        self.outputPreviewLabel = ttk.Label(self.previewFrame, text = "Browse to choose an image", width = 25, background = "white")
        self.outputPreviewLabel.grid(column = 1, row = 10, rowspan = 7, padx = 20, pady = 20)
        
        self.outputImageColors = ttk.Label(self.previewFrame, text = "A8 Colors (PAL)")
        self.outputImageColors.grid(sticky = "W", column = 2, row = 11, columnspan = 2)
        self.outputImageColor0 = ttk.Label(self.previewFrame, background = find_rgb_color(find_nearest_color(255,0,0)), width = 3)
        self.outputImageColor0.grid(column = 2, row = 12, pady = 3)
        self.outputImageColor1 = ttk.Label(self.previewFrame, background = find_rgb_color(find_nearest_color(0,255,0)), width = 3)
        self.outputImageColor1.grid(column = 2, row = 13, pady = 3)
        self.outputImageColor2 = ttk.Label(self.previewFrame, background = find_rgb_color(find_nearest_color(0,0,255)), width = 3)
        self.outputImageColor2.grid(column = 2, row = 14, pady = 3)
        self.outputImageColor3 = ttk.Label(self.previewFrame, background = find_rgb_color(find_nearest_color(0,0,0)), width = 3)
        self.outputImageColor3.grid(column = 2, row = 15, pady = 3)
        self.outputImageColor4= ttk.Label(self.previewFrame, background = find_rgb_color(find_nearest_color(0,0,0)), width = 3)
        self.outputImageColor4.grid(column = 2, row = 16, pady = 3)
        self.outputImageColorValue0 = ttk.Label(self.previewFrame, text = hex(find_nearest_color(255,0,0)) + "(" + str(find_nearest_color(255,0,0)) + ")")
        self.outputImageColorValue0.grid(column = 3, row = 12)
        self.outputImageColorValue1 = ttk.Label(self.previewFrame, text = hex(find_nearest_color(0,255,0)) + "(" + str(find_nearest_color(0,255,0)) + ")")
        self.outputImageColorValue1.grid(column = 3, row = 13)
        self.outputImageColorValue2 = ttk.Label(self.previewFrame, text = hex(find_nearest_color(0,0,255)) + "(" + str(find_nearest_color(0,0,255)) + ")")
        self.outputImageColorValue2.grid(column = 3, row = 14)
        self.outputImageColorValue3 = ttk.Label(self.previewFrame, text = hex(find_nearest_color(0,0,0)) + "(" + str(find_nearest_color(0,0,0)) + ")")
        self.outputImageColorValue3.grid(column = 3, row = 15)
        self.outputImageColorValue4 = ttk.Label(self.previewFrame, text = hex(find_nearest_color(0,0,0)) + "(" + str(find_nearest_color(0,0,0)) + ")")
        self.outputImageColorValue4.grid(column = 3, row = 16)

        self.outputImageSize = ttk.Label(self.previewFrame, text = "Size: 0, 0")
        self.outputImageSize.grid(sticky = "W", column = 4, row = 16, columnspan = 2)
        
        
        antic_modes = [("Text 4 (40x24,4 colors)", 1, "4"), ("Text 5 (40x12,4 colors)", 2, "5"),]

        global antic_mode
        self.rb_antic_mode = StringVar()
        self.rb_antic_mode.set(antic_mode)

        
        # antic_mode_changed - update config file and global variable
        def antic_mode_changed(*args):
            global antic_mode
            antic_mode = self.rb_antic_mode.get()
            update("Output", "anticmode", antic_mode)
    
        
        self.rb_antic_mode.trace("w", antic_mode_changed)
        for text, num, mode in antic_modes:
            self.anticRadioButtons = ttk.Radiobutton(self.previewFrame, text=text, variable=self.rb_antic_mode, value=mode)
            self.anticRadioButtons.grid(column = 4, row = num + 10, padx = 20, pady = 5)

        # skip odd columns for processing images designed for Antic 4 with 2x1 pixel ratio.
        def skip_column_changed(*args):
            global skip_column
            skip_column = self.rb_skip_column.get()
            update("Output", "skip_column", skip_column)
            
        global skip_column
        self.rb_skip_column = StringVar()
        self.rb_skip_column.set(skip_column)
        self.rb_skip_column.trace("w", skip_column_changed)
        
        self.skipColumnCheckBox = ttk.Checkbutton(self.previewFrame, text = "Skip column (Antic 4 compatibility)", variable = self.rb_skip_column)
        self.skipColumnCheckBox.grid(column = 4, row = 14, padx = 20, pady = 5, sticky = "W")

        interleave = IntVar()
        
        self.interleaveCheckBox = ttk.Checkbutton(self.previewFrame, text = "Interleave", variable = interleave)
        self.interleaveCheckBox.grid(column = 4, row = 15, padx = 20, pady = 5, sticky = "W")
        
        self.processButton()

        
    # browse button to open a file browser on click
    def browseButton(self):
        self.browseButton = ttk.Button(self.previewFrame, text = "Browse",command = self.fileDialog)
        self.browseButton.grid(column = 4, row = 6, sticky="E", padx = 20, pady = 20)
        
    # browse button to begin output process
    def processButton(self):
        self.processButton = ttk.Button(self.previewFrame, text = "Process",command = process_cc65_code)
        self.processButton.grid(column = 4, row =16, sticky="E", padx = 20, pady = 20)

        
    def showImg(self):
        load = Image.open(input_directory+'/'+input_filename)
        load.thumbnail((160, 96), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        self.previewLabel.configure(image = render, text = "", width = 200)
        self.previewLabel.image = render
        #self.previewLabel.place(x=0, y=0)

    # when invoked, open the image and extract information on it
    def imageViewer(self):
        global input_directory
        global input_filename
        global img
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
        global yet_another_a8_palette
        yet_another_a8_palette = []
        for j in range(h):
            for i in range(w):
                r, g, b = rgb_im.getpixel((i, j))
                if ((r,g,b) not in rgb_colors):
                    rgb_colors.append((r,g,b))
                    find_pal_color(r,g,b)
                    yet_another_a8_palette.append((Hue_A8, Lum_A8))
        print(rgb_colors)
        #self.imageParamsLabel.configure(text = "Image Format: "+ img.format+"\nwidth:  "+str( w) + "\nheight: "+str(h)+"\ndepth: "+str(d) + "\nNumber of colors: " + str(len(colors)) + str(colors) + "\nPalette (RGB): " + str(rgb_colors) + "\nPalette (A8): " + str(yet_another_a8_palette))
        if (len(yet_another_a8_palette) < 6):
            for i in range (len(yet_another_a8_palette), 6):
                rgb_colors.append((0,0,0))
                yet_another_a8_palette.append((0, 0))

        # now create the ImageTk PhotoImage:
        self.showImg()
        
        self.imageColor0.configure(background = rgb_to_hex(rgb_colors[0]))
        self.imageColor1.configure(background = rgb_to_hex(rgb_colors[1]))
        self.imageColor2.configure(background = rgb_to_hex(rgb_colors[2]))
        self.imageColor3.configure(background = rgb_to_hex(rgb_colors[3]))
        self.imageColor4.configure(background = rgb_to_hex(rgb_colors[4]))

        self.imageColorValue0.configure(text = rgb_to_hex(rgb_colors[0]))
        self.imageColorValue1.configure(text = rgb_to_hex(rgb_colors[1]))
        self.imageColorValue2.configure(text = rgb_to_hex(rgb_colors[2]))
        self.imageColorValue3.configure(text = rgb_to_hex(rgb_colors[3]))
        self.imageColorValue4.configure(text = rgb_to_hex(rgb_colors[4]))

        self.outputImageColor0.configure(background = find_rgb_color(yet_another_a8_palette[0][0]*16+yet_another_a8_palette[0][1]))
        self.outputImageColor1.configure(background = find_rgb_color(yet_another_a8_palette[1][0]*16+yet_another_a8_palette[1][1]))
        self.outputImageColor2.configure(background = find_rgb_color(yet_another_a8_palette[2][0]*16+yet_another_a8_palette[2][1]))
        self.outputImageColor3.configure(background = find_rgb_color(yet_another_a8_palette[3][0]*16+yet_another_a8_palette[3][1]))
        self.outputImageColor4.configure(background = find_rgb_color(yet_another_a8_palette[4][0]*16+yet_another_a8_palette[4][1]))

        self.outputImageColorValue0.configure(text = hex(yet_another_a8_palette[0][0]*16+yet_another_a8_palette[0][1]) + "(" + str(yet_another_a8_palette[0][0]*16+yet_another_a8_palette[0][1]) + ")")
        self.outputImageColorValue1.configure(text = hex(yet_another_a8_palette[1][0]*16+yet_another_a8_palette[1][1]) + "(" + str(yet_another_a8_palette[1][0]*16+yet_another_a8_palette[1][1]) + ")")
        self.outputImageColorValue2.configure(text = hex(yet_another_a8_palette[2][0]*16+yet_another_a8_palette[2][1]) + "(" + str(yet_another_a8_palette[2][0]*16+yet_another_a8_palette[2][1]) + ")")
        self.outputImageColorValue3.configure(text = hex(yet_another_a8_palette[3][0]*16+yet_another_a8_palette[3][1]) + "(" + str(yet_another_a8_palette[3][0]*16+yet_another_a8_palette[3][1]) + ")")
        self.outputImageColorValue4.configure(text = hex(yet_another_a8_palette[4][0]*16+yet_another_a8_palette[4][1]) + "(" + str(yet_another_a8_palette[4][0]*16+yet_another_a8_palette[4][1]) + ")")

        preview_a8 = img.convert('RGB')
        preview_a8 = cga_quantize(preview_a8)
        preview_a8.thumbnail((160, 96), Image.ANTIALIAS)
        preview_render = ImageTk.PhotoImage(preview_a8)
        self.outputPreviewLabel.configure(image = preview_render, text = "", width = 200)
        self.outputPreviewLabel.image = preview_render

        self.imageSize.configure(text = "Size: " + str(w)+", "+str(h))

    # file dialog for choosing our image 2 antic file
    def fileDialog(self):
        global input_directory
        global input_filename
        self.filename =  filedialog.askopenfilename(initialdir = input_directory,title = "Select file",filetypes = (("all files","*.*"),("GIF files","*.gif"),("PNG files","*.png")))
        #self.label = ttk.Label(self.labelFrame, text = "")
        #self.label.grid(column = 1, row = 2)
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
