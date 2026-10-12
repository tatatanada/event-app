import streamlit as st

st.set_page_config(page_title="地域貢献講演会 受付システム", page_icon="📋")

st.title("🏛️ 地域貢献講演会（南大阪支店）受付システム")
st.write("ご来場ありがとうございます。必要事項を入力してください。")

# 入力フォーム
with st.form("registration_form"):
    company = st.text_input("会社名・団体名")
    name = st.text_input("お名前")
    phone = st.text_input("電話番号")
    email = st.text_input("メールアドレス")
    
    submitted = st.form_submit_button("受付を完了する")
    
    if submitted:
        if name and (phone or email):
            st.success(f"【受付完了】{name} 様の登録を受け付けました。ご入場いただけます。")
        else:
            st.error("お名前と、連絡先（電話番号またはメールアドレス）を入力してください。")
