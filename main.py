from modules.analyze import analyze_chat
from modules.visualize import plot_hourly_activity, plot_sentiment_trend

FILE_PATH = "data/Talk.txt"
MY_NAME = "이민준"           # 본인 이름
OPPONENT_NAME = ""      # 상대방 이름

def main():



    print(" 카카오톡 감정 분석 시작 중...\n")
    result = analyze_chat(FILE_PATH, MY_NAME, OPPONENT_NAME)

    print("\n 분석 완료!")
    print("\n 선톡 통계:")
    print(result['first_talker_summary']) #pandas.Series. print()하면 Name: count, dtype: int64 같은 메타가 나올 수 있음.
    print(result['first_text'])

    print("\n  시간대별 대화량 요약:")
    print(result['hour_text'])

    print("\n 상대방 감정 요약:")
    print(result['sentiment_summary_text'])


    # 시각화
    plot_hourly_activity(result['data']) #대화 시간대
    plot_sentiment_trend(result['data']) # 대화수

if __name__ == "__main__":
    main()