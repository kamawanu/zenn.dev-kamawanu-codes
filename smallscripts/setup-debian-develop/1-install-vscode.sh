sudo apt update -yqq # おまじない
sudo apt install -yqq libnss3 libxkbfile1 libsecret-1-0 aria2 # vscodeで必要なパッケージを先回りして入れておく
aria2c "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64" # 最新vscodeダウンロード
sudo dpkg -i code_1.*-*.deb # vscodeインストール
