#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬取进阶版面试题
"""

import sys
import os

# 添加当前目录到系统路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crawler import InterviewCrawler

def main():
    crawler = InterviewCrawler()

    # 爬取进阶版面试题
    improve_url = "https://interview.poetries.top/docs/base/improve.html"

    print("=" * 60)
    print("开始爬取进阶版面试题")
    print("=" * 60)

    main_data = crawler.crawl_main_page(improve_url)

    if main_data:
        # 保存数据
        import json
        from format_questions import clean_text
        import re

        # 保存原始JSON
        with open('进阶面试题_raw.json', 'w', encoding='utf-8') as f:
            json.dump({'main_page': main_data}, ensure_ascii=False, indent=2, fp=f)
        print("✅ 原始数据已保存到 进阶面试题_raw.json")

        # 整理成Markdown格式
        markdown_lines = []
        markdown_lines.append("# 🚀 前端进阶面试题汇总\n\n")
        markdown_lines.append("来源: https://interview.poetries.top/docs/base/improve.html\n\n")
        markdown_lines.append("---\n\n")

        questions = main_data['questions']
        total_questions = 0
        current_category = None

        for item in questions:
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
                    for answer in answers:
                        cleaned_answer = clean_text(answer)
                        if cleaned_answer:
                            markdown_lines.append(f"{cleaned_answer}\n\n")

                markdown_lines.append("\n")

        # 添加统计信息
        stats = f"\n---\n\n## 📊 统计信息\n\n"
        stats += f"- 总问题数: **{total_questions}**\n"

        markdown_content = ''.join(markdown_lines) + stats

        # 保存Markdown文件
        with open('进阶面试题汇总.md', 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"✅ 进阶面试题已保存到 进阶面试题汇总.md")
        print(f"📊 共 {total_questions} 道题目")

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

        with open('进阶面试题_简化版.json', 'w', encoding='utf-8') as f:
            json.dump(simplified_data, ensure_ascii=False, indent=2, fp=f)

        print(f"✅ 简化版JSON已保存到 进阶面试题_简化版.json")
    else:
        print("❌ 爬取失败")

if __name__ == "__main__":
    main()