from win10toast import ToastNotifier  # 导入系统通知对象
import time  # 系统时间模块
from  datetime import datetime
from threading import Timer  # 定时器

def show_toast(notify_head="You've got new msg", notify_min=1, notify_text="test msg"):
    notify = ToastNotifier()# 初始化系统通知对象
    notify_head = '主人，来通知啦！'
    notify_min = 1.0
    #notify_text = '已经过了' + str(int(notify_min)) + '分钟了，该喝水了！'

    notify_sen = notify_min * 1

    
    print('当前时间:%s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    notify.show_toast(f"{notify_head}", f"{notify_text}", duration=5, threaded=True, icon_path='水杯.ico')
    while notify.notification_active():
        time.sleep(1)
    timer = Timer(notify_sen, show_toast)
    timer.start()



def show_msg_once(title="here is title", msg="new message "):
     
    toaster = ToastNotifier()     
    toaster.show_toast(title, msg)
    
    
if __name__ == "__main__":    
    show_msg_once()
    #show_toast()