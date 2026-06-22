import streamlit as st
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from utils.config import IS_WINDOWS, get_system_font_path, get_font_family, STOP_WORDS
from utils.crawler import fetch_text_from_url
from utils.analyzer import analyze_text, get_top_words, get_total_word_count, get_unique_word_count
from utils.visualizer import CHART_GENERATORS, generate_chart
import json
import io
import base64
from datetime import datetime

disable_warnings(InsecureRequestWarning)

st.set_page_config(
    page_title="URL文本词频分析工具",
    page_icon="📊",
    layout="wide"
)

FONT_PATH = get_system_font_path()
FONT_FAMILY = get_font_family()

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #a5b4fc 0%, #fbcfe8 50%, #c7d2fe 100%);
        min-height: 100vh;
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #818cf8 0%, #f472b6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(129, 140, 248, 0.4);
    }
    
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0e7ff;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #818cf8;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2);
    }
    
    .stSlider>div>div>div>div {
        background: linear-gradient(135deg, #818cf8 0%, #f472b6 100%);
    }
    
    .stMetric {
        background: linear-gradient(135deg, #e0e7ff 0%, #fce7f3 100%);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #c7d2fe;
    }
    
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    .status-widget {
        border-radius: 12px;
        overflow: hidden;
    }
    
    .expanderHeader {
        font-weight: 600;
        color: #374151;
    }
    
    h1 {
        color: #000000;
    }
    
    h2, h3 {
        color: #1f2937;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        border-left: 4px solid #22c55e;
    }
    
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 4px solid #3b82f6;
    }
    
    .stTabs [role="tablist"] {
        gap: 0.5rem;
    }
    
    .stTabs [role="tab"] {
        background: #e0e7ff;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #818cf8 0%, #f472b6 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

def export_results(word_count, top_n):
    top_words = get_top_words(word_count, top_n)
    result = {
        "top_words": top_words,
        "word_count": word_count,
        "total_words": get_total_word_count(word_count),
        "unique_words": get_unique_word_count(word_count)
    }
    return json.dumps(result, ensure_ascii=False, indent=2)

def save_to_history(input_source, input_content, word_count, top_n, chart_type):
    """保存分析结果到历史记录"""
    history_entry = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": input_source,
        "content": input_content[:100] + "..." if len(input_content) > 100 else input_content,
        "word_count": word_count,
        "top_n": top_n,
        "chart_type": chart_type,
        "unique_words": get_unique_word_count(word_count),
        "total_words": get_total_word_count(word_count)
    }
    
    if "analysis_history" not in st.session_state:
        st.session_state.analysis_history = []
    
    st.session_state.analysis_history.insert(0, history_entry)
    
    if len(st.session_state.analysis_history) > 20:
        st.session_state.analysis_history = st.session_state.analysis_history[:20]

def load_from_history(entry):
    """从历史记录加载分析结果"""
    return entry["word_count"], entry["top_n"], entry["chart_type"]

def main():
    with st.sidebar:
        st.title("⚙️ 可视化配置")
        chart_type = st.selectbox(
            "图表类型",
            options=list(CHART_GENERATORS.keys()),
            index=0,
            help="选择要展示的图表类型"
        )
        min_freq = st.slider(
            "低频词过滤阈值",
            min_value=1,
            max_value=20,
            value=2,
            step=1,
            help="过滤出现次数少于此值的词汇"
        )
        top_n = st.slider(
            "展示前N个词汇",
            min_value=5,
            max_value=50,
            value=20,
            step=1,
            help="控制图表展示的词汇数量"
        )

        st.divider()
        st.subheader("📝 示例URL")
        example_urls = [
            "http://www.people.com.cn",
            "http://news.sina.com.cn",
            "http://www.xinhuanet.com"
        ]
        for url in example_urls:
            if st.button(url, key=url):
                st.session_state.url = url

        st.divider()
        st.subheader("🔤 自定义停用词")
        custom_stop_words = st.text_area(
            "添加额外停用词",
            placeholder="每行一个词，如：\n测试\n示例\n临时",
            help="这些词将被添加到默认停用词列表中"
        )

        st.divider()
        st.subheader("📊 批量URL分析")
        batch_urls = st.text_area(
            "输入多个URL",
            placeholder="每行一个URL，如：\nhttp://www.people.com.cn\nhttp://news.sina.com.cn",
            help="同时分析多个URL，比较词频差异"
        )

    st.title("🌐 URL文本词频分析工具")
    st.markdown("---")

    tab1, tab2 = st.tabs(["🔗 URL输入", "📝 文本输入"])
    
    with tab1:
        url = st.text_input(
            "输入文章URL",
            value=st.session_state.get('url', ''),
            placeholder="请输入要分析的文章URL...",
            help="优先使用HTTP协议URL，避免SSL验证问题",
            key='url_input'
        )
    
    with tab2:
        input_text = st.text_area(
            "输入文本内容",
            placeholder="请直接输入要分析的文本内容...",
            height=200,
            key='text_input'
        )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        analyze_btn = st.button(
            "🚀 开始分析",
            type="primary",
            use_container_width=True,
            help="点击开始分析"
        )
    with col2:
        pass
    with col3:
        if st.button("🔄 重置", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    if analyze_btn:
        text = None
        input_source = None
        input_content = None
        
        if batch_urls.strip():
            urls = [u.strip() for u in batch_urls.split('\n') if u.strip()]
            if len(urls) > 0:
                with st.status("🔍 正在批量抓取URL文本...", expanded=True) as status:
                    all_texts = []
                    for idx, url_item in enumerate(urls, 1):
                        status.update(label=f"🔍 正在抓取URL {idx}/{len(urls)}: {url_item[:30]}...", state="running")
                        try:
                            url_text = fetch_text_from_url(url_item)
                            if url_text:
                                all_texts.append(url_text)
                            else:
                                st.warning(f"⚠️ URL {url_item} 未能获取到有效文本")
                        except Exception as e:
                            st.warning(f"⚠️ URL {url_item} 抓取失败: {str(e)}")
                    
                    if all_texts:
                        text = "\n\n".join(all_texts)
                        input_source = "批量URL"
                        input_content = f"批量分析 {len(urls)} 个URL"
                        status.update(label="✅ 批量抓取完成", state="complete")
                        st.success(f"共抓取 {len(all_texts)} 个URL，总文本长度：{len(text):,} 字符")
                    else:
                        status.update(label="❌ 批量抓取失败", state="error")
                        st.error("所有URL都未能获取到有效文本")
                        return
        else:
            with tab1:
                if url.strip():
                    text = None
                    input_source = "URL"
                    input_content = url
                elif input_text.strip():
                    text = input_text.strip()
                    input_source = "文本"
                    input_content = input_text[:50] + "..." if len(input_text) > 50 else input_text
                else:
                    st.warning("⚠️ 请输入URL或文本内容！")
                    return

            with tab2:
                if input_text.strip():
                    text = input_text.strip()
                    input_source = "文本"
                    input_content = input_text[:50] + "..." if len(input_text) > 50 else input_text
                elif url.strip():
                    text = None
                    input_source = "URL"
                    input_content = url
                else:
                    st.warning("⚠️ 请输入URL或文本内容！")
                    return

        if input_source == "URL" and url.strip() and not batch_urls.strip():
            with st.status("🔍 正在抓取URL文本...", expanded=True) as status:
                try:
                    text = fetch_text_from_url(url)
                    if not text:
                        status.update(label="❌ 抓取失败", state="error")
                        st.error("未能从URL获取到有效文本")
                        return
                    status.update(label="✅ 文本抓取成功", state="complete")
                    st.success(f"文本长度：{len(text):,} 字符")
                except Exception as e:
                    status.update(label="❌ 抓取失败", state="error")
                    st.error(f"URL抓取失败：{str(e)}")
                    st.info("💡 推荐测试URL：\n1. http://www.people.com.cn（人民网）\n2. http://news.sina.com.cn（新浪新闻）")
                    return

        custom_stop_words_set = set()
        if custom_stop_words:
            custom_stop_words_set = set([word.strip() for word in custom_stop_words.split('\n') if word.strip()])
        
        with st.status("📝 正在分词并统计词频...", expanded=True) as status:
            word_count = analyze_text(text, min_freq=min_freq, extra_stop_words=custom_stop_words_set)
            if not word_count:
                status.update(label="❌ 分词失败", state="error")
                st.warning("分词后无有效词汇，请降低低频词过滤阈值！")
                return
            status.update(label="✅ 词频统计完成", state="complete")
            total_count = get_total_word_count(word_count)
            unique_count = get_unique_word_count(word_count)
            st.success(f"有效词汇数：{unique_count:,} | 总词数：{total_count:,}")

        save_to_history(input_source, input_content, word_count, top_n, chart_type)

        col_stats1, col_stats2, col_stats3 = st.columns(3)
        with col_stats1:
            st.metric("有效词汇数", f"{unique_count:,}")
        with col_stats2:
            st.metric("总词数", f"{total_count:,}")
        with col_stats3:
            st.metric("平均词频", f"{total_count/unique_count:.1f}")

        st.subheader("📈 词频排名")
        top_words = get_top_words(word_count, top_n)
        word_df = {
            "排名": list(range(1, len(top_words)+1)),
            "词汇": [word for word, _ in top_words],
            "频次": [count for _, count in top_words]
        }
        st.dataframe(word_df, use_container_width=True, hide_index=True)

        st.subheader(f"🎨 {chart_type}展示")
        with st.spinner(f"正在生成{chart_type}..."):
            fig = generate_chart(word_count, chart_type, top_n)
            st.pyplot(fig)
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
            buf.seek(0)
            chart_image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            
            col_export1, col_export2, col_export3 = st.columns(3)
            with col_export1:
                export_json = export_results(word_count, top_n)
                st.download_button(
                    "📥 导出JSON数据",
                    export_json,
                    file_name="word_analysis_result.json",
                    mime="application/json",
                    use_container_width=True
                )
            with col_export2:
                csv_content = "\n".join([f"{word},{count}" for word, count in top_words])
                st.download_button(
                    "📥 导出CSV数据",
                    csv_content,
                    file_name="word_analysis_result.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col_export3:
                st.download_button(
                    "🖼️ 下载图表图片",
                    data=buf.getvalue(),
                    file_name=f"word_chart_{chart_type}.png",
                    mime="image/png",
                    use_container_width=True
                )

        with st.expander("📝 查看原始文本", expanded=False):
            st.text_area("原始文本", text, height=300)

    st.markdown("---")
    
    if "analysis_history" in st.session_state and st.session_state.analysis_history:
        st.subheader("📜 分析历史")
        with st.expander("点击展开历史记录", expanded=False):
            for idx, entry in enumerate(st.session_state.analysis_history, 1):
                with st.container():
                    col_hist1, col_hist2, col_hist3, col_hist4 = st.columns([2, 2, 1, 1])
                    with col_hist1:
                        st.write(f"**{idx}.** {entry['source']}: {entry['content']}")
                    with col_hist2:
                        st.write(f"📅 {entry['timestamp']}")
                    with col_hist3:
                        st.write(f"🔤 {entry['unique_words']}词")
                    with col_hist4:
                        if st.button(f"� 重新分析", key=f"reanalyze_{entry['id']}"):
                            word_count, top_n, chart_type = load_from_history(entry)
                            st.session_state.current_word_count = word_count
                            st.session_state.current_top_n = top_n
                            st.session_state.current_chart_type = chart_type
                            st.rerun()
                st.markdown("---")

    st.caption("�💡 提示：若HTTPS URL抓取失败，优先使用HTTP协议URL（如人民网）测试！")

if __name__ == "__main__":
    main()
