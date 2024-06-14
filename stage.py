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
    send_command("EO=3")
    send_command("X-30000")
    send_command("Y1000")

    setup_complete = move_complete("PX", -30000)

    print(f'Complete? {setup_complete}')
    return setup_complete

def snake_loop():
    x_pos = -30000
    y_pos = 1000

    # for i in range(9):
    #     x_move_cmd = "X" + str(x_pos)
    #     y_move_cmd = "Y" + str(y_pos)
    #     send_command(y_move_cmd)
    #     send_command(x_move_cmd)
    #     move_complete("PY", y_pos)
    for j in range(9):
        if move_complete:
            x_move_cmd = "X" + str(x_pos)
            y_move_cmd = "Y" + str(y_pos)
            send_command(y_move_cmd)
            send_command(x_move_cmd)
            move_complete("PX", x_pos)
            x_pos += 3000
       # y_pos += 3000
  
def send_command(command):
    reply = ctypes.create_string_buffer(63)
    result = cmd.SendReceiveCommanderHID(hid_handle, command, reply)
    print(f"Command result: {result}, reply: {reply.value.decode('utf-8')}")

def get_command_reply(command):
    reply = ctypes.create_string_buffer(63)
    result = cmd.SendReceiveCommanderHID(hid_handle, command, reply)
    if result:
        reply = reply.value.decode('utf-8')

    return reply

def move_complete(pos_command, end_pos):
    is_complete = False
    while not is_complete:
        pos = get_command_reply(pos_command)
        if int(pos) == end_pos:
            is_complete = True

    return is_complete

setup_complete = setup_position()

if setup_complete:
    snake_loop()

result = cmd.CloseCommanderHID(hid_handle)
print(f"Close HID result: {result}")