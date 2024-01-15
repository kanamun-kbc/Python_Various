import os
import requests
import pprint
import tkinter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Application(tkinter.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=680, height=280)
        self.root = root
        self.pack()
        self.pack_propagate(0)
        self.create_widgets()
	
    # symbolの入力欄と実行ボタン
    def create_widgets(self):
		# テキストボックス
		# 作成
        self.text_box = tkinter.Entry(self)
		# 幅設定
        self.text_box['width'] = 10
		# 設置
        self.text_box.pack()
		
		# 実行ボタン
		# 作成
        submit_btn = tkinter.Button(self)
		# ボタンの名前を'実行'
        submit_btn['text'] = '実行'
		# 押すとdisplay_graphが呼ばれるようにする
        submit_btn['command'] = self.display_graph
		# 設置
        submit_btn.pack()
		
		# グラフを表示させるためのウィジェット
		# フォントサイズ
        plt.rcParams['font.size'] = 7
		# figureオブジェクトとaxesオブジェクトを作成
		# それぞれのオブジェクトを、繰り返し使いたい、
		# 別のメソッドでも使いたい故のself(インスタンス変数)
        self.fig, self.ax = plt.subplots(figsize=(12, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()

    def display_graph(self):
        try:
            # 環境変数に設定したAPI KEY
            api_key = os.environ['ALPHA_VANTAGE_KEY']
        except KeyError:
            print("環境変数 'ALPHA_VANTAGE_KEY' が設定されていません。")
            return

        # テキストボックスからsymbolを取得
        symbol = self.text_box.get()
        # symbol社の日時の株価
        url = 'https://www.alphavantage.co/query?' \
             f'function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
        data = requests.get(url).json()
        # pprint.pprint(data) # 情報取得確認

        # 逆順にする(グラフにすると未来→過去の順になっていたため)
        daily_data = dict(reversed(data['Time Series (Daily)'].items()))
        # 辞書のキーの部分に日付があることを確認した
        # これをX軸のデータとする
        date_list = daily_data.keys()
        # 終日株価はバリューの「4. close」というところにある
        # データ内で株価は文字列として保存されているのでfloatに変換
        # これをY軸のデータとする
        close_list = [float(x['4. close']) for x in daily_data.values()]

        # 前回のグラフをクリア
        self.ax.clear()
        self.ax.plot(date_list, close_list)
        # 100日分の見にくかったデータを15日ごとに分割
        self.ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))
        self.ax.grid()
        # グラフ描画用ウィジェットに描画
        self.canvas.draw()
        # fig.savefig('./stock.png') # 確認用


def main():
	root = tkinter.Tk()
	root.title('株価チャートアプリ')
	root.geometry('700x300')
	app = Application(root=root)
	app.mainloop()


if __name__ == '__main__':
    main()
