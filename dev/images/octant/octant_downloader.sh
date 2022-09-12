VER=`curl -s https://api.github.com/repos/vmware-tanzu/octant/releases/latest | grep -io 'v[0-9].[0-9]*.[0-9]*' | head -1 | tr -d v`
LINK=https://github.com/vmware-tanzu/octant/releases/download/v$VER/octant_$VER\_Linux-64bit.deb
wget -O octant.deb $LINK
