# 先实现个demo
# 手动将所有的网址放到一个文件里
# 复制ovopark_web_spider.py中的get_all_text()的代码，打开每个链接，通过bs获取文本
import xlwt
import time
# 导入词云制作库wordcloud和中文分词库jieba
import jieba
import wordcloud
# 导入imageio库中的imread函数，并用这个函数读取本地图片，作为词云形状图片
import imageio
from tkinter import *
from bs4 import BeautifulSoup
from selenium import webdriver

browser = None

tag_text_list = []
tag_text_str = ''

# 加载浏览器驱动
def load_driver():

    # 更新
    text.update()

    url_input_str = url_input.get()
    print(url_input_str)

    url = url_input_str
    version = version_input.get()

    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 静默模式
    # 打开chrome浏览器
    browser = webdriver.Chrome(chrome_options=option, executable_path= 'chromedriver/' + version + '/chromedriver.exe')

    # cookies = login(browser)
    # for cookie in cookies:
    #     browser.add_cookie(cookie)

    browser.get(url)
    get_all_text(browser)

    browser.close()

    sys.exit()

# 获取文本
def get_all_text(browser):

    time.sleep(3)

    global tag_text_str
    soup = BeautifulSoup(browser.page_source, "html.parser")

    tags = []

    tags.extend(soup.select('div.intro'))
    tags.extend(soup.select('div.info'))
    tags.extend(soup.select('div.title'))
    tags.extend(soup.select('div.ivu-menu-submenu-title'))
    tags.extend(soup.select('p'))
    tags.extend(soup.select('figcaption'))
    tags.extend(soup.select('span'))

    for tag in tags:
        if tag.text:

            if tag.text.strip() in tag_text_str:
                continue
            if is_number(tag.text.strip()):
                continue
            print(tag.text)

            # 添加数据
            text.insert(END, tag.text)
            # 文本框向下滚动
            text.see(END)
            # 更新
            text.update()

            tag_text_list.append(tag.text.strip())
            tag_text_str = tag_text_str + tag.text.replace('\n', ' ')

    print('tag_text_str：' + tag_text_str)

    generate_word_cloud(tag_text_str)
    data_write('结果.xlsx', tag_text_list)

def login(browser):

    url = "http://www.opretail.com/"
    browser.get(url)

    #通过selenium模拟登录
    username = "***"
    password = "***"

    time.sleep(3)
    login_button = browser.find_element_by_xpath("//button[@class='ivu-btn ivu-btn-default']")
    login_button.click()

    username_ele = browser.find_element_by_xpath("//input[@placeholder='Username']")
    password_ele = browser.find_element_by_xpath("//input[@placeholder='Password']")

    username_ele.send_keys(username)
    password_ele.send_keys(password)

    submit_btn = browser.find_element_by_xpath("//button[@class='login-btn']")
    submit_btn.click()

    time.sleep(3)

    cookies = browser.get_cookies()

    return cookies

def main():
    global url_input, text, version_input
    # 创建空白窗口,作为主载体
    root = Tk()
    root.title('测试——万店掌web')
    # 窗口的大小，后面的加号是窗口在整个屏幕的位置
    root.geometry('550x400+398+279')
    # 标签控件，窗口中放置文本组件
    Label(root, text='请输入下载的url:', font=("华文行楷", 20), fg='black').grid()
    # 定位 pack包 place位置 grid是网格式的布局

    # Entry是可输入文本框
    spider_url = StringVar(value='http://www.opretail.com/')
    url_input = Entry(root, font=("微软雅黑", 15), textvariable=spider_url)
    url_input.grid(row=0, column=1)

    # 标签控件，窗口中放置文本组件
    Label(root, text='请输入chrome版本：', font=("华文行楷", 20), fg='black').grid()
    default_version = StringVar(value='78')
    version_input = Entry(root, font=("微软雅黑", 15), textvariable=default_version, width=3)
    version_input.grid(row=1, column=1)

    # 列表控件
    text = Listbox(root, font=('微软雅黑', 15), width=45, height=10)
    # columnspan 组件所跨越的列数
    text.grid(row=2, columnspan=2)
    # 设置按钮 sticky对齐方式，N S W E
    button = Button(root, text='开始下载', font=("微软雅黑", 15), command=load_driver).grid(row=3, column=0, sticky=W)
    button = Button(root, text='退出', font=("微软雅黑", 15), command=root.quit).grid(row=3, column=1, sticky=E)
    # 使得窗口一直存在
    mainloop()

# 生成词云
def generate_word_cloud(str):
    mk = imageio.imread("image/wandianzhang.png")
    w = wordcloud.WordCloud(mask=mk)

    # 构建并配置词云对象w，注意要加scale参数，提高清晰度， scale=4，这个数值越大，产生的图片分辨率越高，字迹越清晰。
    w = wordcloud.WordCloud(width=800,
                            height=500,
                            background_color='white',
                            font_path='msyh.ttc',
                            mask=mk,
                            scale=4)

    # 将string变量传入w的generate()方法，给词云输入文字
    w.generate(str)

    # 将词云图片导出到当前文件夹
    w.to_file('结果图.png')

#  将数据写入新文件
def data_write(file_path, datas):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet

    # 将数据写入第 i 行，第 j 列
    i = 0
    for data in datas:
        sheet1.write(i, 0, data)
        i = i + 1

    f.save(file_path)  # 保存文件

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

if __name__ == "__main__":

    main()
