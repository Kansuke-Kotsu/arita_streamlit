import streamlit as st
from datetime import date

st.set_page_config(page_title="簡易フォトアップローダー", page_icon="📷", layout="centered")

# ────────────────────────────────────────────────
# 0. ステート初期化
# ────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = "basic"   # basic → consent → upload → done
    st.session_state.basic = {}
    st.session_state.summary = {}

# ────────────────────────────────────────────────
# 1. 基本情報入力
# ────────────────────────────────────────────────
if st.session_state.step == "basic":
    st.markdown("## 基本情報の入力画面")

    with st.form("basic_form", clear_on_submit=False):
        dob = st.date_input("生年月日", value=date(2000, 1, 1), format="YYYY-MM-DD")
        gender = st.radio("性別", ["男性", "女性", "その他"])
        submitted = st.form_submit_button("次へ ▶️")

    if submitted:
        st.session_state.basic = {"dob": dob.isoformat(), "gender": gender}
        st.session_state.step = "consent"
        st.rerun()

# ────────────────────────────────────────────────
# 2. 同意
# ────────────────────────────────────────────────
elif st.session_state.step == "consent":
    st.markdown("## 情報の取り扱いについての同意確認画面")
    st.write("""
    当サービスではアップロードされた写真を 30 日以内に自動削除します。
    詳細はプライバシーポリシーをご確認ください。
    """)
    agree = st.checkbox("上記に同意します ✅")

    if st.button("アップロード画面 ▶️", disabled=not agree):
        st.session_state.step = "upload"
        st.rerun()

    if st.button("戻る ⬅️"):
        st.session_state.step = "basic"
        st.rerun()

# ────────────────────────────────────────────────
# 3. アップロード
# ────────────────────────────────────────────────
elif st.session_state.step == "upload":
    st.markdown("## 画像アップロード")
    st.info("↓一旦そのまま「完了」を押してください（開発用）。")

    # 複数ファイルを選べる設定。空でも可。
    files = st.file_uploader("画像を選択（複数可）", type=["jpg", "jpeg", "png"],
                             accept_multiple_files=True)

    if st.button("完了 ✅"):
        # ファイルが無い & 開発用 → ダミー
        if not files:
            st.session_state.summary = {"total": 10, "person": 3, "landscape": 5, "other": 2}
        else:
            # 実際にはここでファイル保存などを行う
            st.session_state.summary = {
                "total": len(files),
                "person": 0,
                "landscape": 0,
                "other": len(files),  # ここでは分類せず全部「その他」に
            }
        st.session_state.step = "done"
        st.rerun()

    if st.button("戻る ⬅️"):
        st.session_state.step = "consent"
        st.rerun()

# ────────────────────────────────────────────────
# 4. 完了画面
# ────────────────────────────────────────────────
elif st.session_state.step == "done":
    s = st.session_state.summary
    st.success(f"写真が **{s['total']} 枚** アップされました 🎉")
    st.write(f"内訳 ⇒ 人物：{s['person']} 枚、風景：{s['landscape']} 枚、その他：{s['other']} 枚")

    col1, col2 = st.columns(2)
    with col1:
        st.button("人物の写真も含めてアップする（開発用）", use_container_width=True)
    with col2:
        st.button("人物の写真以外をアップする", use_container_width=True)

    st.markdown("---")
    if st.button("もう一度試す 🔄"):
        for key in ("step", "basic", "summary"):
            st.session_state.pop(key, None)
        st.rerun()
