#!/usr/local/bin/python

__author__ = "David Stent"
__copyright__ = "Copyright 2017, David Stent"
__license__ = "GPL"
__version__ = "1"
__maintainer__ = "David Stent"
__email__ = "secopscrazy@gmail.com"
__status__ = "Production"

import sys, getopt, subprocess, os, glob, time

def main(argv):
   task = ''
   parameters = ''
   execute = ''
   home_directory = os.environ['HOME']
   path_to_android_sdk = home_directory + '/Library/Android/sdk/'
   emulator_name = 'Nexus_5_API_21'
   dumpfile = 'dump/lime.dmp'
   volatility_program = 'volatility_2.6_mac64_standalone/volatility_2.6_mac64_standalone'
   try:
      opts, args = getopt.getopt(argv,"ht:p:",["task=","params="])
   except getopt.GetoptError:
      print 'androidforensics.py -t <task: start_emulator, deploy_app, run_lime, volatility, volatility_dump> -p <parameters: linux_pslist>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'androidforensics.py -t <task: start_emulator, deploy_app, run_lime, volatility, volatility_dump> -p <parameters: linux_pslist>'
         sys.exit()
      elif opt in ("-t", "--task"):
         task = arg
      elif opt in ("-p", "--params"):
         parameters = arg
   if task == 'start_emulator':
       subprocess.Popen([path_to_android_sdk + 'tools/emulator', '-avd', emulator_name, '-kernel', 'kernal-image/zImage'])
   elif task == 'deploy_app':
       apps = glob.glob("myapp/*.apk")
       subprocess.Popen([path_to_android_sdk + 'platform-tools/adb', 'install', apps[0]])
   elif task == 'run_lime':
       os.remove(dumpfile) if os.path.exists(dumpfile) else None
       time.sleep( 3 )
       subprocess.Popen([path_to_android_sdk + 'platform-tools/adb', 'push', 'lime-kernel-module/lime-goldfish.ko', '/sdcard/lime.ko'])
       time.sleep( 3 )
       subprocess.Popen([path_to_android_sdk + 'platform-tools/adb', 'forward', 'tcp:4444', 'tcp:4444'])
       time.sleep( 3 )
       subprocess.Popen([path_to_android_sdk + 'platform-tools/adb', 'shell', 'insmod', '/sdcard/lime.ko', '"path=tcp:4444 format=lime"'])
       time.sleep( 3 )
       subprocess.call("nc localhost 4444 > " + dumpfile, shell=True)
   elif task == 'volatility':
       subprocess.Popen([volatility_program, '--plugins=Volatility-plugins/', '-f', dumpfile, '--profile=LinuxAndroid_Goldfish_3_4_67-gd3ffcc7ARM', parameters])
   elif task == 'volatility_dump':
       subprocess.Popen([volatility_program, '--plugins=Volatility-plugins/', '-f', dumpfile, '--profile=LinuxAndroid_Goldfish_3_4_67-gd3ffcc7ARM', 'linux_procdump', '--dump-dir=procdump/'])
if __name__ == "__main__":
   main(sys.argv[1:])
