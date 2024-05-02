/*
 Hive Colony Framework
 Copyright (c) 2008-2020 Hive Solutions Lda.

 This file is part of Hive Colony Framework.

 Hive Colony Framework is free software: you can redistribute it and/or modify
 it under the terms of the Apache License as published by the Apache
 Foundation, either version 2.0 of the License, or (at your option) any
 later version.

 Hive Colony Framework is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 Apache License for more details.

 You should have received a copy of the Apache License along with
 Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

 __author__    = João Magalhães <joamag@hive.pt>
 __copyright__ = Copyright (c) 2008-2020 Hive Solutions Lda.
 __license__   = Apache License, Version 2.0
*/

#include "stdafx.h"

#ifdef COLONY_PLATFORM_WIN32

#include "print_win32.h"

HDC get_default_printer(char *name, int width, int height) {
    return get_printer(name, width, height);
}

HDC get_printer(char *name, int width, int height) {
    /* allocates space for the dev mode related
    structures used to customize the default values
    of the printing operation */
    HANDLE printer;
    LONG dev_mode_size;
    PDEVMODEA dev_mode;

    /* allocates space for the flag that will
    define if the dimension values should be set */
    unsigned char set_values;

    /* allocates a new buffer in the stack
    and then set a long variable with the size
    of it to be used in the printer call */
    char buffer[BUFFER_SIZE];
    unsigned long size = BUFFER_SIZE;

    /* creates the array of definitions to the default
    values of the printer */
    PRINTER_DEFAULTS printer_defaults = {
        NULL, NULL, PRINTER_ACCESS_USE
    };

    /* checks if the default value should be set (they
    are both valid values) */
    set_values = width > 0 && height > 0;

    /* retrieves the default printer and then
    and then uses it to create the appropriate context */
    if(name == NULL) { GetDefaultPrinter(buffer, &size); }
    else { memcpy(buffer, name, strlen(name) + 1); }
    OpenPrinter(name == NULL ? buffer : name, &printer, &printer_defaults);

    /* tries to retrieve empty document properties to
    "gather" the size of the underlying structure and then
    allocates the associated dev mode */
    dev_mode_size = DocumentProperties(NULL, printer, buffer, NULL, NULL, 0);
    if(dev_mode_size < 0) { return NULL; }
    dev_mode = (PDEVMODEA) LocalAlloc(LPTR, dev_mode_size);

    /* retrieves the current print dev mode structure (out mode)
    then updates the structure with the default values and set
    these values again in the dev structure and then create the
    drawing context for the "resulting" printer */
    DocumentProperties(NULL, printer, buffer, dev_mode, NULL, DM_OUT_BUFFER);
    dev_mode->dmPaperSize = DMPAPER_USER;
    dev_mode->dmPaperLength = height;
    dev_mode->dmPaperWidth = width;
    dev_mode->dmFields = DM_PAPERSIZE | DM_PAPERLENGTH | DM_PAPERWIDTH;
    if(set_values) {
        DocumentProperties(NULL, printer, buffer, dev_mode, dev_mode, DM_IN_BUFFER | DM_OUT_BUFFER);
    }
    HDC handle_printer = CreateDC("WINSPOOL\0", buffer, NULL, dev_mode);

    /* releases the dev mode structure and then closes the printer
    structure releasing all its internal values */
    LocalFree(dev_mode);
    ClosePrinter(printer);

    /* retrieves the just created context */
    return handle_printer;
}

BOOL show_print_dialog(PRINTDLG *print_dialog_pointer) {
    /* populates the print dialog structure
    with the appropriate values */
    print_dialog_pointer->lStructSize = sizeof(PRINTDLG);
    print_dialog_pointer->hwndOwner = NULL;
    print_dialog_pointer->hDevMode = NULL;
    print_dialog_pointer->hDevNames = NULL;
    print_dialog_pointer->Flags = PD_USEDEVMODECOPIESANDCOLLATE | PD_RETURNDC;
    print_dialog_pointer->nCopies = 1;
    print_dialog_pointer->nFromPage = 0xffff;
    print_dialog_pointer->nToPage = 0xffff;
    print_dialog_pointer->nMinPage = 1;
    print_dialog_pointer->nMaxPage = 0xffff;

    /* shows the print dialog and then retrieves
    the result of the execution of it, returning it
    to the caller function */
    BOOL result = PrintDlg(print_dialog_pointer);
    return result;
}

