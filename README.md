# どうぶつさんのおうち

2歳10か月前後の子どもが、タブレットやiPhoneで短時間遊ぶことを想定した、勝ち負けなしの動物のおうち合わせゲームです。

## ゲーム概要

画面に出てくる動物を見て、その動物に合うおうちをタップします。合っているおうちを選ぶと、動物がおうちへ帰ります。別のおうちを選んでも否定せず、「こっちかな？」というやさしい反応で続けられます。

動物は10種類用意していて、1ラウンドではその中から5匹をランダムに選びます。おうちの選択肢もその5匹のおうちだけが表示されます。

- いぬ: いぬごや
- ねこ: クッション
- とり: き
- さかな: すいそう
- うさぎ: くさむら
- ぱんだ: たけ
- ぶた: ぶたごや
- かえる: はす
- くま: ほらあな
- ねずみ: あな

## 対象年齢

2歳10か月前後から。文字が読めなくても、絵とタップ操作だけで遊べることを優先しています。

## 遊び方

1. `はじめる` をタップします。
2. 画面に出た動物を見ます。
3. 下または横に並んだおうちをタップします。
4. 動物がおうちへ帰ったら、`つぎのどうぶつ` をタップして次に進みます。
5. 5匹終わったら `もういっかい` で繰り返せます。

スコア、制限時間、ゲームオーバーはありません。
画面右上の `おとオン / おとオフ` で効果音と動物のなき声をいつでも切り替えできます。

## ローカル確認方法

このリポジトリ直下が静的サイトです。PWAとService Workerの確認もあるため、ローカルHTTPサーバで配信して確認します。

```powershell
python -m http.server 8080
```

ブラウザで次を開きます。

```text
http://localhost:8080/
```

ホーム画面追加の導線は、スタート画面の `ホームに追加` から確認できます。

## 素材生成方法

動物とおうちのSVG素材は、Python標準ライブラリだけで生成します。

```powershell
python tools/generate_animal_assets.py
```

生成される主なファイル:

- `assets/animals/*.svg`
- `assets/homes/*.svg`
- `assets/preview.html`

素材プレビューは次で確認できます。

```text
http://localhost:8080/assets/preview.html
```

## iPhoneで確認する方法

PCとiPhoneを同じWi-Fiに接続し、PCのローカルIPアドレスを使ってSafariで開きます。

```text
http://<PCのIPアドレス>:8080/
```

Safariで表示確認し、縦向きと横向きの両方で、動物とおうちが大きく押しやすいかを見ます。
ホーム画面に追加する場合は、スタート画面の `ホームに追加` を開き、Safariの共有ボタンから `ホーム画面に追加` を選びます。

## Androidタブレットで確認する方法

PCとAndroidタブレットを同じWi-Fiに接続し、Chromeで次を開きます。

```text
http://<PCのIPアドレス>:8080/
```

10インチタブレットでは、縦向きと横向きの両方で、おうち候補のタップ領域と動物の見やすさを確認します。
ホーム画面に追加する場合は、スタート画面の `ホームに追加` を開き、Chromeの案内またはメニューから追加します。

## 最終利用形態

QRコードを読み込んでブラウザで開き、ホーム画面に追加して使う想定です。

想定する流れ:

- iPhone用QRコードを読み込む
- Androidタブレット用QRコードを読み込む
- iPhoneはSafari、AndroidタブレットはChromeで開く
- ホーム画面に追加する
- 次回以降はホーム画面アイコンから起動する

## PWA構成

PWA関連ファイルはリポジトリ直下だけで完結しています。

主なファイル:

- `manifest.webmanifest`
- `sw.js`
- `assets/icons/`
- `assets/install/install.html`

Service Workerは同一オリジンのゲーム本体と動物・おうち素材、PWAアイコンをキャッシュします。

## アイコン生成方法

ホーム画面用アイコンはPython標準ライブラリだけで生成します。

```powershell
python tools/generate_pwa_icons.py
```

生成される主なファイル:

- `assets/icons/icon-192.png`
- `assets/icons/icon-512.png`
- `assets/icons/apple-touch-icon.png`

## QRコード生成方法

QRコードはPython標準ライブラリだけで生成します。既定ではGitHub remoteからGitHub PagesのURLを推定します。

公開URL:

```text
https://fzr400r3en2-sys.github.io/doubutsusanno-outi/
```

```powershell
python tools/resolve_public_url.py
python tools/generate_install_qr.py
```

生成される主なファイル:

- `assets/install/qr-iphone.svg`
- `assets/install/qr-android.svg`
- `assets/install/install.html`

公開URLを明示する場合:

```powershell
$env:DOUBUTSU_HOME_PUBLIC_URL = "https://fzr400r3en2-sys.github.io/doubutsusanno-outi/"
python tools/generate_install_qr.py
```

ローカルIPで実機確認する場合:

```powershell
python tools/generate_install_qr.py --base-url http://<PCのIPアドレス>:8080/
```

## 今後の改善候補

- 実機確認後に、動物やおうちの大きさを微調整する
- タップ時の演出を少し増やす
- ゲーム途中で `タイトルへもどる` ボタンを追加する
- 動物の見つけたコレクション要素を入れる
