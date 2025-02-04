import streamlit as st
from openai import OpenAI

# 初始化 OpenAI 客户端，配置 Silicon Flow API
client = OpenAI(
    api_key="sk-hcgspmldivqyiidyknbsfsxneukcxtxzuptwziahltrbjxxb",  # 替换为你的 Silicon Flow API 密钥
    base_url="https://api.siliconflow.cn/v1"  # Silicon Flow 的 API 端点
)

def generate_response(complaint, tone):
    """生成客服回复"""
    prompt = f"""作为一名专业的物业客服代表，请对业主的以下诉求做出{tone}的回应：
    
    业主诉求：{complaint}
    
    要求：
    1. 使用{tone}的语气
    2. 表达同理心
    3. 提供具体的解决方案
    4. 说明后续跟进流程
    5. 留下联系方式
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",  # 使用 Silicon Flow 提供的模型
            messages=[
                {"role": "system", "content": "你是一个专业的物业客服代表。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"API调用错误：{str(e)}")

def main():
    st.set_page_config(page_title="智能物业客服系统", page_icon="🏢")
    
    st.title("🏢 智能物业客服系统")
    st.markdown("### 欢迎使用物业智能客服，请详细描述您的问题")
    
    # 创建表单
    with st.form("service_form"):
        # 诉求输入区
        complaint = st.text_area(
            "请描述您的问题或诉求",
            height=150,
            placeholder="例如：我家楼上漏水，已经影响到天花板了，请尽快处理..."
        )
        
        # 语气选择
        tone = st.select_slider(
            "选择回复语气",
            options=["非常温和", "温和", "中性", "严肃", "非常严肃"],
            value="中性"
        )
        
        # 提交按钮
        submitted = st.form_submit_button("提交诉求")
    
    if submitted:
        if not complaint:
            st.error("请输入您的诉求内容！")
            return
        
        with st.spinner("正在生成回复..."):
            try:
                response = generate_response(complaint, tone)
                
                # 显示回复
                st.success("✅ 回复生成成功")
                st.markdown("### 客服回复：")
                st.markdown(response)
                
                # 添加反馈按钮
                st.markdown("---")
                st.markdown("##### 这个回复对您有帮助吗？")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍 有帮助"):
                        st.success("感谢您的反馈！")
                with col2:
                    if st.button("👎 需要改进"):
                        st.info("我们会继续改进服务质量！")
                
            except Exception as e:
                st.error(f"生成回复时出现错误：{str(e)}")
    
    # 添加页脚
    st.markdown("---")
    st.markdown("💡 提示：如需紧急处理，请直接拨打物业服务热线：400-888-8888")

if __name__ == "__main__":
    main()
