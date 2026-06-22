import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from matplotlib.font_manager import FontProperties, findfont, fontManager
from .config import get_system_font_path, get_local_font_path

# 优先使用本地字体（打包到项目中），其次使用系统字体
font_path = get_local_font_path() or get_system_font_path()

plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans", "Arial Unicode MS", "PingFang SC", "Noto Sans CJK SC"]
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.unicode_minus"] = False

if font_path:
    font_prop = FontProperties(fname=font_path)
else:
    font_prop = FontProperties(family='DejaVu Sans')

def generate_wordcloud(word_data: dict, top_n: int = 20) -> plt.Figure:
    top_words = list(word_data.items())[:top_n]
    word_freq = {word: count for word, count in top_words}
    # 优先使用本地字体，其次使用系统字体
    wc_font_path = get_local_font_path() or get_system_font_path()

    wc = WordCloud(
        font_path=wc_font_path,
        width=800,
        height=500,
        background_color="white",
        max_words=top_n,
        max_font_size=180,
        random_state=42
    ).generate_from_frequencies(word_freq)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    return fig

def generate_bar_chart(word_data: dict, top_n: int = 20) -> plt.Figure:
    top_words = list(word_data.keys())[:top_n]
    top_counts = list(word_data.values())[:top_n]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(top_words, top_counts, color='#4F46E5', alpha=0.8)
    ax.set_xlabel("词汇", fontsize=12, fontproperties=font_prop)
    ax.set_ylabel("频次", fontsize=12, fontproperties=font_prop)
    ax.set_title(f"词频排名前{top_n}（柱状图）", fontsize=14, fontproperties=font_prop)
    plt.xticks(rotation=45, ha='right', fontproperties=font_prop)
    ax.grid(axis='y', alpha=0.3)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}', ha='center', va='bottom')

    plt.tight_layout()
    return fig

def generate_line_chart(word_data: dict, top_n: int = 20) -> plt.Figure:
    top_words = list(word_data.keys())[:top_n]
    top_counts = list(word_data.values())[:top_n]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(top_words, top_counts, marker='o', linewidth=2, color='#F59E0B', markersize=8)
    ax.set_xlabel("词汇", fontsize=12, fontproperties=font_prop)
    ax.set_ylabel("频次", fontsize=12, fontproperties=font_prop)
    ax.set_title(f"词频排名前{top_n}（折线图）", fontsize=14, fontproperties=font_prop)
    plt.xticks(rotation=45, ha='right', fontproperties=font_prop)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

def generate_pie_chart(word_data: dict, top_n: int = 20) -> plt.Figure:
    pie_n = min(top_n, 10)
    pie_words = list(word_data.keys())[:pie_n]
    pie_counts = list(word_data.values())[:pie_n]
    labels = [f"{word}\n({count})" for word, count in zip(pie_words, pie_counts)]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(pie_counts, labels=labels, autopct='%1.1f%%', startangle=90,
           colors=plt.cm.Set3(np.linspace(0, 1, pie_n)), textprops={'fontproperties': font_prop})
    ax.set_title(f"词频排名前{pie_n}（饼图）", fontsize=14, fontproperties=font_prop)
    ax.axis('equal')
    return fig

def generate_radar_chart(word_data: dict, top_n: int = 20) -> plt.Figure:
    radar_n = min(top_n, 8)
    radar_words = list(word_data.keys())[:radar_n]
    radar_counts = list(word_data.values())[:radar_n]
    angles = np.linspace(0, 2 * np.pi, radar_n, endpoint=False).tolist()
    radar_counts += radar_counts[:1]
    angles += angles[:1]

    fig = plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, radar_counts, 'o-', linewidth=2, color='#10B981')
    ax.fill(angles, radar_counts, alpha=0.25, color='#10B981')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(radar_words, fontproperties=font_prop)
    ax.set_title(f"词频排名前{radar_n}（雷达图）", fontsize=14, fontproperties=font_prop, pad=20)
    return fig

def generate_scatter_chart(word_data: dict, top_n: int = 20) -> plt.Figure:
    top_words = list(word_data.keys())[:top_n]
    top_counts = list(word_data.values())[:top_n]

    fig, ax = plt.subplots(figsize=(12, 6))
    scatter = ax.scatter(range(len(top_words)), top_counts, s=150, c=top_counts, 
                         cmap='viridis', alpha=0.8, edgecolors='white', linewidth=2)
    ax.set_xticks(range(len(top_words)))
    ax.set_xticklabels(top_words, rotation=45, ha='right', fontproperties=font_prop)
    ax.set_xlabel("词汇", fontsize=12, fontproperties=font_prop)
    ax.set_ylabel("频次", fontsize=12, fontproperties=font_prop)
    ax.set_title(f"词频排名前{top_n}（散点图）", fontsize=14, fontproperties=font_prop)
    plt.colorbar(scatter, ax=ax, label='频次')
    plt.tight_layout()
    return fig

def generate_heatmap(word_data: dict, top_n: int = 20) -> plt.Figure:
    heat_n = min(top_n, 10)
    heat_data = np.array(list(word_data.values())[:heat_n]).reshape(-1, 1)
    heat_words = list(word_data.keys())[:heat_n]

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(heat_data, cmap='YlOrRd', aspect='auto')
    ax.set_yticks(range(heat_n))
    ax.set_yticklabels(heat_words, fontproperties=font_prop)
    ax.set_xticks([])
    ax.set_title(f"词频排名前{heat_n}（热力图）", fontsize=14, fontproperties=font_prop)
    plt.colorbar(im, ax=ax, label='频次')
    plt.tight_layout()
    return fig

def generate_funnel_chart(word_data: dict, top_n: int = 20) -> plt.Figure:
    funnel_n = min(top_n, 8)
    funnel_words = list(word_data.keys())[:funnel_n]
    funnel_counts = list(word_data.values())[:funnel_n]
    max_count = max(funnel_counts)
    widths = [count / max_count for count in funnel_counts]

    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (word, count, width) in enumerate(zip(funnel_words, funnel_counts, widths)):
        x = (1 - width) / 2
        rect = plt.Rectangle((x, i), width, 0.8, fill=True, alpha=0.7, 
                             color=plt.cm.Blues(0.2 + i / funnel_n * 0.8))
        ax.add_patch(rect)
        ax.text(0.5, i + 0.4, f"{word}\n{count}", ha='center', va='center', 
                fontsize=11, fontproperties=font_prop)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, funnel_n)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title(f"词频排名前{funnel_n}（漏斗图）", fontsize=14, fontproperties=font_prop)
    plt.tight_layout()
    return fig

CHART_GENERATORS = {
    "词云图": generate_wordcloud,
    "柱状图": generate_bar_chart,
    "折线图": generate_line_chart,
    "饼图": generate_pie_chart,
    "雷达图": generate_radar_chart,
    "散点图": generate_scatter_chart,
    "热力图": generate_heatmap,
    "漏斗图": generate_funnel_chart
}

def generate_chart(word_data: dict, chart_type: str, top_n: int = 20) -> plt.Figure:
    generator = CHART_GENERATORS.get(chart_type)
    if generator:
        return generator(word_data, top_n)
    raise ValueError(f"不支持的图表类型: {chart_type}")