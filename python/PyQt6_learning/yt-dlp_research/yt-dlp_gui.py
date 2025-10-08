#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YT-DLP 图形界面封装 (PyQt6)

功能概览：
- 输入框：接受一个或多行链接（每行一个 URL）。
- 勾选框：布尔选项（仅音频、嵌入缩略图、添加元数据、写字幕、自动字幕、整列表、合并为MP4、跳过已存在）。
- 下拉框：格式预设（best、1080p mp4 优先、360p 小文件）；字幕语言多选下拉。
- 自定义变量输入框：按 “key=value” 每行输入，自动解析为 yt-dlp Python API 的参数字典并合并。
- 目录选择：输出路径浏览。
- 进度显示：文件级进度条、日志窗口、当前文件名/速度/ETA。
- 多任务：一次可输入多链接，顺序下载。
- 可中止：点击“取消”中止当前任务。

依赖安装：
    pip install yt-dlp PyQt6
可选（音/视频后处理需要）：
    FFmpeg 可执行文件放入 PATH

打包为 EXE（Windows 示例）：
    pip install pyinstaller
    pyinstaller --name "YTDLP-GUI" --windowed --onefile yt_dlp_gui.py

作者：ChatGPT（示例代码）
"""

from __future__ import annotations
import sys
import os
import shlex
import re
import traceback
from pathlib import Path
from typing import List, Dict, Any, Tuple

from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QObject, QModelIndex
)
from PyQt6.QtGui import QIcon, QStandardItemModel
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QPlainTextEdit, QPushButton, QLabel, QProgressBar, QFileDialog,
    QCheckBox, QComboBox, QGroupBox, QMessageBox, QSizePolicy
)

# ---- yt-dlp Python API ----
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


# =============== 工具：字节/秒、人性化显示 ==================

def human_readable_size(num: float | int | None) -> str:
    if not num and num != 0:
        return "?"
    num = float(num)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024.0:
            return f"{num:.2f} {unit}"
        num /= 1024.0
    return f"{num:.2f} PB"


def human_eta(sec: float | int | None) -> str:
    if sec is None:
        return "?"
    sec = int(sec)
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h:d}:{m:02d}:{s:02d}"
    return f"{m:d}:{s:02d}"


# =============== 自定义：带多选能力的下拉框 ==================
class MultiSelectComboBox(QComboBox):
    """一个可多选的 QComboBox：项目可打勾/取消，显示已选标签串。
    使用：
        combo = MultiSelectComboBox()
        combo.add_check_items([("zh-Hans", "简体中文"), ("zh-Hant", "繁体中文"), ("en", "English"), ("ja", "日本語")])
        langs = combo.checked_keys()  # -> ["zh-Hans", "en"]
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setPlaceholderText("选择一个或多个（点击展开勾选）")
        # 禁止用户在下拉框里输入文本
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        # concrete model for better tooling/type support
        self._model: QStandardItemModel = QStandardItemModel(self)
        self.setModel(self._model)

    def add_check_items(self, items: List[Tuple[str, str]]):
        # items: [(key, label)]
        for key, label in items:
            self.addItem(label, userData=key)
            idx = self._model.index(self.count()-1, 0)
            item = self._model.itemFromIndex(idx)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        self._refresh_text()

    def _refresh_text(self):
        keys = self.checked_keys()
        labels = []
        for i in range(self.count()):
            if self._model.item(i).data(Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked:
                labels.append(self.itemText(i))
        self.lineEdit().setText(
            ", ".join(labels) if labels else ""
        )

    def checked_keys(self) -> List[str]:
        res = []
        for i in range(self.count()):
            item = self._model.item(i)
            if item.data(Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked:
                res.append(self.itemData(i))  # userData
        return res

    def showPopup(self):
        super().showPopup()
        # 弹出后，点击项目切换勾选
        view = self.view()
        view.pressed.connect(self._handle_item_pressed)

    def _handle_item_pressed(self, index: QModelIndex):
        item = self._model.itemFromIndex(index)
        if item is None:
            return
        state = item.data(Qt.ItemDataRole.CheckStateRole)
        item.setData(
            Qt.CheckState.Unchecked if state == Qt.CheckState.Checked else Qt.CheckState.Checked,
            Qt.ItemDataRole.CheckStateRole,
        )
        self._refresh_text()


# =============== 自定义：把日志转发到 GUI 的 logger =============
class QtLogger(QObject):
    message = pyqtSignal(str)

    def debug(self, msg):
        self.message.emit(str(msg))

    def warning(self, msg):
        self.message.emit(f"[WARN] {msg}")

    def error(self, msg):
        self.message.emit(f"[ERROR] {msg}")


# =============== 下载线程（避免阻塞 UI） =====================
class DownloadWorker(QThread):
    progress = pyqtSignal(float, str, int)         # percent(0-100), speed(bytes/s HR), eta(sec)
    status   = pyqtSignal(str)                     # 任意状态文本
    file_changed = pyqtSignal(str)                 # 当前文件名/标题
    finished_one = pyqtSignal(str, bool)           # (url, ok)
    all_done     = pyqtSignal()

    def __init__(self, urls: List[str], ydl_opts: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.urls = urls
        self.ydl_opts = dict(ydl_opts)  # 复制防修改
        self._cancel = False
        self.qt_logger = QtLogger()

    def cancel(self):
        self._cancel = True

    # yt-dlp 进度钩子
    def _hook(self, d: Dict[str, Any]):
        if self._cancel:
            raise DownloadError("用户取消")
        status = d.get('status')
        if status == 'downloading':
            downloaded = d.get('downloaded_bytes') or 0
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or None
            percent = (downloaded / total * 100.0) if total else 0.0
            speed = d.get('speed') or 0
            eta = d.get('eta') or None
            fn = d.get('filename') or d.get('info_dict', {}).get('title')
            if fn:
                self.file_changed.emit(str(fn))
            self.progress.emit(percent, human_readable_size(speed), int(eta or 0))
        elif status == 'finished':
            filename = d.get('filename')
            if filename:
                self.status.emit(f"已下载：{filename}，开始后处理…")

    def run(self):
        # 将 hook 与 logger 接入参数
        opts = dict(self.ydl_opts)
        hooks = list(opts.get('progress_hooks', []))
        hooks.append(self._hook)
        opts['progress_hooks'] = hooks
        opts['logger'] = self.qt_logger

        # 连接 logger 到 status 信号
        self.qt_logger.message.connect(self.status.emit)

        try:
            with YoutubeDL(opts) as ydl:
                for url in self.urls:
                    if self._cancel:
                        break
                    try:
                        self.status.emit(f"开始下载：{url}")
                        ydl.download([url])
                        self.finished_one.emit(url, True)
                    except Exception as e:
                        self.status.emit(f"[ERROR] {url}: {e}")
                        self.finished_one.emit(url, False)
        finally:
            self.all_done.emit()


# =============== 主窗口 ======================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YT-DLP GUI — PyQt6")
        self.resize(980, 720)
        try:
            self.setWindowIcon(QIcon.fromTheme("media-download"))
        except Exception:
            pass

        self.worker: DownloadWorker | None = None
        self._build_ui()

    # ---------- UI 构建 ----------
    def _build_ui(self):
        cw = QWidget()
        self.setCentralWidget(cw)
        root = QVBoxLayout(cw)

        # 输入区
        root.addWidget(self._build_input_group())
        root.addWidget(self._build_options_group())
        root.addWidget(self._build_output_group())

        # 控制区
        ctrl = QHBoxLayout()
        self.btn_start = QPushButton("开始下载")
        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.setEnabled(False)
        ctrl.addWidget(self.btn_start)
        ctrl.addWidget(self.btn_cancel)
        ctrl.addStretch(1)
        root.addLayout(ctrl)

        # 进度 + 日志
        prog = QGridLayout()
        self.lbl_now = QLabel("当前文件：-")
        self.pb = QProgressBar()
        self.pb.setRange(0, 100)
        self.pb.setValue(0)
        self.lbl_speed = QLabel("速度：-")
        self.lbl_eta = QLabel("剩余：-")
        prog.addWidget(self.lbl_now, 0, 0, 1, 4)
        prog.addWidget(self.pb, 1, 0, 1, 4)
        prog.addWidget(self.lbl_speed, 2, 0, 1, 2)
        prog.addWidget(self.lbl_eta, 2, 2, 1, 2)
        root.addLayout(prog)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("日志输出…")
        self.log.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.log.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        root.addWidget(self.log)

        # 事件
        self.btn_browse.clicked.connect(self._choose_dir)
        self.btn_start.clicked.connect(self._start)
        self.btn_cancel.clicked.connect(self._cancel)

    def _build_input_group(self) -> QGroupBox:
        box = QGroupBox("链接与保存目录")
        lay = QGridLayout(box)

        self.ed_urls = QPlainTextEdit()
        self.ed_urls.setPlaceholderText("在此粘贴链接（支持多行，每行一个 URL）")
        self.ed_urls.setFixedHeight(100)

        self.ed_outdir = QLineEdit(str(Path.cwd()))
        self.btn_browse = QPushButton("浏览…")

        lay.addWidget(QLabel("链接"), 0, 0)
        lay.addWidget(self.ed_urls, 0, 1, 1, 3)
        lay.addWidget(QLabel("输出目录"), 1, 0)
        lay.addWidget(self.ed_outdir, 1, 1, 1, 2)
        lay.addWidget(self.btn_browse, 1, 3)
        return box

    def _build_options_group(self) -> QGroupBox:
        box = QGroupBox("下载选项")
        lay = QGridLayout(box)

        # 勾选：布尔选项
        self.cb_audio_only = QCheckBox("仅音频(MP3)")
        self.cb_embed_thumb = QCheckBox("嵌入缩略图")
        self.cb_add_meta = QCheckBox("添加元数据")
        self.cb_write_subs = QCheckBox("写入字幕")
        self.cb_auto_subs = QCheckBox("自动生成字幕(如果可)")
        self.cb_playlist = QCheckBox("下载整个播放列表")
        self.cb_merge_mp4 = QCheckBox("合并为 MP4 (可行时)")
        self.cb_no_overwrite = QCheckBox("不覆盖已存在")

        # 下拉：格式预设（单选）
        self.combo_format = QComboBox()
        self.combo_format.addItem("最佳画质 (bestvideo+bestaudio/best)",
                                  "bestvideo+bestaudio/best")
        self.combo_format.addItem("优先 MP4 的 1080p (尽量)",
                                  "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best")
        self.combo_format.addItem("小文件 360p mp4 优先",
                                  "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]/worst")

        # 多选下拉：字幕语言
        self.combo_sub_langs = MultiSelectComboBox()
        self.combo_sub_langs.add_check_items([
            ("zh-Hans", "简体中文"),
            ("zh-Hant", "繁体中文"),
            ("en", "English"),
            ("ja", "日本語"),
        ])

        # 自定义变量：key=value 每行
        self.ed_custom = QPlainTextEdit()
        self.ed_custom.setPlaceholderText(
            "高级：每行一个 key=value（会 merge 到 YoutubeDL 参数）\n"
            "示例：\n"
            "postprocessors=[{\"key\": \"FFmpegExtractAudio\", \"preferredcodec\": \"flac\"}]\n"
            "proxy=http://127.0.0.1:7890\n"
            "concurrent_fragment_downloads=5\n"
        )
        self.ed_custom.setFixedHeight(120)

        # 排列
        row = 0
        lay.addWidget(QLabel("格式预设"), row, 0)
        lay.addWidget(self.combo_format, row, 1, 1, 3); row += 1

        lay.addWidget(self.cb_audio_only, row, 0)
        lay.addWidget(self.cb_embed_thumb, row, 1)
        lay.addWidget(self.cb_add_meta, row, 2)
        lay.addWidget(self.cb_no_overwrite, row, 3); row += 1

        lay.addWidget(self.cb_write_subs, row, 0)
        lay.addWidget(self.cb_auto_subs, row, 1)
        lay.addWidget(QLabel("字幕语言(多选)"), row, 2)
        lay.addWidget(self.combo_sub_langs, row, 3); row += 1

        lay.addWidget(self.cb_playlist, row, 0)
        lay.addWidget(self.cb_merge_mp4, row, 1); row += 1

        lay.addWidget(QLabel("自定义变量"), row, 0)
        lay.addWidget(self.ed_custom, row, 1, 1, 3)
        return box

    def _build_output_group(self) -> QGroupBox:
        box = QGroupBox("输出模板与其他")
        lay = QGridLayout(box)

        self.ed_outtmpl = QLineEdit("%(title)s.%(ext)s")
        self.ed_proxy = QLineEdit("")
        self.ed_proxy.setPlaceholderText("可选：HTTP/HTTPS/SOCKS 代理，如 http://127.0.0.1:7890")

        lay.addWidget(QLabel("文件名模板(outtmpl)"), 0, 0)
        lay.addWidget(self.ed_outtmpl, 0, 1, 1, 3)
        lay.addWidget(QLabel("代理(proxy)"), 1, 0)
        lay.addWidget(self.ed_proxy, 1, 1, 1, 3)
        return box

    # ---------- 事件 ----------
    def _choose_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择输出目录", self.ed_outdir.text())
        if d:
            self.ed_outdir.setText(d)

    def _append_log(self, text: str):
        self.log.appendPlainText(text)
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())

    def _start(self):
        urls = [u.strip() for u in self.ed_urls.toPlainText().splitlines() if u.strip()]
        if not urls:
            QMessageBox.warning(self, "空链接", "请至少输入一个链接（每行一个）")
            return

        outdir = Path(self.ed_outdir.text()).expanduser().resolve()
        outdir.mkdir(parents=True, exist_ok=True)

        ydl_opts = self._collect_ydl_opts(outdir)
        # 启动线程
        self.worker = DownloadWorker(urls, ydl_opts, self)
        self.worker.progress.connect(self._on_progress)
        self.worker.status.connect(self._append_log)
        self.worker.file_changed.connect(self._on_file_changed)
        self.worker.finished_one.connect(self._on_one_finished)
        self.worker.all_done.connect(self._on_all_done)

        self.btn_start.setEnabled(False)
        self.btn_cancel.setEnabled(True)
        self._append_log("——— 开始任务 ———")
        self.worker.start()

    def _cancel(self):
        if self.worker:
            self.worker.cancel()
            self._append_log("[用户] 请求取消…")

    # ---------- worker 回调 ----------
    def _on_progress(self, percent: float, speed_hr: str, eta_sec: int):
        self.pb.setValue(int(percent))
        self.lbl_speed.setText(f"速度：{speed_hr}/s")
        self.lbl_eta.setText(f"剩余：{human_eta(eta_sec)}")

    def _on_file_changed(self, name: str):
        self.lbl_now.setText(f"当前文件：{name}")

    def _on_one_finished(self, url: str, ok: bool):
        self._append_log(("✅ 完成：" if ok else "❌ 失败：") + url)

    def _on_all_done(self):
        self._append_log("——— 全部任务完成 ———")
        self.btn_start.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        self.worker = None

    # ---------- 参数收集与解析 ----------
    def _collect_ydl_opts(self, outdir: Path) -> Dict[str, Any]:
        opts: Dict[str, Any] = {
            'outtmpl': str(outdir / self.ed_outtmpl.text().strip()),
            'concurrent_fragment_downloads': 1,  # 可根据需要调大
            'noplaylist': not self.cb_playlist.isChecked(),
            'format': self.combo_format.currentData(),
            'merge_output_format': 'mp4' if self.cb_merge_mp4.isChecked() else None,
            'overwrites': False if self.cb_no_overwrite.isChecked() else True,
        }

        # 代理
        proxy = self.ed_proxy.text().strip()
        if proxy:
            opts['proxy'] = proxy

        # 字幕
        if self.cb_write_subs.isChecked():
            opts['writesubtitles'] = True
            langs = self.combo_sub_langs.checked_keys()
            if langs:
                opts['subtitleslangs'] = langs
        if self.cb_auto_subs.isChecked():
            opts['writeautomaticsub'] = True

        # 仅音频
        postprocessors = []
        if self.cb_audio_only.isChecked():
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            })
            # 仅音频时，简化 format
            opts['format'] = 'bestaudio/best'
            opts['merge_output_format'] = None

        if self.cb_embed_thumb.isChecked():
            postprocessors.append({'key': 'EmbedThumbnail'})

        if self.cb_add_meta.isChecked():
            postprocessors.append({'key': 'FFmpegMetadata'})

        if postprocessors:
            opts['postprocessors'] = postprocessors

        # 合并自定义变量（key=value，每行一项）
        custom_text = self.ed_custom.toPlainText().strip()
        if custom_text:
            try:
                extra = self._parse_custom_kv(custom_text)
                # 后写覆盖：用户自定义优先
                opts.update(extra)
            except Exception as e:
                QMessageBox.warning(self, "自定义变量解析失败", f"{e}\n请检查 key=value 语法，或用 Python 字面量。")

        # 清理 None 值（yt-dlp API 中不需要显式 None）
        opts = {k: v for k, v in opts.items() if v is not None}
        return opts

    @staticmethod
    def _parse_custom_kv(text: str) -> Dict[str, Any]:
        """
        支持两种风格（可混合）：
            1) 简单 key=value，如   proxy=http://127.0.0.1:7890
               布尔 true/false、整数、浮点会自动转换。
            2) 复杂 Python 字面量，如 postprocessors=[{...}, {...}]
        每行一条，# 开头的行会被忽略。
        """
        res: Dict[str, Any] = {}
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                raise ValueError(f"缺少 '=' ：{line}")
            k, v = line.split('=', 1)
            k = k.strip()
            v = v.strip()
            # 尝试 Python 字面量解析
            try:
                import ast
                val = ast.literal_eval(v)
            except Exception:
                # 尝试布尔/数字/字符串
                low = v.lower()
                if low in ('true', 'false'):
                    val = (low == 'true')
                else:
                    try:
                        if '.' in v:
                            val = float(v)
                        else:
                            val = int(v)
                    except Exception:
                        val = v  # 原样字符串
            res[k] = val
        return res


# =============== 入口 =========================================
def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
