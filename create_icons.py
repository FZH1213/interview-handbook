#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建tabBar图标
"""

from PIL import Image, ImageDraw

def create_icon(filename, color, size=81):
    """创建简单的圆形图标"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 绘制圆角矩形背景
    margin = 5
    draw.rounded_rectangle(
        [margin, margin, size-margin-1, size-margin-1],
        radius=20,
        fill=color
    )

    return img

# 创建基础题图标（蓝色）
basic_normal = create_icon('basic.png', '#999999')
basic_active = create_icon('basic-active.png', '#4A90D9')

# 创建进阶题图标（红色）
advanced_normal = create_icon('advanced.png', '#999999')
advanced_active = create_icon('advanced-active.png', '#e64340')

# 保存图标
basic_normal.save('miniprogram/assets/basic.png')
basic_active.save('miniprogram/assets/basic-active.png')
advanced_normal.save('miniprogram/assets/advanced.png')
advanced_active.save('miniprogram/assets/advanced-active.png')

print("✅ 图标创建完成！")