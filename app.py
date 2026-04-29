import streamlit as st
import requests
import sqlite3
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# 界面配置
st.set_page_config(page_title="检察干部履职智能评价平台", layout="wide")
st.markdown("""
<style>
/* 全局样式 */
* {box-sizing: border-box;}

/* 页面背景 */
.stApp {background-color: #f0f4f8;}

/* 隐藏侧边栏收起按钮 */
button[data-testid="collapsedControl"] {
    display: none !important;
}

/* 深蓝色导航栏 */
.navbar {
    background: linear-gradient(135deg, #1a365d 0%, #2c5282 50%, #1a365d 100%);
    padding: 18px 20px;
    border-radius: 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    margin: -8px -8px 20px -8px;
}

.navbar-title {
    color: #ffffff;
    font-size: 24px;
    font-weight: 700;
    text-align: center;
    letter-spacing: 2px;
}

/* 日期栏 */
.date-bar {
    text-align: right;
    color: #64748b;
    font-size: 14px;
    margin-bottom: 15px;
    padding-right: 10px;
}

/* 卡片样式 */
.card {
    background: #ffffff;
    padding: 24px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    border: 1px solid #e2e8f0;
}

.card-header {
    font-size: 18px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 2px solid #3b82f6;
}

.card-section {
    padding: 16px;
    background: #f8fafc;
    border-radius: 8px;
    margin-bottom: 16px;
}

/* 徽章样式 */
.score-badge {
    font-size: 48px;
    font-weight: 800;
    color: #1e40af;
    text-shadow: 2px 2px 4px rgba(30, 64, 175, 0.1);
}

.rank-badge {
    font-size: 32px;
    font-weight: 700;
    color: #059669;
}

.badge-label {
    font-size: 14px;
    color: #64748b;
    margin-top: 4px;
}

/* 按钮样式 */
button {
    font-size: 15px !important;
    padding: 10px 24px !important;
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    transition: all 0.3s ease;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4) !important;
}

/* 侧边栏样式 */
div[data-testid="stSidebar"] {
    background: #ffffff;
    padding: 20px;
    border-radius: 0 12px 12px 0;
    box-shadow: 2px 0 16px rgba(0, 0, 0, 0.06);
}

div[data-testid="stSidebar"] div[data-testid="stRadio"] label {
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #334155 !important;
    padding: 12px 16px !important;
    margin: 4px 0 !important;
    border-radius: 8px;
    transition: all 0.2s ease;
}

div[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
    background: #e0f2fe;
}

div[data-testid="stSidebar"] div[data-testid="stRadio"] input[type="radio"]:checked + label {
    background: #dbeafe;
    color: #1e40af !important;
}

/* 输入框样式 */
input, textarea, select {
    border-radius: 8px !important;
    border: 1px solid #cbd5e1 !important;
    padding: 10px 14px !important;
    font-size: 14px !important;
    transition: all 0.2s ease;
}

input:focus, textarea:focus, select:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
}

/* 进度条样式 */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%);
    border-radius: 4px;
}

/* 表格样式 */
table {
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
}

th {
    background: #f1f5f9;
    padding: 12px;
    text-align: left;
    font-weight: 600;
    color: #334155;
    border-bottom: 2px solid #e2e8f0;
}

td {
    padding: 12px;
    border-bottom: 1px solid #e2e8f0;
}

tr:hover {
    background: #f8fafc;
}

/* 分隔线 */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #cbd5e1, transparent);
    margin: 20px 0;
}

/* 文字样式 */
h1, h2, h3, h4, h5, h6 {
    color: #1e293b;
    font-weight: 600;
}

p, span {
    color: #475569;
}

/* 成功/错误提示 */
div[data-testid="stSuccess"] {
    background: #dcfce7;
    border-left: 4px solid #22c55e;
    border-radius: 0 8px 8px 0;
}

div[data-testid="stError"] {
    background: #fee2e2;
    border-left: 4px solid #ef4444;
    border-radius: 0 8px 8px 0;
}

div[data-testid="stWarning"] {
    background: #fef3c7;
    border-left: 4px solid #f59e0b;
    border-radius: 0 8px 8px 0;
}

div[data-testid="stInfo"] {
    background: #dbeafe;
    border-left: 4px solid #3b82f6;
    border-radius: 0 8px 8px 0;
}
</style>
""", unsafe_allow_html=True)

