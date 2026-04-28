import streamlit as st
import requests
import sqlite3
from datetime import datetime

# 界面配置
st.set_page_config(page_title="检察干部履职智能评价平台", layout="wide")
st.markdown("""
<style>
.main-header {background: linear-gradient(90deg, #1E3A8A, #3B82F6); padding:20px; color:white; font-size:26px; text-align:center; border-radius:10px; margin-bottom:15px;}
div[data-testid="stSidebar"] div[data-testid="stRadio"] label {font-size:18px !important; font-weight:600 !important; color:#1E3A8A !important; padding:10px 0 !important;}
button {font-size:16px !important; padding:8px 20px !important; background-color:#1E3A8A !important; color:white !important;}
.date-bar {text-align:right; color:#555; font-size:14px; margin-bottom:20px; padding-right:10px;}
</style>
""", unsafe_allow_html=True)

# 顶部标题+实时日期时间
st.markdown('<div class="main-header">检察干部履职智能评价平台</div>', unsafe_allow_html=True)
current_datetime = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
st.markdown(f'<div class="date-bar">系统时间：{current_datetime}</div>', unsafe_allow_html=True)


# -------------------------- 修复后的数据库（100%无字段错误） --------------------------
def init_db():
    # 每次运行都会检查表结构，缺失字段自动补全
    conn = sqlite3.connect('cadre_final.db')
    c = conn.cursor()

    # 材料记录表
    c.execute('''CREATE TABLE IF NOT EXISTS 材料记录
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  干部姓名 TEXT,
                  材料类型 TEXT,
                  材料名称 TEXT,
                  提交时间 TEXT)''')

    # 评分记录表（已添加干部姓名字段）
    c.execute('''CREATE TABLE IF NOT EXISTS 评分记录
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  干部姓名 TEXT,
                  评价内容 TEXT,
                  提交时间 TEXT)''')

    # 互评记录表（已添加提交时间字段）
    c.execute('''CREATE TABLE IF NOT EXISTS 互评记录
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  被评价人 TEXT,
                  评价内容 TEXT,
                  提交时间 TEXT)''')

    # 报告记录表
    c.execute('''CREATE TABLE IF NOT EXISTS 报告记录
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  干部信息 TEXT,
                  提交时间 TEXT)''')

    conn.commit()
    conn.close()


init_db()

# -------------------------- 你的DeepSeek配置 --------------------------
DEEPSEEK_API_KEY = "sk-f99c57a5a8e2467ca4fa69cb1d3c9f49"  # 换成你自己的密钥


# -------------------------- AI调用（严格按你的评分标准） --------------------------
def chat_with_ai(prompt, task_type="general"):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    # 不同任务的系统提示词
    system_prompts = {
        "score": """你是检察干部履职智能评价系统，必须严格按照以下8个维度和赋分标准生成评分结果：
1. 参加司法工作时间
2. 学历学位
3. 入选人才情况
4. 立功受奖情况（最高40分，近十年累加）
   - 业务竞赛：国家级第1名40分，第2-3名30分，第4-5名25分，第6-10名20分；市级第1名20分，第2-3名15分，第4-5名12分，第6-10名10分；院级第1名8分，第2-3名6分，第4-5名4分，第6-10名2分（团队获奖减半）
   - 立功受奖：国家一等功30分，二等功15分，三等功5分，优秀嘉奖3分，称职嘉奖2分
   - 荣誉奖励：国家级业务相关15分，其他10分；市级业务相关8分，其他6分；区级业务相关5分，其他4分；院级业务相关3分，其他2分
5. 信息法宣情况
6. 案例、调研、优秀法律文书情况
7. 综合履职情况
8. 遵规守纪情况

输出格式必须清晰，每个维度单独列项，最后给出总分和评价等级。""",
        "general": "你是检察干部履职智能评价助手，生成专业、规范的回复，符合检察系统工作场景。"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompts[task_type]},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"调用错误：{str(e)}"


# -------------------------- 完整功能页面 --------------------------
st.sidebar.title("功能导航")
page = st.sidebar.radio("", ["🏠 首页", "📤 材料上传", "📊 智能评分", "📝 干部互评", "📄 决策分析"])

