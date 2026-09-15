#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
面试题整理脚本
将爬取的数据整理成易读的Markdown格式
"""

import json
import re

def clean_text(text):
    """清理文本"""
    # 移除多余的空格和换行
    text = ' '.join(text.split())
    # 移除标题前的#符号
    text = re.sub(r'^#+\s*', '', text)
    return text

def generate_markdown():
    """生成Markdown文件"""
    # 读取爬取的数据
    with open('main_page.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = data['main_page']['questions']

    # 统计数据
    total_questions = 0
    total_answers = 0

    # 开始生成Markdown
    markdown_lines = []
    markdown_lines.append("# 📚 前端面试题汇总\n\n")
    markdown_lines.append("来源: https://interview.poetries.top\n\n")
    markdown_lines.append("---\n\n")

    current_category = None

    for i, item in enumerate(questions):
        question_text = clean_text(item['question'])
        level = item['level']
        answers = item['answer']

        # 判断是否是分类标题
        if level in ['h1', 'h2']:
            if current_category:
                markdown_lines.append("\n---\n\n")
            current_category = question_text
            markdown_lines.append(f"\n## {question_text}\n\n")
        else:
            # 这是一个问题
            total_questions += 1

            # 添加问题标题
            if level == 'h3':
                markdown_lines.append(f"### {question_text}\n\n")
            else:
                markdown_lines.append(f"#### {question_text}\n\n")

            # 添加答案
            if answers:
                total_answers += 1
                for answer in answers:
                    cleaned_answer = clean_text(answer)
                    if cleaned_answer:
                        markdown_lines.append(f"{cleaned_answer}\n\n")
            else:
                markdown_lines.append("*（暂无答案）*\n\n")

            markdown_lines.append("\n")

    # 添加统计信息
    stats = f"\n---\n\n## 📊 统计信息\n\n"
    stats += f"- 总问题数: **{total_questions}**\n"
    stats += f"- 有答案的问题: **{total_answers}**\n"
    stats += f"- 无答案的问题: **{total_questions - total_answers}**\n"

    markdown_content = ''.join(markdown_lines) + stats

    # 保存Markdown文件
    with open('面试题汇总.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"✅ 成功生成面试题汇总文件!")
    print(f"📄 文件名: 面试题汇总.md")
    print(f"\n📊 统计信息:")
    print(f"   - 总问题数: {total_questions}")
    print(f"   - 有答案的问题: {total_answers}")
    print(f"   - 无答案的问题: {total_questions - total_answers}")

    # 同时生成简化版的JSON
    simplified_data = []
    current_cat = None

    for item in questions:
        question_text = clean_text(item['question'])
        level = item['level']

        if level in ['h1', 'h2']:
            current_cat = question_text
        else:
            simplified_data.append({
                'category': current_cat,
                'question': question_text,
                'answer': ' '.join([clean_text(a) for a in item['answer']]) if item['answer'] else ''
            })

    with open('面试题汇总_简化版.json', 'w', encoding='utf-8') as f:
        json.dump(simplified_data, ensure_ascii=False, indent=2, fp=f)

    print(f"\n✅ 同时生成了简化版JSON文件:")
    print(f"📄 文件名: 面试题汇总_简化版.json")

if __name__ == "__main__":
    generate_markdown()