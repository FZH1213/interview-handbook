#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成前端面试题PDF文档
"""

import json
import re
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def register_fonts():
    """注册中文字体"""
    font_paths = [
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
        '/Library/Fonts/Arial Unicode.ttf'
    ]

    for path in font_paths:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont('Chinese', path))
                return 'Chinese'
            except:
                continue

    return 'Helvetica'

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
    """清理文本，移除HTML标签和多余的空白，并转义特殊字符"""
    if not text:
        return ""

    # 移除HTML标签（保留标签内的文本内容）
    text = re.sub(r'<[^>]+>', '', text)

    # 移除多余的空格和换行，但保留段落结构
    text = re.sub(r'\s+', ' ', text)

    # 转义XML/HTML特殊字符（reportlab Paragraph会解析这些字符）
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')

    return text.strip()

def create_pdf():
    """创建PDF文档"""
    # 注册字体
    font_name = register_fonts()

    # 创建PDF文档
    pdf_path = '前端面试题汇总.pdf'
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # 创建样式
    styles = getSampleStyleSheet()

    # 标题样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName=font_name,
        fontSize=24,
        spaceAfter=30,
        alignment=TA_LEFT
    )

    # 章节标题样式
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor='#333333'
    )

    # 题目样式
    question_style = ParagraphStyle(
        'Question',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=12,
        spaceAfter=6,
        spaceBefore=12,
        textColor='#000000',
        leading=18
    )

    # 答案样式
    answer_style = ParagraphStyle(
        'Answer',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        spaceAfter=12,
        textColor='#333333',
        leading=16,
        alignment=TA_JUSTIFY
    )

    # 子问题样式
    sub_question_style = ParagraphStyle(
        'SubQuestion',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=11,
        spaceAfter=4,
        spaceBefore=8,
        textColor='#000000',
        leftIndent=20,
        leading=16
    )

    sub_answer_style = ParagraphStyle(
        'SubAnswer',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        spaceAfter=8,
        textColor='#555555',
        leftIndent=20,
        leading=14
    )

    # 构建文档内容
    story = []

    # 添加总标题
    story.append(Paragraph("前端面试题汇总", title_style))
    story.append(Spacer(1, 30))

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

    # 添加基础题部分
    story.append(Paragraph("第一部分：基础题", section_style))
    story.append(Spacer(1, 20))

    question_num = 1
    current_section = ""

    for q in basic_questions:
        # 章节标题
        section = q.get('s', '')
        if section != current_section:
            current_section = section
            story.append(Spacer(1, 10))
            story.append(Paragraph(f"【{section}】", section_style))
            story.append(Spacer(1, 10))

        # 题目
        title = q.get('t', '')
        if title:
            title_clean = clean_text(title)
            if len(title_clean) > 500:
                title_clean = title_clean[:500] + "..."
            story.append(Paragraph(f"{question_num}. {title_clean}", question_style))

        # 答案
        answer = q.get('m', '')
        if answer:
            answer_clean = clean_text(answer)
            # 截断过长的答案（PDF生成限制）
            if len(answer_clean) > 2000:
                answer_clean = answer_clean[:2000] + "..."
            story.append(Paragraph(answer_clean, answer_style))

        # 相关问题
        follow_ups = q.get('f', [])
        if follow_ups:
            for idx, fu in enumerate(follow_ups, 1):
                fu_q = fu.get('q', '')
                fu_a = fu.get('a', '')
                if fu_q:
                    fu_q_clean = clean_text(fu_q)
                    if len(fu_q_clean) > 500:
                        fu_q_clean = fu_q_clean[:500] + "..."
                    story.append(Paragraph(f"  {idx}) {fu_q_clean}", sub_question_style))
                if fu_a:
                    fu_a_clean = clean_text(fu_a)
                    if len(fu_a_clean) > 1000:
                        fu_a_clean = fu_a_clean[:1000] + "..."
                    story.append(Paragraph(f"  答：{fu_a_clean}", sub_answer_style))

        question_num += 1

    # 添加进阶题部分
    story.append(PageBreak())
    story.append(Paragraph("第二部分：进阶题", section_style))
    story.append(Spacer(1, 20))

    current_section = ""

    for q in advanced_questions:
        # 章节标题
        section = q.get('s', '')
        if section != current_section:
            current_section = section
            story.append(Spacer(1, 10))
            story.append(Paragraph(f"【{section}】", section_style))
            story.append(Spacer(1, 10))

        # 题目
        title = q.get('t', '')
        if title:
            title_clean = clean_text(title)
            if len(title_clean) > 500:
                title_clean = title_clean[:500] + "..."
            story.append(Paragraph(f"{question_num}. {title_clean}", question_style))

        # 答案
        answer = q.get('m', '')
        if answer:
            answer_clean = clean_text(answer)
            if len(answer_clean) > 2000:
                answer_clean = answer_clean[:2000] + "..."
            story.append(Paragraph(answer_clean, answer_style))

        # 相关问题
        follow_ups = q.get('f', [])
        if follow_ups:
            for idx, fu in enumerate(follow_ups, 1):
                fu_q = fu.get('q', '')
                fu_a = fu.get('a', '')
                if fu_q:
                    fu_q_clean = clean_text(fu_q)
                    if len(fu_q_clean) > 500:
                        fu_q_clean = fu_q_clean[:500] + "..."
                    story.append(Paragraph(f"  {idx}) {fu_q_clean}", sub_question_style))
                if fu_a:
                    fu_a_clean = clean_text(fu_a)
                    if len(fu_a_clean) > 1000:
                        fu_a_clean = fu_a_clean[:1000] + "..."
                    story.append(Paragraph(f"  答：{fu_a_clean}", sub_answer_style))

        question_num += 1

    # 构建PDF
    print("\n正在生成PDF...")
    doc.build(story)
    print(f"\n✓ PDF已生成: {pdf_path}")
    print(f"  总题目数: {question_num - 1}")

if __name__ == '__main__':
    create_pdf()