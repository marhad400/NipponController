import ctypes
import os

class CMD:
    def __init__(self):

        # Full path to the CMDHidApi.dll, including spaces in the directory names
        dll_path = r'C:\Users\Mark Haddad\Desktop\Workspaces\NipponController\CMDHidApi.dll'

        # Check if the DLL exists
        if not os.path.isfile(dll_path):
            print(f"Error: DLL not found at {dll_path}")
        else:
            try:
                # Load the DLL
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

        self.dll.OpenCommanderHID.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_char_p]
        self.dll.OpenCommanderHID.restype = ctypes.c_int

        self.dll.CloseCommanderHID.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.dll.CloseCommanderHID.restype = ctypes.c_int

        self.dll.SendReceiveCommanderHID.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_char_p, ctypes.c_char_p]
        self.dll.SendReceiveCommanderHID.restype = ctypes.c_int

    def GetCommanderHIDnumber(self):
        return self.dll.GetCommanderHIDnumber()

    def GetCommanderHIDName(self, HidIndex, HidName):
        return self.dll.GetCommanderHIDName(HidIndex, HidName.encode('utf-8'))

    def OpenCommanderHID(self, HidHandle, HidName):
        result = self.dll.OpenCommanderHID(ctypes.byref(HidHandle), HidName.encode('utf-8'))
        return result, HidHandle

    def CloseCommanderHID(self, HidHandle):
        return self.dll.CloseCommanderHID(HidHandle)

    def SendReceiveCommanderHID(self, HidHandle, command, reply):
        result = self.dll.SendReceiveCommanderHID(HidHandle, command.encode('utf-8'), reply)
        return result, reply.value.decode('utf-8')
