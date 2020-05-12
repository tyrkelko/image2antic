/************************************************
** Image to Antic CC65 code		       **
** Generated with image2antic.py               **
** https://github.com/tyrkelko/image2antic     **
************************************************/
#include <atari.h>
#include <string.h>
##ATARI_MAIN_C_DEFINITIONS##

unsigned char charset_array[] = {
##CHARSETS_MEM##
};

##ATARI_MAIN_C_DL_ARRAY##

unsigned char charset_index;
unsigned char charset_array_size;
unsigned char i;
unsigned int screen_pos;
unsigned char vblank_counter;

void erase_sprite(void);
void update_sprite(void);
void draw_sprite(void);
void handle_input (void);
void wait_for_vblank(void);
void setup_dli(void);
void dli_routine(void);

void main(void)
{
	charset_index = 0;
	screen_pos = 0;

	// SHUT DOWN ANTIC
	OS.sdmctl = 0;

	// CREATE SCREEN
	memcpy((void*) DLIST_MEM,antic4_display_list,sizeof(antic4_display_list));
	OS.sdlst=(void*)DLIST_MEM;

	// SET COLORS
	OS.color0 = ##COLOR0##;
	OS.color1 = ##COLOR1##;
	OS.color2 = ##COLOR2##;
	OS.color3 = ##COLOR3##;
	OS.color4 = ##COLOR4##;

	charset_array_size = sizeof(charset_array) + ##CHARSET_INDEX##;
	setup_dli();
	wait_for_vblank();
	ANTIC.nmien = NMIEN_DLI | NMIEN_VBI; 

	OS.sdmctl = 0x3E;
	// GAME LOOP
	while (1) {
		wait_for_vblank();
		erase_sprite();
		handle_input();
		update_sprite();
		draw_sprite();
	};
}

void wait_for_vblank(void)
{
    asm("lda $14");
wvb:
    asm("cmp $14");
    asm("beq %g", wvb);
    --vblank_counter;
} 
void dli_routine(void)
{
    asm("pha");
    asm("tya");
    asm("pha");
    asm("tya");
    asm("pha");
    ANTIC.chbase = charset_array[charset_index];
    ++charset_index;
    if (charset_index >= charset_array_size)
    	charset_index = 0;
    ANTIC.wsync = 1;
    asm("pla");
    asm("tay");
    asm("pla");
    asm("tax");
    asm("pla");
    asm("rti");
}

void setup_dli(void)
{
	wait_for_vblank();
    OS.vdslst = &dli_routine;
}
void erase_sprite() {
	// ERASE SPRITE
}
void update_sprite() {
	// TODO: UPDATE SPRITE
    ##MAIN_C_UPDATE##
}
void draw_sprite() {
	// TODO: DRAW SPRITE
    ##MAIN_C_DRAW##
}
void handle_input (void)
{
 // TODO: HANDLE INPUT
}
