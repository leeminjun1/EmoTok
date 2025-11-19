import tkinter as tk
from tkinter import filedialog, scrolledtext
from modules.analyze import analyze_chat
from modules.visualize import plot_hourly_activity, plot_sentiment_trend
import pandas as pd
import re

FILE_PATH = None
analyzed_df = None


def remove_emoji(text):
    if not isinstance(text, str):
        text = str(text)
    emoji_pattern = re.compile(
        "[" # 이모지 범위를 포함한 정규식
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def detect_opponent_name(file_path, my_name):
    df = pd.read_csv(file_path)
    df['CleanUser'] = df['User'].apply(remove_emoji)
    names_found = [name for name in df['CleanUser'].unique() if name != my_name]
    return names_found[0] if names_found else None


def select_file():
    global FILE_PATH
    FILE_PATH = filedialog.askopenfilename(
        title="카카오톡 CSV 파일 선택",
        filetypes=[("CSV Files", "*.csv")]
    )
    if FILE_PATH:
        text_area.insert(tk.END, f"[파일 선택됨] {FILE_PATH}\n")


def run_analysis():
    global analyzed_df

    if not FILE_PATH:
        text_area.insert(tk.END, "⚠️ 먼저 CSV 파일을 선택하세요!\n")
        return

    my_name = entry_my_name.get().strip()
    if not my_name:
        text_area.insert(tk.END, "⚠️ 먼저 내 이름을 입력하세요!\n")
        return

    opponent_name = detect_opponent_name(FILE_PATH, my_name)
    if opponent_name is None:
        text_area.insert(tk.END, "⚠️ 상대방 이름을 자동으로 찾지 못했습니다.\n")
        return

    text_area.insert(tk.END, f"🤖 자동 인식된 상대방: {opponent_name}\n\n")
    text_area.insert(tk.END, "📌 카카오톡 감정 분석 시작...\n")

    try:
        result = analyze_chat(FILE_PATH, my_name, opponent_name)
    except Exception as e:
        text_area.insert(tk.END, f"⚠️ 분석 중 오류 발생: {e}\n")
        return

    text_area.insert(tk.END, "🎉 분석 완료!\n\n")

    text_area.insert(tk.END, "📌 [선톡 통계]\n")
    text_area.insert(tk.END, str(result['first_talker_summary']) + "\n")
    text_area.insert(tk.END, result['first_text'] + "\n\n")

    text_area.insert(tk.END, "📌 [시간대별 대화량]\n")
    text_area.insert(tk.END, result['hour_text'] + "\n\n")

    text_area.insert(tk.END, "📌 [감정 요약]\n")
    text_area.insert(tk.END, result['sentiment_summary_text'] + "\n\n")

    analyzed_df = result["data"]


def show_hourly_plot():
    if analyzed_df is None:
        text_area.insert(tk.END, "⚠️ 먼저 감정 분석을 실행하세요!\n")
        return
    plot_hourly_activity(analyzed_df)

def show_sentiment_plot():
    if analyzed_df is None:
        text_area.insert(tk.END, "⚠️ 먼저 감정 분석을 실행하세요!\n")
        return
    plot_sentiment_trend(analyzed_df)


root = tk.Tk()
root.title("EmoTok - 카톡 감정 분석기")
root.geometry("780x620")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

# 내 이름 입력
tk.Label(frame_top, text="내 이름:").grid(row=0, column=0, padx=5)
entry_my_name = tk.Entry(frame_top, width=20)
entry_my_name.grid(row=0, column=1, padx=5)

# 버튼
btn_file = tk.Button(frame_top, text="CSV 파일 선택", command=select_file, width=20)
btn_file.grid(row=1, column=0, padx=5, pady=5)

btn_run = tk.Button(frame_top, text="감정 분석 실행", command=run_analysis, width=20)
btn_run.grid(row=1, column=1, padx=5, pady=5)

btn_plot1 = tk.Button(frame_top, text="시간대 그래프", command=show_hourly_plot, width=20)
btn_plot1.grid(row=1, column=2, padx=5, pady=5)

btn_plot2 = tk.Button(frame_top, text="감정 변화 그래프", command=show_sentiment_plot, width=20)
btn_plot2.grid(row=1, column=3, padx=5, pady=5)

# 출력창
text_area = scrolledtext.ScrolledText(root, width=90, height=32)
text_area.pack(pady=10)

root.mainloop()
