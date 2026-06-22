# 中文字体文件夹

本文件夹用于存放中文字体文件，确保应用在 Streamlit Cloud 上能正确显示中文。

## 下载字体

请下载以下任一字体文件并放入此文件夹：

### 推荐字体

| 字体名称 | 下载地址 | 建议文件名 |
|----------|----------|------------|
| 思源黑体 (Source Han Sans) | https://github.com/adobe-fonts/source-han-sans/releases | SourceHanSansCN-Regular.otf |
| Noto Sans CJK (Simplified Chinese) | https://fonts.google.com/noto | NotoSansSC-Regular.otf |

### 下载步骤

1. 点击上方的下载链接
2. 选择 "SourceHanSansCN-Regular.otf" 或 "NotoSansSC-Regular.otf"
3. 将下载的文件移动到此 `fonts/` 文件夹
4. 文件名建议改为 `SourceHanSansCN-Regular.otf` 或 `NotoSansSC-Regular.otf`

### 支持的字体格式

- `.otf` (OpenType)
- `.ttf` (TrueType)

## 字体说明

- **思源黑体**: Adobe 和 Google 开发的开源中文字体，支持简体中文
- **Noto Sans CJK**: Google 开发的开源中文字体族

这两个字体都已包含在 Streamlit Cloud 的常用字体列表中，如服务器已有这些字体，则无需下载。
