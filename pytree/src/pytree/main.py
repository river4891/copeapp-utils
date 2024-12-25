import argparse
from pathlib import Path

def format_size(size):
    """格式化文件大小为可读的字符串"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"

def load_ignore_patterns(ignore_file):
    """加载忽略文件中的模式"""
    if not ignore_file.exists():
        return []
    with ignore_file.open() as f:
        patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return patterns

def is_ignored(path, patterns, root):
    """判断文件是否匹配忽略模式"""
    relative_path = path.relative_to(root)
    for pattern in patterns:
        if relative_path.match(pattern):
            return True
    return False

def print_tree(startpath, prefix='', level=0, max_level=None, patterns=None):
    if max_level is not None and level > max_level:
        return

    path = Path(startpath)
    contents = sorted(path.iterdir(), key=lambda p: p.name.lower())
    for index, item in enumerate(contents):
        # 跳过忽略的文件和目录
        if patterns and is_ignored(item, patterns, path):
            continue
        
        is_last = index == len(contents) - 1
        connector = '└── ' if is_last else '├── '
        if item.is_file():
            size = format_size(item.stat().st_size)
            print(f"{prefix}{connector}{item.name} ({size})")
        else:
            print(f"{prefix}{connector}{item.name}/")
            extension = '    ' if is_last else '│   '
            print_tree(item, prefix + extension, level + 1, max_level, patterns)

def cli():
    parser = argparse.ArgumentParser(description="Display directory tree structure")
    parser.add_argument('directory', type=str, nargs='?', default='.', help="Directory to list")
    parser.add_argument('-L', '--level', type=int, default=None, help="Level depth of the tree")
    parser.add_argument('--ignore', type=str, nargs='?', default='.gitignore', help="Ignore file to use (default: .gitignore)")

    args = parser.parse_args()

    ignore_file_path = Path(args.directory) / args.ignore
    patterns = load_ignore_patterns(ignore_file_path)

    print_tree(args.directory, max_level=args.level, patterns=patterns)

def main():
    cli()

if __name__ == "__main__":
    main()