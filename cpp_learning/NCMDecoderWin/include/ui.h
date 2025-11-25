#pragma once
#include <windows.h>
#include <string>
#include <vector>

// 控件 ID
#define ID_BTN_SELECT_FILES  1001
#define ID_BTN_SELECT_DIR    1002
#define ID_BTN_START         1003
#define ID_LIST_FILES        2001
#define ID_PROGRESS          3001

// 自定义消息（用于后台线程与 UI 通信）
#define WM_USER_PROGRESS   (WM_USER + 1)  // wParam = done, lParam = total
#define WM_USER_FILE_DONE  (WM_USER + 2)  // wParam = index, lParam = 0
#define WM_USER_FINISHED   (WM_USER + 3)  // wParam/lParam 暂不使用

LRESULT CALLBACK MainWndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam);

bool RegisterMainWindowClass(HINSTANCE hInstance);
HWND CreateMainWindow(HINSTANCE hInstance);

void CreateUIControls(HWND hwnd);

// 供 ui.cpp 内部使用的结构也可以放这里
struct AppState {
    std::vector<std::string> selectedFiles;
    std::string outputDir;
    bool workerRunning = false;
};
