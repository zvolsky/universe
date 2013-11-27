# -*- coding: utf8 -*-

outfile = 'universe.py'

import sys
import vfp

def zpracuj(path):
    '''take documentation from C++ sources and convert it to target files
    '''
    popisy = pober(path)
    vfp.strtoutf8file('# -*- coding: utf8 -*-' +
        '\n\n' + 'class Universe(object):' + '\n', outfile)
    for popis in popisy:
        if popis['NAME']:
            params_desc = ''
            for idx in xrange(1,500):
                param_desc = popis.get('PARAM%s'%idx)
                if param_desc==None: 
                    break
                params_desc += ('\n' + 8*' ' + 'PARAM%s'%idx + ': ' +
                        param_desc.replace('\n', '\n' + 8*' '))
            vfp.strtoutf8file(4*' ' +
                    'def %s(%s):'%(popis['NAME'], popis['params']) +
                    '\n' + 8*' ' + '"""DESC: ' + popis.get('DESC') + '\n' +
                    params_desc[1:] + '\n' +
                    8*' ' + 'RETURN: ' + popis.get('RETURN') + '\n' +
                    8*' ' + '"""\n' +
                    8*' ' +
                    'return %s(%s)'%(popis['NAME'], popis['params']) + '\n\n',
                    outfile, 1)

def pober(path):
    '''take documentation from C++ sources into variable popisy (list of dict) 
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
    popisy = []
    uvnitr = False
    for line in src.splitlines():
        if uvnitr:
            if line.strip()[:2]=='*/':
                popis['params'] = None
                popisy.append(popis)
                uvnitr = False
            elif line.strip()[0]=='@':
                radek1 = line.split(':', 1)
                currname = radek1[0].strip()[1:] 
                popis[currname] = radek1[1].strip()  
            elif currname:
                # přidat další řádky
                popis[currname] += '\n' + line.strip()
        elif line.strip().upper()[:9]=='/*@SCRIPT':
            uvnitr = True
            popis = {}
            currname = ''
        elif popisy[-1]['params']==None:
            prikaz = line.strip()
            if prikaz and prikaz[0]!='/' and '(' in prikaz:
                popisy[-1]['params'] = prikaz.split('(', 1)[1].split(')', 1)[0]
    return popisy

if __name__=="__main__":
    if len(sys.argv)>1:
        zpracuj(sys.argv[1])
    else:
        print "parameter required: path of C++ sources with documentation comments"
