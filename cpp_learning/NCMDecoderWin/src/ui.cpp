#include "../include/ui.h"
#include "../include/ncm_decoder.h"

#include <commctrl.h>
#include <shlobj.h>
#include <thread>
#include <atomic>

#pragma comment(lib, "comctl32.lib")

static HWND g_listFiles = NULL;
static HWND g_progress  = NULL;

static AppState g_app;
static std::thread g_workerThread;
static std::atomic_bool g_stopFlag{ false };

// 前向声明
static void StartConvertWorker(HWND hwnd);
static void WorkerThreadFunc(HWND hwnd);

// 简单帮助：选文件（多选）
static std::vector<std::string> OpenMultiFileDialog(HWND owner);
// 简单帮助：选目录
static std::string BrowseForFolder(HWND owner);

bool RegisterMainWindowClass(HINSTANCE hInstance)
{
    WNDCLASSEXA wc = { sizeof(WNDCLASSEXA) };
    wc.style         = CS_HREDRAW | CS_VREDRAW;
    wc.lpfnWndProc   = MainWndProc;
    wc.cbClsExtra    = 0;
    wc.cbWndExtra    = 0;
    wc.hInstance     = hInstance;
    wc.hIcon         = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor       = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.lpszMenuName  = NULL;
    wc.lpszClassName = "NcmDecoderClass";
    wc.hIconSm       = NULL;

    return RegisterClassExA(&wc);
}

HWND CreateMainWindow(HINSTANCE hInstance)
{
    return CreateWindowExA(
        0,
        "NcmDecoderClass",
        "NCM 转码器 (WinAPI)",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
        NULL, NULL, hInstance, NULL
    );
}

void CreateUIControls(HWND hwnd)
{
    CreateWindowA("BUTTON", "选择 NCM 文件",
        WS_CHILD | WS_VISIBLE,
        20, 20, 150, 30,
        hwnd, (HMENU)ID_BTN_SELECT_FILES, NULL, NULL);

    CreateWindowA("BUTTON", "选择输出文件夹",
        WS_CHILD | WS_VISIBLE,
        200, 20, 150, 30,
        hwnd, (HMENU)ID_BTN_SELECT_DIR, NULL, NULL);

    CreateWindowA("BUTTON", "开始转换",
        WS_CHILD | WS_VISIBLE,
        380, 20, 150, 30,
        hwnd, (HMENU)ID_BTN_START, NULL, NULL);

    // 列表
    g_listFiles = CreateWindowExA(
        WS_EX_CLIENTEDGE, "LISTBOX", "",
        WS_CHILD | WS_VISIBLE | WS_VSCROLL | LBS_NOINTEGRALHEIGHT,
        20, 70, 740, 400,
        hwnd, (HMENU)ID_LIST_FILES, NULL, NULL);

    // 进度条
    INITCOMMONCONTROLSEX icc = { sizeof(icc), ICC_PROGRESS_CLASS };
    InitCommonControlsEx(&icc);

    g_progress = CreateWindowExA(
        0, PROGRESS_CLASSA, "",
        WS_CHILD | WS_VISIBLE,
        20, 490, 740, 25,
        hwnd, (HMENU)ID_PROGRESS, NULL, NULL);

    SendMessageA(g_progress, PBM_SETRANGE, 0, MAKELPARAM(0, 100));
    SendMessageA(g_progress, PBM_SETPOS, 0, 0);
}

