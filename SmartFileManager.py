#!/usr/bin/env python3
"""
SmartFileManager - Enterprise-grade file management application
with smart rename, docking system, dark/light themes
"""

import sys
import os
import re
import shutil
import subprocess
import platform
import datetime
import mimetypes
from pathlib import Path
from typing import Optional, List, Dict

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDockWidget,
    QTreeView, QTableView, QListView, QSplitter,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QPlainTextEdit,
    QComboBox, QCheckBox, QRadioButton, QGroupBox,
    QFileSystemModel, QAbstractItemView, QHeaderView,
    QStatusBar, QToolBar, QMenuBar, QMenu,
    QDialog, QDialogButtonBox, QMessageBox, QInputDialog,
    QProgressBar, QTabWidget, QFrame, QScrollArea,
    QSizePolicy, QSpacerItem, QStyledItemDelegate,
    QTabBar
)
from PySide6.QtCore import (
    Qt, QDir, QFileInfo, QFile, QModelIndex, QSortFilterProxyModel,
    QThread, Signal, QTimer, QSize, QPoint, QRect,
    QStandardPaths, QMimeData, QItemSelectionModel,
    QDateTime, QFileSystemWatcher, QAbstractTableModel,
    QSettings
)
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import (
    QIcon, QPixmap, QColor, QPalette, QFont, QFontMetrics,
    QAction, QKeySequence, QStandardItemModel, QStandardItem,
    QDesktopServices, QDrag, QCursor, QPainter, QBrush, QPen
)


# ─────────────────────────────────────────────
#  THEME SYSTEM
# ─────────────────────────────────────────────

DARK_QSS = """
/* ── GLOBAL ─────────────────────────────────────────── */
* {
    font-family: "Segoe UI", "SF Pro Display", "Ubuntu", sans-serif;
    font-size: 13px;
    color: #E2E8F0;
    outline: none;
}
QMainWindow, QDialog {
    background-color: #0F1117;
}
QWidget {
    background-color: #0F1117;
    color: #E2E8F0;
}

/* ── MENUBAR ─────────────────────────────────────────── */
QMenuBar {
    background-color: #1A1D2E;
    color: #E2E8F0;
    border-bottom: 1px solid #2D3748;
    padding: 2px 0px;
}
QMenuBar::item {
    background: transparent;
    padding: 6px 12px;
    border-radius: 4px;
}
QMenuBar::item:selected, QMenuBar::item:pressed {
    background-color: #2D3748;
    color: #7C3AED;
}
QMenu {
    background-color: #1A1D2E;
    border: 1px solid #2D3748;
    border-radius: 8px;
    padding: 4px;
}
QMenu::item {
    padding: 8px 20px 8px 12px;
    border-radius: 5px;
    margin: 1px 2px;
}
QMenu::item:selected {
    background-color: #2D3748;
    color: #A78BFA;
}
QMenu::separator {
    height: 1px;
    background-color: #2D3748;
    margin: 4px 8px;
}

/* ── TOOLBAR ─────────────────────────────────────────── */
QToolBar {
    background-color: #1A1D2E;
    border-bottom: 1px solid #2D3748;
    spacing: 4px;
    padding: 4px 8px;
}
QToolBar::separator {
    width: 1px;
    background-color: #2D3748;
    margin: 4px 6px;
}
QToolButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 5px 8px;
    color: #CBD5E1;
}
QToolButton:hover {
    background-color: #2D3748;
    border-color: #4B5563;
    color: #E2E8F0;
}
QToolButton:pressed {
    background-color: #374151;
}
QToolButton:checked {
    background-color: #2D3748;
    border-color: #7C3AED;
    color: #A78BFA;
}

/* ── STATUSBAR ───────────────────────────────────────── */
QStatusBar {
    background-color: #1A1D2E;
    border-top: 1px solid #2D3748;
    color: #94A3B8;
    padding: 0px 8px;
}
QStatusBar::item {
    border: none;
}

/* ── DOCKWIDGET ──────────────────────────────────────── */
QDockWidget {
    titlebar-close-icon: url(none);
    background-color: #0F1117;
    color: #E2E8F0;
}
QDockWidget::title {
    background-color: #1A1D2E;
    border-bottom: 1px solid #2D3748;
    padding: 8px 12px;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #94A3B8;
}
QDockWidget::close-button, QDockWidget::float-button {
    background: transparent;
    border: none;
    padding: 2px;
    border-radius: 3px;
}
QDockWidget::close-button:hover, QDockWidget::float-button:hover {
    background-color: #2D3748;
}

/* ── TREEVIEW ────────────────────────────────────────── */
QTreeView {
    background-color: #0F1117;
    border: none;
    outline: none;
    selection-background-color: transparent;
    alternate-background-color: #111827;
}
QTreeView::item {
    height: 28px;
    padding-left: 4px;
    border-radius: 5px;
    margin: 1px 4px;
}
QTreeView::item:hover {
    background-color: #1E2435;
}
QTreeView::item:selected {
    background-color: #1E293B;
    color: #A78BFA;
}
QTreeView::item:selected:hover {
    background-color: #243047;
}
QTreeView::branch {
    background-color: transparent;
}
QTreeView::branch:has-siblings:!adjoins-item {
    border-image: none;
}
QTreeView::branch:open:has-children {
    image: none;
}
QTreeView::branch:closed:has-children {
    image: none;
}

/* ── TABLEVIEW ───────────────────────────────────────── */
QTableView {
    background-color: #0F1117;
    border: none;
    outline: none;
    gridline-color: #1A1D2E;
    selection-background-color: #1E293B;
    selection-color: #E2E8F0;
    alternate-background-color: #111827;
}
QTableView::item {
    padding: 4px 8px;
    border-bottom: 1px solid #1A1D2E;
}
QTableView::item:hover {
    background-color: #1E2435;
}
QTableView::item:selected {
    background-color: #1E293B;
    color: #A78BFA;
}
QHeaderView::section {
    background-color: #1A1D2E;
    color: #94A3B8;
    padding: 8px 10px;
    border: none;
    border-right: 1px solid #2D3748;
    border-bottom: 1px solid #2D3748;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
QHeaderView::section:hover {
    background-color: #2D3748;
    color: #E2E8F0;
}
QHeaderView::section:first {
    border-left: none;
}

/* ── SCROLLBAR ───────────────────────────────────────── */
QScrollBar:vertical {
    background-color: #0F1117;
    width: 8px;
    border-radius: 4px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background-color: #2D3748;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #4B5563;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar:horizontal {
    background-color: #0F1117;
    height: 8px;
    border-radius: 4px;
    margin: 0;
}
QScrollBar::handle:horizontal {
    background-color: #2D3748;
    border-radius: 4px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #4B5563;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

/* ── BUTTONS ─────────────────────────────────────────── */
QPushButton {
    background-color: #1E293B;
    border: 1px solid #2D3748;
    border-radius: 7px;
    padding: 7px 16px;
    color: #E2E8F0;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #2D3748;
    border-color: #4B5563;
}
QPushButton:pressed {
    background-color: #374151;
}
QPushButton:disabled {
    background-color: #1A1D2E;
    color: #4B5563;
    border-color: #2D3748;
}
QPushButton#primaryBtn {
    background-color: #7C3AED;
    border: 1px solid #6D28D9;
    color: white;
    font-weight: 600;
}
QPushButton#primaryBtn:hover {
    background-color: #8B5CF6;
    border-color: #7C3AED;
}
QPushButton#primaryBtn:pressed {
    background-color: #6D28D9;
}
QPushButton#dangerBtn {
    background-color: #991B1B;
    border: 1px solid #7F1D1D;
    color: #FCA5A5;
}
QPushButton#dangerBtn:hover {
    background-color: #B91C1C;
}
QPushButton#successBtn {
    background-color: #065F46;
    border: 1px solid #064E3B;
    color: #6EE7B7;
}
QPushButton#successBtn:hover {
    background-color: #047857;
}

/* ── LINEEDIT ────────────────────────────────────────── */
QLineEdit {
    background-color: #1A1D2E;
    border: 1px solid #2D3748;
    border-radius: 7px;
    padding: 7px 12px;
    color: #E2E8F0;
    selection-background-color: #7C3AED;
}
QLineEdit:focus {
    border-color: #7C3AED;
    background-color: #1E2435;
}
QLineEdit:disabled {
    background-color: #111827;
    color: #4B5563;
}

/* ── COMBOBOX ────────────────────────────────────────── */
QComboBox {
    background-color: #1A1D2E;
    border: 1px solid #2D3748;
    border-radius: 7px;
    padding: 7px 12px;
    color: #E2E8F0;
    min-width: 100px;
}
QComboBox:hover {
    border-color: #4B5563;
}
QComboBox:focus {
    border-color: #7C3AED;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #94A3B8;
    width: 0;
    height: 0;
}
QComboBox QAbstractItemView {
    background-color: #1A1D2E;
    border: 1px solid #2D3748;
    border-radius: 7px;
    selection-background-color: #2D3748;
    color: #E2E8F0;
    padding: 4px;
}

/* ── TEXTEDIT / PLAINTEXTEDIT ────────────────────────── */
QTextEdit, QPlainTextEdit {
    background-color: #111827;
    border: 1px solid #2D3748;
    border-radius: 7px;
    padding: 8px;
    color: #CBD5E1;
    selection-background-color: #7C3AED;
}
QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #7C3AED;
}

/* ── CHECKBOX ────────────────────────────────────────── */
QCheckBox {
    spacing: 8px;
    color: #CBD5E1;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #4B5563;
    background-color: #1A1D2E;
}
QCheckBox::indicator:checked {
    background-color: #7C3AED;
    border-color: #7C3AED;
}
QCheckBox::indicator:hover {
    border-color: #7C3AED;
}

/* ── GROUPBOX ────────────────────────────────────────── */
QGroupBox {
    border: 1px solid #2D3748;
    border-radius: 8px;
    margin-top: 14px;
    padding-top: 8px;
    color: #94A3B8;
    font-weight: 600;
    font-size: 12px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    left: 12px;
    color: #7C3AED;
}

/* ── TABWIDGET ───────────────────────────────────────── */
QTabWidget::pane {
    border: 1px solid #2D3748;
    border-radius: 8px;
    background-color: #111827;
    top: -1px;
}
QTabBar::tab {
    background-color: #1A1D2E;
    border: 1px solid #2D3748;
    border-bottom: none;
    border-radius: 6px 6px 0 0;
    padding: 8px 18px;
    color: #94A3B8;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #111827;
    color: #A78BFA;
    border-bottom: 1px solid #111827;
}
QTabBar::tab:hover:!selected {
    background-color: #2D3748;
    color: #CBD5E1;
}

/* ── PROGRESSBAR ─────────────────────────────────────── */
QProgressBar {
    border: 1px solid #2D3748;
    border-radius: 5px;
    background-color: #1A1D2E;
    text-align: center;
    color: #E2E8F0;
    height: 8px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #7C3AED, stop:1 #06B6D4);
    border-radius: 4px;
}

/* ── FRAME ───────────────────────────────────────────── */
QFrame[frameShape="4"], QFrame[frameShape="5"] {
    color: #2D3748;
}

/* ── SPLITTER ────────────────────────────────────────── */
QSplitter::handle {
    background-color: #2D3748;
    width: 2px;
    height: 2px;
}
QSplitter::handle:hover {
    background-color: #7C3AED;
}

/* ── ADDRESS BAR SPECIAL ─────────────────────────────── */
QLineEdit#addressBar {
    background-color: #111827;
    border: 1px solid #2D3748;
    border-radius: 8px;
    padding: 6px 14px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
    color: #A78BFA;
}
QLineEdit#addressBar:focus {
    border-color: #7C3AED;
    color: #E2E8F0;
}

/* ── RENAME PANEL ────────────────────────────────────── */
QWidget#renamePanel {
    background-color: #111827;
    border: 1px solid #2D3748;
    border-radius: 10px;
}
QLabel#sectionTitle {
    color: #94A3B8;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}
QLabel#previewLabel {
    background-color: #1A1D2E;
    border: 1px solid #2D3748;
    border-radius: 6px;
    padding: 4px 10px;
    color: #6EE7B7;
    font-family: "Consolas", monospace;
}
QLabel#arrowLabel {
    color: #7C3AED;
    font-size: 16px;
}

/* ── LOG PANEL ───────────────────────────────────────── */
QPlainTextEdit#logView {
    background-color: #0A0D16;
    border: none;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
    line-height: 1.6;
    color: #64748B;
    padding: 8px 10px;
}
"""


