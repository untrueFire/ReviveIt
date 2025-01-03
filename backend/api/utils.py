import hashlib

from PIL import Image, ImageDraw, ImageFont


def generate_color_from_hash(input_string):
    """根据字符串哈希生成 RGB 颜色

    Args:
        input_string (str): 输入字符串

    Returns:
        tuple[int, int, int]: 返回一个 RGB 颜色元组
    """    
    # 使用 SHA-256 哈希算法生成哈希值
    hash_object = hashlib.sha256(input_string.encode())
    hex_dig = hash_object.hexdigest()  # 获取十六进制哈希值

    # 从哈希值中提取 RGB 颜色
    red = int(hex_dig[0:2], 16)   # 取前 2 个字符作为红色分量
    green = int(hex_dig[2:4], 16) # 取接下来 2 个字符作为绿色分量
    blue = int(hex_dig[4:6], 16)  # 取接下来 2 个字符作为蓝色分量

    return (red, green, blue)


def generate_avatar(username: str, size=50):
    """
    根据用户名生成用户头像
    
    生成的图片保存在 `files/{username}_avatar.png`
    
    Args:
        username (str): 用户名
        size (int, optional): 图像尺寸，默认为 50.
    """    
    # 获取首字母
    first_letter = username[0]

    # 根据用户名生成背景颜色
    bg_color = generate_color_from_hash(username)

    # 创建画布
    image = Image.new("RGB", (size, size), bg_color)
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default(size=size*0.6)

    # 绘制文字
    draw.text((size // 2, size // 2), first_letter, font=font, fill=(255, 255, 255), anchor="mm")

    # 保存图片
    image.save(f"files/{username}_avatar.png")