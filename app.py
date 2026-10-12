import streamlit as st

st.set_page_config(page_title="地域貢献講演会 受付システム", page_icon="📋")

st.title("地域貢献講演会 受付システム\n南大阪支部 (072-958-3005)")
st.write("ご来場ありがとうございます。必要事項を入力してください。（定員：500名様）")

# 簡易的な登録カウンター（セッション状態を利用）
if "registered_count" not in st.session_state:
    st.session_state.registered_count = 0  # 現在の登録数
    st.session_state.registered_emails = []  # 重複チェック用

MAX_CAPACITY = 500
current_count = st.session_state.registered_count

# 定員に達しているかのチェック
if current_count >= MAX_CAPACITY:
    st.error("申し訳ございません。本イベントは定員（500名）に達したため、受付を終了いたしました。")
else:
    st.info(f"現在の受付状況: 残り枠 {MAX_CAPACITY - current_count} 名様（受付済み: {current_count}名）")

    # 入力フォーム
    with st.form("registration_form"):
        company = st.text_input("会社名・団体名")
        name = st.text_input("お名前 *必須")
        phone = st.text_input("電話番号 *必須")
        email = st.text_input("メールアドレス *必須")
        
        submitted = st.form_submit_button("受付を完了する")
        
        if submitted:
            if not name or not phone or not email:
                st.error("「お名前」「電話番号」「メールアドレス」はすべて入力してください。")
            elif email in st.session_state.registered_emails:
                st.warning("⚠️ このメールアドレスはすでに登録されています（お一人様1回までとなります）。")
            else:
                # 定員を1増やす
                st.session_state.registered_count += 1
                ticket_number = st.session_state.registered_count
                
                # 登録済みメールアドレスとして記録
                st.session_state.registered_emails.append(email)
                
                # 完了メッセージと整理番号の発行
                st.success(f"🎉 受付が完了しました！")
                st.markdown(f"### 【あなたの受付番号】 **第 {ticket_number} 号**")
                st.write(f"**{name} 様**（{company if company else '一般'}）のご登録を承りました。")
                st.info(f"📩 確認メールを **{email}** 宛てに送信しました。当日はこの受付番号をお知らせください。\n\n【お問い合わせ先】南大阪支部 (072-958-3005)")
