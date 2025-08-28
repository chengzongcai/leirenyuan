#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
猿人学第一题 - 混合解决方案
结合Selenium和requests，兼顾效率和成功率
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import json
import hashlib
import datetime

class YuanrenxueHybrid:
    def __init__(self):
        """初始化"""
        self.driver = None
        self.session = requests.Session()
        self.cookies = None
        
    def setup_browser(self):
        """设置浏览器（仅用于获取cookies和验证）"""
        options = Options()
        options.add_argument('--headless')  # 无头模式
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=options)
        print("✅ 浏览器初始化完成")
    
    def get_fresh_cookies(self):
        """获取新鲜的cookies"""
        print("🍪 正在获取最新cookies...")
        
        self.driver.get("https://match.yuanrenxue.cn/match/1")
        time.sleep(3)
        
        # 获取cookies
        selenium_cookies = self.driver.get_cookies()
        self.cookies = {}
        
        for cookie in selenium_cookies:
            self.cookies[cookie['name']] = cookie['value']
        
        print(f"✅ 获取到 {len(self.cookies)} 个cookies")
        return self.cookies
    
    def generate_m_param_browser(self):
        """在浏览器中生成m参数"""
        script = """
        var timestamp_offset = Date.parse(new Date()) + 100000000;
        oo0O0(timestamp_offset.toString());
        var final_ts = parseInt(timestamp_offset / 1000);
        return {
            m_param: window.f + "丨" + final_ts,
            hash: window.f,
            timestamp_offset: timestamp_offset,
            final_timestamp: final_ts
        };
        """
        
        result = self.driver.execute_script(script)
        return result
    
    def generate_m_param_python(self):
        """Python版本的m参数生成（备用）"""
        current_time_ms = int(datetime.datetime.now().timestamp() * 1000)
        timestamp_with_offset = current_time_ms + 100000000
        hash_value = hashlib.md5(str(timestamp_with_offset).encode()).hexdigest()
        final_timestamp = int(timestamp_with_offset / 1000)
        m_param = f"{hash_value}丨{final_timestamp}"
        
        return {
            'm_param': m_param,
            'hash': hash_value,
            'timestamp_offset': timestamp_with_offset,
            'final_timestamp': final_timestamp
        }
    
    def request_with_requests(self, m_param, page=1):
        """使用requests发送请求"""
        url = "https://match.yuanrenxue.cn/api/match/1"
        params = {'m': m_param, 'page': page}
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://match.yuanrenxue.cn/match/1',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        try:
            response = self.session.get(
                url, 
                params=params, 
                headers=headers, 
                cookies=self.cookies, 
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == '1':
                    return [item['value'] for item in data.get('data', [])]
            
            return None
            
        except Exception as e:
            print(f"❌ requests请求异常: {e}")
            return None
    
    def request_with_browser(self, m_param, page=1):
        """在浏览器中发送请求（备用方案）"""
        script = f"""
        return fetch('/api/match/1?m={encodeURIComponent(m_param)}&page={page}', {{
            method: 'GET',
            headers: {{
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest'
            }}
        }}).then(response => response.json());
        """
        
        try:
            data = self.driver.execute_script(script)
            if data and data.get('status') == '1':
                return [item['value'] for item in data.get('data', [])]
            return None
        except Exception as e:
            print(f"❌ 浏览器请求异常: {e}")
            return None
    
    def get_page_data(self, page=1):
        """获取页面数据（混合方案）"""
        print(f"🚀 正在获取第 {page} 页数据...")
        
        # 方案1：浏览器生成参数 + requests请求
        try:
            param_info = self.generate_m_param_browser()
            m_param = param_info['m_param']
            print(f"📝 浏览器生成m参数: {m_param}")
            
            values = self.request_with_requests(m_param, page)
            if values:
                print(f"✅ 第{page}页(requests): {values} (和: {sum(values)})")
                return values
        except Exception as e:
            print(f"⚠️  方案1失败: {e}")
        
        # 方案2：完全在浏览器中执行
        try:
            param_info = self.generate_m_param_browser()
            m_param = param_info['m_param']
            
            values = self.request_with_browser(m_param, page)
            if values:
                print(f"✅ 第{page}页(browser): {values} (和: {sum(values)})")
                return values
        except Exception as e:
            print(f"⚠️  方案2失败: {e}")
        
        print(f"❌ 第{page}页所有方案都失败")
        return None
    
    def solve(self):
        """完整解决方案"""
        try:
            # 1. 设置浏览器
            self.setup_browser()
            
            # 2. 获取cookies
            self.get_fresh_cookies()
            
            # 3. 获取所有数据
            print("\n🎯 开始获取所有页面数据")
            print("=" * 60)
            
            all_values = []
            page_results = []
            
            for page in range(1, 6):
                values = self.get_page_data(page)
                
                if values:
                    all_values.extend(values)
                    page_results.append({
                        'page': page,
                        'values': values,
                        'sum': sum(values)
                    })
                else:
                    print(f"❌ 第{page}页获取失败，停止")
                    break
                
                time.sleep(0.5)
            
            # 4. 显示结果
            if all_values:
                self.display_results(all_values, page_results)
                return sum(all_values)
            else:
                print("❌ 未获取到任何数据")
                return None
                
        except Exception as e:
            print(f"❌ 执行异常: {e}")
            return None
        
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 浏览器已关闭")
    
    def display_results(self, all_values, page_results):
        """显示结果"""
        print("\n" + "=" * 60)
        print("🎉 猿人学第一题 - Python混合方案完成!")
        print("=" * 60)
        
        for result in page_results:
            print(f"📄 第{result['page']}页: {result['values']} (和: {result['sum']})")
        
        total_sum = sum(all_values)
        print(f"\n📊 总数据量: {len(all_values)} 个")
        print(f"📋 所有数据: {all_values}")
        print(f"🧮 最终答案: {total_sum}")
        print("=" * 60)
        
        # 保存结果
        result_data = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'page_results': page_results,
            'all_values': all_values,
            'total_sum': total_sum
        }
        
        with open('yuanrenxue_hybrid_result.json', 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        print("💾 结果已保存到 yuanrenxue_hybrid_result.json")

def main():
    """主函数"""
    print("🚀 猿人学第一题 - 混合解决方案")
    print("🔧 浏览器生成参数 + requests发送请求")
    print("🛡️  多重备用方案，确保成功率")
    print("=" * 60)
    
    solver = YuanrenxueHybrid()
    result = solver.solve()
    
    if result:
        print(f"\n🎊 成功！猿人学第一题答案: {result}")
    else:
        print("\n❌ 执行失败")

if __name__ == "__main__":
    main()