# 顶部导航栏
st.markdown('<div class="navbar"><div class="navbar-title">检察干部履职智能评价平台</div></div>', unsafe_allow_html=True)

# 日期时间
current_datetime = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
st.markdown(f'<div class="date-bar">📅 系统时间：{current_datetime}</div>', unsafe_allow_html=True)


# -------------------------- 数据库初始化 --------------------------
def init_db():
    conn = sqlite3.connect('cadre_final.db')
    c = conn.cursor()

    # 用户表 - 检察干部信息
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  姓名 TEXT,
                  性别 TEXT,
                  部门 TEXT,
                  职务 TEXT,
                  工作年限 INTEGER,
                  学历 TEXT,
                  立功受奖情况 TEXT,
                  维度1得分 INTEGER,
                  维度2得分 INTEGER,
                  维度3得分 INTEGER,
                  维度4得分 INTEGER,
                  维度5得分 INTEGER,
                  维度6得分 INTEGER,
                  维度7得分 INTEGER,
                  维度8得分 INTEGER,
                  综合总分 INTEGER)''')

    # 材料记录表
    c.execute('''CREATE TABLE IF NOT EXISTS 材料记录
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  干部姓名 TEXT,
                  材料类型 TEXT,
                  材料名称 TEXT,
                  提交时间 TEXT)''')

    # 评分记录表
    c.execute('''CREATE TABLE IF NOT EXISTS 评分记录
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  干部姓名 TEXT,
                  评价内容 TEXT,
                  提交时间 TEXT)''')

    # 互评记录表
    c.execute('''CREATE TABLE IF NOT EXISTS 互评记录
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  被评价人 TEXT,
                  评价人 TEXT,
                  优点 TEXT,
                  待提升点 TEXT,
                  建议 TEXT,
                  提交时间 TEXT,
                  审核状态 TEXT)''')

    # 报告记录表
    c.execute('''CREATE TABLE IF NOT EXISTS 报告记录
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  干部信息 TEXT,
                  提交时间 TEXT)''')

    # 历史评分表
    c.execute('''CREATE TABLE IF NOT EXISTS 历史评分
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  干部姓名 TEXT,
                  评分月份 TEXT,
                  综合总分 INTEGER)''')

    conn.commit()
    conn.close()


# -------------------------- 生成虚拟检察干部数据 --------------------------
def generate_fake_users():
    import random
    
    unique_names = [
        '张建国', '李明辉', '王志强', '刘建华', '陈晓东',
        '杨海峰', '赵文博', '黄志刚', '周伟民', '吴晓峰',
        '孙丽娟', '王秀英', '刘淑芬', '陈雅琴', '杨桂芳',
        '赵红梅', '黄月娥', '周凤英', '吴燕华', '郑玉兰'
    ]
    
    departments = ['办公室', '政治部', '第一检察部', '第二检察部', '第三检察部', '第四检察部', '第五检察部', '案件管理部']
    positions = ['检察长', '副检察长', '检察委员会委员', '部门负责人', '检察官', '检察官助理', '书记员']
    educations = ['大专', '本科', '硕士', '博士']
    
    award_records = [
        {'desc': '无', 'score': 0},
        {'desc': '三等功1次', 'score': 5},
        {'desc': '三等功2次', 'score': 10},
        {'desc': '二等功1次', 'score': 15},
        {'desc': '一等功1次', 'score': 30},
        {'desc': '三等功1次+优秀嘉奖', 'score': 8},
        {'desc': '三等功1次+称职嘉奖', 'score': 7},
        {'desc': '二等功1次+三等功1次', 'score': 20},
        {'desc': '优秀嘉奖2次', 'score': 6},
        {'desc': '院级业务竞赛第1名', 'score': 8},
        {'desc': '市级业务竞赛第2名', 'score': 15},
        {'desc': '省级业务竞赛第1名', 'score': 25},
        {'desc': '国家级业务竞赛第5名', 'score': 25},
        {'desc': '院级优秀检察官', 'score': 3},
        {'desc': '市级优秀检察官', 'score': 8},
        {'desc': '省级优秀检察官', 'score': 15},
        {'desc': '国家优秀检察官', 'score': 15},
    ]
    
    conn = sqlite3.connect('cadre_final.db')
    c = conn.cursor()
    
    # 检查是否已有数据，如果有则跳过生成
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    if count > 0:
        conn.close()
        return
    
    random.shuffle(unique_names)
    
    for i in range(20):
        name = unique_names[i]
        gender = '男' if i < 10 else '女'
        department = departments[i % len(departments)]
        position = positions[random.randint(0, len(positions) - 1)]
        work_years = random.randint(2, 35)
        education = random.choice(educations)
        
        award_record = random.choice(award_records)
        award_desc = award_record['desc']
        award_score = award_record['score']
        
        dim1_score = min(100, 50 + work_years * 2 + random.randint(-5, 10))
        
        edu_scores = {'博士': 100, '硕士': 85, '本科': 70, '大专': 55}
        dim2_score = edu_scores.get(education, 70) + random.randint(-5, 5)
        
        dim3_score = random.randint(40, 100)
        
        dim4_score = min(40, award_score)
        
        dim5_score = random.randint(50, 100)
        
        dim6_score = random.randint(50, 100)
        
        dim7_score = random.randint(55, 100)
        
        dim8_score = random.randint(70, 100)
        
        dimensions = [dim1_score, dim2_score, dim3_score, dim4_score, dim5_score, dim6_score, dim7_score, dim8_score]
        dimensions = [max(0, min(100, d)) for d in dimensions]
        
        final_total = round(sum(dimensions) / 8)
        
        if final_total < 60:
            final_total = 60
        elif final_total > 100:
            final_total = 100
        
        award_display = f"{award_desc}（{dim4_score}分）" if dim4_score > 0 else award_desc
        
        c.execute('''INSERT INTO users 
                     (姓名, 性别, 部门, 职务, 工作年限, 学历, 立功受奖情况, 
                      维度1得分, 维度2得分, 维度3得分, 维度4得分, 
                      维度5得分, 维度6得分, 维度7得分, 维度8得分, 综合总分)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (name, gender, department, position, work_years, education, award_display,
                   dimensions[0], dimensions[1], dimensions[2], dimensions[3],
                   dimensions[4], dimensions[5], dimensions[6], dimensions[7], final_total))
    
    conn.commit()
    conn.close()
    print("[OK] 已成功生成20个唯一姓名的虚拟检察干部数据")


