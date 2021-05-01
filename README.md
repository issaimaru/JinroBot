# ワンナイト人狼Bot
Discordのチャネルでワンナイト人狼をすることができるようになります

## 使い方
1. [Discord Developer Portal](https://discord.com/developers/applications)にて、Botを作成する
2. [SETTINGS]-[Bot]のページから、トークンをコピーする
3. [Setting.txt]の*Token*に、コピーしたトークンを貼り付ける
4. main.pyを起動する

##ゲームの進行
1. 下記のコマンド[^1]を打ち込み、

## Setting.txtの使い方
<img src="https://dotup.org/uploda/dotup.org2459758.png" alt="attach:cat" title="attach:cat" width="530" height="400">
このように、各サムネイルのデフォルトURLが貼られているのでこのURLを好みの画像URLに変更することでサムネイルを変更することができます<br>
サムネイルとは、以下のようなメッセージに添付される画像のことです


<br>![embedメッセージ例](https://dotup.org/uploda/dotup.org2459765.png "embedメッセージ例")

**注意:もし[Setting.txt]の行数を変更してしまうと、正常に[Setting.txt]が読み込まれなくなります**

## コマンド
[^1]:### [-T j],[-T 人狼がしたい],[-T 人狼しようぜ]<br></b>
*人狼をプレイすることができます。
尚、最も多い投票を獲得したユーザーが複数人いる場合、その二人のうちどちらかが選ばれる仕様になっています。*
