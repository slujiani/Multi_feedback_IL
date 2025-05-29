# Multi_feedback_IL

## 项目简介
本项目用于处理触觉数据，结合FK模块进行数据处理和转换，生成标准格式的触觉数据文件。

## 目录结构
```
Multi_feedback_IL/
├── Inspire_Hand_FK/          # FK模块，用于计算手指位置
│   ├── __init__.py
│   ├── FK.py                 # 正运动学计算
│   └── angle.py              # 角度计算
├── data_processing/          # 数据处理模块
│   ├── tactile_processing/   # 触觉数据处理
│   │   └── process_tactile_data.py  # 触觉数据处理主程序
│   ├── out/                  # 处理后的数据输出目录
│   └── data/                 # 原始数据存放目录
└── README.md                 # 项目说明文档
```

## 功能说明
- **触觉数据处理**：将原始触觉数据与姿态数据结合，生成标准格式的触觉数据文件。
- **FK模块**：提供手指位置的正运动学计算，支持触觉数据的空间位置映射。

## 运行方法
1. 确保项目根目录下存在 `data` 目录，且包含 `tactile.npy` 和 `pose.npy` 文件。
2. 在项目根目录下运行以下命令：
   ```bash
   python -m data_processing.tactile_processing.process_tactile_data
   ```
3. 处理后的数据将保存在 `data_processing/out/tactile.npy` 文件中。

## 依赖
- Python 3.6+
- NumPy
- Matplotlib (用于FK模块的可视化)