LIGHT_QSS = """
/* ── GLOBAL ─────────────────────────────────────────── */
* {
    font-family: "Segoe UI", "SF Pro Display", "Ubuntu", sans-serif;
    font-size: 13px;
    color: #1E293B;
    outline: none;
}
QMainWindow, QDialog {
    background-color: #F8FAFC;
}
QWidget {
    background-color: #F8FAFC;
    color: #1E293B;
}

/* ── MENUBAR ─────────────────────────────────────────── */
QMenuBar {
    background-color: #FFFFFF;
    color: #1E293B;
    border-bottom: 1px solid #E2E8F0;
    padding: 2px 0px;
}
QMenuBar::item {
    background: transparent;
    padding: 6px 12px;
    border-radius: 4px;
}
QMenuBar::item:selected, QMenuBar::item:pressed {
    background-color: #F1F5F9;
    color: #7C3AED;
}
QMenu {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 4px;
}
QMenu::item {
    padding: 8px 20px 8px 12px;
    border-radius: 5px;
    margin: 1px 2px;
}
QMenu::item:selected {
    background-color: #F1F5F9;
    color: #7C3AED;
}
QMenu::separator {
    height: 1px;
    background-color: #E2E8F0;
    margin: 4px 8px;
}

/* ── TOOLBAR ─────────────────────────────────────────── */
QToolBar {
    background-color: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    spacing: 4px;
    padding: 4px 8px;
}
QToolBar::separator {
    width: 1px;
    background-color: #E2E8F0;
    margin: 4px 6px;
}
QToolButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 5px 8px;
    color: #64748B;
}
QToolButton:hover {
    background-color: #F1F5F9;
    border-color: #CBD5E1;
    color: #1E293B;
}
QToolButton:pressed {
    background-color: #E2E8F0;
}
QToolButton:checked {
    background-color: #EDE9FE;
    border-color: #7C3AED;
    color: #7C3AED;
}

/* ── STATUSBAR ───────────────────────────────────────── */
QStatusBar {
    background-color: #FFFFFF;
    border-top: 1px solid #E2E8F0;
    color: #64748B;
    padding: 0px 8px;
}

/* ── DOCKWIDGET ──────────────────────────────────────── */
QDockWidget {
    background-color: #F8FAFC;
    color: #1E293B;
}
QDockWidget::title {
    background-color: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    padding: 8px 12px;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #64748B;
}
QDockWidget::close-button, QDockWidget::float-button {
    background: transparent;
    border: none;
    padding: 2px;
    border-radius: 3px;
}
QDockWidget::close-button:hover, QDockWidget::float-button:hover {
    background-color: #F1F5F9;
}

/* ── TREEVIEW ────────────────────────────────────────── */
QTreeView {
    background-color: #F8FAFC;
    border: none;
    outline: none;
    selection-background-color: transparent;
    alternate-background-color: #F1F5F9;
}
QTreeView::item {
    height: 28px;
    padding-left: 4px;
    border-radius: 5px;
    margin: 1px 4px;
}
QTreeView::item:hover {
    background-color: #F1F5F9;
}
QTreeView::item:selected {
    background-color: #EDE9FE;
    color: #7C3AED;
}
QTreeView::item:selected:hover {
    background-color: #DDD6FE;
}

/* ── TABLEVIEW ───────────────────────────────────────── */
QTableView {
    background-color: #F8FAFC;
    border: none;
    outline: none;
    gridline-color: #F1F5F9;
    selection-background-color: #EDE9FE;
    selection-color: #1E293B;
    alternate-background-color: #F1F5F9;
}
QTableView::item {
    padding: 4px 8px;
    border-bottom: 1px solid #F1F5F9;
}
QTableView::item:hover {
    background-color: #F1F5F9;
}
QTableView::item:selected {
    background-color: #EDE9FE;
    color: #7C3AED;
}
QHeaderView::section {
    background-color: #FFFFFF;
    color: #64748B;
    padding: 8px 10px;
    border: none;
    border-right: 1px solid #E2E8F0;
    border-bottom: 1px solid #E2E8F0;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
QHeaderView::section:hover {
    background-color: #F1F5F9;
    color: #1E293B;
}

/* ── SCROLLBAR ───────────────────────────────────────── */
QScrollBar:vertical {
    background-color: #F8FAFC;
    width: 8px;
    border-radius: 4px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background-color: #CBD5E1;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #94A3B8;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background-color: #F8FAFC;
    height: 8px;
    border-radius: 4px;
    margin: 0;
}
QScrollBar::handle:horizontal {
    background-color: #CBD5E1;
    border-radius: 4px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover { background-color: #94A3B8; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* ── BUTTONS ─────────────────────────────────────────── */
QPushButton {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 7px;
    padding: 7px 16px;
    color: #1E293B;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #F1F5F9;
    border-color: #94A3B8;
}
QPushButton:pressed {
    background-color: #E2E8F0;
}
QPushButton:disabled {
    background-color: #F8FAFC;
    color: #CBD5E1;
    border-color: #E2E8F0;
}
QPushButton#primaryBtn {
    background-color: #7C3AED;
    border: 1px solid #6D28D9;
    color: white;
    font-weight: 600;
}
QPushButton#primaryBtn:hover {
    background-color: #8B5CF6;
}
QPushButton#primaryBtn:pressed {
    background-color: #6D28D9;
}
QPushButton#dangerBtn {
    background-color: #FEF2F2;
    border: 1px solid #FECACA;
    color: #EF4444;
}
QPushButton#dangerBtn:hover {
    background-color: #FEE2E2;
}
QPushButton#successBtn {
    background-color: #F0FDF4;
    border: 1px solid #BBF7D0;
    color: #16A34A;
}
QPushButton#successBtn:hover {
    background-color: #DCFCE7;
}

/* ── LINEEDIT ────────────────────────────────────────── */
QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 7px;
    padding: 7px 12px;
    color: #1E293B;
    selection-background-color: #7C3AED;
    selection-color: white;
}
QLineEdit:focus {
    border-color: #7C3AED;
    background-color: #FEFEFE;
}
QLineEdit:disabled {
    background-color: #F8FAFC;
    color: #94A3B8;
}

/* ── COMBOBOX ────────────────────────────────────────── */
QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 7px;
    padding: 7px 12px;
    color: #1E293B;
}
QComboBox:hover { border-color: #94A3B8; }
QComboBox:focus { border-color: #7C3AED; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox::down-arrow {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #64748B;
    width: 0; height: 0;
}
QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 7px;
    selection-background-color: #F1F5F9;
    color: #1E293B;
    padding: 4px;
}

/* ── TEXTEDIT / PLAINTEXTEDIT ────────────────────────── */
QTextEdit, QPlainTextEdit {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 7px;
    padding: 8px;
    color: #334155;
    selection-background-color: #7C3AED;
    selection-color: white;
}
QTextEdit:focus, QPlainTextEdit:focus { border-color: #7C3AED; }

/* ── CHECKBOX ────────────────────────────────────────── */
QCheckBox { spacing: 8px; color: #334155; }
QCheckBox::indicator {
    width: 16px; height: 16px;
    border-radius: 4px;
    border: 1px solid #CBD5E1;
    background-color: #FFFFFF;
}
QCheckBox::indicator:checked {
    background-color: #7C3AED;
    border-color: #7C3AED;
}
QCheckBox::indicator:hover { border-color: #7C3AED; }

/* ── GROUPBOX ────────────────────────────────────────── */
QGroupBox {
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    margin-top: 14px;
    padding-top: 8px;
    color: #64748B;
    font-weight: 600;
    font-size: 12px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    left: 12px;
    color: #7C3AED;
}

/* ── TABWIDGET ───────────────────────────────────────── */
QTabWidget::pane {
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    background-color: #FFFFFF;
    top: -1px;
}
QTabBar::tab {
    background-color: #F1F5F9;
    border: 1px solid #E2E8F0;
    border-bottom: none;
    border-radius: 6px 6px 0 0;
    padding: 8px 18px;
    color: #64748B;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #FFFFFF;
    color: #7C3AED;
    border-bottom: 1px solid #FFFFFF;
}
QTabBar::tab:hover:!selected {
    background-color: #E2E8F0;
    color: #1E293B;
}

/* ── PROGRESSBAR ─────────────────────────────────────── */
QProgressBar {
    border: 1px solid #E2E8F0;
    border-radius: 5px;
    background-color: #F1F5F9;
    text-align: center;
    color: #1E293B;
    height: 8px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #7C3AED, stop:1 #06B6D4);
    border-radius: 4px;
}

/* ── SPLITTER ────────────────────────────────────────── */
QSplitter::handle {
    background-color: #E2E8F0;
    width: 2px; height: 2px;
}
QSplitter::handle:hover { background-color: #7C3AED; }

/* ── ADDRESS BAR ─────────────────────────────────────── */
QLineEdit#addressBar {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 6px 14px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
    color: #7C3AED;
}
QLineEdit#addressBar:focus {
    border-color: #7C3AED;
    color: #1E293B;
}

/* ── RENAME PANEL ────────────────────────────────────── */
QWidget#renamePanel {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
}
QLabel#sectionTitle {
    color: #64748B;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.8px;
}
QLabel#previewLabel {
    background-color: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 6px;
    padding: 4px 10px;
    color: #16A34A;
    font-family: "Consolas", monospace;
}
QLabel#arrowLabel {
    color: #7C3AED;
    font-size: 16px;
}

/* ── LOG PANEL ───────────────────────────────────────── */
QPlainTextEdit#logView {
    background-color: #F8FAFC;
    border: none;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
    line-height: 1.6;
    color: #64748B;
    padding: 8px 10px;
}
"""


# ─────────────────────────────────────────────
#  DRIVE TREE MODEL
# ─────────────────────────────────────────────

