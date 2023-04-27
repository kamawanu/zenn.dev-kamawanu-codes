#!/bin/sh
PKG=Kelvin.vscode-sshfs
WS=sshfs.code-workspace
INS=0
code --list-extensions | fgrep $PKG && INS=1 # vscode拡張が入ってるか確認
if [ $INS -eq 0 ]
then
	code --install-extension $PKG # 無ければ入れる
fi
echo '{"folders":[{"name":"SSHFS-vps","uri":"ssh://vps/home/'$LOGNAME'"}],"settings":{"sshfs.configs":[{"name":"vps","host":"153.126.183.193","username":"'$LOGNAME'","root":"/home/'$LOGNAME'"}]}}' > $WS
code $WS
