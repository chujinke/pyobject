import time,HTMLTestRunner
import unittest

if __name__ == "__main__":
    test_data = unittest.defaultTestLoader.discover("./",pattern="test.py")
    report_dir =r"./report"
    now = time.strftime("%Y-%m-%d-%H-%M-%S")
    filename = report_dir+'/result.html'
    with open(filename, 'wb') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f,title='Test Report',description='测试结果总览:')
        runner.run(test_data)
    f.close()
