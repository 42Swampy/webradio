#!/bin/bash
# Install r92su kernel module replacing r8712u

# Initial update
sudo apt-get update

# Install kernel headers
sudo apt-get install raspberrypi-kernel-headers

# Install git
sudo apt-get install git

# Clone the rtl8192su repository if not already cloned
cd ~
if [ ! -d rtl8192su ] ; then
echo " cloning rtl8192su.git"
git clone https://github.com/asig/rtl8192su.git
else
echo " rtl8192su repository already cloned"
fi

# Make kernel updates directory if not already made
UPDATES=/lib/modules/$(uname -r)/updates
if [ ! -d $UPDATES ] ; then
sudo mkdir $UPDATES
echo " creating $UPDATES"
else
echo " $UPDATES already exists"
fi

# Make r92su driver if not already in UPDATES and copy new driver into iy
cd rtl8192su
if [ ! -e $UPDATES/r92su.ko ] ; then
echo " Making r92su.ko driver"
make -f Makefile.r92su
if [ -e r92su/r92su.ko ] ; then
echo " copying r92su.ko"
sudo cp r92su/r92su.ko $UPDATES
else
echo " error creating r92su.ko"
read -p "Error - exit" GO
fi
else
echo " r92su.ko already copied to $UPDATES"
fi

# Blacklist r8712u if not previously black listed
if [ ! -e /etc/modprobe.d/blacklist-r8712u.conf ] ; then
temp_file=$(mktemp)
echo "blacklist r8712u" >temp_file
sudo cp temp_file /etc/modprobe.d/blacklist-r8712u.conf
rm temp_file
echo " module r8712u blacklisted"
else
echo " module r8721u already blacklisted"
fi

# remove r8712u if loaded
lsmod | grep r8712u >/dev/null
if [ $? == 0 ] ; then
echo " stopping networking service"
sudo systemctl stop networking
echo " removing module r8712u"
sudo modprobe -rv r8712u
echo " starting networking service"
sudo systemctl start networking
fi

# install module r92su.ko if available and not already loaded
if [ -e $UPDATES/r92su.ko ] ; then
lsmod | grep r92su >/dev/null
if [ $? == 1 ] ; then
echo " updating dependencies"
sudo depmod
echo " stopping networking service"
sudo systemctl stop networking
echo " inserting module r92su"
sudo modprobe -v r92su
echo " starting networking service"
sudo systemctl start networking
else
echo " module r92su already loaded"
fi
else
echo " module r92su.ko not in $UPDATES"
fi

# pause the exit
read -p " Exit ?" GO
