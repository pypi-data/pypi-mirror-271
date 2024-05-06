import rarfile

def uncompress(src_file, dest_dir):
    """解压各种类型的压缩包

    :param src_file: 你要解压的压缩包文件
    :type src_file: file
    :param dest_dir: 你要解压到的目标路径
    :type dest_dir: str
    """

    # 需要安装rar包：pip install rarfile
    rar = rarfile.RarFile(src_file)
    rar.extractall(dest_dir)
    rar.close()
