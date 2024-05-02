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

#include "base.h"

NPObject *so = NULL;
NPNetscapeFuncs *npnfuncs = NULL;
NPP inst = NULL;

bool invoke_default(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result) {
    result->type = NPVariantType_Int32;
    result->value.intValue = 42;
    return true;
}

bool invoke_status(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result) {
    result->type = NPVariantType_Bool;
    result->value.boolValue = true;
    return true;
}

bool invoke_version(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result) {
    /* allocates static space for the version message and
    then allocates npapi space for it */
    const char version[] = NPCOLONY_VERSION;
    char *version_message = (char *) npnfuncs->memalloc(strlen(version));

    /* copes the version value into the javascript owned
    version message */
    memcpy(version_message, version, strlen(version));

    /* allocates space for the version string and populates
    it with the just copied version message and the length of it */
    NPString version_string;
    version_string.UTF8Characters = version_message;
    version_string.UTF8Length = strlen(version);

    /* sets the version string value in the return value */
    result->type = NPVariantType_String;
    result->value.stringValue = version_string;

    /* returns in success */
    return true;
}

bool invoke_callback(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result) {
    /* validates that the number of arguments is one and that
    the provided argument is an object (callback function) */
    if(arg_count != 1 || args[0].type != NPVariantType_Object) {
        return true;
    }

    /* allocates space for the result of the callback call */
    bool result_c;

    /* allocates space for both the parameter and the return
    value variant values */
    static NPVariant parameter;
    static NPVariant return_value;

    /* allocates static space for the hello message and
    then allocates npapi space for it */
    const char hello[] = "Hello World";
    char *message = (char *) npnfuncs->memalloc(strlen(hello));

    /* copies the hello message into the allocated message
    and then converts it into a variant value */
    memcpy(message, hello, strlen(hello));
    STRINGN_TO_NPVARIANT(message, strlen(hello), parameter);

    /* invokes the callback function and then returns the value of the
    invoke default function */
    result_c = npnfuncs->invokeDefault(
        inst,
        NPVARIANT_TO_OBJECT(args[0]),
        &parameter,
        1,
        &return_value
    );
    if(!result_c) { return true; }

    /* sets the result of the call as null
    and returns the function with a valid value */
    result->type = NPVariantType_Null;
    return true;
}

bool invoke_alert(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result) {
    /* retrieves the first argument as an utf8 string
    and uses it to show the proper alert window */
    struct _NPString message_s = NPVARIANT_TO_STRING(args[0]);
    alert(&message_s);
    return true;
}

bool invoke_pformat(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result) {
    /* allocates static space for the print format message and
    then allocates npapi space for it */
    const char *format = pformat();
    size_t format_size = strlen(format);
    char *pformat_message = (char *) npnfuncs->memalloc(format_size);

    /* copes the print format value into the javascript owned
    print format message */
    memcpy(pformat_message, format, format_size);

    /* allocates space for the print format string and populates
    it with the just copied print format message and the length of it */
    NPString pformat_string;
    pformat_string.UTF8Characters = pformat_message;
    pformat_string.UTF8Length = format_size;

    /* sets the pformat string value in the return value */
    result->type = NPVariantType_String;
    result->value.stringValue = pformat_string;

    /* returns in success */
    return true;
}

