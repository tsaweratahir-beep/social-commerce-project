from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import random

app = Flask(__name__, static_folder='.')
CORS(app)

# ==================== PRODUCT IMAGES MAPPING ====================
product_images = {
    # Beauty Products
    'mac matte lipstick': 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=300',
    'mac ruby woo': 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=300',
    'estee lauder foundation': 'https://images.unsplash.com/photo-1631730359585-38a4935cbec4?w=300',
    'channel no.5 perfume': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=300',
    'dior sauvage': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=300',
    'olay face cream': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300',
    'dyson hair dryer': 'https://images.unsplash.com/photo-1522338140262-f46f5913618a?w=300',
    'dyson airwrap': 'https://images.unsplash.com/photo-1522338140262-f46f5913618a?w=300',
    'opi nail polish': 'https://images.unsplash.com/photo-1583241802345-08fe1940a1f4?w=300',
    'dove shampoo': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=300',
    'pantene conditioner': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=300',
    'neutrogena sunscreen': 'https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8?w=300',
    'lakme sunscreen': 'https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8?w=300',
    'cetaphil moisturizer': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=300',
    'the ordinary serum': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=300',
    'mamaearth face wash': 'https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8?w=300',
    'himalaya face wash': 'https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8?w=300',
    'lakme eyeliner': 'https://images.unsplash.com/photo-1512496015851-a90fb38f96e5?w=300',
    'maybelline mascara': 'https://images.unsplash.com/photo-1512496015851-a90fb38f96e5?w=300',
    'fenty lip gloss': 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=300',
    'biotique face pack': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=300',
    'lotus face cream': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300',
    'nykaa nail paint': 'https://images.unsplash.com/photo-1583241802345-08fe1940a1f4?w=300',
    'philips hair straightener': 'https://images.unsplash.com/photo-1522338140262-f46f5913618a?w=300',
    'nivea moisturizer': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=300',
    
    # Electronics
    'iphone 15 pro': 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=300',
    'iphone 15 plus': 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=300',
    'samsung galaxy s24 ultra': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=300',
    'samsung galaxy s24': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=300',
    'macbook pro m3': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300',
    'macbook air m2': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300',
    'ipad pro': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=300',
    'ipad air': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=300',
    'apple watch series 9': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=300',
    'samsung watch 6': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=300',
    'sony wh-1000xm5': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300',
    'airpods pro 2': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=300',
    'google pixel 8 pro': 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=300',
    'oneplus 12': 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=300',
    'dell xps 15': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300',
    'hp spectre': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300',
    'canon eos r5': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=300',
    'nikon z8': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=300',
    'bose qc45': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300',
    'jbl charge 5': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300',
    'xiaomi 14 ultra': 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=300',
    'nothing phone 2': 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=300',
    'realme gt 5': 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=300',
    'motorola edge 40': 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=300',
    'asus rog phone 7': 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=300',
    
    # Clothing
    'nike air max': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300',
    'nike dunk low': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300',
    'adidas ultraboost': 'https://images.unsplash.com/photo-1518002171953-a080ee817e1f?w=300',
    'adidas yeezy': 'https://images.unsplash.com/photo-1518002171953-a080ee817e1f?w=300',
    "levi's 501 jeans": 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=300',
    "levi's jacket": 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=300',
    'puma rs-x': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300',
    'zara blazer': 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=300',
    'h&m slim fit dress': 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=300',
    'gucci gg marmont bag': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=300',
    'louis vuitton belt': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=300',
    'ray-ban aviator': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=300',
    'supreme hoodie': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=300',
    'tommy hilfiger polo': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300',
    'calvin klein jeans': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=300',
    'under armour tee': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300',
    'reebok nano': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300',
    'converse chuck taylor': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300',
    'vans old skool': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300',
    'puma t-shirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300',
    'nike hoodie': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=300',
    'adidas track suit': 'https://images.unsplash.com/photo-1518002171953-a080ee817e1f?w=300',
    'zara trench coat': 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=300',
    'h&m oversized tshirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300',
    'uniqlo sweater': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300',
    
    # Home
    'l-shaped sofa': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=300',
    'sectional sofa': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=300',
    'solid wood dining table': 'https://images.unsplash.com/photo-1577140917170-285929fb55b7?w=300',
    'king size bed': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=300',
    'queen size bed': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=300',
    'led study lamp': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=300',
    'marble coffee table': 'https://images.unsplash.com/photo-1577140917170-285929fb55b7?w=300',
    'wall bookshelf': 'https://images.unsplash.com/photo-1594620302200-7a762244a1db?w=300',
    'microwave oven': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=300',
    'air fryer': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=300',
    'vacuum cleaner': 'https://images.unsplash.com/photo-1558317374-687fb8cf1d65?w=300',
    'robot vacuum': 'https://images.unsplash.com/photo-1558317374-687fb8cf1d65?w=300',
    'air purifier': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=300',
    'water purifier': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=300',
    'refrigerator': 'https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=300',
    'washing machine': 'https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=300',
    'coffee maker': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=300',
    'dishwasher': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=300',
    'office chair': 'https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?w=300',
    'study table': 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=300',
    'recliner sofa': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=300',
    'bookshelf': 'https://images.unsplash.com/photo-1594620302200-7a762244a1db?w=300',
    'coffee table': 'https://images.unsplash.com/photo-1577140917170-285929fb55b7?w=300',
    'dining table': 'https://images.unsplash.com/photo-1577140917170-285929fb55b7?w=300',
    'bed frame': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=300',
    
    # Sports
    'adidas football': 'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=300',
    'nike football': 'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=300',
    'spalding basketball': 'https://images.unsplash.com/photo-1519861155730-0b5fbf0dd889?w=300',
    'wilson tennis racket': 'https://images.unsplash.com/photo-1595435934249-5df7ed86e1f0?w=300',
    'yonex badminton racket': 'https://images.unsplash.com/photo-1613918431704-6e89bdb58ae7?w=300',
    'premium yoga mat': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=300',
    'bowflex dumbbells': 'https://images.unsplash.com/photo-1586401100295-7a8096fd231a?w=300',
    'cycling helmet': 'https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=300',
    'asics running shoes': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300',
    'speedo swim goggles': 'https://images.unsplash.com/photo-1600965962361-9035dbfd1c50?w=300',
    'sg cricket bat': 'https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=300',
    'ceat cricket bat': 'https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=300',
    'fitness tracker': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=300',
    'gym bag': 'https://images.unsplash.com/photo-1552346154-21d32810aba3?w=300',
    'protein powder': 'https://images.unsplash.com/photo-1579722820308-d74e571813a3?w=300',
    'skipping rope': 'https://images.unsplash.com/photo-1601429166535-e9fc6f7aad79?w=300',
    'boxing gloves': 'https://images.unsplash.com/photo-1552074284-5e88ef1aef18?w=300',
    'treadmill': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=300',
    'exercise bike': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=300',
    'water bottle': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300',
    'tennis racket': 'https://images.unsplash.com/photo-1595435934249-5df7ed86e1f0?w=300',
    'badminton racket': 'https://images.unsplash.com/photo-1613918431704-6e89bdb58ae7?w=300',
    'yoga mat': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=300',
    'dumbbells': 'https://images.unsplash.com/photo-1586401100295-7a8096fd231a?w=300',
    'running shoes': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300',
    
    # Toys
    'lego set': 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=300',
    'barbie doll': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=300',
    'hot wheels': 'https://images.unsplash.com/photo-1565814636199-ae8133055c1c?w=300',
    'teddy bear': 'https://images.unsplash.com/photo-1567225557594-88d73e55f2cb?w=300',
    'remote control car': 'https://images.unsplash.com/photo-1565814636199-ae8133055c1c?w=300',
    'action figures': 'https://images.unsplash.com/photo-1622484211976-929c3dac8f95?w=300',
    'board games': 'https://images.unsplash.com/photo-1610890716171-6b1bb98ffb09?w=300',
    'puzzle': 'https://images.unsplash.com/photo-1611996575749-79a3a239f4a9?w=300',
    'play-doh': 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=300',
    'nerf gun': 'https://images.unsplash.com/photo-1565814636199-ae8133055c1c?w=300',
    
    # Books
    'atomic habits': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300',
    'rich dad poor dad': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300',
    'harry potter': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300',
    'the alchemist': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300',
    'psychology of money': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300',
    'think and grow rich': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300',
    'ikigai': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300',
    'sapiens': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300',
    'the hobbit': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300',
    '1984': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300',
    
    # Jewelry
    'diamond ring': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=300',
    'gold necklace': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=300',
    'silver earrings': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=300',
    'bracelet': 'https://images.unsplash.com/photo-1611652022419-a9419f74343d?w=300',
    'pendant': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=300',
    'nose pin': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=300',
    'anklet': 'https://images.unsplash.com/photo-1611652022419-a9419f74343d?w=300',
    'watch': 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=300',
    
    # Footwear
    'leather boots': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=300',
    'sandals': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=300',
    'loafers': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=300',
    'formal shoes': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=300',
    'casual shoes': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300',
    'sports shoes': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300',
    'heels': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=300',
    'flip flops': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=300',
    
    # Bags
    'laptop bag': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=300',
    'backpack': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300',
    'handbag': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=300',
    'travel bag': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300',
    'school bag': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300',
    'wallet': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=300',
    'sling bag': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=300',
    'duffle bag': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300',
    
    # Kids
    'baby dress': 'https://images.unsplash.com/photo-1522771930-78848d9293e8?w=300',
    'kids toys': 'https://images.unsplash.com/photo-1565814636199-ae8133055c1c?w=300',
    'baby stroller': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=300',
    'kids shoes': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300',
    'baby food': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=300',
    'diapers': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=300',
    'kids backpack': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300',
    'baby lotion': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300',
    
    # Pet Supplies
    'dog food': 'https://images.unsplash.com/photo-1568152950566-c1bf43f4ab28?w=300',
    'cat food': 'https://images.unsplash.com/photo-1568152950566-c1bf43f4ab28?w=300',
    'pet bed': 'https://images.unsplash.com/photo-1541599540903-216a46ca1dc0?w=300',
    'pet toys': 'https://images.unsplash.com/photo-1568152950566-c1bf43f4ab28?w=300',
    'leash': 'https://images.unsplash.com/photo-1541599540903-216a46ca1dc0?w=300',
    'pet shampoo': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=300',
    'bird cage': 'https://images.unsplash.com/photo-1541599540903-216a46ca1dc0?w=300',
    'fish tank': 'https://images.unsplash.com/photo-1541599540903-216a46ca1dc0?w=300',
}

