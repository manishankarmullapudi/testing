VER=`curl -s https://github.com/aquasecurity/starboard-octant-plugin/releases | grep 'tag' | grep -io 'v[0-9].[0-9]*.[0-9]*' | head -1 | tr -d v`

LINK=https://github.com/aquasecurity/starboard-octant-plugin/releases/download/v$VER/starboard-octant-plugin_linux_x86_64.tar.gz

wget -O plugin.tar.gz $LINK

tar -zxvf plugin.tar.gz

mv ./starboard-octant-plugin $HOME/.config/octant/plugins/

rm README.md LICENSE plugin.tar.gz
