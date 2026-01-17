import base64
from pathlib import Path


def image_to_base64(image_path):
    """
    将图片文件转换为base64编码字符串

    参数:
        image_path: 图片文件路径

    返回:
        base64编码的字符串
    """
    try:
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return encoded_string.decode('utf-8')
    except FileNotFoundError:
        print(f"错误: 找不到文件 {image_path}")
        return None
    except Exception as e:
        print(f"错误: {e}")
        return None


def image_to_base64_with_prefix(image_path):
    """
    将图片转换为带data URI前缀的base64字符串(可直接用于HTML/CSS)

    参数:
        image_path: 图片文件路径

    返回:
        带data URI前缀的base64字符串
    """
    # 获取文件扩展名以确定MIME类型
    suffix = Path(image_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.webp': 'image/webp',
        '.svg': 'image/svg+xml'
    }

    mime_type = mime_types.get(suffix, 'image/jpeg')

    base64_string = image_to_base64(image_path)
    if base64_string:
        return f"data:{mime_type};base64,{base64_string}"
    return None


def save_base64_to_file(image_path, output_path):
    """
    将图片转换为base64并保存到文本文件

    参数:
        image_path: 图片文件路径
        output_path: 输出文本文件路径
    """
    base64_string = image_to_base64(image_path)
    if base64_string:
        with open(output_path, 'w') as f:
            f.write(base64_string)
        print(f"Base64字符串已保存到: {output_path}")


def base64_to_image(base64_string, output_path):
    """
    将base64字符串转换回图片文件

    参数:
        base64_string: base64编码的字符串
        output_path: 输出图片文件路径
    """
    try:
        # 如果包含data URI前缀,先去除
        if base64_string.startswith('data:'):
            base64_string = base64_string.split(',')[1]

        image_data = base64.b64decode(base64_string)
        with open(output_path, 'wb') as f:
            f.write(image_data)
        print(f"图片已保存到: {output_path}")
    except Exception as e:
        print(f"错误: {e}")


# 使用示例
if __name__ == "__main__":
    # 示例1: 基本转换
    image_path = "/Users/okonma/Downloads/skirt.png"  # 替换为你的图片路径
    base64_str = image_to_base64(image_path)
    if base64_str:
        print("Base64字符串(前100字符):")
        print(base64_str[:100] + "...")

    # 示例2: 转换为带前缀的格式(适用于HTML)
    data_uri = image_to_base64_with_prefix(image_path)
    if data_uri:
        print("\nData URI格式(前100字符):")
        print(data_uri[:100] + "...")

    # 示例3: 保存到文件
    save_base64_to_file(image_path, "output_base64.txt")

    # # 示例4: base64转回图片
    # if base64_str:
    #     base64_to_image(base64_str, "restored_image.jpg")