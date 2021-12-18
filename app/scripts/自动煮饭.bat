chcp 65001
@echo off 
echo 脚本名称[自动煮饭]
echo 作者[何洁]
echo 创建日期[2021/12/12 12:14:42]

rem ======= 请从以下位置开始编辑脚本 =======

adb shell input keyevent 26 
echo 模拟锁屏键

adb shell input swipe 540 1631 505 459 
echo 从：540 1631 滑动到 505 459，持续  毫秒

echo 延时1秒
ping 127.0.0.1 -n 2 >nul 

adb shell input keyevent 3 
echo 模拟主页键

echo 延时1秒
ping 127.0.0.1 -n 2 >nul 


adb shell am force-stop com.xiaomi.smarthome
echo 强制停止：com.xiaomi.smarthome

echo 延时1秒
ping 127.0.0.1 -n 2 >nul 

adb shell am start -n com.xiaomi.smarthome/com.xiaomi.smarthome.SmartHomeMainActivity
echo 启动活动：com.xiaomi.smarthome/com.xiaomi.smarthome.SmartHomeMainActivity

echo 延时3秒
ping 127.0.0.1 -n 5 >nul 

adb shell input tap 807 884
echo 点击：790 1269

echo 延时3秒
ping 127.0.0.1 -n 5 >nul 

adb shell input tap 705 258
echo 点击：703 276

adb shell input swipe 1048 1229 1031 918 
echo 从：1048 1229 滑动到 1031 918，持续  毫秒


echo 延时1秒
ping 127.0.0.1 -n 2 >nul 

adb shell input tap 568 1782
echo 点击：547 711

adb shell input swipe 1048 1229 1031 418 
echo 从：1048 1229 滑动到 1031 918，持续  毫秒

echo 延时1秒
ping 127.0.0.1 -n 2 >nul 

adb shell input tap 505 1464
echo 点击：505 1464

echo 延时1秒
ping 127.0.0.1 -n 2 >nul 

adb shell input tap 573 1769
echo 点击：573 1769

