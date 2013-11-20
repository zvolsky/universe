# -*- coding: utf8 -*-

import sys
import vfp

def extract(path):
    '''take documentation from C++ sources and convert it to target files
    example of source code:
        /*@SCRIPT
        @NAME: spritecreate
        @DESC: dsfadfbweufencocno csoac
        @PARAM1: gdhsfjhg dhfsjgjh ds hgj dsf
        fjkdshfj dsfjkhjkhdsf jkhsd fjkh
        @RETURN: asfsddsa asdfsd
        */
    '''
    try:
        src = vfp.filetostr(path)
    except IOError:
        print "cannot read C++ sources %s" % path
        return
    buff = []
    in = False
    for line in src.splitlines():
        if line.strip().upper()[:9]=='/*@SCRIPT':
            in = True
            continue
        if in:
            if line.strip()[:2]=='*/':
                __out(buff)
                in = False
                continue
            if line.strip()[0]=='@':
                __out(buff)
                buff = line.split(':', 1)
                buff[0] = buff[0].strip() 
                buff[1] = buff[1].strip()
            elif buff:
                # přidat další řádky
                pass 

def __out(buff):
    buff = []     

if __name__=="__main__":
    if len(sys.argv)>1:
        extract(sys.argv[1])
    else:
        print "parameter required: path of C++ sources with documentation comments"
