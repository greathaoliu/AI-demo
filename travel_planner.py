import streamlit as st
from langchain.llms import Ollama

def generate_travel_plan(destination, duration, budget, people_count):
    """生成旅游计划"""
    # 初始化 Ollama 模型
    llm = Ollama(model="deepseek-r1:1.5b")
    
    # 构建提示词
    prompt = f"""请为以下旅行需求制定详细的旅游计划:
    目的地: {destination}
    行程天数: {duration}天
    预算: {budget}元
    出行人数: {people_count}人
    
    请包含以下内容:
    1. 每日行程安排
    2. 交通建议
    3. 住宿推荐
    4. 美食推荐
    5. 预算分配
    6. 注意事项
    """
    
    # 生成计划
    response = llm(prompt)
    return response

def main():
    st.set_page_config(page_title="AI旅游计划生成器", page_icon="🏖️")
    
    st.title("🌍 AI旅游计划生成器")
    st.markdown("### 让AI为您规划完美的旅行")
    
    # 输入表单
    with st.form("travel_form"):
        destination = st.text_input("目的地", placeholder="例如: 杭州")
        
        col1, col2 = st.columns(2)
        with col1:
            duration = st.number_input("行程天数", min_value=1, max_value=30, value=3)
            budget = st.number_input("总预算(元)", min_value=1000, value=5000)
        with col2:
            people_count = st.number_input("出行人数", min_value=1, max_value=20, value=2)
        
        submitted = st.form_submit_button("生成旅游计划")
    
    if submitted:
        if not destination:
            st.error("请输入目的地!")
            return
        
        with st.spinner("正在规划您的完美旅程..."):
            try:
                # 生成旅游计划
                travel_plan = generate_travel_plan(
                    destination, duration, budget, people_count
                )
                
                # 显示结果
                st.success("✨ 旅游计划生成完成!")
                st.markdown(travel_plan)
                
                # 添加下载按钮
                st.download_button(
                    label="📥 下载旅游计划",
                    data=travel_plan,
                    file_name=f"{destination}旅游计划.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"生成计划时发生错误：{str(e)}")

if __name__ == "__main__":
    main()
