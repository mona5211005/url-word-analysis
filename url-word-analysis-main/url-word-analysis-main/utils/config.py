import os
import platform
from pathlib import Path

SYSTEM = platform.system()
IS_WINDOWS = SYSTEM == "Windows"
IS_LINUX = SYSTEM == "Linux"
IS_MACOS = SYSTEM == "Darwin"

# 项目根目录（向上找到包含 fonts 文件夹的目录）
def get_project_root():
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "fonts").exists() or (parent / "app.py").exists():
            return parent
    return current.parent

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" if IS_WINDOWS else "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

STOP_WORDS = {
    "的", "了", "是", "我", "你", "他", "在", "有", "就", "不", "和", "也", "都", "这", "那", "其", "及",
    "与", "为", "于", "之", "而", "以", "所", "将", "会", "可", "能", "要", "应", "该", "对", "对于",
    "关于", "通过", "如果", "因为", "所以", "虽然", "但是", "而且", "一个", "一些", "全部", "所有",
    "没有", "可能", "一定", "可以", "需要", "进行", "实现", "完成", "具有", "包括", "涉及", "相关",
    "方面", "问题", "方法", "结果", "系统", "功能", "数据", "信息", "内容", "处理", "分析", "显示",
    "说明", "认为", "指出", "发现", "研究", "开发", "设计", "操作", "运行", "支持", "提供", "解决",
    "提高", "降低", "增加", "减少"
}

FONT_PATHS = {
    "Windows": [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/msyh.ttc"
    ],
    "Linux": [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
    ],
    "Darwin": [
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/PingFang.ttc"
    ]
}

def get_system_font_path():
    paths = FONT_PATHS.get(SYSTEM, FONT_PATHS["Linux"])
    for path in paths:
        if os.path.exists(path):
            return path
    return None

def get_font_family():
    if IS_WINDOWS:
        return "SimHei"
    return "DejaVu Sans"

# 本地中文字体文件名（需要下载并放入 fonts 文件夹）
LOCAL_FONT_FILES = [
    "SourceHanSansCN-Regular.otf",
    "NotoSansSC-Regular.otf",
    "NotoSansSC-Regular.ttf",
    "SourceHanSans-Regular.otf",
    "simhei.ttf",
    "msyh.ttc"
]

def get_local_font_path():
    """获取本地字体文件路径（优先从 fonts 文件夹查找）"""
    project_root = get_project_root()
    fonts_dir = project_root / "fonts"

    if fonts_dir.exists():
        for font_file in LOCAL_FONT_FILES:
            font_path = fonts_dir / font_file
            if font_path.exists():
                return str(font_path)

    # 如果 fonts 文件夹不存在或没有字体，返回 None
    return None