LRESULT CALLBACK MainWndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    switch (msg)
    {
    case WM_CREATE:
        CreateUIControls(hwnd);
        break;

    case WM_COMMAND:
        switch (LOWORD(wParam))
        {
        case ID_BTN_SELECT_FILES:
        {
            auto files = OpenMultiFileDialog(hwnd);
            g_app.selectedFiles = files;

            SendMessageA(g_listFiles, LB_RESETCONTENT, 0, 0);
            for (const auto& f : g_app.selectedFiles) {
                SendMessageA(g_listFiles, LB_ADDSTRING, 0, (LPARAM)f.c_str());
            }
            break;
        }
        case ID_BTN_SELECT_DIR:
        {
            auto dir = BrowseForFolder(hwnd);
            if (!dir.empty()) {
                g_app.outputDir = dir;
                // 简单用窗口标题显示输出目录
                std::string title = "NCM 转码器 (输出目录: " + dir + ")";
                SetWindowTextA(hwnd, title.c_str());
            }
            break;
        }
        case ID_BTN_START:
        {
            if (g_app.workerRunning) {
                MessageBoxA(hwnd, "正在转换中，请稍候……", "提示", MB_OK | MB_ICONINFORMATION);
                break;
            }
            if (g_app.selectedFiles.empty()) {
                MessageBoxA(hwnd, "请先选择至少一个 .ncm 文件。", "提示", MB_OK | MB_ICONWARNING);
                break;
            }
            if (g_app.outputDir.empty()) {
                MessageBoxA(hwnd, "请先选择输出文件夹。", "提示", MB_OK | MB_ICONWARNING);
                break;
            }

            StartConvertWorker(hwnd);
            break;
        }
        }
        break;

    case WM_USER_PROGRESS:
    {
        int done  = (int)wParam;
        int total = (int)lParam;
        int percent = (total > 0) ? (done * 100 / total) : 0;
        SendMessageA(g_progress, PBM_SETPOS, percent, 0);
        break;
    }

    case WM_USER_FILE_DONE:
    {
        int index = (int)wParam;
        if (index >= 0 && index < (int)g_app.selectedFiles.size()) {
            // 简单在列表中加个标记
            char buffer[1024];
            SendMessageA(g_listFiles, LB_GETTEXT, index, (LPARAM)buffer);
            std::string text = buffer;
            text += "  ->  DONE";
            SendMessageA(g_listFiles, LB_DELETESTRING, index, 0);
            SendMessageA(g_listFiles, LB_INSERTSTRING, index, (LPARAM)text.c_str());
        }
        break;
    }

    case WM_USER_FINISHED:
    {
        g_app.workerRunning = false;
        MessageBoxA(hwnd, "全部文件转换完成！", "完成", MB_OK | MB_ICONINFORMATION);
        break;
    }

    case WM_DESTROY:
        g_stopFlag = true;
        if (g_workerThread.joinable()) {
            g_workerThread.join();
        }
        PostQuitMessage(0);
        break;
    }

    return DefWindowProcA(hwnd, msg, wParam, lParam);
}

// 启动后台线程
static void StartConvertWorker(HWND hwnd)
{
    g_stopFlag = false;
    g_app.workerRunning = true;
    SendMessageA(g_progress, PBM_SETPOS, 0, 0);

    if (g_workerThread.joinable()) {
        g_workerThread.join();
    }

    g_workerThread = std::thread(WorkerThreadFunc, hwnd);
}

// 后台线程函数：循环调用 DecryptNcmToFile
static void WorkerThreadFunc(HWND hwnd)
{
    int total = (int)g_app.selectedFiles.size();
    int done = 0;

    for (int i = 0; i < total; ++i) {
        if (g_stopFlag) break;
        const auto& inPath = g_app.selectedFiles[i];
        try {
            DecryptNcmToFile(inPath, g_app.outputDir);
        } catch (...) {
            // 这里你可以加日志或者 MessageBox（注意线程问题）
        }
        ++done;
        PostMessageA(hwnd, WM_USER_FILE_DONE, (WPARAM)i, 0);
        PostMessageA(hwnd, WM_USER_PROGRESS, (WPARAM)done, (LPARAM)total);
    }

    PostMessageA(hwnd, WM_USER_FINISHED, 0, 0);
}

// 打开多文件选择对话框（简单版，多字节）
static std::vector<std::string> OpenMultiFileDialog(HWND owner)
{
    std::vector<std::string> result;
    char buffer[65536] = { 0 };

    OPENFILENAMEA ofn = { 0 };
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = owner;
    ofn.lpstrFilter = "NCM Files\0*.ncm\0All Files\0*.*\0";
    ofn.lpstrFile = buffer;
    ofn.nMaxFile = sizeof(buffer);
    ofn.Flags = OFN_ALLOWMULTISELECT | OFN_EXPLORER | OFN_FILEMUSTEXIST;
    ofn.lpstrTitle = "选择 NCM 文件";

    if (GetOpenFileNameA(&ofn)) {
        // 多选格式：dir\0file1\0file2\0...\0\0
        std::string dir = buffer;
        char* p = buffer + dir.size() + 1;
        if (*p == '\0') {
            // 只选一个
            result.push_back(dir);
        } else {
            while (*p) {
                std::string filename = p;
                p += filename.size() + 1;
                result.push_back(dir + "\\" + filename);
            }
        }
    }
    return result;
}

// 选择目录
static std::string BrowseForFolder(HWND owner)
{
    BROWSEINFOA bi = { 0 };
    bi.hwndOwner = owner;
    bi.lpszTitle = "选择输出目录";
    bi.ulFlags = BIF_RETURNONLYFSDIRS | BIF_NEWDIALOGSTYLE;

    LPITEMIDLIST pidl = SHBrowseForFolderA(&bi);
    if (!pidl) return {};

    char path[MAX_PATH];
    if (SHGetPathFromIDListA(pidl, path)) {
        CoTaskMemFree(pidl);
        return std::string(path);
    }
    CoTaskMemFree(pidl);
    return {};
}
