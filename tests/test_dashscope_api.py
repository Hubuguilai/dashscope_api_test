#!/usr/bin/env python3
"""
Dashscope API 可用性测试脚本
测试通义千问API的连接性和基本功能
"""

import sys
import os
import requests
import json
from datetime import datetime
from typing import List

from config import load_settings

class DashscopeAPITester:
    def __init__(self):
        settings = load_settings()
        self.api_key = settings.api_key
        self.api_base = settings.api_base
        self.headers = settings.headers
    
    def check_environment_variables(self):
        """检查环境变量是否设置"""
        print("=" * 50)
        print("1. 环境变量检查")
        print("=" * 50)
        
        if not self.api_key:
            print("❌ DASHSCOPE_API_KEY 环境变量未设置")
            return False
        else:
            print(f"✅ DASHSCOPE_API_KEY: {self.api_key[:20]}...")
        
        if not self.api_base:
            print("❌ DASHSCOPE_API_BASE 环境变量未设置")
            return False
        else:
            print(f"✅ DASHSCOPE_API_BASE: {self.api_base}")
        
        return True
    
    def test_basic_connection(self):
        """测试基本连接"""
        print("\n" + "=" * 50)
        print("2. 基本连接测试")
        print("=" * 50)
        
        if not self.api_base:
            print("❌ API_BASE未设置，无法进行连接测试")
            return False
            
        try:
            # 测试GET请求到根路径
            response = requests.get(self.api_base, timeout=10)
            print(f"✅ 基本连接成功 - 状态码: {response.status_code}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ 基本连接失败: {e}")
            return False
    
    def test_models_endpoint(self):
        """测试模型列表接口"""
        print("\n" + "=" * 50)
        print("3. 模型列表接口测试")
        print("=" * 50)
        
        try:
            models_url = f"{self.api_base}/models"
            response = requests.get(models_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                models_data = response.json()
                print(f"✅ 模型列表获取成功")
                
                if 'data' in models_data:
                    print(f"📊 可用模型数量: {len(models_data['data'])}")
                    print("可用模型列表:")
                    for model in models_data['data'][:5]:  # 只显示前5个
                        print(f"  - {model.get('id', 'Unknown')}")
                    if len(models_data['data']) > 5:
                        print(f"  ... 还有 {len(models_data['data']) - 5} 个模型")
                else:
                    print("⚠️  响应格式异常，未找到模型数据")
                
                return True
            else:
                print(f"❌ 模型列表获取失败 - 状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 模型列表请求失败: {e}")
            return False
    
    def test_chat_completion(self):
        """测试聊天完成接口"""
        print("\n" + "=" * 50)
        print("4. 聊天完成接口测试")
        print("=" * 50)
        
        try:
            chat_url = f"{self.api_base}/chat/completions"
            
            payload = {
                "model": "qwen-turbo",  # 使用通义千问turbo模型
                "messages": [
                    {
                        "role": "user",
                        "content": "你好，请简单介绍一下你自己。"
                    }
                ],
                "max_tokens": 100,
                "temperature": 0.7
            }
            
            response = requests.post(
                chat_url, 
                headers=self.headers, 
                json=payload, 
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 聊天完成接口测试成功")
                
                if 'choices' in result and len(result['choices']) > 0:
                    message = result['choices'][0].get('message', {})
                    content = message.get('content', '')
                    print(f"🤖 AI回复: {content[:200]}...")
                    
                    # 显示使用统计
                    if 'usage' in result:
                        usage = result['usage']
                        print(f"📈 Token使用情况:")
                        print(f"  - 输入Token: {usage.get('prompt_tokens', 'N/A')}")
                        print(f"  - 输出Token: {usage.get('completion_tokens', 'N/A')}")
                        print(f"  - 总计Token: {usage.get('total_tokens', 'N/A')}")
                else:
                    print("⚠️  响应格式异常，未找到回复内容")
                
                return True
            else:
                print(f"❌ 聊天完成接口测试失败 - 状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 聊天完成请求失败: {e}")
            return False
    
    def generate_report(self, results: List[bool]):
        """生成测试报告"""
        print("\n" + "=" * 50)
        print("5. 测试报告")
        print("=" * 50)
        
        passed_tests = sum(results)
        total_tests = len(results)
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"🎯 测试总结:")
        print(f"  - 通过测试: {passed_tests}/{total_tests}")
        print(f"  - 成功率: {success_rate:.1f}%")
        print(f"  - 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if success_rate == 100:
            print("🎉 所有测试通过！API完全可用。")
            status = "完全可用"
        elif success_rate >= 75:
            print("⚠️  大部分测试通过，API基本可用，但可能存在部分问题。")
            status = "基本可用"
        elif success_rate >= 50:
            print("⚠️  部分测试通过，API存在明显问题。")
            status = "部分可用"
        else:
            print("❌ 大部分测试失败，API可能不可用。")
            status = "不可用"
        
        # 保存报告到文件
        report = {
            "test_time": datetime.now().isoformat(),
            "api_key": self.api_key[:20] + "..." if self.api_key else "未设置",
            "api_base": self.api_base,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": success_rate,
            "status": status,
            "test_results": {
                "environment_check": results[0],
                "basic_connection": results[1],
                "models_endpoint": results[2],
                "chat_completion": results[3]
            }
        }
        
        # 确保报告目录存在
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        report_file = os.path.join(reports_dir, "dashscope_api_test_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📄 详细报告已保存到: {report_file}")
        
        return status
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始Dashscope API可用性测试...")
        print(f"⏰ 测试开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        results = []
        
        # 1. 检查环境变量
        results.append(self.check_environment_variables())
        
        if not results[0]:
            print("\n❌ 环境变量检查失败，无法继续测试。")
            print("请确保已正确设置 DASHSCOPE_API_KEY 和 DASHSCOPE_API_BASE")
            return False
        
        # 2. 基本连接测试
        results.append(self.test_basic_connection())
        
        # 3. 模型列表测试
        results.append(self.test_models_endpoint())
        
        # 4. 聊天完成测试
        results.append(self.test_chat_completion())
        
        # 5. 生成报告
        status = self.generate_report(results)
        
        return status

def main():
    """主函数"""
    print("🔍 Dashscope API 可用性测试工具")
    print("=" * 50)
    
    try:
        tester = DashscopeAPITester()
    except RuntimeError as e:
        print(f"❌ 配置错误: {e}")
        print("请在环境变量或项目根目录的 .env 中设置 DASHSCOPE_API_KEY 和可选的 DASHSCOPE_API_BASE。")
        return 1

    status = tester.run_all_tests()
    
    print(f"\n🏁 测试完成，API状态: {status}")
    return 0 if status in ["完全可用", "基本可用"] else 1

if __name__ == "__main__":
    sys.exit(main())
