#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成前端面试题Markdown文档（优化版本）
"""

import json
import re
import os

def parse_js_file(filepath):
    """解析JS数据文件，返回JSON数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取JSON部分
    match = re.search(r'module\.exports\s*=\s*({.*})', content, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            data = json.loads(json_str)
            return data
        except json.JSONDecodeError as e:
            print(f"解析错误 {filepath}: {e}")
            return None
    return None

def clean_text(text):
    """清理文本，移除HTML标签和多余的空白"""
    if not text:
        return ""

    # 移除HTML标签（保留标签内的文本内容）
    text = re.sub(r'<[^>]+>', '', text)

    # 移除多余的空格和换行
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r' +', ' ', text)

    return text.strip()

def create_markdown():
    """创建Markdown文档"""

    # 读取基础题
    print("正在读取基础题...")
    basic_questions = []
    basic_path = 'miniprogram/packageBasic/data'
    for i in range(7):
        filepath = os.path.join(basic_path, f'questions_{i}.js')
        if os.path.exists(filepath):
            data = parse_js_file(filepath)
            if data and 'questions' in data:
                basic_questions.extend(data['questions'])
                print(f"  - 读取 {len(data['questions'])} 道基础题")

    # 读取进阶题
    print("正在读取进阶题...")
    advanced_questions = []
    advanced_path = 'miniprogram/packageAdvanced/data'
    for i in range(3):
        filepath = os.path.join(advanced_path, f'questions_{i}.js')
        if os.path.exists(filepath):
            data = parse_js_file(filepath)
            if data and 'questions' in data:
                advanced_questions.extend(data['questions'])
                print(f"  - 读取 {len(data['questions'])} 道进阶题")

    print(f"\n总共: {len(basic_questions)} 道基础题, {len(advanced_questions)} 道进阶题")

    # 写入文件
    print("\n正在生成Markdown文档...")
    md_path = '前端面试题汇总（基础+进阶）.md'

    with open(md_path, 'w', encoding='utf-8') as f:
        # 写入标题
        f.write("# 前端面试题汇总（基础+进阶）\n\n")
        f.write("---\n\n")

        # 写入基础题部分
        f.write("## 第一部分：基础题\n\n")

        question_num = 1
        current_section = ""

        for q in basic_questions:
            # 章节标题
            section = q.get('s', '')
            if section != current_section:
                current_section = section
                f.write(f"\n### 【{section}】\n\n")

            # 题目
            title = q.get('t', '')
            if title:
                title_clean = clean_text(title)
                f.write(f"#### {question_num}. {title_clean}\n\n")

            # 答案
            answer = q.get('m', '')
            if answer:
                answer_clean = clean_text(answer)
                f.write(f"{answer_clean}\n\n")

            # 相关问题
            follow_ups = q.get('f', [])
            if follow_ups:
                f.write("**相关问题：**\n\n")
                for idx, fu in enumerate(follow_ups, 1):
                    fu_q = fu.get('q', '')
                    fu_a = fu.get('a', '')
                    if fu_q:
                        fu_q_clean = clean_text(fu_q)
                        f.write(f"{idx}. {fu_q_clean}\n")
                    if fu_a:
                        fu_a_clean = clean_text(fu_a)
                        f.write(f"   **答：** {fu_a_clean}\n\n")

            question_num += 1

        # 写入进阶题部分
        f.write("\n---\n\n")
        f.write("## 第二部分：进阶题\n\n")

        current_section = ""

        for q in advanced_questions:
            # 章节标题
            section = q.get('s', '')
            if section != current_section:
                current_section = section
                f.write(f"\n### 【{section}】\n\n")

            # 题目
            title = q.get('t', '')
            if title:
                title_clean = clean_text(title)
                f.write(f"#### {question_num}. {title_clean}\n\n")

            # 答案
            answer = q.get('m', '')
            if answer:
                answer_clean = clean_text(answer)
                f.write(f"{answer_clean}\n\n")

            # 相关问题
            follow_ups = q.get('f', [])
            if follow_ups:
                f.write("**相关问题：**\n\n")
                for idx, fu in enumerate(follow_ups, 1):
                    fu_q = fu.get('q', '')
                    fu_a = fu.get('a', '')
                    if fu_q:
                        fu_q_clean = clean_text(fu_q)
                        f.write(f"{idx}. {fu_q_clean}\n")
                    if fu_a:
                        fu_a_clean = clean_text(fu_a)
                        f.write(f"   **答：** {fu_a_clean}\n\n")

            question_num += 1

    print(f"\n✓ Markdown文档已生成: {md_path}")
    print(f"  总题目数: {question_num - 1}")

if __name__ == '__main__':
    create_markdown()