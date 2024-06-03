from CMD import CMD

cmd = CMD()

hid_number = cmd.GetCommanderHIDnumber()
print(f"Number of HID devices: {hid_number}")

hid_name = "CMD-4CR-01"
hid_index = 0
result = cmd.GetCommanderHIDName(hid_index, hid_name)
print(f"HID Name: {hid_name.strip()}")

result, hid_handle = cmd.OpenCommanderHID(hid_name)
print(f"Open HID result: {result}, handle: {hid_handle}")

command = "X1000"
result, reply = cmd.SendReceiveCommanderHID(hid_handle, command)
print(f"Command result: {result}, reply: {reply.value.decode('utf-8')}")

result = cmd.CloseCommanderHID(hid_handle)
print(f"Close HID result: {result}")