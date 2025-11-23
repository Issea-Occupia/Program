import sys
import os
import struct
import binascii
import base64
import json
from typing import Optional, Tuple

from Crypto.Cipher import AES  # pip install pycryptodome

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QListWidget, QListWidgetItem,
    QLabel, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal


# =========================
#   NCM 解码核心逻辑
# =========================

CORE_KEY = bytes.fromhex("687A4852416d736f356b496e62617857")
META_KEY = bytes.fromhex("2331346C6A6B5F215C5D2630553C2728")


def pkcs7_unpad(data: bytes) -> bytes:
    """简单 PKCS7 去填充。"""
    if not data:
        return data
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 16:
        # 容错：不符合 PKCS7 直接原样返回
        return data
    return data[:-pad_len]


def parse_ncm_file(path: str) -> Tuple[dict, bytes]:
    """
    解析并解密一个 .ncm 文件，返回：
        meta: 字典，包含 musicName / format / artist / album 等
        audio_data: 解密后的完整音频字节（mp3 或 flac 等）

    如果文件损坏或不是合法 ncm，会抛出异常。
    """
    with open(path, "rb") as f:
        # 1. 校验头部魔数
        header = f.read(8)
        # 对应 hex: 4354454e4644414d -> "CTENFDAM"，
        # 实际上是 2 个 uint32 小端 "NETC" + "MADF"
        if binascii.b2a_hex(header) != b"4354454e4644414d":
            raise ValueError("此 ncm 文件已损坏（头部魔数不匹配）")

        # 2. 跳过 2 个保留字节
        f.seek(2, os.SEEK_CUR)

        # 3. 读取加密的密钥区
        key_len_bytes = f.read(4)
        if len(key_len_bytes) != 4:
            raise ValueError("读取 key 长度失败")
        key_len = struct.unpack("<I", key_len_bytes)[0]

        key_data = bytearray(f.read(key_len))
        if len(key_data) != key_len:
            raise ValueError("读取 key 数据不完整")

        # 先整体 XOR 0x64
        for i in range(len(key_data)):
            key_data[i] ^= 0x64

        # 用 CORE_KEY 做 AES-ECB 解密
        cipher_core = AES.new(CORE_KEY, AES.MODE_ECB)
        decrypted_key = cipher_core.decrypt(bytes(key_data))
        decrypted_key = pkcs7_unpad(decrypted_key)
        # 前 17 字节固定无用前缀
        real_key = decrypted_key[17:]

        # 4. 构造 key_box（RC4 风格调度）
        key_box = bytearray(range(256))
        key_len_real = len(real_key)
        if key_len_real == 0:
            raise ValueError("解出的 key 长度为 0")

        last_byte = 0
        key_index = 0
        for i in range(256):
            swap = key_box[i]
            last_byte = (swap + last_byte + real_key[key_index]) & 0xFF
            key_index += 1
            if key_index >= key_len_real:
                key_index = 0
            key_box[i] = key_box[last_byte]
            key_box[last_byte] = swap

        # 5. 读取并解密元数据 meta 区
        meta_len_bytes = f.read(4)
        if len(meta_len_bytes) != 4:
            raise ValueError("读取 meta 长度失败")
        meta_len = struct.unpack("<I", meta_len_bytes)[0]

        if meta_len > 0:
            meta_raw = bytearray(f.read(meta_len))
            if len(meta_raw) != meta_len:
                raise ValueError("读取 meta 数据不完整")

            # XOR 0x63
            for i in range(len(meta_raw)):
                meta_raw[i] ^= 0x63

            # 前 22 字节为标识，后面是 base64
            meta_b64_part = bytes(meta_raw[22:])
            meta_decoded = base64.b64decode(meta_b64_part)

            cipher_meta = AES.new(META_KEY, AES.MODE_ECB)
            meta_plain = cipher_meta.decrypt(meta_decoded)
            meta_plain = pkcs7_unpad(meta_plain)

            # 这里实际是 "label:JSON" 之类，泛化成找第一个冒号
            try:
                text = meta_plain.decode("utf-8", errors="ignore")
            except UnicodeDecodeError:
                text = meta_plain.decode("utf-8", errors="ignore")

            colon_pos = text.find(":")
            if colon_pos != -1:
                json_str = text[colon_pos + 1 :]
            else:
                json_str = text

            meta_obj = json.loads(json_str)

            # 有些是 dj 格式，真正信息在 mainMusic 里
            if isinstance(meta_obj, dict) and "mainMusic" in meta_obj:
                meta = meta_obj["mainMusic"]
            else:
                meta = meta_obj
        else:
            meta = {}

        # 6. 跳过 crc32 / 一些保留字段 / 封面数据
        _crc32 = f.read(4)
        f.seek(5, os.SEEK_CUR)  # 保留 5 字节
        img_size_bytes = f.read(4)
        if len(img_size_bytes) != 4:
            raise ValueError("读取封面大小失败")
        img_size = struct.unpack("<I", img_size_bytes)[0]
        _img_data = f.read(img_size)  # 封面图，可以不用用它

        # 7. 解音频区：分块读取 + RC4 式异或
        audio_chunks = []
        while True:
            chunk = bytearray(f.read(0x8000))
            if not chunk:
                break
            chunk_len = len(chunk)
            for i in range(1, chunk_len + 1):
                j = i & 0xFF
                # 对应原脚本里的：
                # chunk[i-1] ^= key_box[(key_box[j] + key_box[(key_box[j] + j) & 0xff]) & 0xff]
                idx = (key_box[j] + key_box[(key_box[j] + j) & 0xFF]) & 0xFF
                chunk[i - 1] ^= key_box[idx]
            audio_chunks.append(bytes(chunk))

        audio_data = b"".join(audio_chunks)

        return meta, audio_data


