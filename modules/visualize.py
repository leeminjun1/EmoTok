# # import matplotlib.pyplot as plt
# # import matplotlib
# # import seaborn as sns
# #
# # # 한글 폰트 설정 (macOS)
# # matplotlib.rc('font', family='AppleGothic')
# # plt.rcParams['axes.unicode_minus'] = False
# #
# # def plot_hourly_activity(df):
# #     hourly = df.groupby("시").size() # 시로 그룹화하고 각 그룹의 크기를 센다
# #     plt.figure(figsize=(10,5)) # 새 그림 생성 width = 10인치, height = 5인치
# #     sns.barplot(x=hourly.index, y=hourly.values, color="skyblue") # seaborn 의 막대그래프 x축은 시간, y축은 메시지 수
# #     plt.title("시간대별 대화량") # 제목
# #     plt.xlabel("시간") # x 레이블
# #     plt.ylabel("메시지 수") # y 레이블
# #     plt.tight_layout()
# #     plt.show() # 보여줌
# #
# # def plot_sentiment_trend(df):
# #     if "감정" not in df.columns:
# #         print("⚠️ 감정 컬럼이 없습니다. 감정 분석을 먼저 수행하세요.")
# #         return
# #
# #     sentiment_map = {"긍정": 1, "중립": 0, "부정": -1}
# #     df["감정점수"] = df["감정"].map(lambda x: sentiment_map.get(x, 0))
# #
# #     df.plot(y="감정점수", kind="line")
# #
# #     sentiment_map = {"기쁨":1, "행복":1, "설렘":1, "슬픔":-1, "분노":-1, "당황":0, "중립":0} #감정 레이블을 점수로 매핑한 딕셔너리
# #     df["감정점수"] = df["감정"].map(lambda x: sentiment_map.get(x,0))
# #     daily = df.groupby("날짜")["감정점수"].mean() #날짜"별로 그룹화해서 "감정점수"의 평균을 계산
# #
# #     plt.figure(figsize=(10,5)) # 새 그림 생성
# #     sns.lineplot(x=daily.index, y=daily.values, marker="o") # x축은 날짜 인덱스, y축은 평균 감정점수
# #     plt.title("날짜별 평균 감정 추이") # 제목
# #     plt.xlabel("날짜") # x 레이블
# #     plt.ylabel("감정 점수 (긍정↑ / 부정↓)") # y 레이블
# #     plt.xticks(rotation=45)
# #     plt.tight_layout()
# #     plt.show() #보여줌
#
# import matplotlib.pyplot as plt
# import matplotlib
# import seaborn as sns
#
# matplotlib.rc('font', family='AppleGothic')
# plt.rcParams['axes.unicode_minus'] = False
#
#
# def plot_hourly_activity(df):
#     hourly = df.groupby("시").size()
#     plt.figure(figsize=(10,5))
#     sns.barplot(x=hourly.index, y=hourly.values)
#     plt.title("시간대별 대화량")
#     plt.xlabel("시간")
#     plt.ylabel("메시지 수")
#     plt.tight_layout()
#     plt.show()
#
#
# def plot_sentiment_trend(df):
#     if "감정" not in df.columns:
#         print("⚠ 감정 컬럼 없음")
#         return
#
#     score_map = {
#         "기쁨/행복": 1, "설렘": 1,
#         "슬픔": -1, "분노": -1,
#         "당황": 0, "중립": 0
#     }
#
#     df["감정점수"] = df["감정"].map(lambda x: score_map.get(x, 0))
#     daily = df.groupby("날짜")["감정점수"].mean()
#
#     plt.figure(figsize=(10,5))
#     sns.lineplot(x=daily.index, y=daily.values, marker="o")
#     plt.title("날짜별 평균 감정 변화")
#     plt.xlabel("날짜")
#     plt.ylabel("감정 점수")
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()

import matplotlib
matplotlib.use('TkAgg')  # Tkinter용 백엔드
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Arial'

def plot_hourly_activity(df):
    hourly = df.groupby("시").size()
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=hourly.index, y=hourly.values, ax=ax)
    ax.set_title("Conversation volume by time zone")
    ax.set_xlabel("time zone")
    ax.set_ylabel("messages")
    plt.tight_layout()
    plt.show(block=False)  # <-- block=False 필수, 버튼 클릭 시 GUI 멈추지 않게

def plot_sentiment_trend(df):
    if "감정" not in df.columns:
        print("⚠ 감정 컬럼 없음")
        return

    score_map = {
        "기쁨/행복": 1, "설렘": 1,
        "슬픔": -1, "분노": -1,
        "당황": 0, "중립": 0
    }

    df["감정점수"] = df["감정"].map(lambda x: score_map.get(x, 0))
    daily = df.groupby("날짜")["감정점수"].mean()

    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(x=daily.index, y=daily.values, marker="o", ax=ax)
    ax.set_title("Average Emotional Change by Date")
    ax.set_xlabel("date")
    ax.set_ylabel("emotional change")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show(block=False)  # <-- block=False 필수
