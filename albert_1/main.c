/************************************************
** Image to Antic CC65 code		       **
** Generated with image2antic.py               **
** https://github.com/tyrkelko/image2antic     **
************************************************/
#include <atari.h>
#include <string.h>

#define CHARSET0_MEM	0x5000
#define CHARSET1_MEM	0x5400
#define SCREEN_MEM	0x7000
#define DLIST_MEM		0x6C00	// aligned to 1K
//extern unsigned char *L_DLIST_MEM;
extern unsigned char *L_SCREEN_MEM;
extern unsigned char *L_CHARSET0_MEM;
extern unsigned char *L_CHARSET1_MEM;


unsigned int charset_array[] = {CHARSET0_MEM, CHARSET1_MEM};

// CHARSET DLI CHANGES IN LINES: [0, 6]
unsigned char antic4_display_list[] = {
	DL_BLK8,
	DL_BLK8,
	DL_DLI(DL_BLK8),
	DL_LMS(DL_CHR40x16x4),
	0x00,
	SCREEN_MEM >> 8,
	DL_CHR40x16x4,
	DL_CHR40x16x4,
	DL_CHR40x16x4,
	DL_CHR40x16x4,
	DL_CHR40x16x4,
	DL_DLI(DL_CHR40x16x4),
	DL_CHR40x16x4,
	DL_CHR40x16x4,
	DL_CHR40x16x4,
	DL_CHR40x16x4,
	DL_CHR40x16x4,
	DL_JVB,
	0x00,
};


unsigned char charset_index = 0;

void erase_sprite(void);
void update_sprite(void);
void draw_sprite(void);
void handle_input (void);
void wait_for_vblank(void);
void setup_dli(void);
void dli_routine_0(void);
void dli_routine_1(void);

void main(void)
{
	// CREATE SCREEN
	memcpy((void*) DLIST_MEM,antic4_display_list,sizeof(antic4_display_list));
	OS.sdlst=(void*)DLIST_MEM;

	// SET COLORS
	OS.color0 = 138;
	OS.color1 =  28;
	OS.color2 = 24;
	OS.color3 = 126;
	OS.color4 = 132;

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
} 
void dli_routine_0(void)
{
    asm("pha");
    asm("tya");
    asm("pha");
    asm("tya");
    asm("pha");
    ANTIC.chbase = charset_array[charset_index] >> 8;
    ANTIC.wsync = 1;
    charset_index++;
    if (charset_index > 1) charset_index = 0;
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
    OS.vdslst = &dli_routine_0;
}
void erase_sprite() {
	// ERASE SPRITE
}
void update_sprite() {
	// TODO: UPDATE SPRITE
}
void draw_sprite() {
	// TODO: DRAW SPRITE
}
void handle_input (void)
{
 // TODO: HANDLE INPUT
}
