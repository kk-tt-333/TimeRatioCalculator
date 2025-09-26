import streamlit as st

st.title("⏱ 勤務時間割合分配ツール")

# 勤務時間入力
col1, col2 = st.columns(2)
with col1:
    hours = st.number_input("勤務時間（時間）", min_value=0, step=1)
with col2:
    minutes = st.number_input("勤務時間（分）", min_value=0, step=1)

total_time = hours * 60 + minutes

# 割合入力
ratios = st.text_area("割合をカンマ区切りで入力（例: 50,30,20）", "50,30,20")
ratios_list = [float(r.strip()) for r in ratios.split(",") if r.strip().isdigit()]

# 分を hh:mm に変換
def to_hhmm(minutes: float) -> str:
    h, m = divmod(round(minutes), 60)
    return f"{h:02d}:{m:02d}"

if st.button("計算する"):
    if total_time > 0 and len(ratios_list) > 0:
        total_ratio = sum(ratios_list)
        results = []
        for idx, r in enumerate(ratios_list, start=1):
            minutes = (r / total_ratio) * total_time
            results.append(f"作業{idx} → {to_hhmm(minutes)}")
        
        st.subheader("📊 計算結果 (hh:mm)")
        st.write("\n".join(results))

        # コピー用テキスト
        st.code("\n".join(results), language="text")
    else:
        st.warning("勤務時間と割合を正しく入力してください。")