#ifdef __cplusplus
extern "C" {
#endif

const char *pformat() {
    return NPCOLONY_BINIE;
}

void pdevices(struct device_t **devices_p, size_t *devices_c) {
    /* allocates the various variables that are going to be
    used for the creation of the devices' structure buffer */
    size_t index;
    struct device_t *device;
    struct device_t *devices;
    DWORD count = 0;
    DWORD size = 0;
    DWORD level = 2;
    PRINTER_INFO_2 *sequence;
    char default_printer[BUFFER_SIZE];
    unsigned long buffer_size = BUFFER_SIZE;

    /* obtains the name of the default printer so that we
    can then use it to compare to the enumeration and determine
    if the printer is the default one or not */
    GetDefaultPrinter(default_printer, &buffer_size);

    /* runs the initial printers' enumeration to uncover the
    size of the list to be retrieved and then allocate the
    appropriate space for the buffer */
    EnumPrinters(
        PRINTER_ENUM_LOCAL,
        NULL,
        level,
        NULL,
        0,
        &size,
        &count
    );
    sequence = (PRINTER_INFO_2 *) malloc(size);

    /* enumerates the printing devices again for the sequence
    buffer to be populated with the correct values */
    EnumPrinters(
        PRINTER_ENUM_LOCAL,
        NULL,
        level,
        (LPBYTE) sequence,
        size,
        &size,
        &count
    );

    /* allocates space for the devices' structure according to the
    number of devices loaded into the sequence and then iterates
    over the sequence to create the various device structures */
    devices = (struct device_t *) malloc(sizeof(struct device_t) * count);
    memset(devices, 0, sizeof(struct device_t) * count);
    for(index  = 0; index < count; index++) {
        device = &devices[index];
        char *name = sequence[index].pPrinterName;
        size_t name_s = strlen(name);
        memcpy(device->name, name, name_s);
        device->name_s = name_s;
        device->is_default = !strcmp(device->name, default_printer) ? 1 : 0;
    }

    /* releases the memory from the sequence buffer and avoids any
    memory leaks, it's not going to be used anymore */
    free(sequence);

    /* updates the devices pointer and the number of devices
    that have been created (output variables) */
    *devices_p = devices;
    *devices_c = count;
}

int print(
    bool show_dialog,
    struct job_t *config,
    char *data,
    size_t size
) {
    return print_printer(show_dialog, NULL, config, data, size);
}

int print_printer(
    bool show_dialog,
    char *printer,
    struct job_t *config,
    char *data,
    size_t size
) {
    /* reserves space for the printing context to be
    used in the current operation */
    HDC context;

    /* allocates space for the buffer to be used during
    the parsing stage */
    char *buffer = NULL;

    /* in case the data buffer was sent, we should be
    reading the data from there */
    if(data) {
        /* sets the data pointer as the buffer to be
        used for the parsing */
        buffer = data;
    }
    /* otherwise, the data must be read from the local
    file system */
    else {
        /* creates the file object reference and opens
        the target (default) file */
        FILE *file;
        fopen_s(&file, "default.binie", "rb");

        /* retrieves the size of the file by seeking
        to the end of it and then retrieving the offset */
        fseek(file, 0, SEEK_END);
        size_t size = ftell(file);
        fseek(file, 0, SEEK_SET);

        /* allocates space for the buffer to hold the binie
        document file and then reads it into it, closing the
        file afterward */
        buffer = (char *) malloc(size);
        fread(buffer, sizeof(char), size, file);
        fclose(file);
    }

    /* casts the initial part of the buffer into a document
    header element */
    struct document_header_t *document_header =\
        (struct document_header_t *) buffer;

    /* in case the printer dialog is meant to be shown
    the proper show dialog function must be called*/
    if(show_dialog) {
        /* allocates and resets the print dialog structure
        according to the windows rules */
        PRINTDLG print_dialog;
        ZeroMemory(&print_dialog, sizeof(PRINTDLG));
        BOOL result = show_print_dialog(&print_dialog);
        if(!result) { return -1; }
        context = print_dialog.hDC;
    }
    /* otherwise, the requested printer is retrieved */
    else {
        /* retrieves the requested printer as the
        the default context for printing */
        context = get_printer(
            printer,
            document_header->width,
            document_header->height
        );
    }

    /* declares a document information structure
    and populate it */
    DOCINFO document_information;
    document_information.cbSize = sizeof(DOCINFO);
    document_information.lpszDocName = document_header->title;
    if(config == NULL || config->output_path == NULL) {
        document_information.lpszOutput = NULL;
    } else {
        document_information.lpszOutput = config->output_path;
    }
    document_information.fwType = 0;

    /* builds the document information and prints
    it on finishing it (print on closed document) */
    StartDoc(context, &document_information);
    StartPage(context);

    /* sets the map mode of the document to twips */
    SetMapMode(context, MM_TWIPS);

    /* creates a new (drawing) pen for the document to
    be used in the drawing process of it */
    HANDLE pen = CreatePen(0, FONT_SCALE_FACTOR, 0);
    SelectObject(context, pen);

    /* retrieves the initial document element  header */
    struct element_header_t *element_header =\
        (struct element_header_t *) (buffer + sizeof(struct document_header_t));

    /* retrieves the various characteristics of the media for
    the current context so that the size and the density values
    are retrieved as they are going to be used in the print operation */
    int vertical_res = GetDeviceCaps(context, VERTRES);
    int pixel_density = GetDeviceCaps(context, LOGPIXELSY);
    int vertical_size = (int) ((float) vertical_res / pixel_density * MM_PER_INCH);

    /* start the current page value at the initial value
    and the vertical offset that is going to be added for
    the new pages that are going to be incremented */
    int current_page = 0;
    int page_offset = 0;

    /* iterates over the element count in the document to
    process it and generate the correct print instructions */
    for(size_t index = 0; index < document_header->element_count; index++) {
        /* retrieves the type and length of the element */
        unsigned short element_type = element_header->type;
        unsigned int element_length = element_header->length;

        /* allocates space for the various elements to be used
        along the switch instruction */
        SIZE text_size;
        RECT clip_box;
        RECT clip_box_pixel;
        HFONT font;
        int result;
        int text_x;
        int text_y;
        int text_y_bottom;
        double text_y_bottom_millimeter;
        int weight;
        char *text;
        char *image;
        wchar_t *text_unicode;
        struct text_element_header_t *text_element_header;
        struct image_element_header_t *image_element_header;
        char directory_buffer[1024];
        char path[MAX_PATH];
        int image_x;
        int image_y;
        int image_y_bottom;
        double image_y_bottom_millimeter;
        int previous_mode;
        double divisor;
        double multiplier;
        HDC image_context;
        HBITMAP handle_image;
        HANDLE handle_image_new;
        FILE *image_file;
        BITMAP bitmap;
        float scaled_width;
        float scaled_height;
        int new_page;
        double page_size_twips;
        char is_block;
        int page_delta = 0;

        /* switches over the element type to generate the
        appropriate print instructions */
        switch(element_type) {
            case TEXT_VALUE:
                /* "casts" the element header as text element header an retrieves
                the text part from it, then sets the default text weight as normal */
                text_element_header = (struct text_element_header_t *) element_header;
                text = (char *) text_element_header + sizeof(struct text_element_header_t);
                weight = FW_DONTCARE;

                /* in case the text weight is greater than zero, it's
                considered to be bold-sized */
                if(text_element_header->text_weight > 0) { weight = FW_BOLD; }

                /* creates the correct front to display the current text
                instruction, and then selects it */
                font = CreateFont(
                    text_element_header->font_size * FONT_SCALE_FACTOR,
                    0,
                    0,
                    0,
                    weight,
                    text_element_header->text_italic,
                    FALSE,
                    FALSE,
                    DEFAULT_CHARSET,
                    OUT_OUTLINE_PRECIS,
                    CLIP_DEFAULT_PRECIS,
                    DEFAULT_QUALITY,
                    VARIABLE_PITCH,
                    text_element_header->font
                );
                SelectObject(context, font);

                /* converts the text into the appropriate windows unicode
                representation (may represent all charset) */
                text_unicode = new wchar_t[lstrlen(text) + 1];
                result = MultiByteToWideChar(CP_UTF8, NULL, text, -1, text_unicode, lstrlen(text) + 1);

                /* retrieves the extension (size) of the text for the current
                font using the current settings and then retrieves the size of
                the current context (page) where it's going to be "drawn" */
                GetTextExtentPointW(context, text_unicode, lstrlenW(text_unicode), &text_size);
                GetClipBox(context, &clip_box);

                /* in case the block width and height are defined, a block is defined
                so the variable defining the block should be set */
                is_block = text_element_header->block_width != 0 && text_element_header->block_height != 0;

                /* in case the current text is defined inside a block, the
                clip box must be changed accordingly, these values are measured
                as twips and not millimeters (logical units) */
                if(is_block) {
                    clip_box.left = text_element_header->position_x;
                    clip_box.top = text_element_header->position_y * -1;
                    clip_box.right = text_element_header->position_x + text_element_header->block_width;
                    clip_box.bottom = (text_element_header->position_y + text_element_header->block_height) * -1;
                }

                /* calculates the text initial x position (deducting the margins)
                and using the current font scale factor */
                text_x = (text_element_header->margin_left - text_element_header->margin_right) * FONT_SCALE_FACTOR;

                /* in case the text-align is left */
                if(text_element_header->text_align == LEFT_TEXT_ALIGN_VALUE) {
                    text_x += clip_box.left;
                }
                /* in case the text-align is right */
                else if(text_element_header->text_align == RIGHT_TEXT_ALIGN_VALUE) {
                    text_x += clip_box.right - text_size.cx;
                }
                /* in case the text-align is left */
                else if(text_element_header->text_align == CENTER_TEXT_ALIGN_VALUE) {
                    text_x += clip_box.left + (clip_box.right - clip_box.left) / 2 - text_size.cx / 2;
                }

                /* sets the text y as the current position context y
                incremented by the clip box top position */
                text_y = clip_box.top + text_element_header->position.y;

                /* calculates the y position for the bottom position of the
                text and then converts it into a millimeter type, note that
                the resulting millimeter value is rounded to avoid problems
                with the sizes in the device driver (required) */
                text_y_bottom = is_block ? clip_box.bottom : text_y - text_size.cy;
                text_y_bottom_millimeter = (double) text_y_bottom / TWIPS_PER_INCH * MM_PER_INCH * -1.0;
                text_y_bottom_millimeter = ceil(text_y_bottom_millimeter * 100.0) / 100.0;

                /* uses the bottom position of the text in millimeters and
                divides (integer division) over the page size to check
                the current page number (index) */
                new_page = (int) (text_y_bottom_millimeter / vertical_size);

                /* checks if there is a new page for writing, in case
                there is a new page that must be "built" */
                if(new_page > current_page) {
                    /* ends the current page and starts a new
                    on (page break operation) */
                    EndPage(context);
                    StartPage(context);

                    /* calculates the size of the page size in twips units
                    and uses it to re-calculate the text y position, taking
                    into account the already "used" pages (modulus) */
                    page_size_twips = (vertical_size / MM_PER_INCH * TWIPS_PER_INCH);

                    /* updates the current page variable with
                    the new page value and adds the proper offset
                    value to the page offset counter integer */
                    current_page = new_page;
                    page_offset += (int) page_size_twips;
                }
                /* otherwise, sets the new page with the value of the current
                page as expected for default behavior */
                else { new_page = current_page; }

                /* increments the current text's vertical position by the vertical
                offset for the current page position */
                text_y += page_offset;

                /* resets the text y position in case the value is greater
                then the maximum zero value, otherwise uses the "normal" text
                y position value (default case) */
                if(text_y > 0) {
                    page_offset -= text_y;
                    text_y = 0;
                }

                /* outputs the text to the current drawing context for the
                provided (calculated) coordinates */
                TextOutW(context, text_x, text_y, text_unicode, lstrlenW(text_unicode));

                /* deletes the font object as it's no longer going to be used,
                avoiding possible memory leaks */
                DeleteObject(font);

                /* releases the unicode representation of the text */
                delete text_unicode;

                /* breaks the switch */
                break;

            case IMAGE_VALUE:
                /* "casts" the element header as the image element header
                and retrieves the image part from it */
                image_element_header = (struct image_element_header_t *) element_header;
                image = (char *) image_element_header + sizeof(struct image_element_header_t);

                /* retrieves the temporary path (directory) and then uses it to
                generate a temporary path for our image file */
                GetTempPath(1024, directory_buffer);
                GetTempFileName(directory_buffer, "default", 0, path);

                /* opens the image file for binary writing, writes the image contents
                to it and then closes the file*/
                fopen_s(&image_file, path, "wb");
                fwrite(image, sizeof(char), image_element_header->length, image_file);
                fclose(image_file);

                /* loads the (bitmap) image from the file and creates the appropriate in
                memory image handler to be used in the writing of the image */
                handle_image_new = LoadImage(
                    0,
                    (LPCTSTR) path,
                    IMAGE_BITMAP,
                    0,
                    0,
                    LR_LOADFROMFILE | LR_DEFAULTSIZE
                );
                image_context = CreateCompatibleDC(NULL);
                handle_image = SelectBitmap(image_context, handle_image_new);
                GetObject(handle_image_new, sizeof(bitmap), &bitmap);
                DeleteObject(handle_image_new);

                /* removes the temporary image file (it's no longer required)
                as the image was already loaded into memory */
                remove(path);

                /* calculates the pixel divisor (resizing for text mode) and
                calculates the multiplier for the image size */
                divisor = TWIPS_PER_INCH / pixel_density;
                multiplier = (double) IMAGE_SCALE_FACTOR / divisor;

                /* retrieves the current clip box rectangle defined for the
                image context (the place where it's going to be drawn) */
                GetClipBox(context, &clip_box);

                /* in case the block width and height are defined, a block is defined
                so the variable defining the block should be set */
                is_block = image_element_header->block_width != 0 && image_element_header->block_height != 0;

                /* in case the current image is defined inside a block, the
                clip box must be changed accordingly, these values are measured
                as twips and not millimeters (logical units) */
                if(is_block) {
                    clip_box.left = image_element_header->position_x;
                    clip_box.top = image_element_header->position_y * -1;
                    clip_box.right = image_element_header->position_x + image_element_header->block_width;
                    clip_box.bottom = (image_element_header->position_y + image_element_header->block_height) * -1;
                }

                /* updates the clip box pixel definitions using the clip box
                values and dividing them by the divisor value */
                clip_box_pixel.left = (int) ((float) clip_box.left / divisor);
                clip_box_pixel.top = (int) ((float) clip_box.top / divisor);
                clip_box_pixel.right = (int) ((float) clip_box.right / divisor);
                clip_box_pixel.bottom = (int) ((float) clip_box.bottom / divisor);

                /* calculates the scaled with and height taking into account the
                "just" calculated multiplier value */
                scaled_width = (float) bitmap.bmWidth * (float) multiplier;
                scaled_height = (float) bitmap.bmHeight * (float) multiplier;

                /* in case the text-align is left */
                if(image_element_header->text_align == LEFT_TEXT_ALIGN_VALUE) {
                    image_x = clip_box_pixel.left;
                }
                /* in case the text-align is right */
                else if(image_element_header->text_align == RIGHT_TEXT_ALIGN_VALUE) {
                    image_x = clip_box_pixel.right - (int) scaled_width;
                }
                /* in case the text-align is left */
                else if(image_element_header->text_align == CENTER_TEXT_ALIGN_VALUE) {
                    image_x = clip_box_pixel.left + (clip_box_pixel.right - clip_box_pixel.left) / 2 -
                        (int) (scaled_width / 2);
                }

                /* calculates the y position for the bottom position of the
                image and then converts it into a millimeter type */
                image_y_bottom = clip_box.top - image_element_header->position.y + (int) (scaled_height * divisor);
                image_y_bottom_millimeter = (double) image_y_bottom / TWIPS_PER_INCH * MM_PER_INCH;

                /* uses the bottom position of the image in millimeters and
                divides (integer division) over the page size to check
                the current page number (index), note that if the current
                image is inside a block, no page is changed (default layout
                rules, clipping should apply) */
                new_page = is_block ? current_page : (int) (image_y_bottom_millimeter / vertical_size);

                /* checks if there is a new page for writing, in case
                there is a new page that must be "built" */
                if(new_page > current_page) {
                    /* ends the current page and starts a new
                    on (page break operation) */
                    EndPage(context);
                    StartPage(context);

                    /* calculates the size of the page size in twips units
                    and uses it to re-calculate the text y position, taking
                    into account the already "used" pages (modulus) */
                    page_size_twips = (vertical_size / MM_PER_INCH * TWIPS_PER_INCH);

                    /* updates the current page variable with
                    the new page value and adds the proper offset
                    value to the page offset counter integer */
                    current_page = new_page;
                    page_offset += (int) page_size_twips;
                }
                /* otherwise, sets the new page with the value of the current
                page as expected for default behavior */
                else { new_page = current_page; }

                /* calculates the vertical position to be used in the image and
                then adds the current page offset to it (as defined in spec) */
                image_y = (int) ((double) clip_box.top + (double) image_element_header->position.y);
                image_y += page_offset;

                /* resets the image y position in case the value is greater
                then the maximum zero value, otherwise uses the "normal" image
                y position value (default case) */
                if(image_y > 0) {
                    page_offset -= image_y;
                    image_y = 0;
                }

                /* sets the image y as the current position context y using
                the divisor for text mode scale */
                image_y = (int) ((double) image_y / divisor) * -1;

                /* switches the map mode to text (pixel-oriented) and writes
                the image into the current context, then switch back to the
                previous map mode */
                previous_mode = GetMapMode(context);
                SetMapMode(context, MM_TEXT);
                StretchBlt(
                    context,
                    image_x,
                    image_y,
                    (int) scaled_width,
                    (int) scaled_height,
                    image_context,
                    0,
                    0,
                    bitmap.bmWidth,
                    bitmap.bmHeight,
                    SRCCOPY
                );
                SetMapMode(context, previous_mode);

                /* selects the bitmap for the context and then deletes the
                "just" generated drawing context */
                SelectBitmap(image_context, handle_image);
                DeleteDC(image_context);

                /* breaks the switch */
                break;
        }

        /* retrieves te next element header, taking into account the size
        of the current element (this is the increment delta to be used) */
        element_header = (struct element_header_t *) ((char *) element_header + sizeof(struct element_header_t) + element_length);
    }

    /* deletes the pen object as it's no longer going to be
    used and should be discarded */
    DeleteObject(pen);

    /* ends the current page and the document for the
    current context */
    EndPage(context);
    EndDoc(context);

    /* deletes the print context (avoids leaking of memory) */
    DeleteDC(context);

    /* releases the buffer that contains the binie document,
    only in case the buffer was created from the default file */
    if(!data) { free(buffer); }

    /* returns with no error */
    return 0;
}

#ifdef __cplusplus
}
#endif

#endif
