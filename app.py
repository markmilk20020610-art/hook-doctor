import streamlit as st
from openai import OpenAI
import time

# --- 1. 页面基础配置 ---
st.set_page_config(page_title="The Hook Doctor 🪝", page_icon="🩺", layout="wide")

# --- 2. 初始化防抖动变量 (防止用户疯狂点击) ---
if "last_call_time" not in st.session_state:
    st.session_state.last_call_time = 0

# --- 3. 侧边栏：设置区 ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # 输入 DeepSeek API Key
    api_key = st.text_input("DeepSeek API Key", type="password", help="Get it from platform.deepseek.com")
    
    st.markdown("---")
    
    # [未来功能] 订阅验证区 (目前是装饰，以后接 Gumroad)
    st.subheader("💎 Pro Access")
    license_key = st.text_input("License Key (Optional)", placeholder="Paste Gumroad Key here")
    st.caption("Pro features: Unlimited words, Deep Rewrites.")
    
    st.markdown("---")
    st.info("💡 **Tip:** This tool uses DeepSeek-V3 logic optimized for Royal Road & Wattpad trends.")

# --- 4. 主界面 ---
st.title("The Hook Doctor 🩺")
st.markdown("#### 🚀 Fix your Web Novel's First Chapter (MVP Ver.)")
st.markdown("Stop losing readers in the first 300 words. Get a brutal diagnosis + **A Pro Rewrite** from AI.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Input Draft")
    # 输入小说正文
    novel_text = st.text_area("Paste English Chapter Here (Limit: 2000 words):", height=600, placeholder="The dragon roared...")
    
    # 诊断按钮
    analyze_btn = st.button("💉 Diagnose & Rewrite", type="primary", use_container_width=True)

with col2:
    st.subheader("2. Diagnosis Report")
    
    # --- 5. 核心逻辑区 ---
    if analyze_btn:
        current_time = time.time()
        
        # --- 防御 A: 冷却检查 (10秒内不能重复点) ---
        if current_time - st.session_state.last_call_time < 10:
            st.warning("⏳ Whoa, slow down! The doctor is still thinking. Please wait 10 seconds.")
        
        # --- 防御 B: 基础检查 ---
        elif not api_key:
            st.error("❌ Please enter your DeepSeek API Key in the sidebar!")
        elif not novel_text:
            st.warning("⚠️ Please paste your story text first!")
            
        else:
            # 记录这次调用的时间
            st.session_state.last_call_time = current_time
            
            status_box = st.status("🧠 Dr. DeepSeek is reading & rewriting...", expanded=True)
            
            try:
                # 初始化 DeepSeek 客户端
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                
                # --- 核心 System Prompt (高价值版) ---
                system_prompt = """
                Role: You are a ruthless, data-driven Senior Editor for Royal Road (top Western web novel platform). 
                Objective: Analyze the user's Chapter 1 AND provide a superior rewrite to demonstrate the fix.
                
                Output Format (Use Markdown):
                ## 📊 Diagnostic Scorecard
                - **Hook Strength:** [Score]/10 (Did it grab me in 300 words?)
                - **Pacing:** [Score]/10
                - **Agency:** [Score]/10 (Is MC active or reactive?)
                
                ## 🩺 The Diagnosis (Brutal Honesty)
                [Be direct. Quote the exact bad sentences. Explain WHY it fails for Western readers (e.g. passive voice, waking up clichés, info-dumps). No fluff.]
                
                ## 💊 The Prescription (Strategy)
                1. **Fix the Hook:** [Concrete idea to make the opening stronger]
                2. **Cut the Fat:** [Identify boring parts to delete]
                
                ## ✍️ The Rewrite (Demonstration)
                [This is the most important part. Rewrite the first 200-300 words of their story applying your fixes. 
                - Start In Media Res (in the middle of action).
                - Show, Don't Tell.
                - Make the conflict immediate. 
                - Show the user exactly how a pro would write this scene to get more views.]
                """
                
                # 调用 API
                response = client.chat.completions.create(
                    model="deepseek-chat",  # V3 模型，便宜且快
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
                st.info("Check if your API Key is correct and you have balance.")

# 页脚
st.markdown("---")
st.caption("Powered by DeepSeek V3 | Designed for Indie Authors")
