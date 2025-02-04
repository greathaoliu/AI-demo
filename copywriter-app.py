import streamlit as st
from openai import OpenAI
import json

# 创建一个自定义的 OpenAI 客户端，指向本地的 Ollama 服务
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="no-key-required"
)

client_671B = OpenAI(
    api_key="sk-hcgspmldivqyiidyknbsfsxneukcxtxzuptwziahltrbjxxb",
    base_url="https://api.siliconflow.cn/v1"
)


def clean_text(text):
    import re
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return cleaned.strip()


def generate_copy_stream(prompt, model_name="deepseek-r1:1.5b"):
    """
    使用流式输出生成文案
    """
    try:
        response = None
        if model_name == 'deepseek-r1:1.5b':
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )
        else:
            response = client_671B.chat.completions.create(
                model='deepseek-ai/DeepSeek-R1',
                messages=[
                    {'role': 'user', 'content': prompt}
                ],
                stream=True
            )
        return response
    except Exception as e:
        return f"发生错误: {str(e)}"


def main():
    st.set_page_config(page_title="AI文案生成器", page_icon="✍️")

    st.title("📝 AI文案生成器")
    st.markdown("### 使用AI为您的创意生成专业文案")

    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 配置")
        model_name = st.selectbox(
            "选择模型",
            ["deepseek-r1:1.5B", "deepseek-r1:671B"],
            index=0
        )

        st.markdown("---")
        st.markdown("### 💡 使用提示")
        st.markdown("""
        1. 选择合适的AI模型
        2. 输入您的关键词或主题
        3. 根据需要调整文案类型
        4. 点击生成获取文案
        """)

    # 主界面
    col1, col2 = st.columns([2, 1])

    with col1:
        keywords = st.text_area("输入关键词或主题", height=100,
                                placeholder="例如：新鲜水果、夏季促销、健康生活...")

    with col2:
        copy_type = st.selectbox(
            "文案类型",
            ["社交媒体文案", "产品描述", "广告语", "营销文案", "新闻稿"],
        )

        tone = st.selectbox(
            "文案风格",
            ["专业正式", "轻松活泼", "幽默有趣", "温暖亲切", "高端大气"],
        )

    # 初始化session_state
    if "generated_text" not in st.session_state:
        st.session_state.generated_text = ""

    # 生成按钮
    if st.button("✨ 生成文案", type="primary"):
        if not keywords:
            st.error("请输入关键词或主题！")
            return

        # 构建提示词
        prompt = f"""
        请根据以下信息生成一段{copy_type}：
        关键词：{keywords}
        风格要求：{tone}
        要求：
        1. 文案要简洁有力
        2. 突出关键词重点
        3. 符合{copy_type}的特点
        4. 保持{tone}的风格
        """

        # 创建一个空的占位符用于显示流式输出
        placeholder = st.empty()

        # 重置生成的文本
        st.session_state.generated_text = ""

        # 使用 spinner 包装生成过程
        with st.spinner("正在生成文案..."):
            # 获取流式响应
            response_stream = generate_copy_stream(prompt, model_name)

            # 处理流式输出
            full_response = ""
            for chunk in response_stream:
                if hasattr(chunk.choices[0].delta, 'content'):
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        full_response += content
                        # 更新显示
                        placeholder.markdown(full_response)
                        st.session_state.generated_text = full_response

        # 显示最终结果
        st.markdown("### 🎉 生成结果")
        placeholder.markdown("")
        st.markdown(st.session_state.generated_text)

        # 提供复制按钮
        st.markdown("---")
        st.markdown("##### 操作")
        if st.button("📋 复制文案"):
            st.write("文案已复制到剪贴板！")
            st.session_state["clipboard"] = st.session_state.generated_text


if __name__ == "__main__":
    main()