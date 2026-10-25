/* SPDX-License-Identifier: MIT
 * Maintenance reconstruction of the port-owned Dig 2 v8 GLX bridge.
 * The shipped known-good binary is preserved; this is not a claim of a
 * byte-identical reproduction. Build and test separately before replacing it.
 */
#include <stdio.h>
#include <string.h>
#include <dlfcn.h>
static unsigned char fake_display;
void *glXGetCurrentDisplay(void) {
    static int once;
    if (!once++) fprintf(stderr,"[GLX-V8] glXGetCurrentDisplay: synthetic non-NULL display (Wayland)\n");
    return &fake_display;
}
int glXQueryVersion(void *display,int *major,int *minor) {
    (void)display;if(major)*major=1;if(minor)*minor=4;
    fprintf(stderr,"[GLX-V8] glXQueryVersion -> 1.4\n");return 1;
}
const char *glXGetClientString(void *display,int name) {
    (void)display;return name==1?"RGDS GL4ES":name==2?"1.4":name==3?"GLX_ARB_get_proc_address":"";
}
const char *glXQueryServerString(void *display,int screen,int name) {
    (void)screen;return glXGetClientString(display,name);
}
const char *glXQueryExtensionsString(void *display,int screen) {
    (void)display;(void)screen;return "GLX_ARB_get_proc_address";
}
void *glXGetProcAddressARB(const unsigned char *symbol) {
    static int looked;static void *(*real)(const unsigned char *);
    const char *name=(const char *)symbol;void *result;
    if(!name)return NULL;
#define OWN(fn) if(strcmp(name,#fn)==0)return (void *)fn
    OWN(glXGetCurrentDisplay);OWN(glXQueryVersion);OWN(glXGetClientString);
    OWN(glXQueryServerString);OWN(glXQueryExtensionsString);
#undef OWN
    if(!looked) {
        looked=1;real=dlsym(RTLD_NEXT,"glXGetProcAddressARB");
        fprintf(stderr,"[GLX-V8] native resolver: %s\n",real?"present":"missing");
    }
    result=real?real(symbol):NULL;
    if(!result)result=dlsym(RTLD_NEXT,name);
    if(strcmp(name,"glGetString")==0 || strcmp(name,"glCreateShader")==0)
        fprintf(stderr,"[GLX-V8] %s -> %s\n",name,result?"present":"NULL");
    return result;
}
void *glXGetProcAddress(const unsigned char *name) {return glXGetProcAddressARB(name);}
