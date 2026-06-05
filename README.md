# medical-waste-traceability
基于YOLOv8+Flask的医疗废物智能分类与追溯系统，支持图片识别、二维码生成、Excel导出



以下是根据你的项目信息撰写的 `README.md`，可直接用于 GitHub 开源仓库。

markdown
医疗废物智慧追溯平台

基于 **YOLO + Flask + Excel** 的医疗废物识别与追溯系统。  
上传医疗废物照片后，系统自动识别废物类别并生成追溯二维码，所有记录保存至 Excel，支持一键导出报表。

## 功能特点

-  **AI 智能识别**：使用 YOLO 模型（`best.pt`）自动检测医疗废物类别（化学性废物、锐器、感染性废物、病理性废物等）
-  **图片上传**：支持 JPG/PNG 等常见图片格式，上传后即时预览
-  **数据记录**：自动将识别结果、重量、科室、操作员等写入 Excel 文件
-  **追溯二维码**：每次记录自动生成包含完整信息的二维码，便于粘贴在废物包装上
-  **报表导出**：一键导出 Excel 报表，文件自动按时间戳命名
-  **Web 界面**：美观、响应式的前端页面，适配 PC 与移动端

## 技术栈

- **后端**：Python, Flask
- **目标检测**：Ultralytics YOLO
- **数据存储**：openpyxl（Excel）
- **二维码生成**：segno
- **前端**：HTML5 + CSS3 + 原生 JavaScript（使用 Font Awesome 图标）

## 项目目录结构

```
ruanzhuxiangmu/
├── app.py                     # Flask 主程序
├── detector.py                # 独立检测类（可单独调用）
├── best.pt                    # YOLO 模型文件（可自行替换/训练）
├── templates/
│   └── index.html             # 前端页面
├── uploads/                   # 上传的图片临时保存目录（自动创建）
├── qrcodes/                   # 生成的二维码图片（自动创建）
├── medical_waste_records.xlsx # 记录数据库（自动创建）
├── export_*.xlsx              # 导出的报表文件
└── system.log                 # 系统日志（如有）
```

## 快速开始

### 环境要求

- Python 3.8 或以上
- pip 包管理工具

### 1. 克隆项目

```bash
git clone <你的仓库地址>
cd ruanzhuxiangmu
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install flask ultralytics openpyxl segno
```

> 注意：`ultralytics` 会同时安装 PyTorch 等深度学习依赖，请确保系统已正确配置 CUDA（如使用 GPU）或使用 CPU 版 PyTorch。

### 4. 准备模型文件

将你训练好的 YOLO 模型文件命名为 `best.pt` 并放置在项目根目录。

- 模型输出的类别索引必须与 `app.py` 中的 `CLASS_NAMES` 保持一致：
  ```python
  CLASS_NAMES = ['化学性废物', '锐器', '感染性废物', '病理性废物']
  ```
- 如果没有现成模型，可使用 YOLOv8 自行训练，训练完成后将 `best.pt` 拷贝过来。

### 5. 启动服务

```bash
python app.py
```

默认访问地址：`http://127.0.0.1:5000`

首次运行会自动创建 `uploads/`、`qrcodes/` 目录及 `medical_waste_records.xlsx` 文件。

## 使用说明

1. 打开浏览器访问首页。
2. **废物登记**区域：
   - 点击或拖拽上传医疗废物照片（可实时预览）。
   - 填写重量（克）、科室、操作员等信息。
   - 点击 **“智能识别并记录”** 按钮。
3. 系统调用 YOLO 模型识别图片，并将结果显示在右侧 **识别结果 & 追溯码** 面板中。
4. 成功识别后，页面会显示记录编号、废物类别、AI 置信度、处理时间等详细信息，并生成追溯二维码。
5. 点击 **“导出报表”** 按钮可下载最新的 Excel 报表，文件名格式为 `export_YYYYMMDDHHMMSS.xlsx`。

## API 接口

### POST `/upload`

上传图片并进行识别。

- **请求参数**（`multipart/form-data`）：
  - `image`：图片文件（必填）
  - `weight`：重量，单位克（必填）
  - `department`：科室，默认 `未指定`
  - `operator`：操作员，默认 `系统`
- **成功响应**（JSON）：
  ```json
  {
    "record_id": "20250312143022",
    "category": "感染性废物",
    "confidence": 0.92,
    "qr_file": "20250312143022.png",
    "time": "2025-03-12 14:30:22",
    "weight": "100",
    "department": "手术室",
    "operator": "张三"
  }
  ```
- **错误响应**：返回包含 `error` 字段的 JSON，HTTP 状态码 400/500。

### GET `/export`

导出当前 Excel 数据为文件下载。

- 成功：直接返回 Excel 文件流。
- 失败：返回 404 JSON `{"error": "没有数据"}`。

### GET `/qrcodes/<filename>`

访问生成的二维码图片，例如 `/qrcodes/20250312143022.png`。

## detector.py 独立使用

`detector.py` 提供了一个独立的 `WasteDetector` 类，可脱离 Flask 直接调用：

```python
from detector import WasteDetector

detector = WasteDetector(model_path='best.pt')
results = detector.detect('path/to/image.jpg')
for r in results:
    print(r['category'], r['confidence'])
```

> 注意：`detector.py` 中的类别名称可能与 `app.py` 不同，请根据你的模型实际类别调整 `cat_names` 列表。

自定义与扩展

- 更换识别类别：修改 `app.py` 中的 `CLASS_NAMES` 列表，确保顺序与你的 YOLO 模型输出索引完全一致。
- **重新训练模型**：使用 Ultralytics YOLO 训练新模型，替换 `best.pt` 即可。
- **Excel 文件位置**：可在 `app.py` 顶部修改 `EXCEL_FILE` 变量。
- **上传大小限制**：`app.config['MAX_CONTENT_LENGTH']` 默认为 16 MB，可按需调整。

注意事项

- 模型文件 `best.pt` 必须存在，否则程序启动时会报错。
- Excel 文件 `medical_waste_records.xlsx` 会自动创建，但请不要在用 Excel 打开时运行程序，以免文件锁定导致写入失败。
- 生产环境部署时，建议关闭 Flask 的 `debug` 模式，并使用 Gunicorn 或 Waitress 等 WSGI 服务器。



## 许可证

本项目采用 [MIT License](LICENSE) 开源，请根据实际情况添加 LICENSE 文件。  
如果你需要其他开源协议，请自行修改。

---

**维护者**：mengxiangweilai 
**联系方式**：3144964197@qq.com

