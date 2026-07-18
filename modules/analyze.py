import re
import pandas as pd
from transformers import pipeline
import os

# 감정 분석 모델
analyzer = pipeline("text-classification", model="beomi/KcELECTRA-base")

label_map = {
    "LABEL_0": "중립",
    "LABEL_1": "기쁨/행복",
    "LABEL_2": "슬픔",
    "LABEL_3": "분노",
    "LABEL_4": "설렘",
    "LABEL_5": "당황"
}





def analyze_chat(file_path, my_name, opponent_name):
    df = pd.read_csv(file_path) #데이터 프레임으로 변환

    # # 날짜와 시간 컬럼 합치기 필요 시
    # if '시간' in df.columns:
    #     df['시'] = df['시간'].str.split(':').str[0].astype(int)
    # else:
    #     df['시'] = 0  # 기본값 

    df['날짜'] = pd.to_datetime(df['Date']).dt.date # Date 컬럼을 datetime으로 변환
    df['시'] = pd.to_datetime(df['Date']).dt.hour #Date컬럼에서 시간을 추출
    df['사용자'] = df['User'] # 사용자 컬럼을 User 컬럼으로 바꿈
    df['메시지'] = df['Message'] #메세지 커럼을 Message 컬럼으로 바꿈

    # 감정 분석 컬럼 생성
    df["감정"] = df["메시지"].apply(lambda x: label_map.get(analyzer(x)[0]['label'], "모름"))

    df_opponent = df[df["사용자"] == opponent_name]

    # 선톡 통계
    first_talker = df.groupby("날짜").first()["사용자"].value_counts()
    first_text = (
        f"{my_name}가 더 자주 먼저 메시지를 보냅니다."
        if first_talker.idxmax() == opponent_name
        else f"{opponent_name}가(이) 더 자주 먼저 메시지를 보냅니다."
    )

    # 시간대
    hourly = df.groupby("시").size()
    peak_hour = hourly.idxmax()
    peak_count = hourly.max()
    hour_text = f"가장 활발한 시간대는 {peak_hour}시 ({peak_count}개 메시지)"

    # 감정 요약
    # emo_count = df_opponent["감정"].value_counts(normalize=True).head(2)
    # emo_text = ", ".join([f"{k}({round(v*100)}%)" for k, v in emo_count.items()])
    # sentiment_summary = f"상대방은 주로 {emo_text} 감정을 보입니다."
    # emotion_counts = df['감정'].value_counts()
    #
    # if len(emotion_counts) == 0:
    #     return "감정을 분석할 수 없습니다."
    #
    # top_emotion_idx = emotion_counts.idxmax()
    # top_emotion_label = EMOTION_MAP.get(int(top_emotion_idx), "알 수 없음")
    #
    # summary = f"상대방은 주로 {top_emotion_label} 감정을 느낍니다."

    emotion_counts = df['감정'].value_counts()

    if len(emotion_counts) == 0:
        summary = f"상대방은 감정을 분석할 수 없습니다."
    else:
        top_emotion_label = emotion_counts.idxmax()  # 문자열 그대로
        summary = f"상대방은 주로 {top_emotion_label} 감정을 느낍니다."

    return {
        "data": df,
        "first_talker_summary": first_talker.to_string(),
        "first_text": first_text,
        "hour_text": hour_text,
        "sentiment_summary_text": summary
    }