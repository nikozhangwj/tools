# encoding: utf-8

'''
批量修改测试数据文件名
配合PDFGET使用：当PDFget无法正常获取数据文件内容时候，可以修改文件名
'''

import os

read_file_dir = input('Please input file dir: ')
# 定义文件夹路径，可控制台输入，也可以手动代码修改
#read_file_dir = './yihaichengA20180122-odf02'
files = os.listdir(read_file_dir)
# 列出文件夹内容

#find file and rename
for file in files:
# 先遍历文件夹
    fname = file.replace('FiberODF01', '').replace('_1310OE.sor.pdf', '')
    new_name = 'FiberODF02'+ fname + '_1310OE.sor.pdf'
# 设置新文件名格式
    os.rename(file,new_name)
# 将文件名修改成新文件名格式
    print(new_name)
    print('ok')
# 成功修改打印新文件名和状态
