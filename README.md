# NovelCC: 批量繁简转换脚本

批量将繁体直排epub小说转换为简体横排

## Environment

需要opencc库

```bash
pip install opencc
```

## Usage

```bash
python main.py --folder folder_to_your_files --temp_folder temp_folder
```

- `--folder`: 待转换文件的文件夹，递归遍历所有子文件夹，只处理epub文件，默认为`./novel`
- `--temp_folder`: 解压缩使用的临时文件夹，默认为`./temp`
