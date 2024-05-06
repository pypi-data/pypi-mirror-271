import paramiko
from typing import cast


class SSHConnection:
    # 初始化连接创建Transport通道
    def __init__(self, host='127.0.0.1', port=22, user='root', pwd='root'):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.__transport = paramiko.Transport((self.host, self.port))
        self.__transport.connect(username=self.user, password=self.pwd)
        self.sftp = cast(paramiko.SFTPClient, paramiko.SFTPClient.from_transport(self.__transport))

    # 关闭通道
    def close(self):
        self.sftp.close()
        self.__transport.close()

    # 上传文件到远程主机
    def upload(self, local_path, remote_path):
        _ = self.sftp.put(local_path, remote_path)
        return _

    # 从远程主机下载文件到本地
    def download(self, local_path, remote_path):
        self.sftp.get(remote_path, local_path)

    # 在远程主机上创建目录
    def mkdir(self, target_path, mode=777):
        self.sftp.mkdir(target_path, mode)

    # 删除远程主机上的目录
    def rmdir(self, target_path):
        self.sftp.rmdir(target_path)

    # 查看目录下文件以及子目录（如果需要更加细粒度的文件信息建议使用listdir_attr）
    def listdir(self, target_path):
        return self.sftp.listdir(target_path)

    # 删除文件
    def remove(self, target_path):
        self.sftp.remove(target_path)

    # 查看目录下文件以及子目录的详细信息（包含内容和参考os.stat返回一个FSTPAttributes对象，对象的具体属性请用__dict__查看）
    def listdirattr(self, target_path):
        list = []
        try:
            list = self.sftp.listdir_attr(target_path)
        except BaseException as e:
            print(e)

        return list

    # 获取文件详情
    def stat(self, remote_path):
        return self.sftp.stat(remote_path)

    # SSHClient输入命令远程操作主机
    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh._transport = self.__transport  # type:ignore
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read()
        print(result)
        return result
