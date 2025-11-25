#include <windows.h>
#include "../include/ui.h"

int WINAPI WinMain(
    HINSTANCE hInstance,
    HINSTANCE hPrevInstance,
    LPSTR     lpCmdLine,
    int       nCmdShow)
{
    if (!RegisterMainWindowClass(hInstance)) {
        MessageBoxA(NULL, "Failed to register window class.", "Error", MB_ICONERROR);
        return -1;
    }

    HWND hwnd = CreateMainWindow(hInstance);
    if (!hwnd) {
        MessageBoxA(NULL, "Failed to create main window.", "Error", MB_ICONERROR);
        return -1;
    }

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG msg;
    while (GetMessageA(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessageA(&msg);
    }

    return static_cast<int>(msg.wParam);
}
