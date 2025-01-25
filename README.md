# pymunk_de_smartball
## 注釈
Web版に関して：  
1/23までは動作していましたが、1/24現在動作しなくなりました。  
Pyxelのversion upがありましたが影響は無さそうとのこと。  
micropipもpyodideも問題はなさそうで行き詰まり・・・

エラー内容は、pymunkがロードできないエラーが出ています。  
ファイルパスもあってるしファイルも存在するし、何が何やら・・・

エラーログ  
> Wake Lock active.  
> pyodide.asm.js:10 Loading pyxel  
> pyodide.asm.js:10 Loaded pyxel  
> pyodide.asm.js:10 Loading micropip, packaging  
> pyodide.asm.js:10 Loaded micropip, packaging  
> pyxel.js:209 Copied './pymunk_de_smartball.pyxapp' to '/pyxel_working_directory/pymunk_de_smartball.pyxapp'  
> pyodide.asm.js:10 Installing Pymunk...
pyodide.asm.js:10 Error: Cannot download from a non-remote location: 'file:///pymunk-6.10.0-cp312-cp312-pyodide_2024_0_wasm32.whl' (ParseResult(scheme='', netloc='', path='pymunk-6.10.0-cp312-cp312-pyodide_2024_0_wasm32.whl', params='', query='', fragment=''))  

そんなわけで、今のところWeb版は動きません。（20250125記）  
ダウンロードしてローカルでアプリ版：pymunk_de_smartball_a.pyxappを起動すれば遊べます。  
実行コマンド：pyxel play pymunk_de_smartball_a.pyxapp

## 概要
- pymunkライブラリを使ったスマートボールシミュレーター。
- 当たり判定は全てpymunkライブラリの衝突判定を使用しています。
- PERFECT目指してできるだけ少ないボール数でクリアしてください。
- 効果音は、frenchbreadさん作成の「Pyxel RPG SE パック」を使用しています。
- 裏技：一発目のボールを打つ時にYキーまたはYボタンでボールの色を変えられます。
- Web化するとバーチャルゲームパッドに対応できない・・・
- 台の種類を追加して３種類とした。

## 操作方法
Aボタン、または、Zキーでショット  
Bボタン、または、XキーでPyxel Quit  

## スクリーンショット
![SS](sm_title.png)  
![SS](sm_game1.png)  
![SS](sm_game2.png)  
![SS](sm_game3.png)  

## GIFアニメ
![GIF](sm_0116.gif)

## 動作確認
- [URL](https://sanbunno-ichi.github.io/pymunk_de_smartball/)
