
#!/bin/bash
# Install r92su kernel module replacing r8712u

apt-get update
apt-get install raspberrypi-kernel-headers
cd ~
rm -r ./rtl8192su
git clone https://github.com/asig/rtl8192su.git
cd rtl8192su
make -f Makefile.r92su

UPDATES=/lib/modules/$(uname -r)/updates
if [ ! -d $UPDATES ] ; then
mkdir $UPDATES
echo creating $UPDATES
fi
cp r92su/r92su.ko $UPDATES

if [ ! -e /etc/modprobe.d/blacklist-r8712u.conf ] ; then
echo "blacklist r8712u" >/etc/modprobe.d/blacklist-r8712u.conf
fi

depmod