# -------------------------- 生成历史评分数据 --------------------------
def generate_fake_history_scores():
    import random
    
    conn = sqlite3.connect('cadre_final.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM 历史评分")
    count = c.fetchone()[0]
    
    if count > 0:
        conn.close()
        return
    
    c.execute("SELECT 姓名, 综合总分 FROM users")
    users = c.fetchall()
    
    months = ['2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04']
    
    for name, current_score in users:
        for month in months:
            # 历史分数围绕当前分数波动
            history_score = random.randint(max(60, current_score - 10), min(100, current_score + 10))
            c.execute("INSERT INTO 历史评分 (干部姓名, 评分月份, 综合总分) VALUES (?, ?, ?)",
                      (name, month, history_score))
    
    conn.commit()
    conn.close()
    print("[OK] 已成功生成历史评分数据")


# -------------------------- 初始化数据 --------------------------
init_db()
generate_fake_users()
generate_fake_history_scores()


# -------------------------- DeepSeek配置 --------------------------
DEEPSEEK_API_KEY = "sk-f99c57a5a8e2467ca4fa69cb1d3c9f49"


# -------------------------- AI调用 --------------------------
def chat_with_ai(prompt, task_type="general"):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

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


# -------------------------- AI评价内容审核 --------------------------
def ai_audit_evaluation(content):
    """调用AI审核评价内容是否规范"""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = """你是一个评价内容审核系统，负责检测评价内容是否规范。请判断以下评价内容是否包含：
1. 辱骂、人身攻击、侮辱性语言
2. 无意义灌水内容
3. 重复内容或无意义字符
4. 违法违规内容
5. 与工作无关的恶意内容

如果包含以上任何一种情况，请返回"不规范"；如果内容正常、有意义，请返回"规范"。
只返回"规范"或"不规范"两个词中的一个，不要添加其他内容。"""
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content}
        ],
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        result = response.json()
        audit_result = result["choices"][0]["message"]["content"].strip()
        return audit_result
    except Exception as e:
        return "规范"  # 网络错误时默认通过