class DriveTreeModel(QStandardItemModel):
    """Custom model showing only drives and their folders, using OS file system icons."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._icon_provider = __import__(
            "PySide6.QtWidgets", fromlist=["QFileIconProvider"]
        ).QFileIconProvider()
        self.setHorizontalHeaderLabels(["Location"])
        self._populate()

    def _os_icon(self, path: str) -> QIcon:
        """Return the OS-native icon for a given path."""
        info = QFileInfo(path)
        if info.exists():
            return self._icon_provider.icon(info)
        # fallback: generic folder/drive icon from provider
        return self._icon_provider.icon(
            __import__("PySide6.QtWidgets", fromlist=["QFileIconProvider"])
            .QFileIconProvider.IconType.Folder
        )

    def _drive_icon(self) -> QIcon:
        from PySide6.QtWidgets import QFileIconProvider
        return self._icon_provider.icon(QFileIconProvider.IconType.Drive)

    def _folder_icon(self) -> QIcon:
        from PySide6.QtWidgets import QFileIconProvider
        return self._icon_provider.icon(QFileIconProvider.IconType.Folder)

    def _populate(self):
        self.clear()
        self.setHorizontalHeaderLabels(["Location"])

        # ── Quick access header ──────────────────────────
        quick = QStandardItem("  QUICK ACCESS")
        quick.setEditable(False)
        quick.setData("header", Qt.UserRole)
        font = quick.font()
        font.setBold(True)
        font.setPointSize(10)
        quick.setFont(font)
        self.appendRow(quick)

        specials = [
            (QStandardPaths.HomeLocation,      "Home"),
            (QStandardPaths.DesktopLocation,   "Desktop"),
            (QStandardPaths.DownloadLocation,  "Downloads"),
            (QStandardPaths.DocumentsLocation, "Documents"),
            (QStandardPaths.PicturesLocation,  "Pictures"),
            (QStandardPaths.MusicLocation,     "Music"),
            (QStandardPaths.MoviesLocation,    "Videos"),
        ]
        for loc_enum, label in specials:
            locs = QStandardPaths.standardLocations(loc_enum)
            if locs:
                path = locs[0]
                if os.path.exists(path):
                    item = QStandardItem(label)
                    item.setEditable(False)
                    item.setIcon(self._os_icon(path))
                    item.setData(path, Qt.UserRole + 1)
                    item.setData("shortcut", Qt.UserRole)
                    quick.appendRow(item)

        # ── Drives header ────────────────────────────────
        drives_header = QStandardItem("  DRIVES")
        drives_header.setEditable(False)
        drives_header.setData("header", Qt.UserRole)
        font2 = drives_header.font()
        font2.setBold(True)
        font2.setPointSize(10)
        drives_header.setFont(font2)
        self.appendRow(drives_header)

        if platform.system() == "Windows":
            import string
            import ctypes
            for letter in string.ascii_uppercase:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    label = self._get_windows_drive_label(letter, ctypes)
                    item = QStandardItem(label)
                    item.setEditable(False)
                    item.setIcon(self._os_icon(drive))
                    item.setData(drive, Qt.UserRole + 1)
                    item.setData("drive", Qt.UserRole)
                    self._add_subfolders(item, drive)
                    drives_header.appendRow(item)
        else:
            # Linux/macOS: read actual filesystem labels via /proc/mounts or blkid
            mount_labels = self._get_unix_mount_labels()

            for path, fallback_label in [("/", "Root (/)"), ("/home", "/home"), ("/tmp", "/tmp")]:
                if os.path.exists(path):
                    label = mount_labels.get(path, fallback_label)
                    item = QStandardItem(label)
                    item.setEditable(False)
                    item.setIcon(self._drive_icon())
                    item.setData(path, Qt.UserRole + 1)
                    item.setData("drive", Qt.UserRole)
                    self._add_subfolders(item, path)
                    drives_header.appendRow(item)

            for mount_base in ["/media", "/mnt"]:
                if os.path.exists(mount_base):
                    try:
                        for entry in os.scandir(mount_base):
                            if entry.is_dir():
                                label = mount_labels.get(entry.path, entry.name)
                                item = QStandardItem(label)
                                item.setEditable(False)
                                item.setIcon(self._os_icon(entry.path))
                                item.setData(entry.path, Qt.UserRole + 1)
                                item.setData("removable", Qt.UserRole)
                                self._add_subfolders(item, entry.path)
                                drives_header.appendRow(item)
                    except PermissionError:
                        pass

    @staticmethod
    def _get_windows_drive_label(letter: str, ctypes_mod) -> str:
        """Return 'VolumeName (X:)' or 'Local Disk (X:)' on Windows."""
        buf = ctypes_mod.create_unicode_buffer(261)
        try:
            ctypes_mod.windll.kernel32.GetVolumeInformationW(
                f"{letter}:\\", buf, ctypes_mod.sizeof(buf),
                None, None, None, None, 0
            )
            vol_name = buf.value.strip()
        except Exception:
            vol_name = ""
        if vol_name:
            return f"{vol_name} ({letter}:)"
        # Detect drive type for a nicer fallback
        try:
            dtype = ctypes_mod.windll.kernel32.GetDriveTypeW(f"{letter}:\\")
            # 2=Removable, 3=Fixed, 4=Remote, 5=CDROM, 6=RAMDisk
            type_map = {2: "Removable Disk", 4: "Network Drive",
                        5: "CD/DVD Drive", 6: "RAM Disk"}
            fallback = type_map.get(dtype, "Local Disk")
        except Exception:
            fallback = "Local Disk"
        return f"{fallback} ({letter}:)"

    @staticmethod
    def _get_unix_mount_labels() -> dict:
        """
        Return a dict of {mount_point: label_string} on Linux/macOS.
        Tries multiple strategies: /proc/mounts label field, blkid, lsblk, macOS diskutil.
        """
        labels: dict = {}

        sys_name = platform.system()

        if sys_name == "Darwin":
            # macOS: use diskutil list and diskutil info
            try:
                result = subprocess.run(
                    ["diskutil", "list", "-plist"],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    import plistlib
                    data = plistlib.loads(result.stdout.encode())
                    for disk in data.get("AllDisksAndPartitions", []):
                        for part in disk.get("Partitions", []):
                            dev = "/dev/" + part.get("DeviceIdentifier", "")
                            mnt = part.get("MountPoint", "")
                            vol = part.get("VolumeName", "")
                            if mnt and vol:
                                labels[mnt] = f"{vol} ({dev})"
            except Exception:
                pass
            return labels

        # Linux: try lsblk first (most reliable, includes labels + mountpoints)
        try:
            result = subprocess.run(
                ["lsblk", "-o", "MOUNTPOINT,LABEL,MODEL,SIZE", "-J", "--noheadings"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                import json as _json
                data = _json.loads(result.stdout)
                def _walk(devices):
                    for dev in devices:
                        mnt   = (dev.get("mountpoint") or "").strip()
                        lbl   = (dev.get("label")      or "").strip()
                        model = (dev.get("model")      or "").strip()
                        size  = (dev.get("size")       or "").strip()
                        if mnt:
                            parts = []
                            if lbl:   parts.append(lbl)
                            elif model: parts.append(model)
                            if size:  parts.append(size)
                            if parts:
                                labels[mnt] = f"{' — '.join(parts)}  [{mnt}]"
                        for child in dev.get("children") or []:
                            _walk([child])
                _walk(data.get("blockdevices", []))
        except Exception:
            pass

        # Fallback: blkid for labels, then match with /proc/mounts
        if not labels:
            try:
                blkid = subprocess.run(
                    ["blkid", "-o", "export"],
                    capture_output=True, text=True, timeout=5
                )
                dev_labels: dict = {}
                current_dev = ""
                for line in blkid.stdout.splitlines():
                    line = line.strip()
                    if line.startswith("DEVNAME="):
                        current_dev = line.split("=", 1)[1]
                    elif line.startswith("LABEL=") and current_dev:
                        dev_labels[current_dev] = line.split("=", 1)[1]

                with open("/proc/mounts") as f:
                    for line in f:
                        parts_m = line.split()
                        if len(parts_m) >= 2:
                            dev, mnt = parts_m[0], parts_m[1]
                            if dev in dev_labels:
                                labels[mnt] = f"{dev_labels[dev]}  [{mnt}]"
            except Exception:
                pass

        return labels

    def _add_subfolders(self, parent_item: QStandardItem, path: str, depth: int = 0):
        """Lazily add a placeholder; real children added on expand"""
        if depth > 0:
            return
        placeholder = QStandardItem("  loading...")
        placeholder.setEditable(False)
        placeholder.setData("placeholder", Qt.UserRole)
        parent_item.appendRow(placeholder)

    def load_children(self, index: QModelIndex):
        item = self.itemFromIndex(index)
        if not item:
            return
        if item.rowCount() == 1 and item.child(0).data(Qt.UserRole) == "placeholder":
            item.removeRow(0)
            path = item.data(Qt.UserRole + 1)
            if path and os.path.isdir(path):
                try:
                    entries = sorted(
                        [e for e in os.scandir(path) if e.is_dir() and not e.name.startswith(".")],
                        key=lambda e: e.name.lower()
                    )
                    for entry in entries[:100]:
                        child = QStandardItem(entry.name)
                        child.setEditable(False)
                        child.setIcon(self._os_icon(entry.path))
                        child.setData(entry.path, Qt.UserRole + 1)
                        child.setData("folder", Qt.UserRole)
                        self._add_subfolders(child, entry.path, 1)
                        item.appendRow(child)
                except PermissionError:
                    pass


# ─────────────────────────────────────────────
#  FILE TABLE MODEL
# ─────────────────────────────────────────────

class FileTableModel(QAbstractTableModel):
    COLUMNS = ["Name", "Size", "Type", "Modified", "Permissions"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._data: List[Dict] = []
        self._current_path = ""

    def load_path(self, path: str):
        self.beginResetModel()
        self._data = []
        self._current_path = path
        if os.path.isdir(path):
            try:
                entries = sorted(os.scandir(path), key=lambda e: (not e.is_dir(), e.name.lower()))
                for entry in entries:
                    try:
                        stat = entry.stat()
                        size = stat.st_size
                        mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
                        is_dir = entry.is_dir()
                        
                        if is_dir:
                            size_str = "<Folder>"
                            ftype = "Folder"
                        else:
                            size_str = self._format_size(size)
                            ftype = self._get_type(entry.name)
                        
                        perms = self._get_perms(stat.st_mode)
                        icon = "📁" if is_dir else self._get_file_icon(entry.name)
                        
                        self._data.append({
                            "name": entry.name,
                            "path": entry.path,
                            "is_dir": is_dir,
                            "size": size,
                            "size_str": size_str,
                            "type": ftype,
                            "modified": mtime.strftime("%Y-%m-%d  %H:%M"),
                            "perms": perms,
                            "icon": icon,
                        })
                    except (PermissionError, OSError):
                        pass
            except PermissionError:
                pass
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.COLUMNS)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row = self._data[index.row()]
        col = index.column()
        
        if role == Qt.DisplayRole:
            if col == 0:
                return f"  {row['icon']}  {row['name']}"
            elif col == 1:
                return row['size_str']
            elif col == 2:
                return row['type']
            elif col == 3:
                return row['modified']
            elif col == 4:
                return row['perms']
        elif role == Qt.UserRole:
            return row['path']
        elif role == Qt.UserRole + 1:
            return row['is_dir']
        elif role == Qt.UserRole + 2:
            return row
        elif role == Qt.TextAlignmentRole:
            if col == 1:
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.COLUMNS[section]
        return None

    def get_row(self, row: int) -> Optional[Dict]:
        if 0 <= row < len(self._data):
            return self._data[row]
        return None

    def _format_size(self, size: int) -> str:
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} PB"

    def _get_type(self, name: str) -> str:
        ext = Path(name).suffix.lower()
        type_map = {
            ".txt": "Text", ".md": "Markdown", ".pdf": "PDF",
            ".doc": "Word", ".docx": "Word", ".xls": "Excel", ".xlsx": "Excel",
            ".ppt": "PowerPoint", ".pptx": "PowerPoint",
            ".jpg": "Image", ".jpeg": "Image", ".png": "Image",
            ".gif": "Image", ".bmp": "Image", ".svg": "Vector",
            ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio",
            ".mp4": "Video", ".avi": "Video", ".mkv": "Video", ".mov": "Video",
            ".zip": "Archive", ".rar": "Archive", ".7z": "Archive", ".tar": "Archive",
            ".gz": "Archive", ".py": "Python", ".js": "JavaScript",
            ".ts": "TypeScript", ".html": "HTML", ".css": "CSS",
            ".json": "JSON", ".xml": "XML", ".csv": "CSV",
            ".exe": "Executable", ".sh": "Shell Script",
        }
        return type_map.get(ext, ext[1:].upper() + " File" if ext else "File")

    def _get_file_icon(self, name: str) -> str:
        ext = Path(name).suffix.lower()
        icon_map = {
            ".py": "🐍", ".js": "📜", ".ts": "📘", ".html": "🌐", ".css": "🎨",
            ".json": "📋", ".xml": "📋", ".csv": "📊",
            ".jpg": "🖼️", ".jpeg": "🖼️", ".png": "🖼️", ".gif": "🖼️", ".svg": "🖼️",
            ".mp3": "🎵", ".wav": "🎵", ".flac": "🎵",
            ".mp4": "🎬", ".avi": "🎬", ".mkv": "🎬", ".mov": "🎬",
            ".pdf": "📕", ".doc": "📝", ".docx": "📝", ".txt": "📄",
            ".xls": "📊", ".xlsx": "📊", ".ppt": "📊", ".pptx": "📊",
            ".zip": "🗜️", ".rar": "🗜️", ".7z": "🗜️", ".tar": "🗜️",
            ".exe": "⚙️", ".sh": "⚡",
        }
        return icon_map.get(ext, "📄")

    def _get_perms(self, mode: int) -> str:
        perms = ""
        for who in ["USR", "GRP", "OTH"]:
            for what in ["R", "W", "X"]:
                flag = getattr(__import__("stat"), f"S_I{what}{who}")
                perms += what.lower() if mode & flag else "-"
            perms += " "
        return perms.strip()


# ─────────────────────────────────────────────
#  RENAME ENGINE
# ─────────────────────────────────────────────

class RenameRule:
    def __init__(self, pattern: str, replacement: str):
        self.pattern = pattern
        self.replacement = replacement

    def apply(self, name: str) -> str:
        stem = Path(name).stem
        ext = Path(name).suffix
        new_stem = stem.replace(self.pattern, self.replacement)
        return new_stem + ext


class SmartRenameEngine:
    """Multi-pattern rename engine with preview support"""

    @staticmethod
    def parse_rules(rule_str: str) -> List[RenameRule]:
        """Parse comma-separated rules like: LK21-DE, (2023)-"""
        rules = []
        parts = [p.strip() for p in rule_str.split(",")]
        i = 0
        while i < len(parts) - 1:
            pattern = parts[i]
            replacement = parts[i + 1]
            if pattern:
                rules.append(RenameRule(pattern, replacement))
            i += 2
        return rules

    @staticmethod
    def apply_rules(name: str, rules: List[RenameRule], 
                    prefix: str = "", suffix: str = "",
                    numbering: bool = False, num_start: int = 1,
                    num_padding: int = 2, num_sep: str = "_",
                    counter: int = 0,
                    change_ext: str = "",
                    case_mode: str = "none",
                    remove_special: bool = False,
                    remove_spaces: bool = False,
                    space_replacement: str = "_") -> str:
        stem = Path(name).stem
        ext = Path(name).suffix

        # Apply find/replace rules
        for rule in rules:
            stem = stem.replace(rule.pattern, rule.replacement)

        # Remove special characters
        if remove_special:
            stem = re.sub(r'[^\w\s\-.]', '', stem)

        # Space handling
        if remove_spaces:
            stem = stem.replace(" ", space_replacement)

        # Case conversion
        if case_mode == "lower":
            stem = stem.lower()
        elif case_mode == "upper":
            stem = stem.upper()
        elif case_mode == "title":
            stem = stem.title()
        elif case_mode == "camel":
            words = stem.split()
            stem = words[0].lower() + "".join(w.title() for w in words[1:]) if words else stem
        elif case_mode == "snake":
            stem = "_".join(stem.lower().split())

        # Add numbering
        if numbering:
            num = num_start + counter
            num_str = str(num).zfill(num_padding)
            stem = f"{stem}{num_sep}{num_str}"

        # Add prefix/suffix
        if prefix:
            stem = prefix + stem
        if suffix:
            stem = stem + suffix

        # Change extension
        if change_ext:
            ext = change_ext if change_ext.startswith(".") else "." + change_ext

        return stem + ext


# ─────────────────────────────────────────────
#  ACTIVITY LOG
# ─────────────────────────────────────────────

class ActivityLog:
    INFO = "INFO"
    SUCCESS = "✅"
    WARNING = "⚠️"
    ERROR = "❌"
    RENAME = "✏️"
    DELETE = "🗑️"
    COPY = "📋"
    MOVE = "✂️"
    CREATE = "➕"

    def __init__(self, log_widget: QPlainTextEdit):
        self.widget = log_widget
        self.entries = []

    def log(self, message: str, level: str = "INFO"):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        entry = f"[{ts}]  {level}  {message}"
        self.entries.append(entry)
        self.widget.appendPlainText(entry)
        # Auto-scroll
        scrollbar = self.widget.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear(self):
        self.entries.clear()
        self.widget.clear()

    def export(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.entries))


# ─────────────────────────────────────────────
#  RENAME DIALOG (batch preview)
# ─────────────────────────────────────────────

class RenamePreviewDialog(QDialog):
    def __init__(self, renames: List[tuple], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rename Preview — Confirm Changes")
        self.setMinimumSize(700, 500)
        self.renames = renames
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Header
        lbl = QLabel(f"⚠️  {len(self.renames)} file(s) will be renamed. Please confirm.")
        lbl.setStyleSheet("font-size: 14px; font-weight: 600; padding: 4px;")
        layout.addWidget(lbl)

        # Table
        table = QTableView()
        model = QStandardItemModel(len(self.renames), 2)
        model.setHorizontalHeaderLabels(["Original Name", "New Name"])
        for i, (old, new) in enumerate(self.renames):
            old_item = QStandardItem(old)
            new_item = QStandardItem(new)
            old_item.setEditable(False)
            new_item.setEditable(False)
            if old != new:
                new_item.setForeground(QColor("#6EE7B7"))
            else:
                new_item.setForeground(QColor("#EF4444"))
                new_item.setText("(no change)")
            model.setItem(i, 0, old_item)
            model.setItem(i, 1, new_item)
        table.setModel(model)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(table)

        # Buttons
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.button(QDialogButtonBox.Ok).setText("✅  Apply Rename")
        btns.button(QDialogButtonBox.Ok).setObjectName("primaryBtn")
        btns.button(QDialogButtonBox.Cancel).setText("Cancel")
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)


# ─────────────────────────────────────────────
#  PROPERTIES DIALOG
# ─────────────────────────────────────────────

class PropertiesDialog(QDialog):
    def __init__(self, path: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Properties")
        self.setMinimumWidth(400)
        self._build(path)

    def _build(self, path: str):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        p = Path(path)
        stat = p.stat()
        
        info = [
            ("Name", p.name),
            ("Path", str(p.parent)),
            ("Type", "Directory" if p.is_dir() else p.suffix or "File"),
            ("Size", self._fmt(stat.st_size) if p.is_file() else self._calc_dir_size(p)),
            ("Created", datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")),
            ("Modified", datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")),
            ("Accessed", datetime.datetime.fromtimestamp(stat.st_atime).strftime("%Y-%m-%d %H:%M:%S")),
        ]
        
        form = QFormLayout()
        form.setSpacing(8)
        for label, value in info:
            lbl = QLabel(label + ":")
            lbl.setStyleSheet("font-weight: 600; color: #94A3B8;")
            val = QLabel(value)
            val.setWordWrap(True)
            val.setTextInteractionFlags(Qt.TextSelectableByMouse)
            form.addRow(lbl, val)
        
        layout.addLayout(form)
        btns = QDialogButtonBox(QDialogButtonBox.Ok)
        btns.accepted.connect(self.accept)
        layout.addWidget(btns)

    def _fmt(self, size):
        for u in ["B", "KB", "MB", "GB"]:
            if size < 1024: return f"{size:.1f} {u}"
            size /= 1024
        return f"{size:.1f} TB"

    def _calc_dir_size(self, p: Path) -> str:
        try:
            total = sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
            return self._fmt(total) + " (estimated)"
        except:
            return "N/A"



# ─────────────────────────────────────────────
#  HELP CONTENT MODULE
# ─────────────────────────────────────────────

HELP_CONTENT = {
    "Getting Started": {
        "icon": "🚀",
        "sections": [
            ("Welcome to SmartFileManager", """
