import unittest
from proxy.proxy_test import doTest
import os
import configparser
from tools.notification import Notification


class MyTestCase(unittest.TestCase):
    def test_proxy(self):
        doTest()

    def test_notification(self):
        config_file = "../../config.ini"
        if not os.path.exists("../../config.ini"):
            config_file = "../../config-template.ini"

        conf = configparser.ConfigParser()
        conf.read(config_file)

        # 邮件通知配置
        sender = conf.get("notification", "sender")
        pw = conf.get("notification", "passwd")
        receiver = conf.get("notification", "receiver")

        mailObj = Notification(sender, pw, receiver)
        mailObj.notification("Write Kafka ERROR! code: {}".format(404))


if __name__ == '__main__':
    unittest.main()

