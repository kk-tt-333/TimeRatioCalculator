import streamlit as st

st.title("⏱ 時間割合計算ツール")

# 全体の時間を入力
total_time = st.number_input("全体の時間（分）", min_value=0, step=1)

# 割合入力
ratios = st.text_area("割合をカンマ区切りで入力（例: 100,40,20）", "100,40,20")
ratios_list = [float(r.strip()) for r in ratios.split(",") if r.strip().isdigit()]

# 分を hh:mm に変換する関数
def to_hhmm(minutes: float) -> str:
    h, m = divmod(round(minutes), 60)
    return f"{h:02d}:{m:02d}"

if st.button("計算する"):
    if total_time > 0 and len(ratios_list) > 0:
        total_ratio = sum(ratios_list)
        results = []
        for r in ratios_list:
            minutes = (r / total_ratio) * total_time
            results.append(f"割合 {r} → {to_hhmm(minutes)}")
        
        st.subheader("📊 計算結果")
        st.write("\n".join(results))

        # コピー用テキスト（全部 hh:mm）
        st.code("\n".join(results), language="text")
    else:
        st.warning("全体の時間と割合を正しく入力してください。")
