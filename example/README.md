OSCViewer
====

## Description

* オシロスコープ用のアプリケーションです(Windows11 64bit推奨)
* SCPIコマンドに準拠しているオシロスコープにて使用できます
* 推奨オシロスコープ：DS1104Z Plus

## Usage

* [説明書](./doc/01_説明書)を参照（作成中）

## Application 

/src/dist/OSCViewer.exe

## Requirement

* Python (Version: 3.10.5)

### How to compile

1. Python(Version: 3.10.5) をインストールする

2. Ultra Sigmaをインストールする(デバイスドライバのインストール)
    *  Ultra Sigma(PC)Installer_00.01.06.01

2. `pipe` を使用してライブラリをインストールする
    *  pyserial  
    *  PyVISA ※バージョン 1.9.1を推奨    
    *  pillow  
    *  pyinstaller ※バージョンによってはexe生成に失敗するため、バージョン5.1を推奨  

3. exeファイルを作成する  

```
pyinstaller "OSCViewer.py"  --onefile --noconsole --clean --paths="C:\Users\xxxx\AppData\Local\Programs\Python\Python310\Lib\site-packages\cv2"
``` 
※--paths=の先は自身の環境でcv2がインストールされているフォルダを指定する(windowsではxxxxはユーザー名)

## Licence

   Copyright (C) 2024-2025 Daiki Yasuda. All rights reserved.

## Feature Requests

* コンボボックスを使用してCOMポートを選択可能とする
* メッセージ（送信データ、応答データなど）のファイル出力

## Changelog

#### [0.0.1] - 2024-11-02
- 新規作成 

## Author

* v0.0.1 [Daiki Yasuda](mailto:daiki.yasuda@yasuda-tech-studio.info)

