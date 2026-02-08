import streamlit as st
from openai import OpenAI

# --- 页面基础配置 ---
st.set_page_config(page_title="The Hook Doctor 🪝", page_icon="🩺", layout="wide")

# --- 侧边栏：配置区 ---
with st.sidebar:
    st.header("⚙️ Configuration")
    # 这里输入你在 DeepSeek 官网申请的 key
    api_key = st.text_input("DeepSeek API Key", type="password", help="Paste your sk-xxxx key here")
    
    st.markdown("---")
    st.info("💡 **Tip:** This tool uses DeepSeek-V3 to analyze your novel's opening chapter for Western market (Royal Road/Amazon) standards.")

# --- 主界面 ---
st.title("The Hook Doctor 🩺 (MVP Ver.)")
st.markdown("#### 专治网文“黄金三章”劝退病 | Fix your Opening Chapter")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Input Your Chapter")
    # 输入小说正文
    novel_text = st.text_area("Paste English Draft Here (First 1000-2000 words):", height=400, placeholder="The dragon roared and the system window popped up...")
    
    # 诊断按钮
    analyze_btn = st.button("🚀 Diagnose Now", type="primary", use_container_width=True)

with col2:
    st.subheader("2. Diagnosis Report")
    # 结果显示区
    if analyze_btn:
        if not api_key:
            st.error("❌ Please enter your API Key in the sidebar first!")
        elif not novel_text:
            st.warning("⚠️ Please paste your story text first!")
        else:
            status_box = st.status("🧠 Dr. DeepSeek is reading your draft...", expanded=True)
            try:
                # --- 核心：调用 DeepSeek API ---
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                
                # 这里是我们设计的“毒舌编辑” Prompt
                system_prompt = """
                Role: You are a ruthless, data-driven Senior Editor for Royal Road (top Western web novel platform). 
                Objective: Analyze the user's Chapter 1.
                
                Output Format (Use Markdown):
                ## 📊 Scorecard
                - **Hook Strength:** [Score]/10 (Did it grab me in 300 words?)
                - **Pacing:** [Score]/10
                - **Agency:** [Score]/10 (Is MC active or reactive?)
                
                ## 🩺 The Diagnosis
                [Be direct. Quote the exact bad sentences. Explain WHY it fails for Western readers. No fluff.]
                
                ## 💊 The Prescription
                1. **Fix the Hook:** [Concrete rewrite suggestion]
                2. **Cut the Fat:** [Identify boring parts]
                3. **System/Cheat Check:** [Is the unique selling point clear?]
                """
                
                response = client.chat.completions.create(
                    model="deepseek-chat",  # 调用 V3 模型，便宜又快
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": novel_text}
                    ],
                    stream=False
                )
                
                result = response.choices[0].message.content
                
                # 显示结果
                status_box.update(label="✅ Diagnosis Complete!", state="complete", expanded=False)
                st.markdown(result)
                
            except Exception as e:
                status_box.update(label="❌ Error occurred", state="error")
                st.error(f"Error details: {e}")
                st.info("Check if your API Key is correct and you have balance (DeepSeek gives free credits).")