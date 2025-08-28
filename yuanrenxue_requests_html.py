#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
猿人学第一题 - requests-html解决方案
轻量级浏览器环境，支持JavaScript执行
"""

from requests_html import HTMLSession
import time
import json

class YuanrenxueRequestsHTML:
    def __init__(self):
        """初始化session"""
        self.session = HTMLSession()
        print("✅ requests-html session初始化完成")
    
    def load_page(self):
        """加载页面并渲染JavaScript"""
        print("🔄 正在加载页面...")
        
        # 访问页面
        self.r = self.session.get('https://match.yuanrenxue.cn/match/1')
        
        # 渲染JavaScript
        print("🔄 正在渲染JavaScript...")
        self.r.html.render(wait=3, timeout=20)
        
        print("✅ 页面加载和JavaScript渲染完成")
        return self.r
    
    def generate_and_request(self, page=1):
        """生成参数并请求数据"""
        print(f"🚀 正在获取第 {page} 页数据...")
        
        # 在渲染的页面中执行JavaScript生成m参数
        script = f"""
        () => {{
            var timestamp_offset = Date.parse(new Date()) + 100000000;
            oo0O0(timestamp_offset.toString());
            var final_ts = parseInt(timestamp_offset / 1000);
            var m_param = window.f + "丨" + final_ts;
            
            // 直接在页面中发送请求
            return fetch('/api/match/1?m=' + encodeURIComponent(m_param) + '&page={page}', {{
                method: 'GET',
                headers: {{
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'X-Requested-With': 'XMLHttpRequest'
                }}
            }}).then(response => response.json());
        }}
        """
        
        try:
            # 执行JavaScript并获取结果
            result = self.r.html.render(script=script, wait=2)
            
            # 这里需要从渲染结果中提取数据
            # requests-html的JavaScript执行有限制，我们改用直接方法
            
            # 生成m参数
            m_script = """
            () => {
                var timestamp_offset = Date.parse(new Date()) + 100000000;
                oo0O0(timestamp_offset.toString());
                var final_ts = parseInt(timestamp_offset / 1000);
                return {
                    m_param: window.f + "丨" + final_ts,
                    hash: window.f,
                    timestamp: final_ts
                };
            }
            """
            
            # 由于requests-html的限制，我们回退到selenium方案
            print("⚠️  requests-html对复杂JavaScript支持有限")
            print("💡 建议使用Selenium方案获得最佳效果")
            
            return None
            
        except Exception as e:
            print(f"❌ 第{page}页异常: {e}")
            return None
    
    def solve(self):
        """解决方案"""
        try:
            # 加载页面
            self.load_page()
            
            # 尝试获取数据
            result = self.generate_and_request(1)
            
            return result
            
        except Exception as e:
            print(f"❌ 执行异常: {e}")
            return None

def main():
    """主函数"""
    print("🚀 猿人学第一题 - requests-html解决方案")
    print("⚠️  注意：requests-html对复杂JavaScript支持有限")
    print("💡 推荐使用Selenium方案")
    print("=" * 60)
    
    solver = YuanrenxueRequestsHTML()
    result = solver.solve()
    
    if result:
        print(f"✅ 成功: {result}")
    else:
        print("❌ 建议使用Selenium方案")

if __name__ == "__main__":
    main()
