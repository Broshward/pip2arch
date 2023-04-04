#!/usr/bin/python2

TEMP_DIRECTORY = "./src"

help="""
Usage: pip2arch.py [--create-only] [-g] [-C] [-P] package
For python3 see the pip3arch.py utility 

Python2 helper for install to Archlinux python2 modules, which not exists in standart ArchLinux repositories.
This program install latest version of given package with latest versions of its dependencies to ArchLinux system.
If no conflicts it install all packages enjoy. However if file conflicts has happen it will not overwrite files. You must attentively reading pacman messages and fix corresponding PKGBUILDs by your hands!))

What does it:
1. It download packages which needed to ./src/ directory by pip install command. It doing for get install log only and determine dependencies list after.
2. Then it create directories for package and also for all dependencies too.
3. In each directory it create PKGBUILD for following launch.
4. Then it consecutively enters in each packages directories and launchs the "makepkg -f -i --noconfirm [--asdep]".

If --create-only option is added it create PKGBUILDs for handlaunches.

    -g  
        Print more debug information

    -C  
        Remove ./src/ directory before installing

    --create-only 
        Only create PKBUILDS for hand launch of makepkg

    -I
        Install only. It Launch of makepkg -i -f --no-confirm for each package

    -P
        No launch pacman -U command for packages
"""

PKGBUILD_TEMPLATE= """
# This PKGBUILD automatically generated by pip2arch program.

pkgbase='python2'
module='%s'
pkgname=($pkgbase-$module)
pkgver='%s'
pkgrel=4
depends=('python2')
makedepends=('python2-pip')
license=('MIT')
arch=('any')

build() {
    mkdir $srcdir/usr
    PYTHONUSERBASE=$srcdir/usr pip2 install --no-python-version-warning --no-deps --no-cache-dir -I $module==$pkgver
}

package() {
    cp -a $srcdir/* $pkgdir/
    chmod -R 755 $pkgdir
}
"""

import sys, os, subprocess

if '-h' in sys.argv:
    print help
    exit(0)
if '-g' in sys.argv:
    sys.argv.remove('-g')
    debug = True
else:
    debug = False

if '-C' in sys.argv:
    sys.argv.remove('-C')
    clean = True
else:
    clean = False

if '-P' in sys.argv:
    sys.argv.remove('-P')
    pacman = False
else:
    pacman = True

if '--create-only' in sys.argv:
    sys.argv.remove('--create-only')
    create_only = True
else:
    create_only = False

if '-I' in sys.argv:
    sys.argv.remove('-I')
    install_only = True
else:
    install_only = False

sys.argv.pop(0)
if len(sys.argv)<1:
    print 'The name of package for installing must be gotten!'
package = sys.argv[0]

# 1. Create ./src directory
if not os.path.exists(TEMP_DIRECTORY):
    os.mkdir(TEMP_DIRECTORY)
else:
    if clean:
        os.system('rm -rf '+TEMP_DIRECTORY)


# 2. pip install package with dependencies to TEMP_DIRECTORY
cmd = "PYTHONUSERBASE=%s pip2 install --no-cache-dir %s"  %(TEMP_DIRECTORY, package)
out = os.popen(cmd).read()
#out=open('out').read()
#import pdb;pdb.set_trace()
if debug:
    print out
#    f=open('out','w')
#    f.write(out)
#    f.close()
if 'ERROR: No matching distribution found for ipython2' in out:
    print "No such package found!"
    exit(-2)

# 3. Generate PKGBUILDs
import re
dependencies = re.findall('Downloading (\w+)-(\d+\.\d+\.\d+)',out)
if debug:
    print 'Dependencies:'
    for i in dependencies:
        print '\t',i[0]+'-'+i[1]

installed_packages = re.findall('(\w+)==(\d+\.\d+\.\d+)',os.popen('pip2 freeze').read()) #List of already installed packages
if debug:
    print '\nAlready installed packages:'
    for i in installed_packages:
        print '\t',i[0]+'-'+i[1]

for i in dependencies:
    print '\n\t',i[0]+'-'+i[1]+':'
    if not install_only:
        #Create package directory
        if not os.path.exists(i[0]):
            os.mkdir(i[0])
        #Generate PKBUILD for package
        pkgbuild = open(i[0]+'/PKGBUILD','w')
        pkgbuild.write(PKGBUILD_TEMPLATE %(i[0], i[1]))
        pkgbuild.close()
        
        if create_only:
            continue
    if i in installed_packages:
        if debug:
            print '\n!!!Package ',i,' already installed, skipping!!!\n'
            continue

    #Copy package files to src package
        
        # Due to pip search command was deprecated I using install to temporarily dir all packages and depends only for got pip install log to after create corresponding PKGBUILD and package directory. Therefore I cannot simple copy files from src to package src and I need pip install launch twice.
        
    #Launch makepkg
    cmd = 'cd %s\n' %(i[0])
    cmd += 'makepkg -i --noconfirm'
    if i!=package:
        cmd +=' --asdep'
    if install_only:
        cmd += ' -R'

    os.system(cmd)
#    out = subprocess.call(cmd)
#    print out