def get_product_image(product_name, category):
    """Get relevant image based on product name"""
    product_name_lower = product_name.lower()
    for keyword, image_url in product_images.items():
        if keyword in product_name_lower:
            return image_url
    
    # Category default images
    defaults = {
        'Electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=300',
        'Clothing': 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=300',
        'Home': 'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=300',
        'Beauty': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=300',
        'Sports': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=300',
        'Toys': 'https://images.unsplash.com/photo-1565814636199-ae8133055c1c?w=300',
        'Books': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300',
        'Jewelry': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=300',
        'Footwear': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=300',
        'Bags': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=300',
        'Kids': 'https://images.unsplash.com/photo-1522771930-78848d9293e8?w=300',
        'Pet Supplies': 'https://images.unsplash.com/photo-1541599540903-216a46ca1dc0?w=300'
    }
    return defaults.get(category, 'https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=300')


# ==================== ALL PRODUCTS ====================
all_products = [
    # Electronics (25)
    {'name': 'iPhone 15 Pro', 'category': 'Electronics', 'price': 134900, 'discount': 10},
    {'name': 'iPhone 15 Plus', 'category': 'Electronics', 'price': 89900, 'discount': 8},
    {'name': 'Samsung Galaxy S24 Ultra', 'category': 'Electronics', 'price': 129999, 'discount': 15},
    {'name': 'Samsung Galaxy S24', 'category': 'Electronics', 'price': 79999, 'discount': 10},
    {'name': 'MacBook Pro M3', 'category': 'Electronics', 'price': 199900, 'discount': 5},
    {'name': 'MacBook Air M2', 'category': 'Electronics', 'price': 114900, 'discount': 10},
    {'name': 'iPad Pro 12.9', 'category': 'Electronics', 'price': 99900, 'discount': 8},
    {'name': 'iPad Air', 'category': 'Electronics', 'price': 59900, 'discount': 5},
    {'name': 'Apple Watch Series 9', 'category': 'Electronics', 'price': 41900, 'discount': 12},
    {'name': 'Samsung Watch 6', 'category': 'Electronics', 'price': 29999, 'discount': 15},
    {'name': 'Sony WH-1000XM5', 'category': 'Electronics', 'price': 29990, 'discount': 10},
    {'name': 'AirPods Pro 2', 'category': 'Electronics', 'price': 24900, 'discount': 5},
    {'name': 'Google Pixel 8 Pro', 'category': 'Electronics', 'price': 109999, 'discount': 12},
    {'name': 'OnePlus 12', 'category': 'Electronics', 'price': 64999, 'discount': 8},
    {'name': 'Dell XPS 15', 'category': 'Electronics', 'price': 159900, 'discount': 10},
    {'name': 'HP Spectre', 'category': 'Electronics', 'price': 139900, 'discount': 15},
    {'name': 'Canon EOS R5', 'category': 'Electronics', 'price': 285000, 'discount': 5},
    {'name': 'Nikon Z8', 'category': 'Electronics', 'price': 265000, 'discount': 8},
    {'name': 'Bose QC45', 'category': 'Electronics', 'price': 26990, 'discount': 10},
    {'name': 'JBL Charge 5', 'category': 'Electronics', 'price': 11999, 'discount': 15},
    {'name': 'Xiaomi 14 Ultra', 'category': 'Electronics', 'price': 89999, 'discount': 10},
    {'name': 'Nothing Phone 2', 'category': 'Electronics', 'price': 44999, 'discount': 12},
    {'name': 'Realme GT 5', 'category': 'Electronics', 'price': 39999, 'discount': 15},
    {'name': 'Motorola Edge 40', 'category': 'Electronics', 'price': 34999, 'discount': 10},
    {'name': 'Asus ROG Phone 7', 'category': 'Electronics', 'price': 69999, 'discount': 8},
    
    # Beauty (25)
    {'name': 'MAC Matte Lipstick', 'category': 'Beauty', 'price': 2250, 'discount': 10},
    {'name': 'MAC Ruby Woo', 'category': 'Beauty', 'price': 2250, 'discount': 5},
    {'name': 'Estee Lauder Foundation', 'category': 'Beauty', 'price': 4500, 'discount': 15},
    {'name': 'Channel No.5 Perfume', 'category': 'Beauty', 'price': 12500, 'discount': 10},
    {'name': 'Dior Sauvage', 'category': 'Beauty', 'price': 10500, 'discount': 8},
    {'name': 'Olay Face Cream', 'category': 'Beauty', 'price': 899, 'discount': 20},
    {'name': 'Dyson Hair Dryer', 'category': 'Beauty', 'price': 35900, 'discount': 5},
    {'name': 'Dyson Airwrap', 'category': 'Beauty', 'price': 49900, 'discount': 8},
    {'name': 'OPI Nail Polish', 'category': 'Beauty', 'price': 850, 'discount': 15},
    {'name': 'Dove Shampoo', 'category': 'Beauty', 'price': 450, 'discount': 10},
    {'name': 'Pantene Conditioner', 'category': 'Beauty', 'price': 399, 'discount': 5},
    {'name': 'Neutrogena Sunscreen', 'category': 'Beauty', 'price': 699, 'discount': 20},
    {'name': 'Lakme Sunscreen', 'category': 'Beauty', 'price': 499, 'discount': 15},
    {'name': 'Cetaphil Moisturizer', 'category': 'Beauty', 'price': 899, 'discount': 10},
    {'name': 'The Ordinary Serum', 'category': 'Beauty', 'price': 1450, 'discount': 8},
    {'name': 'Mamaearth Face Wash', 'category': 'Beauty', 'price': 399, 'discount': 20},
    {'name': 'Himalaya Face Wash', 'category': 'Beauty', 'price': 199, 'discount': 10},
    {'name': 'Lakme Eyeliner', 'category': 'Beauty', 'price': 399, 'discount': 15},
    {'name': 'Maybelline Mascara', 'category': 'Beauty', 'price': 499, 'discount': 10},
    {'name': 'Fenty Lip Gloss', 'category': 'Beauty', 'price': 2650, 'discount': 5},
    {'name': 'Biotique Face Pack', 'category': 'Beauty', 'price': 299, 'discount': 15},
    {'name': 'Lotus Face Cream', 'category': 'Beauty', 'price': 599, 'discount': 10},
    {'name': 'Nykaa Nail Paint', 'category': 'Beauty', 'price': 299, 'discount': 20},
    {'name': 'Philips Hair Straightener', 'category': 'Beauty', 'price': 2999, 'discount': 15},
    {'name': 'Nivea Moisturizer', 'category': 'Beauty', 'price': 399, 'discount': 10},
    
    # Clothing (25)
    {'name': 'Nike Air Max Shoes', 'category': 'Clothing', 'price': 11999, 'discount': 15},
    {'name': 'Nike Dunk Low', 'category': 'Clothing', 'price': 9999, 'discount': 10},
    {'name': 'Adidas Ultraboost', 'category': 'Clothing', 'price': 15999, 'discount': 20},
    {'name': 'Adidas Yeezy', 'category': 'Clothing', 'price': 24999, 'discount': 5},
    {'name': "Levi's 501 Jeans", 'category': 'Clothing', 'price': 3999, 'discount': 15},
    {'name': "Levi's Jacket", 'category': 'Clothing', 'price': 5999, 'discount': 10},
    {'name': 'Puma RS-X', 'category': 'Clothing', 'price': 8999, 'discount': 20},
    {'name': 'Zara Blazer', 'category': 'Clothing', 'price': 6999, 'discount': 15},
    {'name': 'H&M Slim Fit Dress', 'category': 'Clothing', 'price': 2999, 'discount': 10},
    {'name': 'Gucci GG Marmont Bag', 'category': 'Clothing', 'price': 125000, 'discount': 5},
    {'name': 'Louis Vuitton Belt', 'category': 'Clothing', 'price': 45000, 'discount': 8},
    {'name': 'Ray-Ban Aviator', 'category': 'Clothing', 'price': 8999, 'discount': 15},
    {'name': 'Supreme Hoodie', 'category': 'Clothing', 'price': 12999, 'discount': 10},
    {'name': 'Tommy Hilfiger Polo', 'category': 'Clothing', 'price': 3999, 'discount': 20},
    {'name': 'Calvin Klein Jeans', 'category': 'Clothing', 'price': 4999, 'discount': 15},
    {'name': 'Under Armour Tee', 'category': 'Clothing', 'price': 1999, 'discount': 10},
    {'name': 'Reebok Nano', 'category': 'Clothing', 'price': 8999, 'discount': 20},
    {'name': 'Converse Chuck Taylor', 'category': 'Clothing', 'price': 4999, 'discount': 10},
    {'name': 'Vans Old Skool', 'category': 'Clothing', 'price': 5999, 'discount': 15},
    {'name': 'Puma T-Shirt', 'category': 'Clothing', 'price': 1499, 'discount': 10},
    {'name': 'Nike Hoodie', 'category': 'Clothing', 'price': 5999, 'discount': 15},
    {'name': 'Adidas Track Suit', 'category': 'Clothing', 'price': 7999, 'discount': 20},
    {'name': 'Zara Trench Coat', 'category': 'Clothing', 'price': 8999, 'discount': 10},
    {'name': 'H&M Oversized Tshirt', 'category': 'Clothing', 'price': 1299, 'discount': 15},
    {'name': 'Uniqlo Sweater', 'category': 'Clothing', 'price': 3499, 'discount': 10},
    
    # Home (25)
    {'name': 'L-Shaped Sofa', 'category': 'Home', 'price': 45999, 'discount': 15},
    {'name': 'Sectional Sofa', 'category': 'Home', 'price': 65999, 'discount': 10},
    {'name': 'Solid Wood Dining Table', 'category': 'Home', 'price': 29999, 'discount': 20},
    {'name': 'King Size Bed', 'category': 'Home', 'price': 39999, 'discount': 15},
    {'name': 'Queen Size Bed', 'category': 'Home', 'price': 29999, 'discount': 10},
    {'name': 'LED Study Lamp', 'category': 'Home', 'price': 1899, 'discount': 20},
    {'name': 'Marble Coffee Table', 'category': 'Home', 'price': 12999, 'discount': 15},
    {'name': 'Wall Bookshelf', 'category': 'Home', 'price': 7999, 'discount': 10},
    {'name': 'Microwave Oven', 'category': 'Home', 'price': 12999, 'discount': 20},
    {'name': 'Air Fryer', 'category': 'Home', 'price': 7999, 'discount': 15},
    {'name': 'Vacuum Cleaner', 'category': 'Home', 'price': 15999, 'discount': 10},
    {'name': 'Robot Vacuum', 'category': 'Home', 'price': 29999, 'discount': 20},
    {'name': 'Air Purifier', 'category': 'Home', 'price': 18999, 'discount': 15},
    {'name': 'Water Purifier', 'category': 'Home', 'price': 11999, 'discount': 10},
    {'name': 'Refrigerator', 'category': 'Home', 'price': 45999, 'discount': 15},
    {'name': 'Washing Machine', 'category': 'Home', 'price': 34999, 'discount': 20},
    {'name': 'Coffee Maker', 'category': 'Home', 'price': 8999, 'discount': 10},
    {'name': 'Dishwasher', 'category': 'Home', 'price': 39999, 'discount': 15},
    {'name': 'Office Chair', 'category': 'Home', 'price': 12999, 'discount': 20},
    {'name': 'Study Table', 'category': 'Home', 'price': 9999, 'discount': 10},
    {'name': 'Recliner Sofa', 'category': 'Home', 'price': 54999, 'discount': 15},
    {'name': 'Bookshelf', 'category': 'Home', 'price': 8999, 'discount': 10},
    {'name': 'Coffee Table', 'category': 'Home', 'price': 14999, 'discount': 20},
    {'name': 'Dining Table', 'category': 'Home', 'price': 24999, 'discount': 15},
    {'name': 'Bed Frame', 'category': 'Home', 'price': 34999, 'discount': 10},
    
    # Sports (25)
    {'name': 'Adidas Football', 'category': 'Sports', 'price': 2499, 'discount': 15},
    {'name': 'Nike Football', 'category': 'Sports', 'price': 2999, 'discount': 10},
    {'name': 'Spalding Basketball', 'category': 'Sports', 'price': 3499, 'discount': 20},
    {'name': 'Wilson Tennis Racket', 'category': 'Sports', 'price': 8999, 'discount': 15},
    {'name': 'Yonex Badminton Racket', 'category': 'Sports', 'price': 5999, 'discount': 10},
    {'name': 'Premium Yoga Mat', 'category': 'Sports', 'price': 1999, 'discount': 20},
    {'name': 'Bowflex Dumbbells', 'category': 'Sports', 'price': 14999, 'discount': 15},
    {'name': 'Cycling Helmet', 'category': 'Sports', 'price': 3499, 'discount': 10},
    {'name': 'ASICS Running Shoes', 'category': 'Sports', 'price': 8999, 'discount': 20},
    {'name': 'Speedo Swim Goggles', 'category': 'Sports', 'price': 1499, 'discount': 15},
    {'name': 'SG Cricket Bat', 'category': 'Sports', 'price': 5999, 'discount': 10},
    {'name': 'CEAT Cricket Bat', 'category': 'Sports', 'price': 4999, 'discount': 15},
    {'name': 'Fitness Tracker', 'category': 'Sports', 'price': 3999, 'discount': 20},
    {'name': 'Gym Bag', 'category': 'Sports', 'price': 1999, 'discount': 10},
    {'name': 'Protein Powder', 'category': 'Sports', 'price': 4499, 'discount': 15},
    {'name': 'Skipping Rope', 'category': 'Sports', 'price': 499, 'discount': 10},
    {'name': 'Boxing Gloves', 'category': 'Sports', 'price': 3999, 'discount': 20},
    {'name': 'Treadmill', 'category': 'Sports', 'price': 45999, 'discount': 15},
    {'name': 'Exercise Bike', 'category': 'Sports', 'price': 29999, 'discount': 20},
    {'name': 'Water Bottle', 'category': 'Sports', 'price': 599, 'discount': 10},
    {'name': 'Tennis Racket', 'category': 'Sports', 'price': 7999, 'discount': 15},
    {'name': 'Badminton Racket', 'category': 'Sports', 'price': 4999, 'discount': 10},
    {'name': 'Yoga Mat', 'category': 'Sports', 'price': 1499, 'discount': 20},
    {'name': 'Dumbbells', 'category': 'Sports', 'price': 12999, 'discount': 15},
    {'name': 'Running Shoes', 'category': 'Sports', 'price': 7999, 'discount': 20},
    
    # Toys (10)
    {'name': 'LEGO Set', 'category': 'Toys', 'price': 4999, 'discount': 15},
    {'name': 'Barbie Doll', 'category': 'Toys', 'price': 1999, 'discount': 10},
    {'name': 'Hot Wheels', 'category': 'Toys', 'price': 999, 'discount': 20},
    {'name': 'Teddy Bear', 'category': 'Toys', 'price': 1499, 'discount': 15},
    {'name': 'Remote Control Car', 'category': 'Toys', 'price': 2999, 'discount': 10},
    {'name': 'Action Figures', 'category': 'Toys', 'price': 2499, 'discount': 20},
    {'name': 'Board Games', 'category': 'Toys', 'price': 1999, 'discount': 15},
    {'name': 'Puzzle', 'category': 'Toys', 'price': 499, 'discount': 10},
    {'name': 'Play-Doh', 'category': 'Toys', 'price': 599, 'discount': 20},
    {'name': 'Nerf Gun', 'category': 'Toys', 'price': 2499, 'discount': 15},
    
    # Books (10)
    {'name': 'Atomic Habits', 'category': 'Books', 'price': 550, 'discount': 15},
    {'name': 'Rich Dad Poor Dad', 'category': 'Books', 'price': 450, 'discount': 10},
    {'name': 'Harry Potter Set', 'category': 'Books', 'price': 3999, 'discount': 20},
    {'name': 'The Alchemist', 'category': 'Books', 'price': 350, 'discount': 15},
    {'name': 'Psychology of Money', 'category': 'Books', 'price': 499, 'discount': 10},
    {'name': 'Think and Grow Rich', 'category': 'Books', 'price': 399, 'discount': 20},
    {'name': 'Ikigai', 'category': 'Books', 'price': 450, 'discount': 15},
    {'name': 'Sapiens', 'category': 'Books', 'price': 599, 'discount': 10},
    {'name': 'The Hobbit', 'category': 'Books', 'price': 499, 'discount': 20},
    {'name': '1984', 'category': 'Books', 'price': 350, 'discount': 15},
    
    # Jewelry (8)
    {'name': 'Diamond Ring', 'category': 'Jewelry', 'price': 49999, 'discount': 10},
    {'name': 'Gold Necklace', 'category': 'Jewelry', 'price': 35999, 'discount': 15},
    {'name': 'Silver Earrings', 'category': 'Jewelry', 'price': 4999, 'discount': 20},
    {'name': 'Bracelet', 'category': 'Jewelry', 'price': 2999, 'discount': 10},
    {'name': 'Pendant', 'category': 'Jewelry', 'price': 3999, 'discount': 15},
    {'name': 'Nose Pin', 'category': 'Jewelry', 'price': 1999, 'discount': 20},
    {'name': 'Anklet', 'category': 'Jewelry', 'price': 1499, 'discount': 10},
    {'name': 'Watch', 'category': 'Jewelry', 'price': 19999, 'discount': 15},
    
    # Footwear (8)
    {'name': 'Leather Boots', 'category': 'Footwear', 'price': 5999, 'discount': 15},
    {'name': 'Sandals', 'category': 'Footwear', 'price': 1999, 'discount': 10},
    {'name': 'Loafers', 'category': 'Footwear', 'price': 3999, 'discount': 20},
    {'name': 'Formal Shoes', 'category': 'Footwear', 'price': 4999, 'discount': 15},
    {'name': 'Casual Shoes', 'category': 'Footwear', 'price': 3499, 'discount': 10},
    {'name': 'Sports Shoes', 'category': 'Footwear', 'price': 7999, 'discount': 20},
    {'name': 'Heels', 'category': 'Footwear', 'price': 2999, 'discount': 15},
    {'name': 'Flip Flops', 'category': 'Footwear', 'price': 599, 'discount': 10},
    
    # Bags (8)
    {'name': 'Laptop Bag', 'category': 'Bags', 'price': 2499, 'discount': 15},
    {'name': 'Backpack', 'category': 'Bags', 'price': 2999, 'discount': 10},
    {'name': 'Handbag', 'category': 'Bags', 'price': 3999, 'discount': 20},
    {'name': 'Travel Bag', 'category': 'Bags', 'price': 4999, 'discount': 15},
    {'name': 'School Bag', 'category': 'Bags', 'price': 1499, 'discount': 10},
    {'name': 'Wallet', 'category': 'Bags', 'price': 999, 'discount': 20},
    {'name': 'Sling Bag', 'category': 'Bags', 'price': 1999, 'discount': 15},
    {'name': 'Duffle Bag', 'category': 'Bags', 'price': 3999, 'discount': 10},
    
    # Kids (8)
    {'name': 'Baby Dress', 'category': 'Kids', 'price': 899, 'discount': 15},
    {'name': 'Kids Toys', 'category': 'Kids', 'price': 1499, 'discount': 10},
    {'name': 'Baby Stroller', 'category': 'Kids', 'price': 12999, 'discount': 20},
    {'name': 'Kids Shoes', 'category': 'Kids', 'price': 1999, 'discount': 15},
    {'name': 'Baby Food', 'category': 'Kids', 'price': 299, 'discount': 10},
    {'name': 'Diapers', 'category': 'Kids', 'price': 899, 'discount': 20},
    {'name': 'Kids Backpack', 'category': 'Kids', 'price': 1299, 'discount': 15},
    {'name': 'Baby Lotion', 'category': 'Kids', 'price': 399, 'discount': 10},
    
    # Pet Supplies (8)
    {'name': 'Dog Food', 'category': 'Pet Supplies', 'price': 1499, 'discount': 15},
    {'name': 'Cat Food', 'category': 'Pet Supplies', 'price': 1299, 'discount': 10},
    {'name': 'Pet Bed', 'category': 'Pet Supplies', 'price': 2499, 'discount': 20},
    {'name': 'Pet Toys', 'category': 'Pet Supplies', 'price': 599, 'discount': 15},
    {'name': 'Leash', 'category': 'Pet Supplies', 'price': 499, 'discount': 10},
    {'name': 'Pet Shampoo', 'category': 'Pet Supplies', 'price': 399, 'discount': 20},
    {'name': 'Bird Cage', 'category': 'Pet Supplies', 'price': 3999, 'discount': 15},
    {'name': 'Fish Tank', 'category': 'Pet Supplies', 'price': 4999, 'discount': 10},
]

