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

#include "gui_win32.h"

#ifdef __cplusplus
extern "C" {
#endif

void alert(struct _NPString *message_s) {
    /* allocates space for both the title and the message
    of the alert box then converts them from the base string
    encoded utf8 values to the win32 api unicode representation */
    wchar_t *title = new wchar_t[6];
    wchar_t *message = new wchar_t[message_s->UTF8Length + 1];
    MultiByteToWideChar(CP_UTF8, NULL, "Alert", -1, title, 6);
    size_t count = MultiByteToWideChar(
        CP_UTF8,
        NULL,
        message_s->UTF8Characters,
        message_s->UTF8Length,
        message,
        message_s->UTF8Length
    );
    message[count] = '\0';

    /* creates the alert box with the "just" converted title
    and message values (both encoded in unicode) */
    int return_value = MessageBoxW(
        NULL,
        message,
        title,
        MB_ICONINFORMATION | MB_OK
    );

    /* releases the title and the message, then returns
    the execution control to the caller */
    delete message;
    delete title;
}

#ifdef __cplusplus
}
#endif

#endif
