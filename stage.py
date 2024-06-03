from CMD import CMD
import ctypes

cmd = CMD()

hid_number = cmd.GetCommanderHIDnumber()
print(f"Number of HID devices: {hid_number}")

hid_index = 0
result, hid_name = cmd.GetCommanderHIDName(hid_index)
print(f"HID Name: {hid_name}")

result, hid_handle = cmd.OpenCommanderHID(hid_name)
print(f"Open HID result: {result}, handle: {hid_handle}")

command = "EO=3"
reply = ctypes.create_string_buffer(63)

result = cmd.SendReceiveCommanderHID(hid_handle, command, reply)
print(f"Command result: {result}, reply: {reply.value.decode('utf-8')}")

command = "X10000"
reply = ctypes.create_string_buffer(63)

result = cmd.SendReceiveCommanderHID(hid_handle, command, reply)
print(f"Command result: {result}, reply: {reply.value.decode('utf-8')}")

result = cmd.CloseCommanderHID(hid_handle)
print(f"Close HID result: {result}")
