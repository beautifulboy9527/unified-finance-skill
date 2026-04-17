---
name: pypi-release-skill
description: |
  PyPI发布自动化 - 标准化发布流程
  
  功能:
  - 版本号同步检查
  - Git提交和推送
  - GitHub Release创建
  - PyPI构建和发布
  - 发布后验证
  
  触发: 发布新版本、PyPI发布、版本更新
metadata:
  openclaw:
    emoji: "📦"
    triggers:
      - "发布"
      - "PyPI"
      - "release"
      - "版本更新"
      - "发包"
    inputs:
      version:
        type: string
        description: 新版本号 (如 4.5.0)
        required: true
      release_notes:
        type: string
        description: 发布说明
        required: false
---

# PyPI Release Skill - 发布自动化

## 标准发布流程

### P0: 发布前检查

```bash
# 1. 检查版本号一致性
grep -E "version.*=.*['\"]" setup.py pyproject.toml README.md

# 2. 检查Git状态
git status --short

# 3. 运行测试
python -m pytest tests/ -v
```

### P1: Git提交和推送

```bash
# 1. 提交所有更改
git add .
git commit -m "release: v{VERSION} - {RELEASE_NOTES}"

# 2. 推送到GitHub
git push origin master

# 3. 创建Tag
git tag -a v{VERSION} -m "Release v{VERSION}"
git push origin v{VERSION}
```

### P2: PyPI发布

```bash
# 1. 安装工具
python -m pip install --upgrade pip build twine

# 2. 清理旧构建
rm -rf build dist *.egg-info

# 3. 构建
python -m build

# 4. 检查
python -m twine check dist/*

# 5. 上传到PyPI
python -m twine upload dist/*
```

### P3: GitHub Release

```bash
# 创建GitHub Release
gh release create v{VERSION} \
  --title "v{VERSION} - {TITLE}" \
  --notes-file RELEASE_NOTES.md
```

### P4: 发布后验证

```bash
# 1. 等待PyPI同步 (2-5分钟)
sleep 300

# 2. 验证安装
pip install --upgrade {PACKAGE_NAME}
pip show {PACKAGE_NAME}

# 3. 测试CLI
{CLI_COMMAND} --version
```

## 常见问题

### 1. 版本号不一致

**问题**: setup.py、pyproject.toml、README.md版本号不一致

**解决**:
```bash
# 统一更新版本号
sed -i 's/version=".*"/version="{VERSION}"/' setup.py
sed -i 's/version = ".*"/version = "{VERSION}"/' pyproject.toml
```

### 2. Windows编码问题

**问题**: twine上传时遇到GBK编码错误

**解决**:
```python
# 使用Python调用，设置UTF-8编码
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
import subprocess
subprocess.run(['twine', 'upload', 'dist/*'], check=True)
```

### 3. CLI入口点错误

**问题**: ModuleNotFoundError

**解决**:
```python
# setup.py正确配置
entry_points={
    "console_scripts": [
        "neo-finance=neo9527_finance_skill:main",
    ],
}

# 创建包入口文件
# neo9527_finance_skill/__init__.py
def main():
    from scripts.finance import main as cli_main
    cli_main()
```

### 4. PyPI Token配置

**问题**: 需要API Token

**解决**:
```bash
# 创建 ~/.pypirc
[pypi]
username = __token__
password = pypi-{YOUR_TOKEN}
```

## 发布检查清单

### 发布前 ✅

- [ ] 更新版本号 (setup.py, pyproject.toml, README.md)
- [ ] 更新更新日志
- [ ] 运行测试
- [ ] 检查依赖
- [ ] 更新文档

### 发布中 ✅

- [ ] Git提交
- [ ] Git推送
- [ ] 创建Tag
- [ ] 构建包
- [ ] 检查包
- [ ] 上传PyPI
- [ ] 创建GitHub Release

### 发布后 ✅

- [ ] 验证PyPI安装
- [ ] 测试CLI命令
- [ ] 更新文档链接
- [ ] 发布公告

## 自动化脚本

```python
#!/usr/bin/env python3
"""
自动化发布脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def release(version: str, notes: str):
    """执行完整发布流程"""
    
    # P0: 检查
    print(f"📦 开始发布 v{version}")
    check_version_consistency(version)
    
    # P1: Git
    git_commit_and_push(version, notes)
    
    # P2: PyPI
    build_and_upload()
    
    # P3: GitHub Release
    create_github_release(version, notes)
    
    # P4: 验证
    verify_release(version)
    
    print(f"✅ 发布完成！")

def check_version_consistency(version: str):
    """检查版本号一致性"""
    files = ['setup.py', 'pyproject.toml']
    for file in files:
        with open(file) as f:
            content = f.read()
            if f'version="{version}"' not in content and f'version = "{version}"' not in content:
                raise Exception(f"版本号不一致: {file}")

def git_commit_and_push(version: str, notes: str):
    """Git提交和推送"""
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', f'release: v{version} - {notes}'], check=True)
    subprocess.run(['git', 'push', 'origin', 'master'], check=True)
    subprocess.run(['git', 'tag', '-a', f'v{version}', '-m', f'Release v{version}'], check=True)
    subprocess.run(['git', 'push', 'origin', f'v{version}'], check=True)

def build_and_upload():
    """构建并上传PyPI"""
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # 清理
    Path('build').exists() and subprocess.run(['rm', '-rf', 'build'], check=True)
    Path('dist').exists() and subprocess.run(['rm', '-rf', 'dist'], check=True)
    
    # 构建
    subprocess.run(['python', '-m', 'build'], check=True)
    
    # 检查
    subprocess.run(['python', '-m', 'twine', 'check', 'dist/*'], check=True)
    
    # 上传
    subprocess.run(['python', '-m', 'twine', 'upload', 'dist/*'], check=True)

def create_github_release(version: str, notes: str):
    """创建GitHub Release"""
    subprocess.run([
        'gh', 'release', 'create', f'v{version}',
        '--title', f'v{version} - {notes}',
        '--notes-file', 'RELEASE_NOTES.md'
    ], check=True)

def verify_release(version: str):
    """验证发布"""
    import time
    print("⏳ 等待PyPI同步...")
    time.sleep(300)  # 等待5分钟
    
    subprocess.run(['pip', 'install', '--upgrade', 'neo9527-finance-skill'], check=True)
    result = subprocess.run(['pip', 'show', 'neo9527-finance-skill'], capture_output=True, text=True)
    
    if f'Version: {version}' in result.stdout:
        print(f"✅ PyPI发布成功: v{version}")
    else:
        raise Exception("PyPI版本验证失败")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python release.py <version> <notes>")
        sys.exit(1)
    
    release(sys.argv[1], sys.argv[2])
```

## 经验总结

### 成功要素

1. **版本号统一** - 确保所有文件版本号一致
2. **编码处理** - Windows环境设置UTF-8编码
3. **CLI入口** - 正确配置entry_points
4. **Token配置** - 提前配置PyPI Token
5. **分步验证** - 每步都验证成功再继续

### 避免的坑

1. ❌ 版本号不一致导致用户困惑
2. ❌ Windows编码问题导致上传失败
3. ❌ CLI入口点配置错误
4. ❌ 忘记创建GitHub Release
5. ❌ 发布后未验证

---

*下次发布时，直接使用此Skill标准化流程！* 📦
