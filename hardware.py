import win32api
import win32con

class WindowsInputHandler:
    ACTIONS = {
        "QUIT": win32con.VK_END,
        "TOGGLE": win32con.VK_DELETE,
        "TRIGGER": win32con.VK_XBUTTON2
    }

    def is_action_pressed(self, action_name):
        key_code = self.ACTIONS.get(action_name)
        return win32api.GetAsyncKeyState(key_code) < 0

    def mouse_left_down(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

    def mouse_left_up(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
