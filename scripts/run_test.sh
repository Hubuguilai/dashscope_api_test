#!/bin/bash
# Dashscope API 测试环境设置脚本（无明文密钥）
set -euo pipefail

echo "🔧 加载环境变量 (优先从现有环境，其次从 .env)..."

# 从 .env 加载（如果存在）
if [ -f .env ]; then
  # shellcheck disable=SC2046
  export $(grep -v '^#' .env | xargs -I{} echo {})
fi

if [ -z "${DASHSCOPE_API_BASE:-}" ]; then
  export DASHSCOPE_API_BASE="https://dashscope.aliyuncs.com/compatible-mode/v1"
fi

if [ -z "${DASHSCOPE_API_KEY:-}" ]; then
  echo "❌ 未检测到 DASHSCOPE_API_KEY。请在 .env 或环境变量中设置。"
  echo "   示例: DASHSCOPE_API_KEY=your_api_key_here"
  exit 1
fi

echo "✅ 当前配置:"
echo "   DASHSCOPE_API_KEY: ${DASHSCOPE_API_KEY:0:20}..."
echo "   DASHSCOPE_API_BASE: $DASHSCOPE_API_BASE"

echo ""
echo "🚀 开始运行API可用性测试..."
# 使用模块方式执行，确保可以从项目根部导入
python3 -m tests.test_dashscope_api || exit_code=$? || true

echo ""
echo "📋 测试完成！请查看上方输出结果和生成的报告文件。"
exit ${exit_code:-0}
