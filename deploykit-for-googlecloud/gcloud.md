デプロイには依然として gcloud が必要。バージョンが頻繁に進むので注意。

# gcloud cli

## install

https://cloud.google.com/sdk/docs/install

archlinux では　AUR がある。
https://aur.archlinux.org/packages/google-cloud-sdk
2022現在では401.0.0

- gcloud components installが一切使えなくなる。
- PATHが通ってない
> $ source /etc/profile.d/google-cloud-sdk.sh

非常に不便なので linux汎用版/tar.gz を入れた方がよい。

https://cloud.google.com/sdk/docs/install#mac
macos版はアーキテクチャによってバージョンにばらつきがあるようなので注意。

> gcloud components install app-engine-python

## gcloud init


gcloud init で認証。

- OAUTH2ログイン
- CLIに戻って、プロジェクト＆zoneを聴かれる。
- region:us-central==zone:us-central1らしい。
