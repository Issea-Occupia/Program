from typing import List
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QComboBox

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

    def add_check_items(self, items: List[tuple[str, str]]):
        # items: [(key, label)]
        for key, label in items:
            self.addItem(label, userData=key)
            idx = self.model().index(self.count()-1, 0)
            item = self.model().itemFromIndex(idx)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        self._refresh_text()

    def _refresh_text(self):
        keys = self.checked_keys()
        labels = []
        for i in range(self.count()):
            if self.model().item(i).data(Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked:
                labels.append(self.itemText(i))
        self.lineEdit().setText(
            ", ".join(labels) if labels else ""
        )

    def checked_keys(self) -> List[str]:
        res = []
        for i in range(self.count()):
            item = self.model().item(i)
            if item.data(Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked:
                res.append(self.itemData(i))  # userData
        return res

    def showPopup(self):
        super().showPopup()
        # 弹出后，点击项目切换勾选
        view = self.view()
        view.pressed.connect(self._handle_item_pressed)

    def _handle_item_pressed(self, index):
        item = self.model().itemFromIndex(index)
        if item is None:
            return
        state = item.data(Qt.ItemDataRole.CheckStateRole)
        item.setData(
            Qt.CheckState.Unchecked if state == Qt.CheckState.Checked else Qt.CheckState.Checked,
            Qt.ItemDataRole.CheckStateRole,
        )
        self._refresh_text()

