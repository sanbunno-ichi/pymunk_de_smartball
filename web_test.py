import asyncio
import micropip
#import os

#実行させたいファイルをここに定義
from pymunk_de_smartball import App


# メイン関数を非同期で実行するための関数
def run_asyncio():
    # 現在のイベントループを取得
    loop = asyncio.get_event_loop()

    # イベントループが実行中か確認
    if loop.is_running():
        # 実行中の場合は、非同期タスクとしてmain()を登録
        asyncio.ensure_future(main())
    else:
        # 実行中でない場合は、新しいイベントループでmain()を実行
        asyncio.run(main())


# 非同期のメイン関数
async def main():
    try:
        # micropipを使ってwhlファイルからpymunkをインストール
        print("Installing Pymunk...")
        #await micropip.install("pymunk-6.10.0-cp312-cp312-pyodide_2024_0_wasm32.whl")
        #→NG
        #await micropip.install("https://github.com/sanbunno-ichi/pymunk_de_smartball/blob/main/pymunk-6.10.0-cp312-cp312-pyodide_2024_0_wasm32.whl")
        #→CORSでエラー

        ##カレントディレクトリの絶対パスを取得
        #path = os.getcwd()
        #print(path)
        #await micropip.install(path + "/pymunk-6.10.0-cp312-cp312-pyodide_2024_0_wasm32.whl")
        #→path="/pyxel_working_directory"となってしまうためNG

        await micropip.install("https://sanbunno-ichi.github.io/pymunk_de_smartball/pymunk-6.10.0-cp312-cp312-pyodide_2024_0_wasm32.whl")
        #→OK
        print("Pymunk installed successfully")

        # pymunkをインポート
        import pymunk

        # Appクラスを初期化して実行
        App(pymunk)
    except Exception as e:
        print(f"Error: {e}")


# メイン関数を実行
run_asyncio()