SmartFileManager is a professional, enterprise-grade file management application built with PySide6.
It features a docking system, smart batch rename, activity logging, and full dark/light theme support.

<b>Key Interface Areas:</b>
<ul>
  <li><b>Left Panel</b> — Drive Explorer Tree: quick-access shortcuts and drive/folder tree</li>
  <li><b>Center</b> — File list with sortable columns, breadcrumb navigation, search</li>
  <li><b>Bottom</b> — Smart Rename Panel with live preview</li>
  <li><b>Right</b> — Activity Log</li>
</ul>
"""),
            ("Navigation", """
<b>Navigating folders:</b>
<ul>
  <li>Double-click a folder to open it</li>
  <li>Click any segment of the <b>breadcrumb bar</b> to jump there</li>
  <li>Type a path directly in the <b>address bar</b> and press Enter</li>
  <li>Use <b>Alt+Left / Alt+Right</b> to go back and forward</li>
  <li>Use <b>Alt+Up</b> to go up one level</li>
  <li>Press <b>F5</b> to refresh</li>
</ul>

<b>Drive Tree (left panel):</b>
<ul>
  <li>The <b>Quick Access</b> section shows Home, Desktop, Downloads, Documents, Pictures, Music, Videos</li>
  <li>The <b>Drives</b> section shows all mounted drives and partitions</li>
  <li>Click any item to navigate; click the arrow to expand sub-folders</li>
</ul>
"""),
        ]
    },
    "Smart Rename": {
        "icon": "✏️",
        "sections": [
            ("Overview", """
Smart Rename allows you to rename one or many files at once using powerful rules,
with a live preview before any changes are made.

<b>How to use:</b>
<ol>
  <li>Select files in the file list (or select none to rename all)</li>
  <li>Open the <b>Smart Rename</b> panel at the bottom</li>
  <li>Enter your rename rules</li>
  <li>Review the <b>live preview</b></li>
  <li>Click <b>Apply Rename</b> and confirm in the preview dialog</li>
</ol>
"""),
            ("Find & Replace Rules", """
<b>Rule format:</b> <code>pattern, replacement, pattern2, replacement2, ...</code>
<br><br>
Rules are separated by commas. Each pair is <code>what-to-find, what-to-replace-with</code>.
An empty replacement removes the matched text.

<b>Examples:</b>
<table>
  <tr><td><code>LK21-DE, </code></td><td>→ Removes "LK21-DE" from filenames</td></tr>
  <tr><td><code>(2023)-, HD-</code></td><td>→ Removes "(2023)" and "HD"</td></tr>
  <tr><td><code>Copy of , </code></td><td>→ Removes "Copy of " prefix</td></tr>
  <tr><td><code>IMG_, Photo_</code></td><td>→ Replaces "IMG_" with "Photo_"</td></tr>
</table>
<br>
<b>Additional options:</b>
<ul>
  <li><b>Prefix / Suffix</b> — Add text to the beginning or end of every filename</li>
  <li><b>Case</b> — Convert to lowercase, UPPERCASE, Title Case, camelCase, or snake_case</li>
  <li><b>Extension</b> — Change the file extension for all selected files</li>
  <li><b>Remove special chars</b> — Strip non-alphanumeric characters</li>
  <li><b>Replace spaces</b> — Substitute spaces with a custom character (default: _)</li>
</ul>
"""),
            ("Auto-Numbering", """
The <b>Numbering</b> tab adds sequential numbers to filenames.

<b>Settings:</b>
<ul>
  <li><b>Start from</b> — The first number to use (e.g. 1, 100)</li>
  <li><b>Zero padding</b> — Minimum digits, padded with zeros (e.g. 2 → 01, 02, ...)</li>
  <li><b>Separator</b> — Character between filename and number (e.g. _, -, .)</li>
</ul>

<b>Example:</b> Files "photo.jpg", "photo.jpg", "photo.jpg" with start=1, padding=3, sep=_
<br>→ photo_001.jpg, photo_002.jpg, photo_003.jpg
"""),
            ("Regex Mode", """
The <b>Regex</b> tab enables full regular expression find/replace.

<b>Pattern syntax (Python regex):</b>
<ul>
  <li><code>\\d+</code> — Match one or more digits</li>
  <li><code>[A-Z]+</code> — Match uppercase letters</li>
  <li><code>(\\d{4})</code> — Capture a 4-digit year group</li>
  <li><code>^prefix</code> — Match at start of filename stem</li>
  <li><code>suffix$</code> — Match at end of filename stem</li>
</ul>

<b>Example:</b> Pattern <code>(\\d{4})</code>, Replacement <code>[\\1]</code>
<br>→ Wraps any 4-digit number in brackets: <code>movie_2023.mp4</code> → <code>movie_[2023].mp4</code>
"""),
            ("Undo Rename", """
After applying a batch rename, you can undo the entire operation using:
<ul>
  <li>The <b>Undo Last Rename</b> button in the rename panel</li>
</ul>
Only the most recent batch operation can be undone. After navigating away or performing
another rename, the undo history is cleared.
"""),
        ]
    },
    "File Operations": {
        "icon": "📁",
        "sections": [
            ("Basic Operations", """
<b>Selection:</b>
<ul>
  <li><b>Click</b> — Select a single file</li>
  <li><b>Ctrl+Click</b> — Add/remove from selection</li>
  <li><b>Shift+Click</b> — Select a range</li>
  <li><b>Ctrl+A</b> — Select all</li>
  <li><b>Ctrl+I</b> — Invert selection</li>
</ul>

<b>Operations via keyboard:</b>
<ul>
  <li><b>Ctrl+C</b> — Copy</li>
  <li><b>Ctrl+X</b> — Cut</li>
  <li><b>Ctrl+V</b> — Paste</li>
  <li><b>Delete</b> — Delete selected</li>
  <li><b>F2</b> — Rename selected file</li>
  <li><b>Ctrl+Shift+N</b> — New folder</li>
  <li><b>Ctrl+N</b> — New file</li>
</ul>
"""),
            ("Context Menu", """
Right-click any file or folder to access the context menu:
<ul>
  <li><b>Open</b> — Open with default application</li>
  <li><b>Cut / Copy / Paste</b> — Clipboard operations</li>
  <li><b>Rename</b> — Quick inline rename (single file)</li>
  <li><b>Delete</b> — Delete with confirmation</li>
  <li><b>Properties</b> — View file details (size, dates, permissions)</li>
  <li><b>Copy Path</b> — Copy full path to clipboard</li>
  <li><b>New Folder / New File</b> — Create in current directory</li>
  <li><b>Open Terminal Here</b> — Launch terminal at current path</li>
</ul>
"""),
        ]
    },
    "Tools": {
        "icon": "🛠️",
        "sections": [
            ("Duplicate Finder", """
<b>Find Duplicate Files</b> (Tools menu) scans the current folder for files with identical content
using MD5 hashing.

Results are displayed in the Activity Log showing which files are duplicates.
This operation only scans the immediate folder, not subdirectories.
"""),
            ("Folder Size Calculator", """
<b>Calculate Folder Size</b> (Tools menu) recursively sums the sizes of all files
within the selected folder(s), or the current folder if nothing is selected.

Results appear in the Activity Log with total size and file count.
"""),
            ("Export Report", """
<b>Export Report</b> (Tools menu) exports a full listing of the current folder's contents.

<b>Formats available:</b>
<ul>
  <li><b>.txt</b> — Plain text table, human-readable</li>
  <li><b>.csv</b> — Comma-separated values, importable into Excel/Sheets</li>
</ul>

The report includes: filename, size, type, last modified date, and permissions.
"""),
        ]
    },
    "Interface & Docking": {
        "icon": "🪟",
        "sections": [
            ("Dock Panels", """
SmartFileManager uses a flexible docking system. Each panel can be:
<ul>
  <li><b>Moved</b> — Drag the title bar to a new position</li>
  <li><b>Floated</b> — Click the float button to make it a separate window</li>
  <li><b>Closed</b> — Click the X on the dock to hide it</li>
  <li><b>Restored</b> — Use <b>View → Panels</b> menu to show hidden docks</li>
</ul>
"""),
            ("Panel Profiles", """
<b>View → Panels → Reset to Default Layout</b> restores all panels to their original positions.

Panel visibility and layout are saved automatically using <b>QSettings</b> and restored
the next time you launch the application.

<b>Available panels:</b>
<ul>
  <li>Explorer (Drive Tree) — left</li>
  <li>Smart Rename — bottom</li>
  <li>Activity Log — right</li>
</ul>
"""),
            ("Themes", """
Two built-in themes are available:
<ul>
  <li><b>🌙 Dark</b> — Dark background, violet accent</li>
  <li><b>☀️ Light</b> — Clean white background, violet accent</li>
</ul>

Themes are applied via explicit QSS stylesheets and do <b>not</b> inherit from or conflict
with the operating system theme. The app uses the <b>Fusion</b> Qt style as a neutral base.

Theme selection is saved and restored between sessions.
"""),
        ]
    },
    "Activity Log": {
        "icon": "📋",
        "sections": [
            ("Overview", """
The <b>Activity Log</b> records every operation performed during the session:
file copies, moves, renames, deletions, navigations, errors, and more.