bool invoke_pdevices(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result) {
    /* allocates the various variables that are going to be
    used both for the retrieval of the devices and for the
    creation of the structures for npapi return */
    size_t index;
    size_t devices_c;
    struct device_t *device;
    struct device_t *devices;
    NPVariant name_i;
    NPVariant media_i;
    NPVariant is_default_i;
    NPVariant width_i;
    NPVariant length_i;
    NPVariant result_i;
    NPVariant object_v;
    NPObject *object;
    NPObject *window = NULL;
    NPObject *_array = NULL;

    /* retrieves the complete set of devices available in the
    current system according to the specification */
    pdevices(&devices, &devices_c);

    /* retrieves the reference to the window object and uses
    it to create a new array that will be used as the return
    value of the current function */
    npnfuncs->getvalue(inst, NPNVWindowNPObject, &window);
    npnfuncs->invoke(
        inst,
        window,
        npnfuncs->getstringidentifier("Array"),
        NULL,
        0,
        result
    );
    _array = result->value.objectValue;

    /* iterates over the complete set of devices to create a
    new object for each of them and then populate it with the
    various properties that define the device */
    for(index = 0; index < devices_c; index++) {
        /* retrieves the current device for the iteration, this
        value is going to be used across the iteration */
        device = &devices[index];

        /* creates a new object by invoking the global function
        for the construction of it and then retrieves the underlying
        object reference from the variadic owner */
        npnfuncs->invoke(
            inst,
            window,
            npnfuncs->getstringidentifier("Object"),
            NULL,
            0,
            &object_v
        );
        object = object_v.value.objectValue;

        /* converts the device name into a string structure and
        sets the name property of the object with its value */
        STRINGN_TO_NPVARIANT(device->name, device->name_s, name_i);
        npnfuncs->setproperty(
            inst,
            object,
            npnfuncs->getstringidentifier("name"),
            &name_i
        );

        /* converts the device media into a string structure and
        sets the media property of the object with its value */
        STRINGN_TO_NPVARIANT(device->media, device->media_s, media_i);
        npnfuncs->setproperty(
            inst,
            object,
            npnfuncs->getstringidentifier("media"),
            &media_i
        );

        /* converts the device is default into a boolean structure and
        sets the is default property of the object with its value */
        BOOLEAN_TO_NPVARIANT(device->is_default, is_default_i);
        npnfuncs->setproperty(
            inst,
            object,
            npnfuncs->getstringidentifier("isDefault"),
            &is_default_i
        );

        /* converts the device width into a double structure and
        sets the width property of the object with its value */
        DOUBLE_TO_NPVARIANT(device->width, width_i);
        npnfuncs->setproperty(
            inst,
            object,
            npnfuncs->getstringidentifier("width"),
            &width_i
        );

        /* converts the device length into a double structure and
        sets the length property of the object with its value */
        DOUBLE_TO_NPVARIANT(device->length, length_i);
        npnfuncs->setproperty(
            inst,
            object,
            npnfuncs->getstringidentifier("length"),
            &length_i
        );

        /* "pushes" the object structure into the returning array
        by invoking the push function on the returning object */
        npnfuncs->invoke(
            inst,
            _array,
            npnfuncs->getstringidentifier("push"),
            &object_v,
            1,
            &result_i
        );
        npnfuncs->releasevariantvalue(&result_i);
        npnfuncs->releasevariantvalue(&object_v);
    }

    /* releases the devices buffer as it's not going to
    be used anymore (avoid memory leak) */
    free(devices);

    /* returns in success */
    return true;
}

bool invoke_print(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result) {
    /* retrieves both the show dialog and the data string
    values to be used in the printing operation */
    bool show_dialog = NPVARIANT_TO_BOOLEAN(args[0]);
    struct _NPString data_string = NPVARIANT_TO_STRING(args[1]);

    /* allocates space for the decoded data buffer and for
    the storage of the length (size) of it */
    char *data;
    size_t data_length;

    /* decodes the data value from the base 64 encoding
    and then uses it to print the data */
    decode_base64(
        (unsigned char *) data_string.UTF8Characters,
        data_string.UTF8Length,
        (unsigned char **) &data,
        &data_length
    );
    print(show_dialog, NULL, (char *) data, data_length);

    /* releases the decoded buffer (avoids memory leak)
    and then returns in success */
    _free_base64((unsigned char *) data);
    return true;
}

bool invoke(NPObject* obj, NPIdentifier method_name, const NPVariant *args, uint32_t arg_count, NPVariant *result) {
    log_m("npcolony: invoke\n");
    char *name = npnfuncs->utf8fromidentifier(method_name);

    if(name) {
        if(!strcmp(name, "status")) {
           /* returns the result of the status invoking */
            return invoke_status(obj, args, arg_count, result);
        } else if(!strcmp(name, "version")) {
           /* returns the result of the version invoking */
            return invoke_version(obj, args, arg_count, result);
        } else if(!strcmp(name, "foo")) {
            /* returns the result of the default invoking */
            return invoke_default(obj, args, arg_count, result);
        } else if(!strcmp(name, "callback")) {
            /* returns the result of the callback invoking */
            return invoke_callback(obj, args, arg_count, result);
        } else if(!strcmp(name, "alert")) {
            /* returns the result of the alert invoking */
            return invoke_alert(obj, args, arg_count, result);
        } else if(!strcmp(name, "pformat")) {
            /* returns the result of the pformat invoking */
            return invoke_pformat(obj, args, arg_count, result);
        } else if(!strcmp(name, "pdevices")) {
            /* returns the result of the pdevices invoking */
            return invoke_pdevices(obj, args, arg_count, result);
        } else if(!strcmp(name, "print")) {
            /* returns the result of the print invoking */
            return invoke_print(obj, args, arg_count, result);
        }
    }

    /* in case the control reaches this area an exception
    must have occured (invalid name) sets it in the environment */
    npnfuncs->setexception(obj, "exception during invocation");

    return false;
}

