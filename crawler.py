#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
面试题网站爬虫脚本
爬取 https://interview.poetries.top 的面试题内容
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re

class InterviewCrawler:
    def __init__(self):
        self.base_url = "https://interview.poetries.top"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.interview_data = []

    def get_page(self, url):
        """获取页面内容"""
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            print(f"获取页面失败: {url}, 错误: {e}")
            return None

    def parse_sidebar(self, html):
        """解析侧边栏，获取所有面试题分类链接"""
        soup = BeautifulSoup(html, 'html.parser')

        # 查找侧边栏导航
        sidebar = soup.find('aside') or soup.find('nav') or soup.find(class_='sidebar')

        if sidebar:
            links = sidebar.find_all('a', href=True)
            category_links = []
            for link in links:
                href = link.get('href')
                text = link.get_text(strip=True)
                if href and text:
                    if not href.startswith('http'):
                        href = self.base_url + href
                    category_links.append({
                        'title': text,
                        'url': href
                    })
            return category_links
        return []

    def parse_content(self, html):
        """解析页面内容，提取面试题"""
        soup = BeautifulSoup(html, 'html.parser')

        # 查找主要内容区域
        main_content = soup.find('article') or soup.find('main') or soup.find(class_='content') or soup.find(id='main')

        if main_content:
            # 提取所有标题和段落
            questions = []
            current_question = None

            for element in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'pre', 'ul', 'ol']):
                if element.name in ['h1', 'h2', 'h3', 'h4']:
                    # 新问题开始
                    if current_question:
                        questions.append(current_question)

                    current_question = {
                        'question': element.get_text(strip=True),
                        'level': element.name,
                        'answer': []
                    }
                elif current_question:
                    # 添加答案内容
                    text = element.get_text(strip=True)
                    if text:
                        current_question['answer'].append(text)

            if current_question:
                questions.append(current_question)

            return questions
        return []

    def crawl_main_page(self, url=None):
        """爬取主页面"""
        if url is None:
            url = self.base_url + "/docs/base.html"

        print(f"正在爬取主页面... {url}")
        html = self.get_page(url)

        if html:
            # 保存原始HTML
            with open('raw_html.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print("原始HTML已保存到 raw_html.html")

            # 解析侧边栏
            categories = self.parse_sidebar(html)
            print(f"找到 {len(categories)} 个分类")

            # 解析内容
            questions = self.parse_content(html)
            print(f"找到 {len(questions)} 个问题")

            return {
                'categories': categories,
                'questions': questions
            }
        return None

    def crawl_all_categories(self, categories):
        """爬取所有分类的内容"""
        all_data = {}

        for i, category in enumerate(categories):
            print(f"\n正在爬取 [{i+1}/{len(categories)}]: {category['title']}")
            print(f"URL: {category['url']}")

            html = self.get_page(category['url'])
            if html:
                questions = self.parse_content(html)
                all_data[category['title']] = {
                    'url': category['url'],
                    'questions': questions
                }
                print(f"  找到 {len(questions)} 个问题")

            time.sleep(1)  # 避免请求过快

        return all_data

    def save_to_json(self, data, filename='interview_questions.json'):
        """保存到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, ensure_ascii=False, indent=2, fp=f)
        print(f"\n数据已保存到 {filename}")

    def save_to_markdown(self, data, filename='interview_questions.md'):
        """保存到Markdown文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# 面试题汇总\n\n")

            for category, content in data.items():
                f.write(f"## {category}\n\n")

                if isinstance(content, dict) and 'questions' in content:
                    for q in content['questions']:
                        f.write(f"### {q['question']}\n\n")
                        for answer in q['answer']:
                            f.write(f"{answer}\n\n")
                        f.write("---\n\n")
                else:
                    # 主页面的直接问题列表
                    for q in content:
                        f.write(f"### {q['question']}\n\n")
                        for answer in q['answer']:
                            f.write(f"{answer}\n\n")
                        f.write("---\n\n")

        print(f"数据已保存到 {filename}")

    def run(self, url=None, crawl_all=True):
        """运行爬虫"""
        print("=" * 50)
        print("面试题网站爬虫启动")
        print("=" * 50)

        # 爬取主页面
        if url is None:
            url = self.base_url + "/docs/base.html"

        print(f"正在爬取: {url}")
        main_data = self.crawl_main_page(url)

        if main_data:
            # 保存主页面数据
            self.save_to_json({'main_page': main_data}, 'main_page.json')

            if crawl_all and main_data['categories']:
                # 爬取所有分类
                print("\n" + "=" * 50)
                print("开始爬取所有分类")
                print("=" * 50)

                all_data = self.crawl_all_categories(main_data['categories'])

                # 合并并保存所有数据
                result = {
                    'main_page': main_data,
                    'categories': all_data
                }
                self.save_to_json(result, 'all_interview_questions.json')
                self.save_to_markdown(all_data, 'all_interview_questions.md')

                print("\n" + "=" * 50)
                print("爬取完成!")
                print("=" * 50)
                print(f"总共爬取了 {len(main_data['categories'])} 个分类")
                print(f"数据已保存到:")
                print("  - all_interview_questions.json")
                print("  - all_interview_questions.md")
        else:
            print("爬取失败，无法获取主页面内容")


if __name__ == "__main__":
    crawler = InterviewCrawler()
    crawler.run(crawl_all=True)