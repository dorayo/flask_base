import os
from datetime import datetime

def get_storage_path(filename: str) -> str:
    # 获取文件扩展名
    file_extension = os.path.splitext(filename)[1].lower()
    
    # 定义文件类型和对应的文件夹名称
    file_type_map = {
        '.jpg': 'image',
        '.jpeg': 'image',
        '.png': 'image',
        '.gif': 'image',
        '.bmp': 'image',
        '.mp4': 'video',
        '.avi': 'video',
        '.mkv': 'video',
        '.mov': 'video',
        '.mp3': 'audio',
        '.wav': 'audio',
        '.flac': 'audio',
        '.txt': 'document',
        '.pdf': 'document',
        '.doc': 'document',
        '.docx': 'document',
        '.xlsx': 'document',
        '.csv': 'document'
    }
    
    # 根据扩展名确定文件类型文件夹
    file_type_folder = file_type_map.get(file_extension, 'others')
    
    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # 生成存储路径
    storage_path = f"{file_type_folder}/{current_date}/{filename}"
    
    return storage_path
