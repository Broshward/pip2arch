# pip2arch
pip2arch is a PKGBUILD generator and installing tool for python2 packages. pip3arch - for python3 packages.

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
