
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

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
                
                # メール送信の試行（Secrets未設定時は安全に画面表示のみ行われます）
                try:
                    smtp_server = "smtp.mail.yahoo.co.jp"
                    smtp_port = 587
                    sender_email = st.secrets["YAHOO_EMAIL"]
                    sender_password = st.secrets["YAHOO_PASSWORD"]
                    
                    msg_text = f"""{name} 様

この度は「地域貢献講演会（南大阪支部）」にお申し込みいただき、誠にありがとうございます。
以下の内容でご登録を承りました。

【ご登録内容】
・受付番号：第 {ticket_number} 号
・会社名・団体名：{company if company else '一般'}
・お名前：{name} 様
・電話番号：{phone}
・メールアドレス：{email}

当日は受付にてこちらの受付番号またはメール画面をお伝えください。

--------------------------------------------------
南大阪支部 (072-958-3005)
--------------------------------------------------"""

                    msg = MIMEText(msg_text, "plain", "utf-8")
                    msg["Subject"] = "【地域貢献講演会】受付完了のお知らせ（南大阪支部）"
                    msg["From"] = formataddr(("南大阪支部 事務局", sender_email))
                    msg["To"] = email

                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.send_message(msg)
                    
                    email_status = "📩 確認メールを送信しました。"
                except Exception:
                    email_status = "（※メール送信設定は未設定のため、画面表示のみで行いました）"

                st.success(f"🎉 受付が完了しました！")
                st.markdown(f"### 【あなたの受付番号】 **第 {ticket_number} 号**")
                st.write(f"**{name} 様**（{company if company else '一般'}）のご登録を承りました。")
                st.info(f"{email_status}\n\n【お問い合わせ先】南大阪支部 (072-958-3005)")
