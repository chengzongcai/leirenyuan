#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
猿人学第一题逆向脚本
基于逆向分析的完整实现
算法：m参数 = MD5(时间戳字符串) + "丨" + 时间戳
"""

import requests
import hashlib
import time
import json
# from urllib.parse import quote  # 不再需要手动编码

def generate_m_param():
    """
    生成m参数
    真正的算法：MD5(时间戳+偏移量) + "丨" + (时间戳+偏移量)/1000
    """
    # 1. 获取当前时间戳（毫秒），模拟JavaScript的Date.parse(new Date())
    import datetime
    current_time_ms = int(datetime.datetime.now().timestamp() * 1000)
    timestamp_with_offset = current_time_ms + 100000000

    # 2. 对(时间戳+偏移量)字符串进行MD5哈希
    hash_value = hashlib.md5(str(timestamp_with_offset).encode()).hexdigest()

    # 3. 最终时间戳 = (时间戳+偏移量) / 1000，转换为整数（与浏览器一致）
    final_timestamp = int(timestamp_with_offset / 1000)

    # 4. 构建m参数：哈希值 + 特殊字符 + 最终时间戳
    m_param = f"{hash_value}丨{final_timestamp}"

    print(f"当前时间戳(ms): {current_time_ms}")
    print(f"时间戳+偏移量: {timestamp_with_offset}")
    print(f"MD5哈希: {hash_value}")
    print(f"最终时间戳: {final_timestamp}")
    print(f"m参数: {m_param}")

    return m_param

def init_session():
    """
    初始化session，使用有效的cookies
    """
    session = requests.Session()

    # 设置有效的cookies（从浏览器中获取的）
    cookies = {
        'no-alert3': 'true',
        'm': 'c81e1a43733653f18d0621e972820f0b|1755846027000',
        'tk': '8716229639966551463',
        'Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3': '1755846365',
        'HMACCOUNT': 'C90A27A43AFCA84A',
        'sessionid': 'dr4zlgx4f62fvtm817cgo4arqwtggh2o',
        'Hm_lpvt_434c501fe98c1a8ec74b813751d4e3e3': '1756363954'
    }

    # 设置基本请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }

    session.headers.update(headers)
    session.cookies.update(cookies)

    print("🔄 正在初始化session...")
    print(f"设置的cookies: {cookies}")
    print("✅ Session初始化成功")

    return session

def make_request(session, page=1):
    """
    发送请求获取数据
    """
    if not session:
        print("❌ Session无效")
        return None

    # 生成动态m参数（使用正确的算法）
    m_param_raw = generate_m_param()

    # 请求URL和参数
    url = "https://match.yuanrenxue.cn/api/match/1"
    params = {
        'm': m_param_raw,
        'page': page
    }

    # API请求头
    api_headers = {
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

    # 更新session的请求头
    session.headers.update(api_headers)

    try:
        print(f"\n=== 发送请求 (第{page}页) ===")
        response = session.get(url, params=params, timeout=10)

        print(f"状态码: {response.status_code}")
        print(f"请求URL: {response.url}")
        print(f"实际发送的m参数: {params['m'][:50]}...")  # 只显示前50个字符

        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('status') == '1':
                    print("✅ 请求成功！")
                    print("响应数据:")
                    print(json.dumps(data, ensure_ascii=False, indent=2))
                    return data
                else:
                    print("❌ API返回错误:")
                    print(json.dumps(data, ensure_ascii=False, indent=2))
            except json.JSONDecodeError:
                print("❌ 响应不是有效的JSON格式")
                print("响应内容:", response.text[:500])
        else:
            print(f"❌ HTTP请求失败，状态码: {response.status_code}")
            print("响应内容:", response.text[:500])

    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")

    return None

def get_all_pages(session):
    """
    获取所有页面的数据
    """
    all_data = []

    for page in range(1, 6):  # 获取前5页数据
        print(f"\n{'='*60}")
        print(f"正在获取第 {page} 页数据...")

        data = make_request(session, page)
        if data and data.get('status') == '1':
            page_values = [item['value'] for item in data.get('data', [])]
            all_data.extend(page_values)
            print(f"第{page}页数据: {page_values}")
            print(f"第{page}页数据总和: {sum(page_values)}")
        else:
            print(f"第{page}页获取失败")
            break

        # 避免请求过快
        time.sleep(1)

    if all_data:
        print(f"\n{'='*60}")
        print("汇总结果:")
        print(f"总共获取数据: {len(all_data)} 个")
        print(f"所有数据: {all_data}")
        print(f"数据总和: {sum(all_data)}")

    return all_data

if __name__ == "__main__":
    print("猿人学第一题 - JS混淆源码乱码")
    print("算法: m参数 = MD5(时间戳+偏移量) + '丨' + (时间戳+偏移量)/1000")
    print("="*60)

    # 初始化session
    session = init_session()
    if not session:
        print("❌ 无法初始化session，程序退出")
        exit(1)

    # 测试单页请求
    print("\n测试单页请求:")

    # 先测试浏览器中验证成功的参数
    print("=== 测试浏览器验证成功的参数 ===")
    test_m_param = "d0bf4f6a923f5e907f7ebdc4ce393015丨1756470011"
    test_url = "https://match.yuanrenxue.cn/api/match/1"
    test_params = {'m': test_m_param, 'page': 1}

    api_headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://match.yuanrenxue.cn/match/1'
    }
    session.headers.update(api_headers)

    try:
        test_response = session.get(test_url, params=test_params, timeout=10)
        print(f"测试状态码: {test_response.status_code}")
        if test_response.status_code == 200:
            test_data = test_response.json()
            print("✅ 浏览器参数测试成功!")
            print(f"测试数据: {test_data}")
        else:
            print(f"❌ 浏览器参数测试失败: {test_response.text}")
    except Exception as e:
        print(f"❌ 测试异常: {e}")

    print("\n=== 测试Python生成的参数 ===")
    make_request(session, 1)

    # 获取所有页面数据
    print("\n开始获取所有页面数据...")
    get_all_pages(session)
