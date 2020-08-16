import logging,time
class Logger:
    def log(self):

        logger=logging.getLogger("logger")
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            sh = logging.StreamHandler()
            fh=logging.FileHandler(filename="../log/logfile/{}_log".format(time.strftime("%Y-%m-%d  %H-%M-%S",time.localtime())),encoding="utf-8")
            formator=logging.Formatter(fmt="%(asctime)s %(filename)s %(levelname)s %(msg)s", datefmt="%Y-%m-%d %X")
            sh.setFormatter(formator)
            fh.setFormatter(formator)
            logger.addHandler(fh)
            logger.addHandler(sh)
        return logger