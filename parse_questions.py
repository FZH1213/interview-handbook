#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进版解析脚本 - 正确处理速记、摘要和追问
"""

import json
import re
import os

def parse_markdown_to_json(md_content, file_name):
    """将markdown内容解析为结构化JSON"""
    questions = []
    lines = md_content.split('\n')

    current_section = ""
    current_question = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 匹配大章节 (## 一、XXX 或 ## 二、XXX)
        if line.startswith('## '):
            section_match = re.match(r'^##\s*[一二三四五六七八九十]+[、\.：]?\s*(.+)', line)
            if section_match:
                current_section = section_match.group(1).strip()
            else:
                section_text = line[3:].strip()
                if section_text and not section_text.startswith('#'):
                    current_section = section_text
            i += 1
            continue

        # 匹配题目 (### 数字 标题)
        if line.startswith('### '):
            # 保存上一个问题
            if current_question and current_question.get('t'):
                questions.append(current_question)

            # 提取题目标题
            title_match = re.match(r'^###\s*\d+[\.\s：]*(.+)', line)
            if title_match:
                current_question = {
                    's': current_section,
                    't': title_match.group(1).strip(),
                    'q': '',  # quickNote
                    'm': '',  # summary
                    'f': []   # followUp
                }
            i += 1
            continue

        # 匹配速记 (⚡ 30 秒速记)
        if current_question and '⚡' in line and '速记' in line:
            i += 1
            # 跳过空行
            while i < len(lines) and not lines[i].strip():
                i += 1

            quick_note_lines = []
            # 收集聚记内容，直到遇到空行
            while i < len(lines):
                next_line = lines[i].strip()
                # 遇到空行，速记段落结束
                if not next_line:
                    i += 1
                    break
                # 遇到新题目或新章节就停止
                if next_line.startswith('###') or next_line.startswith('##'):
                    break
                # 遇到追问标识也停止
                if next_line.startswith('💬'):
                    break
                quick_note_lines.append(next_line)
                i += 1
            current_question['q'] = '\n'.join(quick_note_lines)
            continue

        # 匹配面试官追问 (💬 面试官追问)
        if current_question and '💬' in line and '追问' in line:
            i += 1
            follow_ups = []

            # 跳过空行
            while i < len(lines) and not lines[i].strip():
                i += 1

            # 跳过第一个紧凑段落（它是后面详细问题的重复）
            # 紧凑段落特征：非常长的行，包含多个问号
            if i < len(lines):
                first_line = lines[i].strip()
                # 如果这一行包含多个问号且很长，说明是紧凑段落
                if first_line.count('？') >= 2 and len(first_line) > 100:
                    i += 1
                    # 跳过后面的空行
                    while i < len(lines) and not lines[i].strip():
                        i += 1

            # 解析详细追问（问题以？结尾，后面跟答案）
            while i < len(lines):
                next_line = lines[i].strip()

                # 遇到新题目或新章节就停止
                if next_line.startswith('###') or next_line.startswith('##'):
                    break
                # 遇到速记标识也停止
                if next_line.startswith('⚡'):
                    break

                # 检测问题（以？结尾）
                if next_line.endswith('？'):
                    question_text = next_line
                    i += 1

                    # 跳过空行
                    while i < len(lines) and not lines[i].strip():
                        i += 1

                    # 收集答案（直到下一个问题或结束标记）
                    answer_lines = []
                    while i < len(lines):
                        ans_line = lines[i].strip()
                        # 遇到新题目或新章节就停止
                        if ans_line.startswith('###') or ans_line.startswith('##'):
                            break
                        # 遇到速记标识也停止
                        if ans_line.startswith('⚡'):
                            break
                        # 遇到下一个问题（以？结尾）
                        if ans_line.endswith('？'):
                            break
                        # 遇到空行，答案段落结束
                        if not ans_line:
                            i += 1
                            break
                        answer_lines.append(ans_line)
                        i += 1

                    if answer_lines:
                        follow_ups.append({
                            'q': question_text,
                            'a': '\n'.join(answer_lines)
                        })
                else:
                    i += 1

            current_question['f'] = follow_ups
            continue

        # 其他内容作为正文（摘要）
        if current_question and line and not line.startswith('#') and not line.startswith('⚡') and not line.startswith('💬'):
            # 只有当摘要为空时才收集
            if not current_question['m']:
                summary_lines = []
                while i < len(lines):
                    next_line = lines[i].strip()
                    if next_line.startswith('###') or next_line.startswith('##'):
                        break
                    if next_line.startswith('⚡') or next_line.startswith('💬'):
                        break
                    if next_line:
                        summary_lines.append(next_line)
                    i += 1
                current_question['m'] = '\n'.join(summary_lines)
                continue

        i += 1

    # 保存最后一个问题
    if current_question and current_question.get('t'):
        questions.append(current_question)

    return questions

def split_into_chunks(questions, chunk_size=80):
    """将问题列表分成多个块"""
    chunks = []
    for i in range(0, len(questions), chunk_size):
        chunk = {
            'total': len(questions),
            'startIndex': i,
            'endIndex': min(i + chunk_size, len(questions)),
            'questions': questions[i:i + chunk_size]
        }
        chunks.append(chunk)
    return chunks

def get_sections(questions):
    """获取所有章节列表"""
    sections = []
    section_set = set()
    for q in questions:
        if q.get('s') and q['s'] not in section_set:
            sections.append({
                'name': q['s'],
                'count': sum(1 for x in questions if x.get('s') == q['s'])
            })
            section_set.add(q['s'])
    return sections

def save_as_js(data, filepath):
    """将数据保存为JS模块"""
    js_content = f"// 数据文件 - 自动生成\nmodule.exports = {json.dumps(data, ensure_ascii=False, separators=(',', ':'))}"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(js_content)

def main():
    # 读取前端面试题完整汇总
    print("正在处理前端面试题完整汇总...")
    with open('前端面试题完整汇总.md', 'r', encoding='utf-8') as f:
        basic_content = f.read()

    basic_questions = parse_markdown_to_json(basic_content, '前端面试题完整汇总.md')
    print(f"解析到 {len(basic_questions)} 道面试题")

    # 读取进阶面试题汇总
    print("正在处理进阶面试题汇总...")
    with open('进阶面试题汇总.md', 'r', encoding='utf-8') as f:
        advanced_content = f.read()

    advanced_questions = parse_markdown_to_json(advanced_content, '进阶面试题汇总.md')
    print(f"解析到 {len(advanced_questions)} 道进阶题")

    # 创建输出目录
    os.makedirs('miniprogram/packageBasic/data', exist_ok=True)
    os.makedirs('miniprogram/packageAdvanced/data', exist_ok=True)

    # 处理基础题 - 分块存储为JS文件
    print("正在保存前端面试题数据...")
    basic_chunks = split_into_chunks(basic_questions, 80)
    for idx, chunk in enumerate(basic_chunks):
        filename = f'miniprogram/packageBasic/data/questions_{idx}.js'
        save_as_js(chunk, filename)
        print(f"  已保存: {filename} ({len(chunk['questions'])}题)")

    # 保存章节索引
    basic_sections = get_sections(basic_questions)
    save_as_js({
        'total': len(basic_questions),
        'chunks': len(basic_chunks),
        'sections': basic_sections
    }, 'miniprogram/packageBasic/data/sections.js')

    # 处理进阶题 - 分块存储为JS文件
    print("正在保存进阶题数据...")
    advanced_chunks = split_into_chunks(advanced_questions, 80)
    for idx, chunk in enumerate(advanced_chunks):
        filename = f'miniprogram/packageAdvanced/data/questions_{idx}.js'
        save_as_js(chunk, filename)
        print(f"  已保存: {filename} ({len(chunk['questions'])}题)")

    # 保存章节索引
    advanced_sections = get_sections(advanced_questions)
    save_as_js({
        'total': len(advanced_questions),
        'chunks': len(advanced_chunks),
        'sections': advanced_sections
    }, 'miniprogram/packageAdvanced/data/sections.js')

    # 打印统计信息
    print("\n=== 解析统计 ===")
    print(f"前端面试题完整汇总: {len(basic_questions)} 道")
    print(f"进阶面试题汇总: {len(advanced_questions)} 道")
    print(f"总计: {len(basic_questions) + len(advanced_questions)} 道")

    # 打印前几个问题的结构验证
    print("\n=== 结构验证（前3题）===")
    for i, q in enumerate(basic_questions[:3]):
        print(f"\n题目 {i+1}: {q['t']}")
        print(f"  速记长度: {len(q['q'])} 字符")
        print(f"  摘要长度: {len(q['m'])} 字符")
        print(f"  追问数量: {len(q['f'])} 个")
        if q['f']:
            print(f"  第一个追问: {q['f'][0]['q'][:30]}...")

    # 打印章节统计
    print("\n=== 章节统计 ===")
    print("前端面试题章节:")
    for sec in basic_sections[:10]:
        print(f"  {sec['name']}: {sec['count']}题")
    if len(basic_sections) > 10:
        print(f"  ... 还有 {len(basic_sections) - 10} 个章节")

    print("\n进阶面试题章节:")
    for sec in advanced_sections[:10]:
        print(f"  {sec['name']}: {sec['count']}题")
    if len(advanced_sections) > 10:
        print(f"  ... 还有 {len(advanced_sections) - 10} 个章节")

    print("\n✅ 数据处理完成！")

if __name__ == '__main__':
    main()