bool has_method(NPObject* obj, NPIdentifier method_name) {
    /* retrieves the correct string for the method name
    as a normal comparision structure */
    char *name = npnfuncs->utf8fromidentifier(method_name);

    /* iterates over all the methods in the static structure
    to compare them against the requesed method */
    for(size_t index = 0; index < METHODS_COUNT; index++) {
        /* in case the current method is the same as the
        requested on returns valid */
        if(!strcmp(name, methods[index])) { return true; }
    }

    /* by default returns method not found */
    return false;
}

bool has_property(NPObject *obj, NPIdentifier property_name) {
    log_m("npcolony: has_property\n");
    return false;
}

bool get_property(NPObject *obj, NPIdentifier property_name, NPVariant *result) {
    log_m("npcolony: get_property\n");
    return false;
}

NPError nevv(NPMIMEType plugin_type, NPP instance, uint16_t mode, int16_t argc, char *argn[], char *argv[], NPSavedData *saved) {
    log_m("npcolony: new\n");
    inst = instance;

#ifdef COLONY_PLATFORM_UNIX
    NPBool has_windowless = false;
    npnfuncs->getvalue(instance, NPNVSupportsWindowless, &has_windowless);
    if(!has_windowless) { return NPERR_GENERIC_ERROR; }
    npnfuncs->setvalue(instance, NPPVpluginWindowBool, (void*) false);
#endif

#ifdef COLONY_PLATFORM_MACOSX
    NPBool has_cg = false;
    if(npnfuncs->getvalue(instance, NPNVsupportsCoreGraphicsBool, &has_cg) == NPERR_NO_ERROR && has_cg) {
        npnfuncs->setvalue(instance, NPPVpluginDrawingModel, (void *) NPDrawingModelCoreGraphics);
    } else {
        return NPERR_INCOMPATIBLE_VERSION_ERROR;
    }

    NPBool has_cocoa = false;
    if(npnfuncs->getvalue(instance, NPNVsupportsCocoaBool, &has_cocoa) == NPERR_NO_ERROR && has_cocoa) {
        npnfuncs->setvalue(instance, NPPVpluginEventModel, (void *) NPEventModelCocoa);
    } else {
        return NPERR_INCOMPATIBLE_VERSION_ERROR;
    }
#endif

    return NPERR_NO_ERROR;
}

NPError destroy(NPP instance, NPSavedData **save) {
    log_m("npcolony: destroy\n");

    /* in case the shared object is defined
    releases it from memory (avoids leaking) */
    if(so) { npnfuncs->releaseobject(so); }

    /* unsets the shared object reference, so that no more
    usage of it may be done without null pointing*/
    so = NULL;

    /* returns with no error */
    return NPERR_NO_ERROR;
}

NPError get_value(NPP instance, NPPVariable variable, void *value) {
    log_m("npcolony: get_value\n");
    inst = instance;

    switch(variable) {
        case NPPVpluginNameString:
            *((char **)value) = NPCOLONY_NAME;
            break;

        case NPPVpluginDescriptionString:
            *((char **)value) = NPCOLONY_DESCRIPTION;
            break;

        case NPPVpluginScriptableNPObject:
            if(!so) { so = npnfuncs->createobject(instance, &ref_object); }
            npnfuncs->retainobject(so);
            * (NPObject **) value = so;
            break;

        default:
            return NPERR_INVALID_PARAM;
    }

    return NPERR_NO_ERROR;
}

NPError set_value(NPP instance, NPNVariable variable, void *value) {
    log_m("npcolony: set_value\n");
    return NPERR_GENERIC_ERROR;
}

NPError handle_event(NPP instance, void *ev) {
    log_m("npcolony: handle_event\n");
    inst = instance;
    return NPERR_NO_ERROR;
}

NPError set_window(NPP instance, NPWindow *window) {
    log_m("npcolony: set_window\n");
    inst = instance;
    return NPERR_NO_ERROR;
}

