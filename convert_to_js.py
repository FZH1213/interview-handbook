#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将JSON文件转换为JS文件
"""

import os
import json

def convert_json_to_js(json_file, js_file):
    """将JSON文件转换为JS模块"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 创建JS文件内容
    js_content = f"// 数据文件 - 自动生成\nmodule.exports = {json.dumps(data, ensure_ascii=False, separators=(',', ':'))}"

    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_content)

def main():
    # 转换基础题数据
    print("正在转换基础题数据...")
    basic_data_dir = 'miniprogram/packageBasic/data'
    for filename in os.listdir(basic_data_dir):
        if filename.endswith('.json'):
            json_path = os.path.join(basic_data_dir, filename)
            js_path = json_path.replace('.json', '.js')
            convert_json_to_js(json_path, js_path)
            print(f"  转换: {filename} -> {filename.replace('.json', '.js')}")

    # 转换进阶题数据
    print("正在转换进阶题数据...")
    advanced_data_dir = 'miniprogram/packageAdvanced/data'
    for filename in os.listdir(advanced_data_dir):
        if filename.endswith('.json'):
            json_path = os.path.join(advanced_data_dir, filename)
            js_path = json_path.replace('.json', '.js')
            convert_json_to_js(json_path, js_path)
            print(f"  转换: {filename} -> {filename.replace('.json', '.js')}")

    print("✅ 转换完成！")

if __name__ == '__main__':
    main()