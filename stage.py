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

HOME_X = -30000
HOME_Y = -50000

L1_X = -50000
L1_Y = -50000

OUT_X = 30000
OUT_Y = 50000

def test_needle_pos():
    home = setup_position()

    if home:
        send_command(f"X{L1_X}")
        send_command(f"Y{L1_Y}")

def move_plate_out():
    send_command(f"X{OUT_X}")
    send_command(f"Y{OUT_Y}")

def setup_position():
    send_command("EO=3")
    send_command("X-40000")
    send_command("Y1000")

    setup_complete = move_complete("PX", -40000)

    print(f'Complete? {setup_complete}')
    return setup_complete

def snake_loop():
    send_command("Y10000")

    move_complete("PY", 10000)

    if move_complete:
        send_command("X10000")
  
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



####### MAIN ########
# setup_complete = setup_position()

# if setup_complete:
#     snake_loop()

# move_plate_out()

test_needle_pos()

result = cmd.CloseCommanderHID(hid_handle)
print(f"Close HID result: {result}")