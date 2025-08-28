#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
猿人学第一题
在真实浏览器环境中执行，确保环境正确，100%成功
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

class YuanrenxueSolver:
    def __init__(self, headless=True):
        """初始化浏览器"""
        self.driver = None
        self.setup_driver(headless)
    
    def setup_driver(self, headless=True):
        """设置Chrome浏览器"""
        options = Options()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-logging')
        options.add_argument('--log-level=3')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 使用webdriver-manager自动管理ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ 浏览器初始化完成 (无头模式)" if headless else "✅ 浏览器初始化完成")
    
    def load_page(self):
        """加载猿人学页面"""
        print("🔄 正在加载页面...")
        self.driver.get("https://match.yuanrenxue.cn/match/1")
        
        # 等待页面加载完成
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # 等待JavaScript加载
        time.sleep(3)
        print("✅ 页面加载完成")
    
    def generate_m_param(self):
        """在浏览器中生成m参数"""
        script = """
        var timestamp_offset = Date.parse(new Date()) + 100000000;
        oo0O0(timestamp_offset.toString());
        var final_ts = parseInt(timestamp_offset / 1000);
        var m_param = window.f + "丨" + final_ts;
        return {
            m_param: m_param,
            timestamp_offset: timestamp_offset,
            hash: window.f,
            final_timestamp: final_ts
        };
        """
        
        result = self.driver.execute_script(script)
        print(f"📝 生成m参数: {result['m_param']}")
        return result
    
    def get_page_data(self, page=1):
        """获取指定页面数据"""
        print(f"🚀 正在获取第 {page} 页数据...")
        
        # 生成m参数
        param_info = self.generate_m_param()
        m_param = param_info['m_param']
        
        # 在浏览器中发送请求
        script = f"""
        return fetch('/api/match/1?m=' + encodeURIComponent('{m_param}') + '&page={page}', {{
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
                values = [item['value'] for item in data.get('data', [])]
                page_sum = sum(values)
                print(f"✅ 第{page}页: {values} (和: {page_sum})")
                return values
            else:
                print(f"❌ 第{page}页失败: {data}")
                return None
                
        except Exception as e:
            print(f"❌ 第{page}页异常: {e}")
            return None
    
    def get_all_data(self):
        """获取所有页面数据"""
        print("🎯 开始获取所有页面数据")
        print("=" * 60)
        
        all_values = []
        page_results = []
        
        for page in range(1, 6):  # 获取5页数据
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
            
            # 短暂延迟
            time.sleep(0.5)
        
        return all_values, page_results
    
    def display_results(self, all_values, page_results):
        """显示结果"""
        print("\n" + "=" * 60)
        print("🎉 猿人学第一题 - Python获取完成!")
        print("=" * 60)

        for result in page_results:
            print(f"📄 第{result['page']}页: {result['values']} (和: {result['sum']})")

        total_sum = sum(all_values)
        average = total_sum / len(all_values) if all_values else 0

        print(f"\n📊 总数据量: {len(all_values)} 个")
        print(f"📋 所有数据: {all_values}")
        print(f"🧮 数据总和: {total_sum}")
        print(f"📈 平均值: {average:.2f}")
        print(f"🎯 最终答案(平均值): {average:.2f}")
        print("=" * 60)

        return average
    
    def save_results(self, all_values, page_results, average):
        """保存结果到文件"""
        total_sum = sum(all_values)
        result_data = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'page_results': page_results,
            'all_values': all_values,
            'total_sum': total_sum,
            'total_count': len(all_values),
            'average': round(average, 2),
            'final_answer': round(average, 2)
        }
        
        with open('yuanrenxue_python_result.json', 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        print("💾 结果已保存到 yuanrenxue_python_result.json")
    
    def solve(self):
        """完整解决方案"""
        try:
            # 1. 加载页面
            self.load_page()
            
            # 2. 获取所有数据
            all_values, page_results = self.get_all_data()
            
            if all_values:
                # 3. 显示结果
                average = self.display_results(all_values, page_results)

                # 4. 保存结果
                self.save_results(all_values, page_results, average)

                return average
            else:
                print("❌ 未获取到任何数据")
                return None
                
        except Exception as e:
            print(f"❌ 执行异常: {e}")
            return None
        
        finally:
            self.close()
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("🔒 浏览器已关闭")

def main():
    """主函数"""
    print("🚀 猿人学第一题 - Python Selenium解决方案")
    print("📋 使用无头浏览器环境，计算平均值")
    print("=" * 60)

    # 创建解决器实例（无头模式）
    solver = YuanrenxueSolver(headless=False)
    
    # 执行解决方案
    result = solver.solve()
    
    if result:
        print(f"\n🎊 成功！猿人学第一题答案(平均值): {result:.2f}")
    else:
        print("\n❌ 执行失败，请检查网络连接和Chrome浏览器")

if __name__ == "__main__":
    main()
