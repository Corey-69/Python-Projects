import subprocess
import uiautomator2 as u2

print(u2.connect())
print()

# def check_adb_devices():
#     try:
#         result = subprocess.run(
#             ["adb", "devices"],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             encoding='utf-8'
#         )
#
#         if result.returncode != 0:
#             print("命令执行失败:")
#             print(result.stderr)
#         else:
#             result_list = result.stdout.splitlines()
#             result_list_sum = len(result.stdout.splitlines())
#             if  result_list_sum == 2:
#                 print("当前未检测到任何连接的设备。")
#                 print("请检查：\n   1. USB线是否连接正常\n   2. 手机端是否开启USB调试模式\n   3. 是否授权了本机调试权限")
#             elif result_list_sum > 2:
#                 if result_list_sum == 3:
#                     print(f"当前已连接一个设备：\n{result_list[1]}")
#                     return result_list[1]
#                 else:
#                     print("当前已连接多个设备,请选择要使用的设备:")
#                     for i, line in enumerate(result_list):
#                         if i > 0:
#                             print(f"{i}. {line}")
#                             if i == result_list_sum - 2:
#                                 break
#                         return line
#
#     except Exception as e:
#         print(f"发生异常: {e}")
#
#
# if __name__ == '__main__':
#     adb_device = check_adb_devices()
#     print()
#     print()
#     print()
#     print(adb_device)