# -------------------------- 提交互评评价 --------------------------
def submit_peer_evaluation(evaluator_name, evaluatee_name, strengths, improvements, suggestions):
    """提交互评评价，包含AI审核"""
    # 组合评价内容用于审核
    full_content = f"优点：{strengths}\n待提升点：{improvements}\n建议：{suggestions}"
    
    # AI审核
    audit_result = ai_audit_evaluation(full_content)
    
    if audit_result != "规范":
        return False, "评价内容不规范，包含辱骂、人身攻击、无意义灌水或重复内容，请重新填写。"
    
    conn = sqlite3.connect('cadre_final.db')
    c = conn.cursor()
    
    # 检查是否已对同一人评价（防止重复评价）
    c.execute("SELECT COUNT(*) FROM 互评记录 WHERE 评价人 = ? AND 被评价人 = ?",
              (evaluator_name, evaluatee_name))
    count = c.fetchone()[0]
    if count > 0:
        conn.close()
        return False, f"您已经对 {evaluatee_name} 进行过评价，请勿重复评价。"
    
    c.execute('''INSERT INTO 互评记录 
                 (被评价人, 评价人, 优点, 待提升点, 建议, 提交时间, 审核状态)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (evaluatee_name, evaluator_name, strengths, improvements, suggestions,
               datetime.now().strftime("%Y-%m-%d %H:%M"), "已审核"))
    
    conn.commit()
    conn.close()
    return True, f"成功提交对 {evaluatee_name} 的评价！"


# -------------------------- 获取用户的匿名互评汇总 --------------------------
def get_peer_evaluations(name):
    """获取用户收到的匿名互评（隐藏评价人信息）"""
    conn = sqlite3.connect('cadre_final.db')
    c = conn.cursor()
    c.execute("SELECT 优点, 待提升点, 建议, 提交时间 FROM 互评记录 WHERE 被评价人 = ? AND 审核状态 = '已审核' ORDER BY 提交时间 DESC",
              (name,))
    evaluations = c.fetchall()
    conn.close()
    return evaluations


# -------------------------- 获取用户列表 --------------------------
def get_user_list():
    conn = sqlite3.connect('cadre_final.db')
    c = conn.cursor()
    c.execute("SELECT 姓名 FROM users ORDER BY 姓名")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users


# -------------------------- 获取用户详情 --------------------------
def get_user_details(name):
    conn = sqlite3.connect('cadre_final.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE 姓名 = ?", (name,))
    user = c.fetchone()
    conn.close()
    return user


# -------------------------- 获取排名 --------------------------
def get_user_rank(name):
    conn = sqlite3.connect('cadre_final.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE 综合总分 > (SELECT 综合总分 FROM users WHERE 姓名 = ?)", (name,))
    rank = c.fetchone()[0] + 1
    c.execute("SELECT COUNT(*) FROM users")
    total = c.fetchone()[0]
    conn.close()
    return rank, total


# -------------------------- 获取历史评分 --------------------------
def get_history_scores(name):
    conn = sqlite3.connect('cadre_final.db')
    c = conn.cursor()
    c.execute("SELECT 评分月份, 综合总分 FROM 历史评分 WHERE 干部姓名 = ? ORDER BY 评分月份", (name,))
    history = c.fetchall()
    conn.close()
    return history





# -------------------------- 登录页面 --------------------------
def login_page():
    # 居中显示登录卡片
    col_center = st.columns([1, 2, 1])[1]
    
    with col_center:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">🔐 用户登录</div>', unsafe_allow_html=True)
        st.write("<p style='color:#64748b; margin-bottom:20px;'>请选择您的姓名登录系统：</p>", unsafe_allow_html=True)
        
        users = get_user_list()
        
        if users:
            selected_user = st.selectbox("", users, index=0)
            st.write("")
            if st.button("进入个人中心", use_container_width=True):
                st.session_state['current_user'] = selected_user
                st.rerun()
        else:
            st.warning("暂未找到用户数据，请先初始化数据")
        
        st.markdown('</div>', unsafe_allow_html=True)


# -------------------------- 个人中心页面 --------------------------
def personal_center():
    user_name = st.session_state['current_user']
    user = get_user_details(user_name)
    rank, total = get_user_rank(user_name)
    history_scores = get_history_scores(user_name)
    peer_evaluations = get_peer_evaluations(user_name)
    
    # 页面标题
    st.markdown(f"<h2 style='color:#1e293b; margin-bottom:20px;'>👤 {user_name} 的个人中心</h2>", unsafe_allow_html=True)
    
    # 第一行：基本信息 + 分数排名
    col1, col2 = st.columns([1, 1.5])
    
    # 左侧：基本信息卡片
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">📋 基本信息</div>', unsafe_allow_html=True)
        info_items = [
            ('姓名', user[1]),
            ('性别', user[2]),
            ('部门', user[3]),
            ('职务', user[4]),
            ('工作年限', f'{user[5]}年'),
            ('学历', user[6]),
            ('立功受奖', user[7])
        ]
        for label, value in info_items:
            st.write(f"<span style='color:#64748b; width:80px; display:inline-block;'>{label}：</span><span style='color:#1e293b; font-weight:500;'>{value}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 右侧：分数和排名卡片
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">🏆 当前评分</div>', unsafe_allow_html=True)
        score_col, rank_col = st.columns([1, 1])
        
        with score_col:
            st.markdown(f'<span class="score-badge">{user[16]}</span>', unsafe_allow_html=True)
            st.markdown('<div class="badge-label">综合总分</div>', unsafe_allow_html=True)
        
        with rank_col:
            st.markdown(f'<span class="rank-badge">第{rank}名</span>', unsafe_allow_html=True)
            st.markdown(f'<div class="badge-label">全团队 {total} 人</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 维度得分卡片
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">📊 各维度得分</div>', unsafe_allow_html=True)
        dimension_names = ['司法工作时间', '学历学位', '入选人才情况', '立功受奖情况', 
                           '信息法宣情况', '案例调研文书', '综合履职情况', '遵规守纪情况']
        dimensions = user[8:16]
        
        # 两列显示维度
        dim_cols = st.columns(2)
        for i, (dim_name, dim_score) in enumerate(zip(dimension_names, dimensions)):
            with dim_cols[i % 2]:
                st.write(f"<span style='font-size:14px; color:#475569;'>{dim_name}</span>", unsafe_allow_html=True)
                st.progress(dim_score / 100)
                st.write(f"<span style='font-size:13px; color:#64748b;'>得分：{dim_score}分</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 第二行：历史评分趋势
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">📈 历史评分趋势</div>', unsafe_allow_html=True)
    if history_scores:
        months = [h[0] for h in history_scores]
        scores = [h[1] for h in history_scores]
        df = pd.DataFrame({'月份': months, '综合总分': scores})
        st.line_chart(df, x='月份', y='综合总分', height=300)
    else:
        st.write("<p style='color:#94a3b8; text-align:center; padding:20px;'>暂无历史评分数据</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 第三行：匿名互评汇总
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">💬 收到的匿名互评</div>', unsafe_allow_html=True)
    if peer_evaluations:
        for idx, (strengths, improvements, suggestions, submit_time) in enumerate(peer_evaluations, 1):
            st.markdown(f"<div style='background:#f8fafc; padding:16px; border-radius:8px; margin-bottom:12px;'>", unsafe_allow_html=True)
            st.markdown(f"<strong style='color:#1e293b;'>评价 {idx}</strong>", unsafe_allow_html=True)
            st.markdown(f"👍 <span style='color:#059669;'>优点：</span><span style='color:#475569;'>{strengths}</span>", unsafe_allow_html=True)
            st.markdown(f"📈 <span style='color:#f59e0b;'>待提升：</span><span style='color:#475569;'>{improvements}</span>", unsafe_allow_html=True)
            st.markdown(f"💡 <span style='color:#3b82f6;'>建议：</span><span style='color:#475569;'>{suggestions}</span>", unsafe_allow_html=True)
            st.markdown(f"🕐 <span style='color:#94a3b8; font-size:12px;'>提交时间：{submit_time}</span>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("<p style='color:#94a3b8; text-align:center; padding:20px;'>暂无互评记录</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 退出登录按钮
    st.markdown('<div style="text-align:right; margin-top:20px;">', unsafe_allow_html=True)
    if st.button("🔓 退出登录"):
        del st.session_state['current_user']
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# -------------------------- 主页面逻辑 --------------------------
if 'current_user' not in st.session_state:
    login_page()
else:
    personal_center()
    
    # 侧边栏导航（仅登录后显示）
    st.sidebar.title("功能导航")
    page = st.sidebar.radio("", ["🏠 个人中心", "📤 材料上传", "📊 智能评分", "📝 干部互评", "📄 决策分析"])
    
    if page == "🏠 个人中心":
        pass  # 已在个人中心
    
    elif page == "📤 材料上传":
        st.markdown("<h2 style='color:#1e293b; margin-bottom:20px;'>📤 干部材料上传</h2>", unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">� 材料信息</div>', unsafe_allow_html=True)
        
        name = st.text_input("干部姓名", value=st.session_state['current_user'])
        material_type = st.selectbox("材料类型", ["奖状", "证书", "荣誉称号", "其他"])
        title = st.text_input("材料名称/标题")

        st.write("")
        if st.button("✅ 提交录入", use_container_width=True):
            if name and title:
                with st.spinner("AI处理中..."):
                    prompt = f"处理材料上传：干部姓名{name}，材料类型{material_type}，材料名称{title}"
                    ai_response = chat_with_ai(prompt)

                    conn = sqlite3.connect('cadre_final.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO 材料记录 (干部姓名, 材料类型, 材料名称, 提交时间) VALUES (?, ?, ?, ?)",
                              (name, material_type, title, datetime.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit()
                    conn.close()

                    st.success(ai_response)
            else:
                st.error("请填写完整信息！")
        
        st.markdown('</div>', unsafe_allow_html=True)

    elif page == "📊 智能评分":
        st.markdown("<h2 style='color:#1e293b; margin-bottom:20px;'>📊 干部履职智能评分</h2>", unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">📋 评分信息</div>', unsafe_allow_html=True)
        
        name = st.text_input("干部姓名", value=st.session_state['current_user'])
        evaluation_text = st.text_area("", height=180,
                                       placeholder="请输入干部履职情况描述...\n\n例如：从事检察工作15年，本科学历，2025年获市级优秀检察官，三等功1次...")

        st.write("")
        if st.button("⚡ 生成评分", use_container_width=True):
            if evaluation_text:
                with st.spinner("AI正在按标准生成评分..."):
                    prompt = f"根据以下情况为{name}生成履职评分：{evaluation_text}"
                    ai_response = chat_with_ai(prompt, task_type="score")

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
        st.markdown("<h2 style='color:#1e293b; margin-bottom:20px;'>📝 半匿名互评</h2>", unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">💡 评价说明</div>', unsafe_allow_html=True)
        st.info("评价为半匿名：被评价人看不到评价人姓名，但后台会记录评价人信息用于审计。")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 获取所有用户（排除当前登录用户）
        all_users = get_user_list()
        current_user = st.session_state['current_user']
        available_users = [u for u in all_users if u != current_user]
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">👥 选择评价对象</div>', unsafe_allow_html=True)
        
        # 多选框选择同事
        selected_users = st.multiselect("请选择要评价的同事（可多选）", available_users)
        
        if not selected_users:
            st.warning("请至少选择一位同事进行评价")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 如果选择了同事，显示评价表单
            evaluations = {}
            
            for idx, user in enumerate(selected_users, 1):
                st.markdown(f'<div class="card">', unsafe_allow_html=True)
                st.markdown(f'<div class="card-header">📋 评价 {idx}：{user}</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    strengths = st.text_area("", 
                                           placeholder="👍 请描述该同事的优点...", 
                                           height=100,
                                           key=f"strengths_{user}")
                with col2:
                    improvements = st.text_area("", 
                                               placeholder="📈 请描述该同事需要提升的方面...", 
                                               height=100,
                                               key=f"improvements_{user}")
                
                suggestions = st.text_area("", 
                                          placeholder="💡 请给出改进建议...", 
                                          height=80,
                                          key=f"suggestions_{user}")
                
                evaluations[user] = {
                    'strengths': strengths,
                    'improvements': improvements,
                    'suggestions': suggestions
                }
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 提交按钮
            st.markdown('<div style="text-align:right; margin-top:20px;">', unsafe_allow_html=True)
            if st.button("✅ 提交所有评价", use_container_width=False):
                # 验证所有评价内容
                all_valid = True
                for user, eval_data in evaluations.items():
                    if not eval_data['strengths'] or not eval_data['improvements'] or not eval_data['suggestions']:
                        st.error(f"请完整填写对 {user} 的评价内容！")
                        all_valid = False
                        break
                
                if all_valid:
                    success_count = 0
                    fail_messages = []
                    
                    with st.spinner("AI审核中..."):
                        for user, eval_data in evaluations.items():
                            success, message = submit_peer_evaluation(
                                current_user,
                                user,
                                eval_data['strengths'],
                                eval_data['improvements'],
                                eval_data['suggestions']
                            )
                            
                            if success:
                                success_count += 1
                                st.success(message)
                            else:
                                fail_messages.append(message)
                    
                    if fail_messages:
                        for msg in fail_messages:
                            st.error(msg)
                    
                    st.info(f"本次共提交 {success_count} 条评价，{len(fail_messages)} 条未通过审核或重复评价。")
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == "📄 决策分析":
        st.markdown("<h2 style='color:#1e293b; margin-bottom:20px;'>📄 干部队伍研判报告</h2>", unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">📝 报告参数</div>', unsafe_allow_html=True)
        
        report_info = st.text_area("", height=180,
                                   placeholder="请输入干部基本信息和履职情况...")

        st.write("")
        if st.button("📊 生成研判报告", use_container_width=True):
            if report_info:
                with st.spinner("AI生成报告中..."):
                    prompt = f"根据以下信息生成干部队伍研判报告：{report_info}"
                    ai_response = chat_with_ai(prompt)

                    conn = sqlite3.connect('cadre_final.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO 报告记录 (干部信息, 提交时间) VALUES (?, ?)",
                              (report_info, datetime.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit()
                    conn.close()

                    st.write(ai_response)
            else:
                st.error("请输入相关信息！")
