# !/usr/bin/python3
# encoding: utf-8
"""
@author: niko.zhang
@software: PyCharm
@date: 2018/4/11
@language: Python3
@光纤测试数据PDF文档距离/损耗数据提取工具
"""

import logging
import os
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
import csv
from tqdm import tqdm,trange
logger = logging.getLogger('Task')
logging.basicConfig()
logger.setLevel(logging.INFO)


class Task(object):
    def Process_task (self, _file_dir, _csv_file,debug=False):
        with open(_csv_file,'w',newline='') as csvfile:
            skywriter = csv.writer(csvfile,dialect='excel')
            for root, dirs, files in os.walk(_file_dir):
                for name in files:
                    if os.path.join(root, name).endswith('.pdf'):
                        logger.info('Deal with file : ' + name + '.')
                        files_path = os.path.join(root, name)
                        # 以二进制读模式打开pdf
                        fp = open(files_path, 'rb')
                        # 用文件对象创建一个pdf文档分析器
                        praser = PDFParser(fp)
                        # 创建一个PDF文档
                        doc = PDFDocument()
                        # 链接分析器与文档对象
                        praser.set_document(doc)
                        doc.set_parser(praser)
                        # 创建pdf资源管理器
                        rsrcmgr = PDFResourceManager()
                        # 创建一个pdf设备对象
                        laparm = LAParams()
                        device = PDFPageAggregator(rsrcmgr, laparams=laparm)
                        # 创建一个pdf解释器对象
                        interpreter = PDFPageInterpreter(rsrcmgr, device)
                        for pages in doc.get_pages():
                            all_text = []
                            interpreter.process_page(pages)
                            layout = device.get_result()
                            for x in layout:
                                if isinstance(x, LTTextBoxHorizontal):
                                    try:
                                        results = x.get_text()
                                        all_text.append(results)
                                    except AttributeError:
                                        continue
                        #print(all_text)
                        distance_index = all_text.index('距离距离\n')
                        loss_index = all_text.index('激光器 nm\n1310\n')
                        distance = (all_text[distance_index + 1].split('\n'))[-2]
                        loss = (all_text[loss_index + 1].split('\n'))[-2]
                        #print(distance,loss)
                        fname = name.replace('Fiber', '').replace('_1310OE.sor.pdf', '')
                        skywriter.writerow([fname, distance, loss])
                        device.close()
                        fp.close()
                        if debug:
                            print(fname,distance,loss)
        csvfile.close()


if __name__ == '__main__':
    print('-'*10)
    input_dir = input('Please enter a file directory:\n')
    print('-'*10)
    out_file_path = input('Please enter the output file name:\n')
    print('-'*10)
    print('开始提取数据，请勿关闭窗口')
    print('-'*10)
    task = Task()
    task.Process_task(input_dir, out_file_path)

print('提取完毕', out_file_path)
os.popen(out_file_path)