def decrypt_ncm_to_file(in_path: str, out_dir: str) -> str:
    """
    解密单个 ncm 文件并写入输出目录。
    返回实际输出的文件路径。
    """
    meta, audio_data = parse_ncm_file(in_path)

    # 歌曲名 / 格式 / 歌手 / 专辑
    music_name = meta.get("musicName") or os.path.splitext(os.path.basename(in_path))[0]
    ext = meta.get("format") or "mp3"
    # 防止文件名里有不合法字符，做个简单清理
    def clean(name: str) -> str:
        bad = r'\/:*?"<>|'
        for ch in bad:
            name = name.replace(ch, "_")
        return name.strip() or "untitled"

    safe_name = clean(music_name)
    out_filename = f"{safe_name}.{ext}"
    out_path = os.path.join(out_dir, out_filename)

    # 如已存在，加个序号防冲突
    base_name, base_ext = os.path.splitext(out_filename)
    counter = 1
    while os.path.exists(out_path):
        out_filename = f"{base_name}_{counter}{base_ext}"
        out_path = os.path.join(out_dir, out_filename)
        counter += 1

    with open(out_path, "wb") as out_f:
        out_f.write(audio_data)

    return out_path


# =========================
#   后台线程：批量转换
# =========================

class ConvertWorker(QThread):
    """
    在后台线程中执行批量 NCM 转换，避免卡死 UI。
    """
    progress = pyqtSignal(int, int)           # 已完成数，总数
    file_done = pyqtSignal(str, str)          # in_path, out_path 或错误信息
    finished_all = pyqtSignal()

    def __init__(self, files: list[str], out_dir: str):
        super().__init__()
        self.files = files
        self.out_dir = out_dir
        self._stop = False

    def run(self):
        total = len(self.files)
        done = 0
        for in_path in self.files:
            if self._stop:
                break
            try:
                out_path = decrypt_ncm_to_file(in_path, self.out_dir)
                self.file_done.emit(in_path, out_path)
            except Exception as e:
                self.file_done.emit(in_path, f"ERROR: {e}")
            done += 1
            self.progress.emit(done, total)
        self.finished_all.emit()

    def stop(self):
        self._stop = True


# =========================
#   PyQt 主窗口
# =========================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NCM 转码器 (PyQt6)")
        self.resize(700, 500)

        self.selected_files: list[str] = []
        self.output_dir: Optional[str] = None
        self.worker: Optional[ConvertWorker] = None

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        # 顶部按钮区域
        btn_layout = QHBoxLayout()
        self.btn_choose_files = QPushButton("选择 NCM 文件")
        self.btn_choose_dir = QPushButton("选择输出文件夹")
        self.btn_start = QPushButton("开始转换")

        btn_layout.addWidget(self.btn_choose_files)
        btn_layout.addWidget(self.btn_choose_dir)
        btn_layout.addWidget(self.btn_start)

        # 显示输出目录
        self.label_outdir = QLabel("输出目录：未选择")
        self.label_outdir.setWordWrap(True)

        # 文件列表
        self.list_files = QListWidget()

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.label_outdir)
        main_layout.addWidget(self.list_files)
        main_layout.addWidget(self.progress_bar)

        # 绑定事件
        self.btn_choose_files.clicked.connect(self.choose_files)
        self.btn_choose_dir.clicked.connect(self.choose_output_dir)
        self.btn_start.clicked.connect(self.start_convert)

    # ---------- 事件处理 ----------

    def choose_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择 NCM 文件",
            "",
            "NCM 文件 (*.ncm);;所有文件 (*.*)",
        )
        if not files:
            return

        self.selected_files = files
        self.list_files.clear()
        for path in self.selected_files:
            item = QListWidgetItem(path)
            self.list_files.addItem(item)

    def choose_output_dir(self):
        out_dir = QFileDialog.getExistingDirectory(self, "选择输出文件夹", "")
        if out_dir:
            self.output_dir = out_dir
            self.label_outdir.setText(f"输出目录：{out_dir}")

    def start_convert(self):
        if not self.selected_files:
            QMessageBox.warning(self, "提示", "请先选择至少一个 .ncm 文件。")
            return
        if not self.output_dir:
            QMessageBox.warning(self, "提示", "请先选择输出文件夹。")
            return
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(self, "提示", "正在转换中，请稍候……")
            return

        # 重置进度条和列表状态显示
        self.progress_bar.setValue(0)
        for i in range(self.list_files.count()):
            item = self.list_files.item(i)
            item.setText(self.selected_files[i])  # 恢复纯路径

        # 启动后台线程
        self.worker = ConvertWorker(self.selected_files, self.output_dir)
        self.worker.progress.connect(self.on_progress)
        self.worker.file_done.connect(self.on_file_done)
        self.worker.finished_all.connect(self.on_finished_all)
        self.worker.start()
        self.btn_start.setEnabled(False)

    # ---------- 后台线程信号回调 ----------

    def on_progress(self, done: int, total: int):
        if total <= 0:
            self.progress_bar.setValue(0)
            return
        percent = int(done * 100 / total)
        self.progress_bar.setValue(percent)

    def on_file_done(self, in_path: str, result: str):
        # 更新对应列表项文本（简单找路径匹配）
        for i in range(self.list_files.count()):
            item = self.list_files.item(i)
            if item.text().startswith(in_path):
                if result.startswith("ERROR:"):
                    item.setText(f"{in_path}  ->  {result}")
                else:
                    item.setText(f"{in_path}  ->  {result}")
                break

    def on_finished_all(self):
        self.btn_start.setEnabled(True)
        QMessageBox.information(self, "完成", "全部文件转换完成！")


# =========================
#   程序入口
# =========================

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
