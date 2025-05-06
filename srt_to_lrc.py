import re
import sys

def convert_time(srt_time):
    """将SRT时间格式转换为LRC时间格式"""
    match = re.match(r'(\d+):(\d+):(\d+),(\d+)', srt_time)
    if not match:
        return None
    h, m, s, ms = match.groups()
    total_min = int(h) * 60 + int(m)
    return f"{total_min:02}:{s}.{ms[:2]}"

def srt_to_lrc(srt_content):
    """核心转换函数"""
    blocks = srt_content.strip().split('\n\n')
    lrc_lines = []
    
    for block in blocks:
        lines = block.split('\n')
        if len(lines) < 3:
            continue  # 跳过无效块
        
        # 解析时间轴
        try:
            time_line = lines[1]
            start_time_str = time_line.split(' --> ')[0].strip()
            lrc_time = convert_time(start_time_str)
        except:
            continue  # 时间格式错误时跳过
        
        # 提取双语文本
        text_lines = [line.strip() for line in lines[2:] if line.strip()]
        
        # 生成LRC格式
        for text in text_lines[:2]:  # 每个时间点最多两行
            lrc_lines.append(f"[{lrc_time}] {text}")
    
    return '\n'.join(lrc_lines)

def main():
    if len(sys.argv) != 3:
        print("用法：python srt_to_lrc.py 输入文件.srt 输出文件.lrc")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        srt_content = f.read()
    
    lrc_content = srt_to_lrc(srt_content)
    
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        f.write(lrc_content)

if __name__ == "__main__":
    main()