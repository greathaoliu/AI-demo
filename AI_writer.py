import streamlit as st
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate

def generate_content(keywords, content_type):
    # 初始化Ollama模型
    llm = Ollama(model="deepseek-r1:1.5b")
    
    # 创建提示模板
    template = """
    请根据以下关键词生成一篇{content_type}文案：
    关键词：{keywords}
    
    要求：
    1. 文案要简洁有力
    2. 突出关键词的核心价值
    3. 语言要生动活泼
    
    生成的文案：
    """
    
    prompt = PromptTemplate(
        input_variables=["keywords", "content_type"],
        template=template
    )
    
    # 生成文案
    final_prompt = prompt.format(keywords=keywords, content_type=content_type)
    response = llm(final_prompt)
    
    return response

def main():
    st.set_page_config(page_title="AI文案生成器", page_icon="✍️")
    
    # 页面标题
    st.title("✨ AI文案生成器")
    st.markdown("使用AI快速生成优质文案，让创作更轻松！")
    
    # 输入区域
    with st.form("content_form"):
        keywords = st.text_area("请输入关键词（多个关键词请用逗号分隔）", height=100)
        
        # 文案类型选择
        content_type = st.selectbox(
            "选择文案类型",
            ["产品描述", "营销文案", "社交媒体帖子", "广告语", "品牌故事"]
        )
        
        submitted = st.form_submit_button("生成文案")
        
    # 生成文案
    if submitted and keywords:
        with st.spinner("AI正在创作中..."):
            try:
                generated_content = generate_content(keywords, content_type)
                st.success("文案生成成功！")
                st.markdown("### 生成的文案：")
                st.markdown(generated_content)
                
                # 添加复制按钮
                st.markdown("---")
                st.markdown("复制文案到剪贴板：")
                st.code(generated_content)
                
            except Exception as e:
                st.error(f"生成过程中出现错误：{str(e)}")
    
    # 添加页脚
    st.markdown("---")
    st.markdown("powered by Deepseek & Streamlit")

if __name__ == "__main__":
    main()
