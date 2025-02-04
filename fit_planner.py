import streamlit as st
from langchain.llms import Ollama

def generate_fitness_plan(height, weight, gender, body_fat, fitness_goal):
    # 初始化 Ollama 模型
    llm = Ollama(model="deepseek-r1:1.5b")
    
    # 构建提示词
    prompt = f"""
    请为以下条件的用户制定一个详细的健身计划：
    
    基本信息：
    - 身高：{height}cm
    - 体重：{weight}kg
    - 性别：{gender}
    - 体脂率：{body_fat}%
    - 健身目标：{fitness_goal}
    
    请提供：
    1. 身体状况评估
    2. 每周训练计划（含具体动作和组数）
    3. 饮食建议
    4. 注意事项
    
    要求：
    - 计划要科学合理
    - 适合初学者
    - 循序渐进
    - 包含具体的动作建议
    """
    
    # 生成计划
    response = llm(prompt)
    return response

def main():
    st.set_page_config(page_title="AI健身计划生成器", page_icon="💪")
    
    st.title("💪 AI健身计划生成器")
    st.markdown("### 输入您的基本信息，获取个性化健身计划")
    
    # 创建表单
    with st.form("fitness_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            height = st.number_input("身高(cm)", min_value=100, max_value=250, value=170)
            weight = st.number_input("体重(kg)", min_value=30, max_value=200, value=65)
        
        with col2:
            gender = st.selectbox("性别", ["男", "女"])
            body_fat = st.number_input("体脂率(%)", min_value=1, max_value=50, value=20)
        
        fitness_goal = st.selectbox(
            "健身目标",
            ["减脂", "增肌", "保持健康", "提高力量", "提升耐力"]
        )
        
        submitted = st.form_submit_button("生成健身计划")
    
    if submitted:
        with st.spinner("正在生成您的个性化健身计划..."):
            try:
                fitness_plan = generate_fitness_plan(
                    height, weight, gender, body_fat, fitness_goal
                )
                
                st.success("健身计划生成成功！")
                st.markdown("### 您的个性化健身计划")
                st.markdown(fitness_plan)
                
                # 添加下载按钮
                st.download_button(
                    label="📥 下载健身计划",
                    data=fitness_plan,
                    file_name="my_fitness_plan.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"生成计划时出现错误：{str(e)}")
    
    # 添加页脚
    st.markdown("---")
    st.markdown("💡 提示：请根据自身情况调整计划，如有疑问请咨询专业教练")

if __name__ == "__main__":
    main()