NPError new_stream(NPP instance, NPMIMEType type, NPStream *stream, NPBool seekable, uint16_t *stype) {
    log_m("npcolony: new_stream\n");
    *stype = NP_ASFILEONLY;
    return NPERR_NO_ERROR;
}

NPError destroy_stream(NPP instance, NPStream *stream, NPReason reason) {
    log_m("npcolony: destroy_stream\n");
    return NPERR_NO_ERROR;
}

int32_t write_ready(NPP instance, NPStream *stream) {
    log_m("npcolony: write_ready\n");
    return 0;
}

int32_t nwrite(NPP instance, NPStream *stream, int32_t offset, int32_t len, void *buffer) {
    log_m("npcolony: nwrite\n");
    return 0;
}

void as_file(NPP instance, NPStream *stream, const char *fname) {
    log_m("npcolony: as_file\n");
}

void nprint(NPP instance, NPPrint *platform_print) {
    log_m("npcolony: nprint\n");
}

void nurl_notify(NPP instance, const char *url, NPReason reason, void *notify_data) {
    log_m("npcolony: nurl_notify\n");
}

#ifdef __cplusplus
extern "C" {
#endif

NPError OSCALL NP_GetEntryPoints(NPPluginFuncs *nppfuncs) {
    log_m("npcolony: NP_GetEntryPoints\n");

    nppfuncs->version = (NP_VERSION_MAJOR << 8) | NP_VERSION_MINOR;
    nppfuncs->newp = nevv;
    nppfuncs->destroy = destroy;
    nppfuncs->newstream = new_stream;
    nppfuncs->destroystream = destroy_stream;
    nppfuncs->asfile = as_file;
    nppfuncs->writeready = write_ready;
    nppfuncs->write = (NPP_WriteProcPtr) nwrite;
    nppfuncs->getvalue = get_value;
    nppfuncs->setvalue = set_value;
    nppfuncs->event = handle_event;
    nppfuncs->setwindow = set_window;
    nppfuncs->print = nprint;
    nppfuncs->urlnotify = nurl_notify;

    return NPERR_NO_ERROR;
}

#ifdef COLONY_PLATFORM_LINUX
NPError OSCALL NP_Initialize(NPNetscapeFuncs *npnf, NPPluginFuncs *nppfuncs) {
#else
NPError OSCALL NP_Initialize(NPNetscapeFuncs *npnf) {
#endif
    log_m("npcolony: NP_Initialize\n");

    /* in case the functions table is not valid,
    must return in error */
    if(npnf == NULL) {
        /* returns in error (invalid function table) */
        return NPERR_INVALID_FUNCTABLE_ERROR;
    }

    /* checks if there are incompatible version for
    the plugin interface */
    if(HIBYTE(npnf->version) > NP_VERSION_MAJOR) {
        /* returns in error (incompatbile version) */
        return NPERR_INCOMPATIBLE_VERSION_ERROR;
    }

#ifdef COLONY_PLATFORM_LINUX
    nppfuncs->newp = nevv;
    nppfuncs->destroy = destroy;
    nppfuncs->newstream = new_stream;
    nppfuncs->destroystream = destroy_stream;
    nppfuncs->asfile = as_file;
    nppfuncs->writeready = write_ready;
    nppfuncs->write = (NPP_WriteProcPtr) nwrite;
    nppfuncs->getvalue = get_value;
    nppfuncs->setvalue = set_value;
    nppfuncs->event = handle_event;
    nppfuncs->setwindow = set_window;
    nppfuncs->print = nprint;
    nppfuncs->urlnotify = nurl_notify;
#endif

    /* save the functions in a global variable
    and returns in no error */
    npnfuncs = npnf;
    return NPERR_NO_ERROR;
}

NPError OSCALL NP_Shutdown() {
    log_m("npcolony: NP_Shutdown\n");
    return NPERR_NO_ERROR;
}

const char *NP_GetPluginVersion() {
    log_m("npcolony: NP_GetPluginVersion\n");
    return NPCOLONY_VERSION;
}

const char *NP_GetMIMEDescription() {
    log_m("npcolony: NP_GetMIMEDescription\n");
    return NPCOLONY_MIME;
}

NPError OSCALL NP_GetValue(void *npp, NPPVariable variable, void *value) {
    log_m("npcolony: NP_GetValue\n");
    inst = (NPP) npp;
    return get_value((NPP) npp, variable, value);
}

#ifdef __cplusplus
}
#endif
