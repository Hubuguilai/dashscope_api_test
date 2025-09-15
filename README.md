# Dashscope API 可用性测试工具

这个工具用于验证阿里云Dashscope API（通义千问）的可用性和连接状态。

## 功能特性

- ✅ 环境变量检查
- ✅ 基本连接测试
- ✅ 模型列表获取测试
- ✅ 聊天完成接口测试
- ✅ 详细的测试报告生成

## 使用方法

### 方法1：使用一键测试脚本（推荐）

```bash
# 运行一键测试脚本（会自动设置环境变量并运行测试）
bash scripts/run_test.sh
```

### 方法2：手动设置环境变量

```bash
# 设置环境变量（示例：不要将密钥写入仓库）
export DASHSCOPE_API_KEY=your_api_key_here
export DASHSCOPE_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1

# 安装依赖（如果需要）
pip install -r requirements.txt

# 从项目根目录运行测试（模块方式执行，避免导入路径问题）
python3 -m tests.test_dashscope_api
```

### 方法3：模型功能演示

```bash
# 运行不同模型的功能演示（对比不同模型的效果）
python3 model_demo.py
```

## 输出结果

测试工具会执行以下检查：

1. **环境变量检查** - 验证API密钥和基础URL是否正确设置
2. **基本连接测试** - 测试到API服务器的网络连接
3. **模型列表测试** - 获取可用的模型列表
4. **聊天完成测试** - 实际调用AI模型进行对话测试

## 测试报告

测试完成后会生成：
- 控制台输出：实时显示测试进度和结果
- JSON报告文件：`reports/dashscope_api_test_report.json` - 包含详细的测试数据

## 项目结构

```
.
├─ config.py                 # 配置与环境变量加载
├─ model_demo.py             # 模型使用演示脚本
├─ requirements.txt          # Python 依赖
├─ scripts/
│  └─ run_test.sh            # 一键测试脚本
├─ tests/
│  └─ test_dashscope_api.py  # API 可用性测试
└─ reports/                  # 测试报告输出目录（自动生成，已忽略）
```

## API配置说明

- 建议通过`.env`或环境变量配置，不要在代码或README中放置明文密钥。
- `.env.example`提供了模板，复制为`.env`后填入自己的密钥：

```bash
cp .env.example .env
vi .env # 编辑并填写你的密钥
```

这个项目使用阿里云Dashscope的OpenAI兼容模式（`DASHSCOPE_API_BASE`），调用方式与OpenAI相似。

## 模型选择提示（示例）

根据不同使用场景可选择：

- 通用对话: `qwen-plus-latest`, `qwen-turbo-latest`
- 代码生成: `qwen-coder-plus-latest`, `qwen3-coder-plus`
- 数学推理: `qwen-math-plus-latest`
- 轻量级推理: `qwen2.5-3b-instruct`, `qwen3-4b`

## 故障排除

如果测试失败，请检查：

1. **网络连接** - 确保可以访问阿里云服务
2. **API密钥** - 确认密钥是否有效且未过期
3. **配额限制** - 检查是否达到API调用限额
4. **防火墙设置** - 确保网络策略允许访问外部API

## 依赖项

- Python 3.6+
- requests 库

## 许可协议

本项目采用 MIT License，详见项目根目录的 `LICENSE` 文件。

## 文件说明

- `test_dashscope_api.py` - 主测试脚本，验证API可用性
- `model_demo.py` - 模型功能演示脚本，展示不同模型的使用效果
- `run_test.sh` - 一键运行脚本
- `requirements.txt` - Python依赖列表
- `README.md` - 本说明文件
- `dashscope_api_test_report.json` - 测试报告文件（自动生成）