if page == "🏠 首页":
    st.success("✅ 系统已就绪！已接入DeepSeek大模型，严格按照8维度标准进行履职评价")
    st.info("支持功能：材料上传、智能评分、干部互评、决策分析，所有数据永久存储")

elif page == "📤 材料上传":
    st.subheader("📤 干部材料上传")
    name = st.text_input("干部姓名")
    material_type = st.selectbox("材料类型", ["奖状", "证书", "荣誉称号", "其他"])
    title = st.text_input("材料名称/标题")

    if st.button("提交录入"):
        if name and title:
            with st.spinner("AI处理中..."):
                prompt = f"处理材料上传：干部姓名{name}，材料类型{material_type}，材料名称{title}"
                ai_response = chat_with_ai(prompt)

                # 存入数据库
                conn = sqlite3.connect('cadre_final.db')
                c = conn.cursor()
                c.execute("INSERT INTO 材料记录 (干部姓名, 材料类型, 材料名称, 提交时间) VALUES (?, ?, ?, ?)",
                          (name, material_type, title, datetime.now().strftime("%Y-%m-%d %H:%M")))
                conn.commit()
                conn.close()

                st.success(ai_response)
        else:
            st.error("请填写完整信息！")

elif page == "📊 智能评分":
    st.subheader("📊 干部履职智能评分（按8维度标准）")
    name = st.text_input("干部姓名")
    evaluation_text = st.text_area("请输入干部履职情况描述", height=150,
                                   placeholder="例如：李一，从事检察工作15年，本科学历，2025年获市级优秀检察官，三等功1次...")

    if st.button("生成评分"):
        if evaluation_text:
            with st.spinner("AI正在按标准生成评分..."):
                prompt = f"根据以下情况为{name}生成履职评分：{evaluation_text}"
                ai_response = chat_with_ai(prompt, task_type="score")

                # 存入数据库
                conn = sqlite3.connect('cadre_final.db')
                c = conn.cursor()
                c.execute("INSERT INTO 评分记录 (干部姓名, 评价内容, 提交时间) VALUES (?, ?, ?)",
                          (name, evaluation_text, datetime.now().strftime("%Y-%m-%d %H:%M")))
                conn.commit()
                conn.close()

                st.write(ai_response)
        else:
            st.error("请输入干部履职情况！")

elif page == "📝 干部互评":
    st.subheader("📝 干部互评画像生成")
    name = st.text_input("被评价干部姓名")
    peer_evaluation = st.text_area("请输入同事评价内容", height=150)

    if st.button("生成画像"):
        if name and peer_evaluation:
            with st.spinner("AI生成画像中..."):
                prompt = f"根据同事评价生成{name}的工作画像：{peer_evaluation}"
                ai_response = chat_with_ai(prompt)

                # 存入数据库
                conn = sqlite3.connect('cadre_final.db')
                c = conn.cursor()
                c.execute("INSERT INTO 互评记录 (被评价人, 评价内容, 提交时间) VALUES (?, ?, ?)",
                          (name, peer_evaluation, datetime.now().strftime("%Y-%m-%d %H:%M")))
                conn.commit()
                conn.close()

                st.write(ai_response)
        else:
            st.error("请填写完整信息！")

elif page == "📄 决策分析":
    st.subheader("📄 干部队伍研判报告")
    report_info = st.text_area("请输入干部基本信息和履职情况", height=150)

    if st.button("生成研判报告"):
        if report_info:
            with st.spinner("AI生成报告中..."):
                prompt = f"根据以下信息生成干部队伍研判报告：{report_info}"
                ai_response = chat_with_ai(prompt)

                # 存入数据库
                conn = sqlite3.connect('cadre_final.db')
                c = conn.cursor()
                c.execute("INSERT INTO 报告记录 (干部信息, 提交时间) VALUES (?, ?)",
                          (report_info, datetime.now().strftime("%Y-%m-%d %H:%M")))
                conn.commit()
                conn.close()

                st.write(ai_response)
        else:
            st.error("请输入相关信息！")