Each entry includes a timestamp and a status icon:
<ul>
  <li>✅ — Success</li>
  <li>⚠️ — Warning</li>
  <li>❌ — Error</li>
  <li>✏️ — Rename</li>
  <li>🗑️ — Delete</li>
  <li>📋 — Copy</li>
  <li>✂️ — Move/Cut</li>
  <li>➕ — Create</li>
</ul>
"""),
            ("Export Log", """
Click <b>Export</b> in the Activity Log panel or use <b>Tools → Export Activity Log</b>
to save the log as a <code>.txt</code> file.

Use <b>Clear</b> to reset the log for the current session.
"""),
        ]
    },
    "Keyboard Shortcuts": {
        "icon": "⌨️",
        "sections": [
            ("Full Shortcut Reference", """
<table width="100%" cellspacing="4">
<tr><th align="left">Shortcut</th><th align="left">Action</th></tr>
<tr><td><b>Alt+Left</b></td><td>Go Back</td></tr>
<tr><td><b>Alt+Right</b></td><td>Go Forward</td></tr>
<tr><td><b>Alt+Up</b></td><td>Go Up one level</td></tr>
<tr><td><b>F5</b></td><td>Refresh current folder</td></tr>
<tr><td><b>Ctrl+H</b></td><td>Toggle hidden files</td></tr>
<tr><td><b>Ctrl+A</b></td><td>Select all</td></tr>
<tr><td><b>Ctrl+I</b></td><td>Invert selection</td></tr>
<tr><td><b>Ctrl+C</b></td><td>Copy</td></tr>
<tr><td><b>Ctrl+X</b></td><td>Cut</td></tr>
<tr><td><b>Ctrl+V</b></td><td>Paste</td></tr>
<tr><td><b>Delete</b></td><td>Delete selected</td></tr>
<tr><td><b>F2</b></td><td>Rename selected file</td></tr>
<tr><td><b>Ctrl+N</b></td><td>New file</td></tr>
<tr><td><b>Ctrl+Shift+N</b></td><td>New folder</td></tr>
<tr><td><b>Ctrl+R</b></td><td>Open Smart Rename panel</td></tr>
<tr><td><b>Ctrl+Shift+R</b></td><td>Batch Rename</td></tr>
<tr><td><b>Ctrl+Alt+T</b></td><td>Open Terminal here</td></tr>
<tr><td><b>Ctrl+Q</b></td><td>Quit</td></tr>
</table>
"""),
        ]
    },
}


class HelpDialog(QDialog):
    """Full help content dialog with sidebar navigation."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SmartFileManager — Help")
        self.setMinimumSize(900, 620)
        self.resize(980, 680)
        self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────
        sidebar = QWidget()
        sidebar.setFixedWidth(210)
        sidebar.setObjectName("helpSidebar")
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(0, 0, 0, 0)
        sb_layout.setSpacing(0)

        title_lbl = QLabel("  📖  Help")
        title_lbl.setFixedHeight(48)
        title_lbl.setStyleSheet(
            "font-size: 15px; font-weight: 700; padding-left: 16px; "
            "border-bottom: 1px solid rgba(255,255,255,0.08);"
        )
        sb_layout.addWidget(title_lbl)

        self._nav_buttons: List[QPushButton] = []
        for topic in HELP_CONTENT:
            meta = HELP_CONTENT[topic]
            btn = QPushButton(f"  {meta['icon']}  {topic}")
            btn.setFlat(True)
            btn.setCheckable(True)
            btn.setFixedHeight(38)
            btn.setStyleSheet(
                "QPushButton { text-align: left; padding-left: 12px; border-radius: 0; "
                "border: none; font-size: 13px; }"
                "QPushButton:hover { background: rgba(124,58,237,0.12); }"
                "QPushButton:checked { background: rgba(124,58,237,0.22); "
                "color: #A78BFA; border-left: 3px solid #7C3AED; }"
            )
            btn.clicked.connect(lambda _, t=topic: self._show_topic(t))
            sb_layout.addWidget(btn)
            self._nav_buttons.append(btn)

        sb_layout.addStretch()
        layout.addWidget(sidebar)

        # ── Vertical separator ───────────────────────────
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        layout.addWidget(sep)

        # ── Content area ─────────────────────────────────
        self._content = QTextEdit()
        self._content.setReadOnly(True)
        self._content.setObjectName("helpContent")
        self._content.setStyleSheet(
            "QTextEdit { border: none; padding: 20px; font-size: 13px; }"
        )
        layout.addWidget(self._content, 1)

        # Close button row
        close_row = QHBoxLayout()
        close_row.setContentsMargins(0, 0, 12, 12)
        close_row.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setMinimumWidth(90)
        close_btn.clicked.connect(self.accept)
        close_row.addWidget(close_btn)

        wrapper = QWidget()
        wrapper.setLayout(close_row)
        
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        right_layout.addWidget(self._content)
        right_layout.addWidget(wrapper)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        layout.addWidget(right_widget, 1)
        layout.removeWidget(self._content)

        # Show first topic by default
        if self._nav_buttons:
            self._nav_buttons[0].setChecked(True)
            first_topic = list(HELP_CONTENT.keys())[0]
            self._show_topic(first_topic)

    def _show_topic(self, topic: str):
        # Uncheck all, check active
        for btn in self._nav_buttons:
            label = btn.text().strip().split("  ", 2)[-1]
            btn.setChecked(label == topic)

        meta = HELP_CONTENT.get(topic, {})
        sections = meta.get("sections", [])

        html = f"<h2>{meta.get('icon', '')} {topic}</h2>"
        for title, body in sections:
            html += f"<h3>{title}</h3>{body}<hr>"

        self._content.setHtml(html)
        self._content.verticalScrollBar().setValue(0)


# ─────────────────────────────────────────────
#  EXPORT REPORT DIALOG
# ─────────────────────────────────────────────

class ExportReportDialog(QDialog):
    """Dialog to choose export format and destination for folder report."""

    def __init__(self, current_path: str, file_data: list, parent=None):
        super().__init__(parent)
        self.current_path = current_path
        self.file_data = file_data
        self.setWindowTitle("Export Report")
        self.setFixedSize(460, 220)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        lbl = QLabel(f"Export listing of: <b>{self.current_path}</b>")
        lbl.setWordWrap(True)
        layout.addWidget(lbl)

        fmt_grp = QGroupBox("Format")
        fmt_lay = QHBoxLayout(fmt_grp)
        self.rb_txt = QRadioButton("Plain Text (.txt)")
        self.rb_csv = QRadioButton("CSV (.csv)")
        self.rb_txt.setChecked(True)
        fmt_lay.addWidget(self.rb_txt)
        fmt_lay.addWidget(self.rb_csv)
        layout.addWidget(fmt_grp)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.button(QDialogButtonBox.Ok).setText("📄  Save Report")
        btns.button(QDialogButtonBox.Ok).setObjectName("primaryBtn")
        btns.accepted.connect(self._do_export)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _do_export(self):
        fmt = "txt" if self.rb_txt.isChecked() else "csv"
        default_name = f"report_{Path(self.current_path).name or 'root'}.{fmt}"
        default_path = os.path.join(str(Path.home()), default_name)
        filter_str = "Text Files (*.txt)" if fmt == "txt" else "CSV Files (*.csv)"
        path, _ = QFileDialog.getSaveFileName(self, "Save Report", default_path, filter_str)
        if not path:
            return
        try:
            if fmt == "txt":
                self._write_txt(path)
            else:
                self._write_csv(path)
            self.accept()
            QMessageBox.information(self.parent(), "Export Complete", f"Report saved to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))

    def _write_txt(self, path: str):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            "=" * 80,
            "  SmartFileManager — Folder Report",
            f"  Path      : {self.current_path}",
            f"  Generated : {ts}",
            f"  Items     : {len(self.file_data)}",
            "=" * 80,
            "",
            f"{'Name':<50}  {'Size':>12}  {'Type':<16}  {'Modified':<20}  {'Perms'}",
            "-" * 80,
        ]
        for row in self.file_data:
            lines.append(
                f"{row['name']:<50}  {row['size_str']:>12}  {row['type']:<16}  "
                f"{row['modified']:<20}  {row['perms']}"
            )
        lines += ["", f"© Macan Angkasa — All Rights Reserved", ""]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def _write_csv(self, path: str):
        import csv
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Size", "Type", "Modified", "Permissions"])
            for row in self.file_data:
                writer.writerow([
                    row["name"], row["size_str"], row["type"],
                    row["modified"], row["perms"]
                ])



class SmartFileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = "dark"
        self.current_path = str(Path.home())
        self.history: List[str] = [self.current_path]
        self.history_idx = 0
        self._clipboard_paths: List[str] = []
        self._clipboard_mode = "copy"  # or "cut"
        self._settings = QSettings("MacanAngkasa", "SmartFileManager")

        self.setWindowTitle("SmartFileManager — Enterprise Edition")
        self.setMinimumSize(1280, 800)
        self.resize(1400, 900)
        icon_path = "icon.ico"
        if hasattr(sys, "_MEIPASS"):
            icon_path = os.path.join(sys._MEIPASS, icon_path)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
          

        self._build_ui()
        self._restore_settings()
        self._navigate(self.current_path, add_history=False)

    def _restore_settings(self):
        """Restore window geometry, theme, and dock layout from QSettings."""
        # Window geometry
        geometry = self._settings.value("window/geometry")
        if geometry:
            self.restoreGeometry(geometry)
        state = self._settings.value("window/state")
        if state:
            self.restoreState(state)

        # Theme
        theme = self._settings.value("app/theme", "dark")
        self._apply_theme(theme)

        # Last path
        last_path = self._settings.value("app/lastPath", str(Path.home()))
        if os.path.isdir(last_path):
            self.current_path = last_path
            self.history = [self.current_path]

    def _save_settings(self):
        """Save window geometry, theme, dock layout to QSettings."""
        self._settings.setValue("window/geometry", self.saveGeometry())
        self._settings.setValue("window/state", self.saveState())
        self._settings.setValue("app/theme", self.current_theme)
        self._settings.setValue("app/lastPath", self.current_path)

    def closeEvent(self, event):
        self._save_settings()
        super().closeEvent(event)

    # ── UI CONSTRUCTION ──────────────────────────────────

    def _build_ui(self):
        self._build_menu()
        self._build_toolbar()
        self._build_status_bar()
        self._build_docks()
        self._build_central()

    def _build_menu(self):
        mb = self.menuBar()

        # File
        file_menu = mb.addMenu("&File")
        self._add_action(file_menu, "New Folder", "Ctrl+Shift+N", self._new_folder)
        self._add_action(file_menu, "New File", "Ctrl+N", self._new_file)
        file_menu.addSeparator()
        self._add_action(file_menu, "Open Terminal Here", "Ctrl+Alt+T", self._open_terminal)
        file_menu.addSeparator()
        self._add_action(file_menu, "Export Report…", None, self._export_report)
        file_menu.addSeparator()
        self._add_action(file_menu, "Exit", "Ctrl+Q", self.close)

        # Edit
        edit_menu = mb.addMenu("&Edit")
        self._add_action(edit_menu, "Copy", "Ctrl+C", self._copy_files)
        self._add_action(edit_menu, "Cut", "Ctrl+X", self._cut_files)
        self._add_action(edit_menu, "Paste", "Ctrl+V", self._paste_files)
        edit_menu.addSeparator()
        self._add_action(edit_menu, "Select All", "Ctrl+A", self._select_all)
        self._add_action(edit_menu, "Invert Selection", "Ctrl+I", self._invert_selection)
        edit_menu.addSeparator()
        self._add_action(edit_menu, "Delete", "Delete", self._delete_files)
        self._add_action(edit_menu, "Rename", "F2", self._rename_single)

        # View
        view_menu = mb.addMenu("&View")
        self._add_action(view_menu, "Refresh", "F5", self._refresh)
        view_menu.addSeparator()
        self._add_action(view_menu, "Show Hidden Files", "Ctrl+H", self._toggle_hidden)
        view_menu.addSeparator()

        # Theme submenu
        theme_menu = view_menu.addMenu("Theme")
        self._add_action(theme_menu, "🌙 Dark Theme", None, lambda: self._apply_theme("dark"))
        self._add_action(theme_menu, "☀️ Light Theme", None, lambda: self._apply_theme("light"))

        view_menu.addSeparator()

        # Panels submenu — populated after docks are built
        self._panels_menu = view_menu.addMenu("Panels")
        view_menu.addSeparator()
        self._add_action(view_menu, "Reset Default Layout", None, self._reset_layout)

        # Tools
        tools_menu = mb.addMenu("&Tools")
        self._add_action(tools_menu, "Smart Rename…", "Ctrl+R", self._show_rename_panel)
        self._add_action(tools_menu, "Batch Rename", "Ctrl+Shift+R", self._batch_rename_dialog)
        tools_menu.addSeparator()
        self._add_action(tools_menu, "Calculate Folder Size", None, self._calc_folder_size)
        self._add_action(tools_menu, "Find Duplicate Files", None, self._find_duplicates)
        tools_menu.addSeparator()
        self._add_action(tools_menu, "Export Activity Log", None, self._export_log)
        self._add_action(tools_menu, "Export Report…", None, self._export_report)
        self._add_action(tools_menu, "Clear Activity Log", None, lambda: self.activity_log.clear())

        # Help
        help_menu = mb.addMenu("&Help")
        self._add_action(help_menu, "Help Contents", "F1", self._show_help)
        help_menu.addSeparator()
        self._add_action(help_menu, "About SmartFileManager", None, self._show_about)

    def _add_action(self, menu, text, shortcut, slot):
        action = QAction(text, self)
        if shortcut:
            action.setShortcut(QKeySequence(shortcut))
        action.triggered.connect(slot)
        menu.addAction(action)
        return action

    def _build_toolbar(self):
        tb = self.addToolBar("Main")
        tb.setMovable(False)
        tb.setIconSize(QSize(20, 20))
        tb.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.btn_back = QAction("◀  Back", self)
        self.btn_back.setShortcut("Alt+Left")
        self.btn_back.triggered.connect(self._go_back)
        tb.addAction(self.btn_back)

        self.btn_forward = QAction("▶  Forward", self)
        self.btn_forward.setShortcut("Alt+Right")
        self.btn_forward.triggered.connect(self._go_forward)
        tb.addAction(self.btn_forward)

        btn_up = QAction("▲  Up", self)
        btn_up.setShortcut("Alt+Up")
        btn_up.triggered.connect(self._go_up)
        tb.addAction(btn_up)

        btn_refresh = QAction("↻  Refresh", self)
        btn_refresh.setShortcut("F5")
        btn_refresh.triggered.connect(self._refresh)
        tb.addAction(btn_refresh)

        tb.addSeparator()

        btn_home = QAction("🏠  Home", self)
        btn_home.triggered.connect(lambda: self._navigate(str(Path.home())))
        tb.addAction(btn_home)

        tb.addSeparator()

        # Address bar
        self.address_bar = QLineEdit()
        self.address_bar.setObjectName("addressBar")
        self.address_bar.setMinimumWidth(400)
        self.address_bar.returnPressed.connect(self._navigate_address)
        tb.addWidget(self.address_bar)

        tb.addSeparator()

        # Search
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍  Search files...")
        self.search_bar.setMinimumWidth(200)
        self.search_bar.textChanged.connect(self._filter_files)
        tb.addWidget(self.search_bar)

        tb.addSeparator()

        # Theme toggle
        self.theme_btn = QAction("🌙  Dark", self)
        self.theme_btn.setCheckable(True)
        self.theme_btn.setChecked(True)
        self.theme_btn.triggered.connect(self._toggle_theme)
        tb.addAction(self.theme_btn)

    def _build_status_bar(self):
        sb = self.statusBar()
        self.status_path = QLabel("")
        self.status_count = QLabel("")
        self.status_size = QLabel("")
        self.status_selection = QLabel("")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(150)
        self.progress_bar.setMaximumHeight(14)
        self.progress_bar.setVisible(False)

        sb.addWidget(self.status_path)
        sb.addPermanentWidget(self.status_selection)
        sb.addPermanentWidget(self.status_count)
        sb.addPermanentWidget(self.status_size)
        sb.addPermanentWidget(self.progress_bar)

    def _build_docks(self):
        # ── Left Dock: Drive Tree ──────────────────────────
        self.drive_dock = QDockWidget("Explorer", self)
        self.drive_dock.setObjectName("driveDock")
        self.drive_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.drive_dock.setMinimumWidth(240)

        self.drive_tree = QTreeView()
        self.drive_tree.setHeaderHidden(True)
        self.drive_tree.setAnimated(True)
        self.drive_tree.setIndentation(16)
        self.drive_tree.setUniformRowHeights(True)

        self.drive_model = DriveTreeModel()
        self.drive_tree.setModel(self.drive_model)
        self.drive_tree.expanded.connect(self._on_tree_expanded)
        self.drive_tree.clicked.connect(self._on_tree_clicked)
        self.drive_tree.expandToDepth(0)

        self.drive_dock.setWidget(self.drive_tree)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.drive_dock)

        # ── Bottom Dock: Rename Panel ──────────────────────
        self.rename_dock = QDockWidget("Smart Rename", self)
        self.rename_dock.setObjectName("renameDock")
        self.rename_dock.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea)
        self.rename_dock.setMinimumHeight(200)
        self.rename_dock.setWidget(self._build_rename_panel())
        self.addDockWidget(Qt.BottomDockWidgetArea, self.rename_dock)

        # ── Right Dock: Activity Log ──────────────────────
        self.log_dock = QDockWidget("Activity Log", self)
        self.log_dock.setObjectName("logDock")
        self.log_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
        self.log_dock.setMinimumWidth(300)
        self.log_dock.setWidget(self._build_log_panel())
        self.addDockWidget(Qt.RightDockWidgetArea, self.log_dock)

        # Tabify rename and log at bottom
        self.splitDockWidget(self.rename_dock, self.log_dock, Qt.Horizontal)

        # ── Build Panels menu entries ──────────────────────
        self._dock_list = [
            (self.drive_dock,  "Explorer"),
            (self.rename_dock, "Smart Rename"),
            (self.log_dock,    "Activity Log"),
        ]
        for dock, label in self._dock_list:
            action = self._panels_menu.addAction(label)
            action.setCheckable(True)
            action.setChecked(True)
            # Keep action in sync with dock visibility
            dock.visibilityChanged.connect(lambda vis, a=action: a.setChecked(vis))
            action.triggered.connect(lambda checked, d=dock: d.setVisible(checked))

        self._panels_menu.addSeparator()
        reset_act = self._panels_menu.addAction("Reset to Default Layout")
        reset_act.triggered.connect(self._reset_layout)

    def _build_rename_panel(self) -> QWidget:
        w = QWidget()
        w.setObjectName("renamePanel")
        layout = QVBoxLayout(w)
        layout.setSpacing(10)
        layout.setContentsMargins(12, 12, 12, 12)

        tabs = QTabWidget()

        # ── Tab 1: Find & Replace ──────────────────────────
        tab1 = QWidget()
        t1 = QVBoxLayout(tab1)
        t1.setSpacing(8)

        row1 = QHBoxLayout()
        lbl1 = QLabel("RULES")
        lbl1.setObjectName("sectionTitle")
        row1.addWidget(lbl1)
        row1.addStretch()
        help_lbl = QLabel("? Format: pattern, replacement, pattern2, replacement2, ...")
        help_lbl.setStyleSheet("color: #64748B; font-size: 11px;")
        row1.addWidget(help_lbl)
        t1.addLayout(row1)

        self.rule_input = QLineEdit()
        self.rule_input.setPlaceholderText("LK21-DE, (2023)-")
        self.rule_input.textChanged.connect(self._update_rename_preview)
        t1.addWidget(self.rule_input)

        # Options grid
        opts = QGridLayout()
        opts.setSpacing(8)

        opts.addWidget(QLabel("Prefix:"), 0, 0)
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("Add prefix...")
        self.prefix_input.textChanged.connect(self._update_rename_preview)
        opts.addWidget(self.prefix_input, 0, 1)

        opts.addWidget(QLabel("Suffix:"), 0, 2)
        self.suffix_input = QLineEdit()
        self.suffix_input.setPlaceholderText("Add suffix...")
        self.suffix_input.textChanged.connect(self._update_rename_preview)
        opts.addWidget(self.suffix_input, 0, 3)

        opts.addWidget(QLabel("Case:"), 1, 0)
        self.case_combo = QComboBox()
        self.case_combo.addItems(["No Change", "lowercase", "UPPERCASE", "Title Case", "camelCase", "snake_case"])
        self.case_combo.currentIndexChanged.connect(self._update_rename_preview)
        opts.addWidget(self.case_combo, 1, 1)

        opts.addWidget(QLabel("Extension:"), 1, 2)
        self.ext_input = QLineEdit()
        self.ext_input.setPlaceholderText(".txt, .jpg, ...")
        self.ext_input.textChanged.connect(self._update_rename_preview)
        opts.addWidget(self.ext_input, 1, 3)

        t1.addLayout(opts)

        # Checkboxes
        checks = QHBoxLayout()
        self.chk_remove_special = QCheckBox("Remove special chars")
        self.chk_remove_special.stateChanged.connect(self._update_rename_preview)
        self.chk_remove_spaces = QCheckBox("Replace spaces with:")
        self.chk_remove_spaces.stateChanged.connect(self._update_rename_preview)
        self.space_rep = QLineEdit("_")
        self.space_rep.setMaximumWidth(50)
        self.space_rep.textChanged.connect(self._update_rename_preview)
        checks.addWidget(self.chk_remove_special)
        checks.addWidget(self.chk_remove_spaces)
        checks.addWidget(self.space_rep)
        checks.addStretch()
        t1.addLayout(checks)

        tabs.addTab(tab1, "🔍 Find & Replace")

        # ── Tab 2: Numbering ──────────────────────────────
        tab2 = QWidget()
        t2 = QFormLayout(tab2)
        t2.setSpacing(8)

        self.chk_numbering = QCheckBox("Enable auto-numbering")
        self.chk_numbering.stateChanged.connect(self._update_rename_preview)
        t2.addRow(self.chk_numbering)

        self.num_start = QLineEdit("1")
        self.num_start.textChanged.connect(self._update_rename_preview)
        t2.addRow("Start from:", self.num_start)

        self.num_padding = QLineEdit("2")
        self.num_padding.textChanged.connect(self._update_rename_preview)
        t2.addRow("Zero padding:", self.num_padding)

        self.num_sep = QLineEdit("_")
        self.num_sep.textChanged.connect(self._update_rename_preview)
        t2.addRow("Separator:", self.num_sep)

        tabs.addTab(tab2, "🔢 Numbering")

        # ── Tab 3: Regex ──────────────────────────────────
        tab3 = QWidget()
        t3 = QVBoxLayout(tab3)
        t3.setSpacing(8)

        self.regex_pattern = QLineEdit()
        self.regex_pattern.setPlaceholderText("Regex pattern (e.g. \\d{4})")
        self.regex_pattern.textChanged.connect(self._update_rename_preview)
        self.regex_replace = QLineEdit()
        self.regex_replace.setPlaceholderText("Replacement (use \\1, \\2 for groups)")
        self.regex_replace.textChanged.connect(self._update_rename_preview)
        
        t3.addWidget(QLabel("Pattern:"))
        t3.addWidget(self.regex_pattern)
        t3.addWidget(QLabel("Replacement:"))
        t3.addWidget(self.regex_replace)
        
        self.chk_regex_enabled = QCheckBox("Enable regex mode")
        self.chk_regex_enabled.stateChanged.connect(self._update_rename_preview)
        t3.addWidget(self.chk_regex_enabled)
        t3.addStretch()

        tabs.addTab(tab3, "⚡ Regex")

        layout.addWidget(tabs)

        # Preview section
        preview_lbl = QLabel("LIVE PREVIEW")
        preview_lbl.setObjectName("sectionTitle")
        layout.addWidget(preview_lbl)

        self.preview_table = QTableView()
        self.preview_model = QStandardItemModel()
        self.preview_model.setHorizontalHeaderLabels(["Original", "→", "Renamed"])
        self.preview_table.setModel(self.preview_model)
        self.preview_table.setMaximumHeight(100)
        self.preview_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.preview_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.preview_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.preview_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.preview_table.setAlternatingRowColors(True)
        layout.addWidget(self.preview_table)

        # Action buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_apply = QPushButton("✅  Apply Rename")
        btn_apply.setObjectName("primaryBtn")
        btn_apply.clicked.connect(self._apply_rename)

        btn_preview = QPushButton("👁  Preview All")
        btn_preview.clicked.connect(self._show_full_preview)

        btn_undo = QPushButton("↩  Undo Last Rename")
        btn_undo.setObjectName("dangerBtn")
        btn_undo.clicked.connect(self._undo_last_rename)

        btn_row.addWidget(btn_apply)
        btn_row.addWidget(btn_preview)
        btn_row.addWidget(btn_undo)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self._last_rename_ops = []
        return w

    def _build_log_panel(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar for log
        log_toolbar = QHBoxLayout()
        log_toolbar.setContentsMargins(8, 6, 8, 6)
        log_toolbar.setSpacing(6)

        lbl = QLabel("ACTIVITY LOG")
        lbl.setObjectName("sectionTitle")
        log_toolbar.addWidget(lbl)
        log_toolbar.addStretch()

        btn_export = QPushButton("Export")
        btn_export.setMaximumHeight(26)
        btn_export.clicked.connect(self._export_log)
        btn_clear = QPushButton("Clear")
        btn_clear.setMaximumHeight(26)
        btn_clear.setObjectName("dangerBtn")
        btn_clear.clicked.connect(lambda: self.activity_log.clear())
        log_toolbar.addWidget(btn_export)
        log_toolbar.addWidget(btn_clear)

        toolbar_widget = QWidget()
        toolbar_widget.setLayout(log_toolbar)
        layout.addWidget(toolbar_widget)

        # Log view
        self.log_view = QPlainTextEdit()
        self.log_view.setObjectName("logView")
        self.log_view.setReadOnly(True)
        # Set font explicitly to ensure no clipping
        log_font = QFont("Consolas", 10)
        log_font.setStyleHint(QFont.StyleHint.Monospace)
        self.log_view.setFont(log_font)
        self.log_view.document().setDefaultFont(log_font)
        layout.addWidget(self.log_view)

        self.activity_log = ActivityLog(self.log_view)
        self.activity_log.log("SmartFileManager started", ActivityLog.SUCCESS)
        return w

    def _build_central(self):
        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Breadcrumb bar
        self.breadcrumb_widget = QWidget()
        self.breadcrumb_widget.setMinimumHeight(36)
        self.breadcrumb_layout = QHBoxLayout(self.breadcrumb_widget)
        self.breadcrumb_layout.setContentsMargins(8, 4, 8, 4)
        self.breadcrumb_layout.setSpacing(2)
        main_layout.addWidget(self.breadcrumb_widget)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        main_layout.addWidget(sep)

        # File table
        self.file_table = QTableView()
        self.file_model = FileTableModel()
        
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.file_model)
        self.proxy_model.setFilterKeyColumn(0)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.file_table.setModel(self.proxy_model)
        self.file_table.setAlternatingRowColors(True)
        self.file_table.setSortingEnabled(True)
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.file_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.file_table.doubleClicked.connect(self._on_file_double_click)
        self.file_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_table.customContextMenuRequested.connect(self._show_context_menu)
        self.file_table.selectionModel().selectionChanged.connect(self._on_selection_changed)

        # Column widths
        hdr = self.file_table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.Stretch)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.file_table.verticalHeader().setVisible(False)
        self.file_table.verticalHeader().setDefaultSectionSize(30)

        main_layout.addWidget(self.file_table)
        self.setCentralWidget(central)

        # File watcher
        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.directoryChanged.connect(self._on_dir_changed)

        self._show_hidden = False

    # ── NAVIGATION ───────────────────────────────────────

    def _navigate(self, path: str, add_history: bool = True):
        if not os.path.isdir(path):
            return
        
        self.current_path = path
        
        if add_history:
            # Trim forward history
            self.history = self.history[:self.history_idx + 1]
            if not self.history or self.history[-1] != path:
                self.history.append(path)
                self.history_idx = len(self.history) - 1

        self.address_bar.setText(path)
        self.file_model.load_path(path)
        self._update_breadcrumb(path)
        self._update_status()
        self._update_nav_buttons()
        self._update_rename_preview()

        # Update file watcher
        self.file_watcher.removePaths(self.file_watcher.directories())
        self.file_watcher.addPath(path)

        self.activity_log.log(f"Navigated to: {path}", ActivityLog.INFO)

    def _navigate_address(self):
        path = self.address_bar.text().strip()
        if os.path.isdir(path):
            self._navigate(path)
        else:
            self.status_path.setText(f"❌ Invalid path: {path}")

    def _go_back(self):
        if self.history_idx > 0:
            self.history_idx -= 1
            self._navigate(self.history[self.history_idx], add_history=False)

    def _go_forward(self):
        if self.history_idx < len(self.history) - 1:
            self.history_idx += 1
            self._navigate(self.history[self.history_idx], add_history=False)

    def _go_up(self):
        parent = str(Path(self.current_path).parent)
        if parent != self.current_path:
            self._navigate(parent)

    def _update_nav_buttons(self):
        self.btn_back.setEnabled(self.history_idx > 0)
        self.btn_forward.setEnabled(self.history_idx < len(self.history) - 1)

    def _update_breadcrumb(self, path: str):
        # Clear
        while self.breadcrumb_layout.count():
            item = self.breadcrumb_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        parts = Path(path).parts
        full = ""
        for i, part in enumerate(parts):
            full = os.path.join(full, part) if full else part
            if platform.system() == "Windows" and i == 0:
                full = part + "\\"
            
            btn = QPushButton(part)
            btn.setFlat(True)
            btn.setStyleSheet("QPushButton { padding: 2px 6px; border-radius: 4px; font-size: 12px; }"
                            "QPushButton:hover { background: rgba(124,58,237,0.15); color: #A78BFA; }")
            p = full
            btn.clicked.connect(lambda _, p=p: self._navigate(p))
            self.breadcrumb_layout.addWidget(btn)

            if i < len(parts) - 1:
                sep = QLabel("›")
                sep.setStyleSheet("color: #4B5563; padding: 0 2px;")
                self.breadcrumb_layout.addWidget(sep)

        self.breadcrumb_layout.addStretch()

    def _update_status(self):
        count = self.file_model.rowCount()
        self.status_path.setText(f"  📁  {self.current_path}")
        self.status_count.setText(f"  {count} items  ")

    def _on_selection_changed(self):
        indices = self.file_table.selectionModel().selectedRows()
        if not indices:
            self.status_selection.setText("")
            return
        total_size = 0
        names = []
        for idx in indices:
            src_idx = self.proxy_model.mapToSource(idx)
            row = self.file_model.get_row(src_idx.row())
            if row:
                if row['is_dir']:
                    pass
                else:
                    total_size += row['size']
                names.append(row['name'])
        
        count = len(names)
        if count == 1:
            self.status_selection.setText(f"  Selected: {names[0]}  ")
        else:
            size_str = self.file_model._format_size(total_size) if total_size else ""
            self.status_selection.setText(f"  {count} selected  {size_str}  ")
        
        self._update_rename_preview()

    def _on_dir_changed(self, path: str):
        if path == self.current_path:
            self._refresh()

    def _on_tree_expanded(self, index: QModelIndex):
        self.drive_model.load_children(index)

    def _on_tree_clicked(self, index: QModelIndex):
        item = self.drive_model.itemFromIndex(index)
        if not item:
            return
        kind = item.data(Qt.UserRole)
        if kind == "header":
            return
        path = item.data(Qt.UserRole + 1)
        if path and os.path.isdir(path):
            self._navigate(path)

    def _on_file_double_click(self, index: QModelIndex):
        src_idx = self.proxy_model.mapToSource(index)
        row = self.file_model.get_row(src_idx.row())
        if not row:
            return
        if row['is_dir']:
            self._navigate(row['path'])
        else:
            try:
                QDesktopServices.openUrl(
                    __import__("PySide6.QtCore", fromlist=["QUrl"]).QUrl.fromLocalFile(row['path'])
                )
                self.activity_log.log(f"Opened: {row['name']}", ActivityLog.INFO)
            except Exception as e:
                self.activity_log.log(f"Failed to open {row['name']}: {e}", ActivityLog.ERROR)

    def _filter_files(self, text: str):
        self.proxy_model.setFilterWildcard(f"*{text}*")

    def _refresh(self):
        self.file_model.load_path(self.current_path)
        self._update_status()
        self._update_rename_preview()

    def _toggle_hidden(self):
        self._show_hidden = not self._show_hidden
        self._refresh()

    # ── FILE OPERATIONS ───────────────────────────────────

    def _get_selected_paths(self) -> List[str]:
        paths = []
        for idx in self.file_table.selectionModel().selectedRows():
            src_idx = self.proxy_model.mapToSource(idx)
            row = self.file_model.get_row(src_idx.row())
            if row:
                paths.append(row['path'])
        return paths

    def _new_folder(self):
        name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if ok and name:
            new_path = os.path.join(self.current_path, name)
            try:
                os.makedirs(new_path, exist_ok=True)
                self.activity_log.log(f"Created folder: {name}", ActivityLog.CREATE)
                self._refresh()
            except Exception as e:
                self.activity_log.log(f"Error creating folder: {e}", ActivityLog.ERROR)
                QMessageBox.critical(self, "Error", str(e))

    def _new_file(self):
        name, ok = QInputDialog.getText(self, "New File", "File name:")
        if ok and name:
            new_path = os.path.join(self.current_path, name)
            try:
                with open(new_path, "w") as f:
                    pass
                self.activity_log.log(f"Created file: {name}", ActivityLog.CREATE)
                self._refresh()
            except Exception as e:
                self.activity_log.log(f"Error creating file: {e}", ActivityLog.ERROR)

    def _copy_files(self):
        paths = self._get_selected_paths()
        if paths:
            self._clipboard_paths = paths
            self._clipboard_mode = "copy"
            self.activity_log.log(f"Copied {len(paths)} item(s) to clipboard", ActivityLog.COPY)
            self.status_selection.setText(f"  📋 {len(paths)} copied  ")

    def _cut_files(self):
        paths = self._get_selected_paths()
        if paths:
            self._clipboard_paths = paths
            self._clipboard_mode = "cut"
            self.activity_log.log(f"Cut {len(paths)} item(s) to clipboard", ActivityLog.MOVE)

    def _paste_files(self):
        if not self._clipboard_paths:
            return
        errors = []
        for src in self._clipboard_paths:
            name = os.path.basename(src)
            dst = os.path.join(self.current_path, name)
            # Avoid overwrite
            if os.path.exists(dst):
                base, ext = os.path.splitext(name)
                dst = os.path.join(self.current_path, f"{base}_copy{ext}")
            try:
                if self._clipboard_mode == "copy":
                    if os.path.isdir(src):
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
                    self.activity_log.log(f"Copied: {name} → {self.current_path}", ActivityLog.COPY)
                else:
                    shutil.move(src, dst)
                    self.activity_log.log(f"Moved: {name} → {self.current_path}", ActivityLog.MOVE)
            except Exception as e:
                errors.append(str(e))
                self.activity_log.log(f"Error pasting {name}: {e}", ActivityLog.ERROR)
        
        if self._clipboard_mode == "cut":
            self._clipboard_paths = []
        
        self._refresh()
        if errors:
            QMessageBox.warning(self, "Paste Errors", "\n".join(errors))

    def _select_all(self):
        self.file_table.selectAll()

    def _invert_selection(self):
        sel = self.file_table.selectionModel()
        all_rows = set(range(self.proxy_model.rowCount()))
        selected_rows = set(idx.row() for idx in sel.selectedRows())
        self.file_table.clearSelection()
        for r in all_rows - selected_rows:
            self.file_table.selectRow(r)

    def _delete_files(self):
        paths = self._get_selected_paths()
        if not paths:
            return
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete {len(paths)} item(s)?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            for path in paths:
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                    self.activity_log.log(f"Deleted: {os.path.basename(path)}", ActivityLog.DELETE)
                except Exception as e:
                    self.activity_log.log(f"Error deleting: {e}", ActivityLog.ERROR)
            self._refresh()

    def _rename_single(self):
        paths = self._get_selected_paths()
        if len(paths) != 1:
            return
        old_path = paths[0]
        old_name = os.path.basename(old_path)
        new_name, ok = QInputDialog.getText(self, "Rename", "New name:", text=old_name)
        if ok and new_name and new_name != old_name:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            try:
                os.rename(old_path, new_path)
                self.activity_log.log(f"Renamed: {old_name} → {new_name}", ActivityLog.RENAME)
                self._refresh()
            except Exception as e:
                self.activity_log.log(f"Rename error: {e}", ActivityLog.ERROR)
                QMessageBox.critical(self, "Error", str(e))

    def _open_terminal(self):
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["cmd"], cwd=self.current_path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-a", "Terminal", self.current_path])
            else:
                for term in ["gnome-terminal", "xterm", "konsole", "xfce4-terminal"]:
                    try:
                        subprocess.Popen([term], cwd=self.current_path)
                        break
                    except FileNotFoundError:
                        continue
            self.activity_log.log(f"Opened terminal at: {self.current_path}", ActivityLog.INFO)
        except Exception as e:
            self.activity_log.log(f"Terminal error: {e}", ActivityLog.ERROR)

    # ── SMART RENAME ─────────────────────────────────────

    def _get_rename_params(self) -> dict:
        case_map = {0: "none", 1: "lower", 2: "upper", 3: "title", 4: "camel", 5: "snake"}
        try:
            num_start = int(self.num_start.text() or 1)
        except:
            num_start = 1
        try:
            num_padding = int(self.num_padding.text() or 2)
        except:
            num_padding = 2
        return {
            "rules": SmartRenameEngine.parse_rules(self.rule_input.text()),
            "prefix": self.prefix_input.text(),
            "suffix": self.suffix_input.text(),
            "case_mode": case_map.get(self.case_combo.currentIndex(), "none"),
            "numbering": self.chk_numbering.isChecked(),
            "num_start": num_start,
            "num_padding": num_padding,
            "num_sep": self.num_sep.text() or "_",
            "change_ext": self.ext_input.text(),
            "remove_special": self.chk_remove_special.isChecked(),
            "remove_spaces": self.chk_remove_spaces.isChecked(),
            "space_replacement": self.space_rep.text() or "_",
            "regex_enabled": self.chk_regex_enabled.isChecked(),
            "regex_pattern": self.regex_pattern.text(),
            "regex_replace": self.regex_replace.text(),
        }

    def _compute_new_name(self, name: str, params: dict, counter: int = 0) -> str:
        new_name = name
        
        # Regex mode
        if params.get("regex_enabled") and params.get("regex_pattern"):
            try:
                stem = Path(new_name).stem
                ext = Path(new_name).suffix
                stem = re.sub(params["regex_pattern"], params.get("regex_replace", ""), stem)
                new_name = stem + ext
            except re.error:
                pass
        
        return SmartRenameEngine.apply_rules(
            new_name,
            rules=params["rules"],
            prefix=params["prefix"],
            suffix=params["suffix"],
            numbering=params["numbering"],
            num_start=params["num_start"],
            num_padding=params["num_padding"],
            num_sep=params["num_sep"],
            counter=counter,
            change_ext=params["change_ext"],
            case_mode=params["case_mode"],
            remove_special=params["remove_special"],
            remove_spaces=params["remove_spaces"],
            space_replacement=params["space_replacement"],
        )

    def _update_rename_preview(self):
        params = self._get_rename_params()
        
        # Use selected files, or first 5 in folder
        selected = self._get_selected_paths()
        if selected:
            names = [os.path.basename(p) for p in selected[:10]]
        else:
            names = [self.file_model.get_row(i)['name'] 
                    for i in range(min(5, self.file_model.rowCount()))
                    if self.file_model.get_row(i)]

        self.preview_model.clear()
        self.preview_model.setHorizontalHeaderLabels(["Original", "→", "Renamed"])

        for i, name in enumerate(names):
            new_name = self._compute_new_name(name, params, i)
            old_item = QStandardItem(name)
            old_item.setEditable(False)
            arrow_item = QStandardItem("→")
            arrow_item.setEditable(False)
            arrow_item.setTextAlignment(Qt.AlignCenter)
            new_item = QStandardItem(new_name)
            new_item.setEditable(False)
            
            if new_name != name:
                new_item.setForeground(QColor("#6EE7B7" if self.current_theme == "dark" else "#16A34A"))
            else:
                new_item.setForeground(QColor("#64748B"))
                
            self.preview_model.appendRow([old_item, arrow_item, new_item])

    def _apply_rename(self):
        params = self._get_rename_params()
        
        selected = self._get_selected_paths()
        if not selected:
            # Ask if user wants to rename all
            reply = QMessageBox.question(
                self, "Apply Rename",
                "No files selected. Rename all files in current folder?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
            selected = [
                self.file_model.get_row(i)['path']
                for i in range(self.file_model.rowCount())
                if self.file_model.get_row(i)
            ]

        renames = []
        for i, path in enumerate(selected):
            old_name = os.path.basename(path)
            new_name = self._compute_new_name(old_name, params, i)
            if new_name != old_name:
                renames.append((old_name, new_name, path))

        if not renames:
            QMessageBox.information(self, "No Changes", "No files would be renamed with current rules.")
            return

        preview_pairs = [(old, new) for old, new, _ in renames]
        dlg = RenamePreviewDialog(preview_pairs, self)
        if dlg.exec() == QDialog.Accepted:
            self._last_rename_ops = []
            errors = []
            for old_name, new_name, old_path in renames:
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                try:
                    os.rename(old_path, new_path)
                    self._last_rename_ops.append((new_path, old_path))
                    self.activity_log.log(f"Renamed: {old_name} → {new_name}", ActivityLog.RENAME)
                except Exception as e:
                    errors.append(f"{old_name}: {e}")
                    self.activity_log.log(f"Rename error {old_name}: {e}", ActivityLog.ERROR)
            
            self._refresh()
            if errors:
                QMessageBox.warning(self, "Some Errors", "\n".join(errors))
            else:
                self.activity_log.log(f"Batch rename complete: {len(renames)} files", ActivityLog.SUCCESS)

    def _show_full_preview(self):
        params = self._get_rename_params()
        selected = self._get_selected_paths()
        if not selected:
            selected = [
                self.file_model.get_row(i)['path']
                for i in range(self.file_model.rowCount())
                if self.file_model.get_row(i)
            ]
        
        pairs = []
        for i, path in enumerate(selected):
            old_name = os.path.basename(path)
            new_name = self._compute_new_name(old_name, params, i)
            pairs.append((old_name, new_name))
        
        dlg = RenamePreviewDialog(pairs, self)
        dlg.exec()

    def _undo_last_rename(self):
        if not self._last_rename_ops:
            QMessageBox.information(self, "Undo", "No rename operations to undo.")
            return
        
        errors = []
        for new_path, old_path in self._last_rename_ops:
            try:
                os.rename(new_path, old_path)
                name = os.path.basename(old_path)
                self.activity_log.log(f"Undone rename: → {name}", ActivityLog.WARNING)
            except Exception as e:
                errors.append(str(e))
        
        self._last_rename_ops = []
        self._refresh()
        if errors:
            QMessageBox.warning(self, "Undo Errors", "\n".join(errors))

    def _batch_rename_dialog(self):
        self.rename_dock.show()
        self.rename_dock.raise_()

    def _show_rename_panel(self):
        self.rename_dock.show()
        self.rename_dock.raise_()
        self.rule_input.setFocus()

    # ── CONTEXT MENU ─────────────────────────────────────

    def _show_context_menu(self, pos: QPoint):
        menu = QMenu(self)
        selected = self._get_selected_paths()
        
        if selected:
            menu.addAction("📂  Open", lambda: self._open_selected())
            menu.addSeparator()
            menu.addAction("✂️  Cut", self._cut_files)
            menu.addAction("📋  Copy", self._copy_files)
        
        if self._clipboard_paths:
            menu.addAction("📌  Paste", self._paste_files)
        
        if selected:
            menu.addSeparator()
            if len(selected) == 1:
                menu.addAction("✏️  Rename", self._rename_single)
            menu.addAction("🗑️  Delete", self._delete_files)
            menu.addSeparator()
            menu.addAction("📊  Properties", lambda: self._show_properties())
            menu.addAction("📋  Copy Path", lambda: self._copy_path_to_clipboard())

        menu.addSeparator()
        menu.addAction("➕  New Folder", self._new_folder)
        menu.addAction("📄  New File", self._new_file)
        menu.addSeparator()
        menu.addAction("↻  Refresh", self._refresh)
        menu.addAction("💻  Open Terminal Here", self._open_terminal)
        
        menu.exec(self.file_table.viewport().mapToGlobal(pos))

    def _open_selected(self):
        for path in self._get_selected_paths():
            if os.path.isdir(path):
                self._navigate(path)
            else:
                from PySide6.QtCore import QUrl
                QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def _show_properties(self):
        paths = self._get_selected_paths()
        if paths:
            dlg = PropertiesDialog(paths[0], self)
            dlg.exec()

    def _copy_path_to_clipboard(self):
        paths = self._get_selected_paths()
        if paths:
            QApplication.clipboard().setText("\n".join(paths))
            self.activity_log.log(f"Path copied to clipboard: {len(paths)} path(s)", ActivityLog.INFO)

    # ── TOOLS ─────────────────────────────────────────────

    def _calc_folder_size(self):
        paths = self._get_selected_paths()
        dirs = [p for p in paths if os.path.isdir(p)]
        if not dirs:
            dirs = [self.current_path]
        
        for d in dirs:
            total = 0
            count = 0
            try:
                for f in Path(d).rglob("*"):
                    if f.is_file():
                        total += f.stat().st_size
                        count += 1
            except:
                pass
            size_str = self.file_model._format_size(total)
            self.activity_log.log(
                f"Folder size: {os.path.basename(d)} = {size_str} ({count} files)",
                ActivityLog.INFO
            )
        
        self.statusBar().showMessage(f"Size calculation complete. See Activity Log.", 3000)

    def _find_duplicates(self):
        import hashlib
        self.activity_log.log("Scanning for duplicates...", ActivityLog.INFO)
        
        hashes: Dict[str, List[str]] = {}
        try:
            for f in Path(self.current_path).iterdir():
                if f.is_file():
                    try:
                        h = hashlib.md5(f.read_bytes()).hexdigest()
                        hashes.setdefault(h, []).append(f.name)
                    except:
                        pass
        except:
            pass
        
        dupes = {h: names for h, names in hashes.items() if len(names) > 1}
        if dupes:
            for h, names in dupes.items():
                self.activity_log.log(
                    f"Duplicates: {', '.join(names)}",
                    ActivityLog.WARNING
                )
            QMessageBox.information(
                self, "Duplicates Found",
                f"Found {len(dupes)} group(s) of duplicate files. See Activity Log."
            )
        else:
            self.activity_log.log("No duplicates found in current folder", ActivityLog.SUCCESS)
            QMessageBox.information(self, "No Duplicates", "No duplicate files found.")

    def _export_log(self):
        from PySide6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Log", 
            os.path.join(str(Path.home()), "smartfilemanager_log.txt"),
            "Text Files (*.txt)"
        )
        if path:
            self.activity_log.export(path)
            self.activity_log.log(f"Log exported to: {path}", ActivityLog.SUCCESS)

    # ── THEME ─────────────────────────────────────────────

    def _apply_theme(self, theme: str):
        self.current_theme = theme
        if theme == "dark":
            self.setStyleSheet(DARK_QSS)
            self.theme_btn.setText("🌙  Dark")
            self.theme_btn.setChecked(True)
        else:
            self.setStyleSheet(LIGHT_QSS)
            self.theme_btn.setText("☀️  Light")
            self.theme_btn.setChecked(False)
        
        # Breadcrumb needs re-styling
        self._update_breadcrumb(self.current_path)

    def _toggle_theme(self):
        if self.current_theme == "dark":
            self._apply_theme("light")
        else:
            self._apply_theme("dark")

    # ── HELP & ABOUT ──────────────────────────────────────

    def _show_help(self):
        dlg = HelpDialog(self)
        dlg.exec()

    def _show_about(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("About SmartFileManager")
        dlg.setFixedSize(480, 400)
        layout = QVBoxLayout(dlg)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QWidget()
        header.setFixedHeight(100)
        header.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:1,"
                             "stop:0 #4C1D95, stop:1 #1E1B4B);")
        h_layout = QVBoxLayout(header)
        h_layout.setContentsMargins(24, 16, 24, 16)
        title = QLabel("SmartFileManager")
        title.setStyleSheet("font-size: 22px; font-weight: 700; color: white; background: transparent;")
        sub = QLabel("Enterprise Edition v2.0  •  Built with PySide6")
        sub.setStyleSheet("font-size: 12px; color: #A78BFA; background: transparent;")
        h_layout.addWidget(title)
        h_layout.addWidget(sub)
        layout.addWidget(header)

        # Body
        body = QWidget()
        b_layout = QVBoxLayout(body)
        b_layout.setContentsMargins(24, 16, 24, 12)
        b_layout.setSpacing(10)

        desc = QLabel(
            "A professional file management application with smart rename, "
            "multi-pattern batch operations, docking system, and activity logging."
        )
        desc.setWordWrap(True)
        b_layout.addWidget(desc)

        features = QLabel(
            "<b>Features:</b><br>"
            "• Smart multi-pattern rename with live preview<br>"
            "• Regex-based rename, auto-numbering, case conversion<br>"
            "• Docking system with Drive Tree Explorer<br>"
            "• Activity Log with TXT/CSV export<br>"
            "• Duplicate file detection<br>"
            "• Dark and Light themes (no OS theme conflict)<br>"
            "• Breadcrumb navigation &amp; history<br>"
            "• QSettings: layout &amp; preferences persistence"
        )
        features.setWordWrap(True)
        b_layout.addWidget(features)
        b_layout.addStretch()

        # Copyright
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        b_layout.addWidget(sep)

        copy_lbl = QLabel("© Macan Angkasa — All Rights Reserved")
        copy_lbl.setAlignment(Qt.AlignCenter)
        copy_lbl.setStyleSheet("color: #7C3AED; font-weight: 600; padding: 6px 0;")
        b_layout.addWidget(copy_lbl)

        btns = QDialogButtonBox(QDialogButtonBox.Ok)
        btns.accepted.connect(dlg.accept)
        b_layout.addWidget(btns)

        layout.addWidget(body)
        dlg.exec()

    # ── LAYOUT RESET ──────────────────────────────────────

    def _reset_layout(self):
        """Restore all docks to default positions and show them."""
        # Show all docks
        for dock, _ in self._dock_list:
            dock.setVisible(True)
            dock.setFloating(False)

        # Re-add to default positions
        self.addDockWidget(Qt.LeftDockWidgetArea, self.drive_dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.rename_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.log_dock)
        self.splitDockWidget(self.rename_dock, self.log_dock, Qt.Horizontal)
        self.activity_log.log("Layout reset to default", ActivityLog.INFO)

    # ── EXPORT REPORT ─────────────────────────────────────

    def _export_report(self):
        data = [self.file_model.get_row(i)
                for i in range(self.file_model.rowCount())
                if self.file_model.get_row(i)]
        dlg = ExportReportDialog(self.current_path, data, self)
        if dlg.exec() == QDialog.Accepted:
            self.activity_log.log(f"Report exported from: {self.current_path}", ActivityLog.SUCCESS)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SmartFileManager")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("MacanAngkasa")
    app.setOrganizationDomain("macanangkasa.com")

    # Use Fusion style as base to avoid OS theme conflicts;
    # all visual customization is done via explicit QSS
    app.setStyle("Fusion")

    window = SmartFileManager()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()