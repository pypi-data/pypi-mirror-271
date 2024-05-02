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

#include "util.h"

#ifdef COLONY_DEBUG
void log_m(const char *message) {
    /* allocates space for a file reference */
    FILE *file;

    /* opens the logging file for wirting (appending)
    this is the file to be used for logging  */
    fopen_s(&file, "\\npcolony.log", "a");

    /* in case the file was not correclty
    opened, avoid any operation, returns
    immediately cannot write in it */
    if(file == NULL) { return; }

    /* prints the message into file (printing)
    and then closes it immediately */
    fputs(message, file);
    fclose(file);
}
#else
void log_m(const char *message) { }
#endif