# Create final dataframe
products = []
product_id = 1

for item in all_products:
    name = item['name']
    cat = item['category']
    price = item['price']
    discount = item['discount']
    disc_price = price * (1 - discount/100)
    rating = round(random.uniform(3.5, 5.0), 1)
    sold = random.randint(50, 5000)
    
    image_url = get_product_image(name, cat)
    
    products.append({
        'product_id': f'P{product_id:04d}',
        'product_name': name,
        'product_category': cat,
        'price': price,
        'discount_percent': discount,
        'discounted_price': round(disc_price, 2),
        'rating': rating,
        'quantity_sold': sold,
        'image_url': image_url
    })
    product_id += 1

df = pd.DataFrame(products)
print("="*60)
print(f"✅ Loaded {len(df)} products")
print(f"📂 Total Categories: {df['product_category'].nunique()}")
print("\n📊 Products per category:")
for cat in sorted(df['product_category'].unique()):
    count = len(df[df['product_category'] == cat])
    print(f"   • {cat}: {count} products")
print("="*60)

# ==================== API ROUTES ====================
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

@app.route('/script.js')
def js():
    return send_from_directory('.', 'script.js')

@app.route('/api/trending')
def trending():
    df['score'] = df['rating'] * 0.4 + (df['quantity_sold'] / df['quantity_sold'].max()) * 0.6
    data = df.nlargest(12, 'score').to_dict('records')
    return jsonify({'success': True, 'data': data})

