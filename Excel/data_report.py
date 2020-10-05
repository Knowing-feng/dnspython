import xlsxwriter

workbook = xlsxwriter.Workbook('./chart.xlsx')  # 创建一个Excel文件
worksheet = workbook.add_worksheet()  # 创建一个工作表对象
chart = workbook.add_chart({'type': 'column'})  # 创建一个column(柱形)图表

# 定义数据表头列表
title = ['业务名称', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日', '平均流量', ]
buname = ['业务官网', '新闻中心', '购物频道', '体育频道', '亲子频道']  # 定义频道名称

# 定义5频道一周7舔流量数据列表

data = [
    [150, 152, 158, 149, 155, 145, 148, ],
    [89, 88, 95, 93, 98, 100, 99, ],
    [201, 200, 198, 175, 170, 198, 195, ],
    [75, 77, 78, 78, 74, 70, 79, ],
    [88, 85, 87, 90, 93, 88, 84, ],
]

gl_format = workbook.add_format()  # 定义gl_format格式对象
gl_format.set_border(1)  # 定义gl_format对象单元格表框加粗（1像素）的格式

gl_format_title = workbook.add_format()  # 定义gl_format_title格式对象
gl_format_title.set_border(1)  # 定义gl_format_title对象单元格表框加粗（1像素）的格式
gl_format_title.set_bg_color('#cccccc')  # 定义gl_format_title对象单元格背景颜色为'#cccccc'的格式
gl_format_title.set_align('center')  # 定义gl_format_title对象单元格居中对齐的格式
gl_format_title.set_bold()  # 定义gl_format_title对象单元格内容加粗的格式

gl_format_ave = workbook.add_format()  # 定义gl_format_ave格式对象
gl_format_ave.set_border()  # 定义ggl_format_ave对象单元格表框加粗（1像素）的格式
gl_format_ave.set_num_format('0.00')  # 定义gl_format_ave单元格数字类别显示格式

# 下面分别以行或列写入方法将标题，业务名称，数据流量写入起初单元格，同时引用不同格式对象
worksheet.write_row('A1', title, gl_format_title)
worksheet.write_column('A2', buname, gl_format)
worksheet.write_row('B2', data[0], gl_format)
worksheet.write_row('B3', data[1], gl_format)
worksheet.write_row('B4', data[2], gl_format)
worksheet.write_row('B5', data[3], gl_format)
worksheet.write_row('B6', data[4], gl_format)


# 定义图表数据系列函数
def chart_series(cur_row):
    worksheet.write_formula('I' + cur_row, '=AVERAGE(B' + cur_row + ':H' + cur_row + ')',
                            gl_format_ave)  # 计算(AVERAGE函数)频道周平均流量
    chart.add_series({
        'categories': '=Sheet1!$B$1:$H$1',  # 将星期一至星期日作为图表数据标签（X轴）
        'values': '=Sheet1!$B$' + cur_row + ':$H$' + cur_row,   # 频道一周所有数据作为数据区域
        'line': {'color': 'black'},         # 线条颜色定义为black(黑色)
        'name': '=Sheet1!$A$' + cur_row  # 引用业务名称为图例项
    })

for row in range(2,7): # 数据域以第2~6行进行图表数据系列函数调用
    chart_series(str(row))

chart.set_size({'width': 577, 'height': 287})   # 设置图表大小
chart.set_title({'name': '业务流量周报图表'})       # 设置图表（上方）大标题
chart.set_y_axis({'name': 'Mb/s'})          # 设置y轴（左侧）小标题

worksheet.insert_chart('A8', chart)
workbook.close()
