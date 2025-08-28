#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
猿人学第一题 - 最终工作版本
使用标准浏览器User-Agent和正确的算法
"""

import requests
import hashlib
import datetime
import time

def generate_m_param():
    """生成m参数 - 猿人学第一题算法"""
    current_time_ms = int(datetime.datetime.now().timestamp() * 1000)
    timestamp_with_offset = current_time_ms + 100000000
    hash_value = hashlib.md5(str(timestamp_with_offset).encode()).hexdigest()
    final_timestamp = int(timestamp_with_offset / 1000)
    m_param = f"{hash_value}丨{final_timestamp}"
    return m_param

def get_page_data(page=1, sessionid="dr4zlgx4f62fvtm817cgo4arqwtggh2o"):
    """获取指定页面的数据"""
    print(f"🚀 正在获取第 {page} 页数据...")
    
    # 生成m参数
    m_param = generate_m_param()
    print(f"📝 m参数: {m_param}")
    
    # 请求配置
    url = "https://match.yuanrenxue.cn/api/match/1"
    params = {'m': m_param, 'page': page}
    
    # 成功的请求头配置
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Referer': 'https://match.yuanrenxue.cn/match/1',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    
    # 完整的cookies
    cookies = {
        'sessionid': sessionid,
        'no-alert3': 'true',
        'm': 'c81e1a43733653f18d0621e972820f0b|1755846027000',
        'tk': '8716229639966551463',
        'Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3': '1755846365',
        'HMACCOUNT': 'C90A27A43AFCA84A',
        'Hm_lpvt_434c501fe98c1a8ec74b813751d4e3e3': '1756363954'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == '1':
                values = [item['value'] for item in data.get('data', [])]
                print(f"✅ 第{page}页成功: {values} (和: {sum(values)})")
                return values
            else:
                print(f"❌ API错误: {data}")
        else:
            print(f"❌ HTTP错误 {response.status_code}: {response.text[:100]}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    return None

def get_all_pages(sessionid="dr4zlgx4f62fvtm817cgo4arqwtggh2o"):
    """获取所有页面数据"""
    print("🎯 猿人学第一题 - 获取所有页面数据")
    print("=" * 60)
    print(f"🍪 SessionID: {sessionid}")
    print("🔧 算法: MD5(时间戳+100000000) + 丨 + 时间戳")
    print("=" * 60)
    
    all_values = []
    
    for page in range(1, 6):  # 获取5页数据
        values = get_page_data(page, sessionid)
        
        if values:
            all_values.extend(values)
        else:
            print(f"❌ 第{page}页获取失败，停止")
            break
        
        # 短暂延迟
        time.sleep(0.5)
    
    if all_values:
        print("\n" + "=" * 60)
        print("🎉 获取完成!")
        print(f"📊 总数据量: {len(all_values)} 个")
        print(f"📋 所有数据: {all_values}")
        print(f"🧮 最终答案: {sum(all_values)}")
        print("=" * 60)
        
        # 保存结果到文件
        with open('yuanrenxue_result.txt', 'w', encoding='utf-8') as f:
            f.write(f"猿人学第一题结果\n")
            f.write(f"获取时间: {datetime.datetime.now()}\n")
            f.write(f"所有数据: {all_values}\n")
            f.write(f"数据总和: {sum(all_values)}\n")
        
        print("💾 结果已保存到 yuanrenxue_result.txt")
    
    return all_values

if __name__ == "__main__":
    # 使用提供的sessionid
    sessionid = "dr4zlgx4f62fvtm817cgo4arqwtggh2o"
    
    print("🚀 猿人学第一题自动化脚本")
    print("📋 逆向工程完成，开始获取数据...")
    
    # 先测试单页
    test_values = get_page_data(1, sessionid)
    
    if test_values:
        print("\n✅ 单页测试成功，开始获取所有数据...")
        get_all_pages(sessionid)
    else:
        print("\n❌ 单页测试失败")
        print("💡 解决方案:")
        print("1. 确保sessionid有效（在浏览器中获取最新的）")
        print("2. 快速执行脚本（token有时效性）")
        print("3. 检查网络连接")