@app.route('/api/popular')
def popular():
    data = df.nlargest(12, 'quantity_sold').to_dict('records')
    return jsonify({'success': True, 'data': data})

@app.route('/api/categories')
def categories_list():
    cats = df['product_category'].unique().tolist()
    return jsonify({'success': True, 'data': cats})

@app.route('/api/category/<cat>')
def category_products(cat):
    data = df[df['product_category'] == cat].nlargest(12, 'rating').to_dict('records')
    return jsonify({'success': True, 'data': data})

@app.route('/api/search')
def search():
    q = request.args.get('q', '').lower()
    if not q:
        return jsonify({'success': True, 'data': []})
    results = df[df['product_name'].str.lower().str.contains(q, na=False)].head(20).to_dict('records')
    return jsonify({'success': True, 'data': results})

@app.route('/api/recommendations/<pid>')
def recommendations(pid):
    product = df[df['product_id'] == pid]
    if len(product) > 0:
        cat = product.iloc[0]['product_category']
        recs = df[df['product_category'] == cat].head(12).to_dict('records')
    else:
        recs = df.head(12).to_dict('records')
    return jsonify({'success': True, 'data': recs})

if __name__ == '__main__':
    print("\n🚀 SERVER RUNNING on http://localhost:5000")
    print("="*60)
    app.run(debug=True, port=5000)