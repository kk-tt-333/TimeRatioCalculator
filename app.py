import streamlit as st

st.title("⏱ 勤務時間割合分配ツール")

# 勤務時間入力（4桁の数字で入力）
time_input = st.text_input(
    "勤務時間 (4桁で入力: 例 0123 = 1時間23分)", 
    placeholder="0123",
    max_chars=4,
    help="半角数字のみ入力可能"
)

# 全角数字を半角数字に変換
def to_halfwidth(text):
    """全角数字を半角数字に変換"""
    full_to_half = str.maketrans('０１２３４５６７８９', '0123456789')
    return text.translate(full_to_half)

# 4桁の数字を時間と分に変換
def parse_time_input(input_str):
    # 全角数字を半角に変換
    input_str = to_halfwidth(input_str)
    if len(input_str) == 4 and input_str.isdigit():
        hours = int(input_str[:2])
        minutes = int(input_str[2:4])
        return hours * 60 + minutes
    return 0

# 入力値を半角に変換
time_input_halfwidth = to_halfwidth(time_input)
total_time = parse_time_input(time_input_halfwidth)

# 変換結果を表示（デバッグ用）
if time_input != time_input_halfwidth:
    st.info(f"入力値を半角に変換しました: {time_input} → {time_input_halfwidth}")

# 割合入力
ratios = st.text_area(
    "割合をカンマ区切りで入力（例: 50,30,20）", 
    "50,30,20",
    help="半角数字とカンマのみ入力可能"
)

# 割合入力を半角に変換して処理
ratios_halfwidth = to_halfwidth(ratios)
ratios_list = [float(r.strip()) for r in ratios_halfwidth.split(",") if r.strip().replace(".", "").isdigit()]

# 変換結果を表示（デバッグ用）
if ratios != ratios_halfwidth:
    st.info(f"割合入力を半角に変換しました: {ratios} → {ratios_halfwidth}")

# 分を hh:mm に変換
def to_hhmm(minutes: float) -> str:
    h, m = divmod(round(minutes), 60)
    return f"{h:02d}:{m:02d}"

# セッション状態で結果を保持
if 'results' not in st.session_state:
    st.session_state.results = []
if 'time_only_results' not in st.session_state:
    st.session_state.time_only_results = []

if st.button("計算する"):
    if total_time > 0 and len(ratios_list) > 0:
        total_ratio = sum(ratios_list)
        results = []
        time_only_results = []
        
        for idx, r in enumerate(ratios_list, start=1):
            minutes = (r / total_ratio) * total_time
            hhmm = to_hhmm(minutes)
            results.append(f"作業{idx} → {hhmm}")
            time_only_results.append(hhmm)
        
        # セッション状態に保存
        st.session_state.results = results
        st.session_state.time_only_results = time_only_results
        st.session_state.ratios_list = ratios_list
            
    else:
        st.warning("勤務時間と割合を正しく入力してください。")

# 結果表示（セッション状態から）
if st.session_state.results:
    st.subheader("📊 計算結果 (hh:mm)")
    
    # 作業ごとに分けて表示
    for idx, (result, time_only) in enumerate(zip(st.session_state.results, st.session_state.time_only_results), start=1):
        st.write(f"**作業{idx}**: 割合 {st.session_state.ratios_list[idx-1]} → {time_only}")
        
        # コピー用テキストを表示（選択可能）
        st.code(time_only, language="text")
    
    # 全時間をコピー
    all_times = "\n".join(st.session_state.time_only_results)
    
    # コピー用のテキストを表示（選択可能）
    if st.session_state.time_only_results:
        st.markdown("**全時間（選択してコピーしてください）:**")
        st.code(all_times, language="text")
