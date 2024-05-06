from __future__ import annotations

from dknovautils.commons import *

import pathlib


_debug = False


class DkFile(object):
    def __init__(self, pathstr: str) -> None:
        self.pathstr = str(pathstr)

        self.path = Path(pathstr)

    def __key(self) -> Any:
        return self.path

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other: Any) -> Any:
        if isinstance(other, DkFile):
            return self.__key() == other.__key()
        return NotImplemented

    @property
    def basename(self) -> str:
        return os.path.basename(self.path)

    @property
    def filesize(self) -> int:
        return getsize(self.path)

    @property
    def dirname(self) -> str:
        return os.path.dirname(self.path)

    @property
    def extension(self) -> str:
        """包括点号 比如 .txt 如果没有扩展名 则返回空串"""
        # function to return the file extension
        file_extension = self.path.suffix
        return file_extension

    def exists(self) -> bool:
        return self.path.exists()

    def is_file(self) -> bool:
        return self.path.is_file()

    def is_dir(self) -> bool:
        return self.path.is_dir()

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return str(self.path)

    @staticmethod
    def clear_dir(folder: str) -> None:
        """

        https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder

        """
        import os, shutil

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                iprint("Failed to delete %s. Reason: %s" % (file_path, e))

    @staticmethod
    def file_md5(f: str, md5Cache: Dict[str, str] | None = None) -> str:
        # todo 更换为合理的计算方式

        if md5Cache is None:
            md5Cache = {}

        if f in md5Cache:
            r = md5Cache[f]
            assert len(r) == 32
            return r
        else:
            iprint_debug(f"gen md5 {f}")
            bs = Path(f).read_bytes()
            md5 = hashlib.md5()
            # md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
            md5.update(bs)
            r = md5.hexdigest().lower()
            assert len(r) == 32

            md5Cache[f] = r
            return r

    @staticmethod
    def listdir(d: str) -> List[DkFile]:
        fs = [DkFile(join(d, f)) for f in os.listdir(d)]
        # fs=[DkFile(f) for f in fs]
        return fs

    @staticmethod
    def file_sha1(f: str) -> str:
        import hashlib

        bs = Path(f).read_bytes()
        md5 = hashlib.sha1()
        # md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
        md5.update(bs)
        r = md5.hexdigest().lower()
        assert len(r) == 32
        return r

    @staticmethod
    def fill_disk_simple(
        *,
        dir: str = ".",
        verify: bool = True,
        size: int = 1024 * 1024 * 100,
        pre: str = "tmp",
        verbose: bool = False,
    ) -> None:
        import numpy as np

        """
        在目录下创建文件. 文件大小约为10M. 创建之后马上读出检查内容是否正确. 用来对硬盘进行简单的检查.
        直到写满磁盘为止, [Errno 28] No space left on device 最后退出.
        
        mkdir tmp
        python3.10 -c "from dknovautils import *; DkFile.fill_disk_simple(dir='./tmp',verify=True,verbose=True)" |& tee -a ~/fill.log

        """
        bse = b"a"
        bs = np.frombuffer(bse * (1024 * 1024), dtype=np.uint8)

        if isinstance(size, int):
            assert size >= 1024 * 1024
            N = size // len(bs)
        else:
            raise Exception("unimplemented")

        def fpath(fid: int) -> Path:
            return Path(f"{dir}/{pre}{fid:08d}")

        iprint("begin write file")
        fid = 1
        while True:
            file = fpath(fid)
            if verbose:
                iprint(f"write file {file}")
            try:
                with file.open(mode="wb") as f:
                    for i in range(N):
                        f.write(bs)
                    f.flush()
                fid += 1
            except Exception as e:
                iprint(f"error {file} {e}")
                break

        iprint("fill disk end")

        if verify:
            DkFile.verify_disk_simple(dir=dir, pre=pre, verbose=verbose)

    @staticmethod
    def verify_disk_simple(
        *,
        dir: str = ".",
        pre: str = "tmp",
        verbose: bool = False,
    ) -> None:
        import numpy as np

        """
        在目录下创建文件. 文件大小约为10M. 创建之后马上读出检查内容是否正确. 用来对硬盘进行简单的检查.
        直到写满磁盘为止, [Errno 28] No space left on device 最后退出.
        
        注意,下面命令的日志文件不要记录在当前磁盘中.因为当前磁盘会充满,会无法写入日志.
        mkdir tmp
        python3.10 -c "from dknovautils import *; DkFile.verify_disk_simple(dir='./tmp',verbose=True)" |& tee -a ~/verify.log

        """
        bse = b"a"
        bs = np.frombuffer(bse * (1024 * 1024), dtype=np.uint8)

        iprint("begin verify")

        files = (f for f in DkFile.listdir(dir) if f.basename.startswith(pre))
        for idx, file in enumerate(files):
            file = file.path
            if verbose:
                iprint(f"verify file {idx} {file}")
            try:
                with file.open(mode="rb") as f:
                    r = f.read(len(bs))
                    bs2 = np.frombuffer(r, dtype=np.uint8)
                    if len(bs2) == len(bs):
                        assert np.all(bs2 == bs), f"err56373 verify error {file}"
                    else:
                        condition = bs2 == bs[0]
                        assert np.all(condition), f"err56374 verify error {file}"
                # fid += 1
            except Exception as e:
                iprint(f"error idx{idx} {file} {e}")
                break

        iprint("verify disk end")


class DkPyFiles(object):
    pass


if __name__ == "__main__":
    print("OK")
