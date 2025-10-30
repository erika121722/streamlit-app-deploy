import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os



# 環境変数の読み込み
load_dotenv()

def get_expert_response(input_text: str, expert_type: str) -> str:
    """
    選択された専門家の種類に基づいてLLMから回答を取得する関数
    
    Args:
        input_text (str): ユーザーからの入力テキスト
        expert_type (str): 選択された専門家の種類
    
    Returns:
        str: LLMからの回答
    """
    # 専門家の種類に応じたシステムメッセージを設定
    system_messages = {
        "ITコンサルタント": "あなたは経験豊富なITコンサルタントです。IT戦略、システム開発、デジタルトランスフォーメーション、" \
                    "技術選定などについて、実践的かつ専門的なアドバイスを提供してください。",
        "キャリアアドバイザー": "あなたは経験豊富なキャリアアドバイザーです。転職、キャリア開発、スキルアップ、" \
                    "職務経歴書の作成などについて、実践的かつ具体的なアドバイスを提供してください。"
    }
    
    # ChatGPTモデルのインスタンスを作成
    chat = ChatOpenAI(
        temperature=0.7,
        model_name="gpt-3.5-turbo",
    )
    
    # メッセージを作成
    messages = [
        SystemMessage(content=system_messages[expert_type]),
        HumanMessage(content=input_text)
    ]
    
    # LLMに質問を送信し、回答を取得
    response = chat.invoke(messages)
    
    return response.content

# Streamlitアプリケーションのメイン部分
def main():
    # アプリケーションのタイトルを設定
    st.title("専門家AI アドバイザー")
    
    # アプリケーションの説明を追加
    st.markdown("""
    ### 📱 アプリケーションの使い方
    1. 右側のラジオボタンから相談したい専門家を選択してください
    2. テキストボックスに質問や相談内容を入力してください
    3. 「送信」ボタンをクリックすると、選択した専門家からの回答が表示されます
    
    ### 👨‍💼 選択可能な専門家
    - **ITコンサルタント**: IT戦略、システム開発、技術選定などに関するアドバイス
    - **キャリアアドバイザー**: 転職、キャリア開発、スキルアップなどに関するアドバイス
    """)
    
    # 専門家の選択（ラジオボタン）
    expert_type = st.radio(
        "相談したい専門家を選択してください：",
        ["ITコンサルタント", "キャリアアドバイザー"]
    )
    
    # 入力フォーム
    user_input = st.text_area(
        "質問や相談内容を入力してください：",
        height=150
    )
    
    # 送信ボタン
    if st.button("送信"):
        if user_input:
            # ローディング表示
            with st.spinner("回答を生成中..."):
                try:
                    # LLMから回答を取得
                    response = get_expert_response(user_input, expert_type)
                    # 回答を表示
                    st.markdown("### 💡 回答")
                    st.write(response)
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")
        else:
            st.warning("質問や相談内容を入力してください。")

if __name__ == "__main__":
    main()