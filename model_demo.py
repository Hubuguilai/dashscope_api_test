#!/usr/bin/env python3
"""
Dashscope API 模型使用示例
演示如何使用不同类型的模型
"""

import requests
import json
from typing import Dict, Any

from config import load_settings

class DashscopeModelDemo:
    def __init__(self):
        settings = load_settings()
        self.api_base = settings.api_base
        self.headers = settings.headers
    
    def chat_with_model(self, model_name: str, message: str, max_tokens: int = 200) -> Dict[str, Any]:
        """与指定模型进行对话"""
        chat_url = f"{self.api_base}/chat/completions"
        
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": message}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(chat_url, headers=self.headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    usage = result.get('usage', {})
                    return {
                        'success': True,
                        'content': content,
                        'usage': usage
                    }
            return {
                'success': False,
                'error': f"HTTP {response.status_code}: {response.text}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def demo_general_chat(self):
        """演示通用对话模型"""
        print("=" * 60)
        print("🤖 通用对话模型演示")
        print("=" * 60)
        
        models = ['qwen-turbo-latest', 'qwen-plus-latest', 'qwen-max-latest']
        message = "请用一句话介绍人工智能的发展历程。"
        
        for model in models:
            print(f"\n📋 模型: {model}")
            print(f"💬 问题: {message}")
            result = self.chat_with_model(model, message)
            
            if result['success']:
                print(f"🤖 回答: {result['content']}")
                print(f"📊 Token使用: {result['usage']}")
            else:
                print(f"❌ 错误: {result['error']}")
    
    def demo_code_generation(self):
        """演示代码生成模型"""
        print("\n" + "=" * 60)
        print("💻 代码生成模型演示")
        print("=" * 60)
        
        models = ['qwen-coder-turbo-latest', 'qwen3-coder-plus']
        message = "请写一个Python函数来计算斐波那契数列的第n项。"
        
        for model in models:
            print(f"\n📋 模型: {model}")
            print(f"💬 问题: {message}")
            result = self.chat_with_model(model, message, max_tokens=300)
            
            if result['success']:
                print(f"🤖 回答: {result['content']}")
                print(f"📊 Token使用: {result['usage']}")
            else:
                print(f"❌ 错误: {result['error']}")
    
    def demo_math_models(self):
        """演示数学专用模型"""
        print("\n" + "=" * 60)
        print("🧮 数学专用模型演示")
        print("=" * 60)
        
        models = ['qwen-math-turbo-latest', 'qwen-math-plus-latest']
        message = "解这个方程: 2x² + 5x - 3 = 0"
        
        for model in models:
            print(f"\n📋 模型: {model}")
            print(f"💬 问题: {message}")
            result = self.chat_with_model(model, message)
            
            if result['success']:
                print(f"🤖 回答: {result['content']}")
                print(f"📊 Token使用: {result['usage']}")
            else:
                print(f"❌ 错误: {result['error']}")
    
    def demo_lightweight_models(self):
        """演示轻量级模型"""
        print("\n" + "=" * 60)
        print("🪶 轻量级模型演示")
        print("=" * 60)
        
        models = ['qwen2.5-3b-instruct', 'qwen3-4b']
        message = "什么是机器学习？"
        
        for model in models:
            print(f"\n📋 模型: {model}")
            print(f"💬 问题: {message}")
            result = self.chat_with_model(model, message)
            
            if result['success']:
                print(f"🤖 回答: {result['content']}")
                print(f"📊 Token使用: {result['usage']}")
            else:
                print(f"❌ 错误: {result['error']}")

def main():
    print("🌟 Dashscope API 模型使用示例")
    print("展示不同类型模型的使用方法和效果对比")
    
    demo = DashscopeModelDemo()
    
    # 运行各种演示
    demo.demo_general_chat()
    demo.demo_code_generation()
    demo.demo_math_models()
    demo.demo_lightweight_models()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("💡 提示: 可以根据需要选择不同的模型来优化性能和成本")
    print("=" * 60)

if __name__ == "__main__":
    main()
