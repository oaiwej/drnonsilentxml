# DRNonSilentXML

動画ファイル内の無音部分を自動的に検出し、無音部分をカットした XML タイムラインを生成するツールです。

## コマンドライン引数

### 必須引数

- `-i, --input`
  - 入力動画ファイルのパス
  - サポート形式: MP4, MOV, MKV, AVI など pydub で音声抽出可能な動画形式
  - 例: `-i "interview.mp4"`

- `-if, --input-fps`
  - 入力動画のフレームレート（フレーム/秒）
  - 動画素材のフレームレートに合わせて指定
  - 一般的な値: 60
  - 例: `-if 60`

- `-o, --output`
  - 出力 XML ファイルのパス
  - 生成される XML ファイルの保存先を指定します
  - 例: `-o "edited_timeline.xml"`

- `-of, --output-fps`
  - 出力タイムラインのフレームレート（フレーム/秒）
  - Davinci Resolve のタイムライン設定に合わせて指定
  - 一般的な値: 59.94
  - 例: `-of 59.94`

### オプション引数

- `-t, --threshold` (デフォルト: -40)
  - 無音検出のしきい値
  - 値を上げるほど
    - 例: `-t -30` (より小さな音量を無音として検出)

- `-p, --padding` (デフォルト: 300)
  - 非無音部分の前後に追加するパディング（ミリ秒単位）
  - 音声の切れ目を滑らかにするために、検出された無音でない部分の前後に追加する余白
  - 例: `-p 500` (より長いパディングを設定)

## セットアップ方法

### 前提条件

- Python 3.11 以上
- pip (Python パッケージ管理ツール)

### セットアップ手順

1. リポジトリをクローンします：

    ```powershell
    git clone https://github.com/oaiwej/drnonsilentxml.git DRNonSilentXML
    cd DRNonSilentXML
    ```

2. 依存パッケージをインストールします：

    ```powershell
    py -3.11 -m venv venv
    venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

3. フォルダ直下に **ffmpeg.exe** と **ffprobe.exe** 配置するか、パスを通してください。


## 使い方

### 無音カットタイムラインの作成

以下のようなコマンドを実行して、無音カット編集用の XML タイムラインを生成します：

```powershell
python -m drnonsilentxml -i "input.mp4" -if 60 -o "output.xml" -of 59.94 -t -40 -p 300
```

<br>

または、`silence_cut_xml.bat` に動画ファイル(複数ファイル可)をドラッグ＆ドロップすることで、簡単に無音カット編集用の XML タイムラインを生成できます。60FPS->59.94FPSに設定されているので、適宜編集してください。

### Davinci Resolveでの読み込み方法

1. 先に`input.mp4`にあたるファイルをDavinci Resolveのビンに追加しておいてください。
1. `ファイル` > `読み込み` > `タイムライン`（または`CTRL+Shift+I`）で生成された XML ファイルを読み込むと、無音カット編集が適用されたタイムラインが表示されます。
1. 読み込まれたタイムラインは何故かモノラルになってしまうので、ステレオにする場合は以下の手順を実行してください。
    1. タイムラインのクリップをすべて選択
    1. クリップを右クリック > クリップ属性 > 音声タブ
    1. フォーマットを`Stereo`に変更

