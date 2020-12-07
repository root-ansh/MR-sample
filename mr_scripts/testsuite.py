from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import commands
import sys
import datetime
import time
"""
Note: This version of jython uses java version 1.8 and python version 2.7.x
Therefore a lot of syntax differences would be there ,so checkout this link 
for more syntax info: https://jython.readthedocs.io/en/latest/LangSyntax/
also try to use neutral syntax, i.e syntax that would work on both py2 and py 3 for 
easier migration in future. checkout here to learn the differences between py 2 and py 3
https://www.geeksforgeeks.org/important-differences-between-python-2-x-and-python-3-x-with-examples/.
most of the py3 syntax works for py2, but gives slightly different output, which won't effect much 
"""

#==============global vars===============================
apk_path = "app/build/outputs/apk/debug/apkname.apk" #apk path relative to monkeyrunner location( which runs from project root). generate via built/generate apk
package_name = "work.curioustools.monkey_runner"
activities_path = package_name + "/" + package_name

script_op_path = "mr_scripts_results/" #IMP :  must create this directory before running this testsuite


#==============global funcs===============================

def show_system_details():
    print("=======================welcome to monkey runner test suite  ==================")
    print("[MR:]System details :")
    print(sys.version)
    print("==============================================================================")

def select_device(wait_time):
    devices_list = commands.getoutput('adb devices').strip().split('\n')[1:]
    choice = -1
    if (len(devices_list) == 0):
        choice = -1
        MonkeyRunner.alert("No devices Found. Start an emulator or connect a device", "Exit")
        raise Exception("No devices Found. Start an emulator or connect a device")

    elif (len(devices_list) == 1):
        choice = 0
    else:
        choice = MonkeyRunner.choice("More than 1 devices found. please select a target device:", devices_list, "Your Device Selection:")

    device_id = devices_list[choice].split('\t')[0]
    device = MonkeyRunner.waitForConnection(wait_time, device_id)# google example does not pass timer in it
    print ("[MR]:connected to device id:",device_id)
    return device




def install_or_nothing_on_device(device):
    if(device is None):
        raise Exception("[MR]:device is null")

    already_installed_package_name = device.shell("pm path " + package_name)
    if (already_installed_package_name.startswith("package:")):
        print("[MR]:App is already installed")
    else:
        print("[MR]:App not installed, installing the app")
        device.installPackage(apk_path)
        print("[MR]:App is successfully installed")

def install_or_update_on_device(device):
    if(device is None):
        raise Exception("[MR]:device is null")

    device.installPackage(apk_path)
    print("[MR]:App is successfully installed")

def start_activity(device,activity):
    device.startActivity(component=activities_path + activity)
    print("[MR]:starting activity:" + activity)

def takeScreenshot(device,wait_time_sec):
    if(abs(wait_time_sec)>0):
        print("[MR]:waiting "+str(wait_time_sec)+ "seconds before taking a screenshot")
        time.sleep(wait_time_sec)

    result = device.takeSnapshot()
    name = "PIC"+ str(datetime.datetime.now()).split('.')[0]+".png"
    result.writeToFile(script_op_path+name,'png')
    print("[MR]:Saved screenshot")

show_system_details()
d = select_device(3)
install_or_update_on_device(d)
start_activity(d,".MainActivity")
takeScreenshot(d,3)

