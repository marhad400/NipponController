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

def setup_position():
    setup_complete = False
    command = "EO=3"
    reply = ctypes.create_string_buffer(63)
    result = cmd.SendReceiveCommanderHID(hid_handle, command, reply)
    print(f"Command result: {result}, reply: {reply.value.decode('utf-8')}")
    command = "X-40000"
    x_pos = -40000
    reply = ctypes.create_string_buffer(63)
    result = cmd.SendReceiveCommanderHID(hid_handle, command, reply)
    print(f"Command result: {result}, reply: {reply.value.decode('utf-8')}")
    command = "Y1000"
    reply = ctypes.create_string_buffer(63)
    result = cmd.SendReceiveCommanderHID(hid_handle, command, reply)
    print(f"Command result: {result}, reply: {reply.value.decode('utf-8')}")

    while not setup_complete:
        command = "PX"
        reply = ctypes.create_string_buffer(63)
        result = cmd.SendReceiveCommanderHID(hid_handle, command, reply)

        if int(reply.value.decode('utf-8')) == x_pos:
            setup_complete = True

    print(f'Complete? {setup_complete}')
    return setup_complete

def snake_loop():
    reply = ctypes.create_string_buffer(63)
    result = cmd.SendReceiveCommanderHID(hid_handle, "Y10000", reply)
    y_pos = 10000
    print(f"Command result: {result}, reply: {reply.value.decode('utf-8')}")

    move_complete = False
    while not move_complete:
        command = "PY"
        reply = ctypes.create_string_buffer(63)
        result = cmd.SendReceiveCommanderHID(hid_handle, command, reply)

        if int(reply.value.decode('utf-8')) == y_pos:
            move_complete = True

    if move_complete:
        reply = ctypes.create_string_buffer(63)
        result = cmd.SendReceiveCommanderHID(hid_handle, "X10000", reply)
        print(f"Command result: {result}, reply: {reply.value.decode('utf-8')}")
        


setup_complete = setup_position()

if setup_complete:
    snake_loop()

result = cmd.CloseCommanderHID(hid_handle)
print(f"Close HID result: {result}")
