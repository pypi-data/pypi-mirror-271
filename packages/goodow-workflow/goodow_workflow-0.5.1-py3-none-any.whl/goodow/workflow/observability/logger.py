import logging
import os

def setup_logging(level=logging.INFO, filename=None):
    """
    该方法在执行 logging.info() 之后再调用会无效
    """
    try:
        import pandas as pd

        pd.options.display.max_columns = 20
        pd.options.display.width = 1000
    except ImportError:
        pass
    logging.getLogger("qlib").propagate = False  # 避免 root log 重复打印
    try:
        from datacompy import LOG

        LOG.setLevel(logging.WARNING)  # datacompy.Compare 默认相同时也打印日志
    except ImportError:
        pass

    root = logging.getLogger()
    root.level = level
    format = "%(asctime)s %(name)s:%(levelname)s:%(message)s"
    logging.basicConfig(level=level, format=format)
    if len(root.handlers) > 1:
        print(f"已设置 {len(root.handlers)} 个日志输出的格式: {root.handlers}")
    if filename:
        found = False
        for handle in root.handlers:
            if isinstance(
                handle, logging.handlers.TimedRotatingFileHandler
            ) and handle.baseFilename == os.path.abspath(os.fspath(filename)):
                found = handle
                break
        if found:
            print(f"文件日志已存在, 不再重复添加: {found}")
        else:
            file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=filename, when="W0", encoding="utf-8"  # 每周一
            )
            root.addHandler(file_handler)

    for handler in root.handlers:
        handler.setFormatter(logging.Formatter(format))
