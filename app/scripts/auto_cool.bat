@echo off
rem ======= 请从以下位置开始编辑脚本 =======
echo 0
E:\adb shell input keyevent 26
echo 1
E:\adb shell input swipe 540 1631 505 459

ping 127.0.0.1 -n 2 >nul

E:\adb shell input keyevent 3 

ping 127.0.0.1 -n 2 >nul

E:\adb shell am force-stop com.xiaomi.smarthome

ping 127.0.0.1 -n 2 >nul

E:\adb shell am start -n com.xiaomi.smarthome/com.xiaomi.smarthome.SmartHomeMainActivity

ping 127.0.0.1 -n 10 >nul

E:\adb shell input tap 790 1269

ping 127.0.0.1 -n 10 >nul

E:\adb shell input tap 703 276

ping 127.0.0.1 -n 2 >nul

E:\adb shell input tap 542 808

ping 127.0.0.1 -n 2 >nul

E:\adb shell input tap 291 1783

ping 127.0.0.1 -n 2 >nul

E:\adb shell input tap 264 911

ping 127.0.0.1 -n 2 >nul

E:\adb shell input tap 810 1770

ping 127.0.0.1 -n 2 >nul

