import ctypes
import os

class CMD:
    def __init__(self):

        #dll_path = r'C:\Users\Mark Haddad\Desktop\Workspaces\NipponController\CMDHidApi64.dll'
        dll_path = r'C:\Users\abh36\OneDrive\Desktop\NipponPyController\NipponController\CMDHidApi64.dll'

        if not os.path.isfile(dll_path):
            print(f"Error: DLL not found at {dll_path}")
        else:
            try:
                self.dll = ctypes.CDLL(dll_path)
                print("DLL loaded successfully.")
            except OSError as e:
                print(f"Error loading DLL: {e}")

        self._setup_functions()


    def _setup_functions(self):
        self.dll.GetCommanderHIDnumber.argtypes = []
        self.dll.GetCommanderHIDnumber.restype = ctypes.c_int

        self.dll.GetCommanderHIDName.argtypes = [ctypes.c_int, ctypes.c_char_p]
        self.dll.GetCommanderHIDName.restype = ctypes.c_int

        self.dll.OpenCommanderHID.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.dll.OpenCommanderHID.restype = ctypes.c_int

        self.dll.CloseCommanderHID.argtypes = [ctypes.c_void_p]
        self.dll.CloseCommanderHID.restype = ctypes.c_int

        self.dll.SendReceiveCommanderHID.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
        self.dll.SendReceiveCommanderHID.restype = ctypes.c_int

    def GetCommanderHIDnumber(self):
        return self.dll.GetCommanderHIDnumber()

    def GetCommanderHIDName(self, HidIndex, buffer_size=256):
        HidName = ctypes.create_string_buffer(buffer_size)
        result = self.dll.GetCommanderHIDName(HidIndex, HidName)
        return result, HidName.value.decode('utf-8')

    def OpenCommanderHID(self, HidName):
        HidHandle = ctypes.c_void_p()
        result = self.dll.OpenCommanderHID(ctypes.byref(HidHandle), HidName.encode('utf-8'))
        return result, HidHandle

    def CloseCommanderHID(self, HidHandle):
        return self.dll.CloseCommanderHID(HidHandle)

    def SendReceiveCommanderHID(self, HidHandle, command, reply):
        padded_command = (command + "\x00").ljust(63, "\x00")
        padded_reply = ctypes.create_string_buffer(63)
        
        result = self.dll.SendReceiveCommanderHID(HidHandle, padded_command.encode('utf-8'), padded_reply)
        
        # Copy the reply to the provided buffer
        reply.value = padded_reply.raw
        
        return result
