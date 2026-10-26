
import sys
import csv
import sqlite3
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QTabWidget,
    QMessageBox,
    QInputDialog,
    QFileDialog,
    QAbstractItemView,
)


DB_PATH = Path(__file__).resolve().parent / "database.db"


class BookManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Book Manager")
        self.resize(900, 600)
        self.setMinimumSize(750, 500)

        self.init_database()
        self.build_ui()
        self.apply_styles()
        self.load_books()

    # =====================================================
    # DATABASE
    # =====================================================
    def init_database(self):
        with sqlite3.connect(DB_PATH) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year TEXT NOT NULL
                )
            """)
            connection.commit()

    # =====================================================
    # MAIN UI
    # =====================================================
    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(20, 16, 20, 14)
        root.setSpacing(12)

        # Header
        header = QHBoxLayout()
        header.setSpacing(10)

        heading = QVBoxLayout()
        heading.setSpacing(3)

        eyebrow = QLabel("PERSONAL LIBRARY")
        eyebrow.setObjectName("eyebrow")

        page_title = QLabel("Book Manager")
        page_title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Organize your books and manage your collection."
        )
        subtitle.setObjectName("subtitle")

        heading.addWidget(eyebrow)
        heading.addWidget(page_title)
        heading.addWidget(subtitle)

        self.count_badge = QLabel("0 BOOKS")
        self.count_badge.setObjectName("countBadge")
        self.count_badge.setAlignment(Qt.AlignCenter)

        header.addLayout(heading)
        header.addStretch()
        header.addWidget(self.count_badge, alignment=Qt.AlignTop)

        root.addLayout(header)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setUsesScrollButtons(False)
        self.tabs.tabBar().setExpanding(False)

        self.tabs.addTab(self.create_library_tab(), "My Library")
        self.tabs.addTab(self.create_export_tab(), "Export Data")

        self.tabs.tabBar().setMinimumWidth(180)

        root.addWidget(self.tabs, 1)

        footer = QLabel("BOOK MANAGER  •  Hndraa Apps")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignCenter)

        root.addWidget(footer)

    # =====================================================
    # LIBRARY TAB
    # =====================================================
    def create_library_tab(self):
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Add book form
        form_card = QFrame()
        form_card.setObjectName("card")

        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(14, 12, 14, 14)
        form_layout.setSpacing(9)

        form_title = QLabel("Add a New Book")
        form_title.setObjectName("sectionTitle")
        form_layout.addWidget(form_title)

        fields = QHBoxLayout()
        fields.setSpacing(10)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Book title")

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Author name")

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("e.g. 2025")
        self.year_input.setMaxLength(4)

        fields.addWidget(
            self.make_field("BOOK TITLE", self.title_input), 3
        )
        fields.addWidget(
            self.make_field("AUTHOR", self.author_input), 2
        )
        fields.addWidget(
            self.make_field("YEAR", self.year_input), 1
        )

        form_layout.addLayout(fields)

        button_row = QHBoxLayout()
        button_row.setSpacing(8)
        button_row.addStretch()

        clear_button = QPushButton("Clear")
        clear_button.setObjectName("secondaryButton")
        clear_button.clicked.connect(self.clear_form)

        add_button = QPushButton("+ Add Book")
        add_button.setObjectName("primaryButton")
        add_button.clicked.connect(self.add_book)

        button_row.addWidget(clear_button)
        button_row.addWidget(add_button)

        form_layout.addLayout(button_row)
        layout.addWidget(form_card)

        # Book collection
        library_card = QFrame()
        library_card.setObjectName("card")

        library_layout = QVBoxLayout(library_card)
        library_layout.setContentsMargins(14, 12, 14, 12)
        library_layout.setSpacing(9)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        collection_title = QLabel("Your Collection")
        collection_title.setObjectName("sectionTitle")

        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("Search title or author...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self.filter_books)

        toolbar.addWidget(collection_title)
        toolbar.addStretch()
        toolbar.addWidget(self.search_input, 1)

        library_layout.addLayout(toolbar)

        self.table = QTableWidget()
        self.table.setObjectName("booksTable")
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["ID", "BOOK TITLE", "AUTHOR", "YEAR"]
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )
        self.table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(34)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.table.cellDoubleClicked.connect(self.edit_book)

        library_layout.addWidget(self.table, 1)

        actions = QHBoxLayout()
        actions.setSpacing(7)

        self.table_status = QLabel("Ready to manage your collection")
        self.table_status.setObjectName("mutedText")

        actions.addWidget(self.table_status)
        actions.addStretch()

        edit_button = QPushButton("Edit")
        edit_button.setObjectName("secondaryButton")
        edit_button.clicked.connect(self.edit_selected)

        delete_button = QPushButton("Delete")
        delete_button.setObjectName("dangerButton")
        delete_button.clicked.connect(self.delete_book)

        actions.addWidget(edit_button)
        actions.addWidget(delete_button)

        library_layout.addLayout(actions)
        layout.addWidget(library_card, 1)

        return page

    # =====================================================
    # EXPORT TAB
    # =====================================================
    def create_export_tab(self):
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(12, 12, 12, 12)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(22, 22, 22, 22)
        card_layout.setSpacing(12)

        icon = QLabel("CSV")
        icon.setObjectName("exportIcon")
        icon.setAlignment(Qt.AlignCenter)
        icon.setFixedSize(54, 54)

        title = QLabel("Export Your Library")
        title.setObjectName("exportTitle")

        description = QLabel(
            "Export your book collection into a CSV file "
            "that can be opened in spreadsheet applications."
        )
        description.setObjectName("subtitle")
        description.setWordWrap(True)

        self.export_count = QLabel("0 books ready to export")
        self.export_count.setObjectName("exportCount")

        export_button = QPushButton("Export to CSV")
        export_button.setObjectName("primaryButton")
        export_button.setMaximumWidth(180)
        export_button.clicked.connect(self.export_csv)

        card_layout.addWidget(icon, alignment=Qt.AlignLeft)
        card_layout.addWidget(title)
        card_layout.addWidget(description)
        card_layout.addWidget(self.export_count)
        card_layout.addWidget(export_button, alignment=Qt.AlignLeft)
        card_layout.addStretch()

        layout.addWidget(card)
        return page

    def make_field(self, label_text, input_widget):
        container = QWidget()

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        label = QLabel(label_text)
        label.setObjectName("fieldLabel")

        layout.addWidget(label)
        layout.addWidget(input_widget)

        return container

    # =====================================================
    # STYLES
    # =====================================================
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #FBF7F0;
                color: #49372B;
                font-family: "Segoe UI", Arial, sans-serif;
                font-size: 9pt;
            }

            QLabel {
                background: transparent;
                border: none;
            }

            QLabel#eyebrow {
                color: #B86B3D;
                font-size: 8pt;
                font-weight: 700;
                letter-spacing: 1.5px;
            }

            QLabel#pageTitle {
                color: #4A3428;
                font-size: 22pt;
                font-weight: 700;
            }

            QLabel#subtitle {
                color: #927D6D;
                font-size: 8.5pt;
            }

            QLabel#mutedText {
                color: #927D6D;
                font-size: 8pt;
            }

            QLabel#countBadge {
                background-color: #F3E5D5;
                color: #8A4D2D;
                border: 1px solid #E7D2BD;
                border-radius: 8px;
                padding: 7px 10px;
                font-size: 8pt;
                font-weight: 700;
            }

            QTabWidget::pane {
                background-color: #FFFDF9;
                border: 1px solid #E9DED1;
                border-radius: 11px;
                top: -1px;
            }

            QTabBar::tab {
                background-color: transparent;
                color: #927D6D;
                padding: 8px 18px;
                min-width: 75px;
                margin-right: 4px;
                border: 1px solid transparent;
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
                font-weight: 600;
            }

            QTabBar::tab:selected {
                background-color: #FFFDF9;
                color: #9B542F;
                border: 1px solid #E9DED1;
                border-bottom: 2px solid #D88752;
            }

            QTabBar::tab:hover:!selected {
                color: #70452F;
                background-color: #F6EDE2;
            }

            QFrame#card {
                background-color: #FFFDF9;
                border: 1px solid #E9DED1;
                border-radius: 11px;
            }

            QLabel#sectionTitle {
                color: #4A3428;
                font-size: 11pt;
                font-weight: 700;
            }

            QLabel#fieldLabel {
                color: #6F5543;
                font-size: 8pt;
                font-weight: 600;
            }

            QLineEdit {
                background-color: #FFFCF7;
                color: #49372B;
                border: 1px solid #E2D3C3;
                border-radius: 7px;
                padding: 7px 9px;
                min-height: 16px;
                selection-background-color: #E7B18A;
            }

            QLineEdit:focus {
                border: 1px solid #D88752;
                background-color: #FFFFFF;
            }

            QLineEdit#searchInput {
                padding: 7px 10px;
            }

            QTableWidget#booksTable {
                background-color: #FFFEFB;
                alternate-background-color: #FAF2E8;
                color: #49372B;
                border: 1px solid #E9DED1;
                border-radius: 7px;
                selection-background-color: #F0D5BE;
                selection-color: #4A3428;
                outline: 0;
            }

            QTableWidget#booksTable::item {
                padding: 5px;
                border: none;
            }

            QHeaderView::section {
                background-color: #F2E5D7;
                color: #80563D;
                border: none;
                border-bottom: 1px solid #E2D3C3;
                padding: 8px 7px;
                font-size: 8pt;
                font-weight: 700;
            }

            QScrollBar:vertical {
                background: #F8F0E6;
                width: 8px;
                margin: 2px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background: #D9B99E;
                min-height: 22px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:hover {
                background: #C89A76;
            }

            QScrollBar:horizontal {
                background: #F8F0E6;
                height: 8px;
                margin: 2px;
                border-radius: 4px;
            }

            QScrollBar::handle:horizontal {
                background: #D9B99E;
                min-width: 22px;
                border-radius: 4px;
            }

            QPushButton {
                border: none;
                border-radius: 7px;
                padding: 7px 11px;
                font-weight: 600;
                min-height: 14px;
            }

            QPushButton#primaryButton {
                color: #FFFFFF;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E5A06D, stop:1 #C87542
                );
            }

            QPushButton#primaryButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #D88752, stop:1 #B96638
                );
                color: #FFFFFF;
            }

            QPushButton#primaryButton:pressed {
                background-color: #A95832;
                color: #FFFFFF;
            }

            QPushButton#secondaryButton {
                background-color: #F5EADF;
                color: #79563F;
                border: 1px solid #E4D2C0;
            }

            QPushButton#secondaryButton:hover {
                background-color: #EEDBC9;
            }

            QPushButton#dangerButton {
                background-color: #FBE9E5;
                color: #A64035;
                border: 1px solid #F0C9C1;
            }

            QPushButton#dangerButton:hover {
                background-color: #F6D9D2;
            }

            QLabel#exportIcon {
                background-color: #F3E1CF;
                color: #A65E37;
                border: 1px solid #E7C9AF;
                border-radius: 11px;
                font-size: 12pt;
                font-weight: 800;
            }

            QLabel#exportTitle {
                color: #4A3428;
                font-size: 17pt;
                font-weight: 700;
            }

            QLabel#exportCount {
                color: #9B542F;
                font-weight: 700;
                padding: 5px 0;
            }

            QLabel#footer {
                color: #A18B79;
                font-size: 7pt;
            }

            QMessageBox {
                background-color: #FFFDF9;
            }

            QMessageBox QLabel {
                color: #49372B;
                min-width: 230px;
            }

            QMessageBox QPushButton {
                min-width: 70px;
                background-color: #D88752;
                color: #FFFFFF;
            }
        """)

    # =====================================================
    # ADD BOOK
    # =====================================================
    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        year = self.year_input.text().strip()

        if not title or not author or not year:
            QMessageBox.warning(
                self,
                "Incomplete Information",
                "Please fill in the title, author, and year."
            )
            return

        if not year.isdigit() or len(year) != 4:
            QMessageBox.warning(
                self,
                "Invalid Year",
                "Please enter a valid four-digit year."
            )
            return

        with sqlite3.connect(DB_PATH) as connection:
            connection.execute(
                """
                INSERT INTO books (title, author, year)
                VALUES (?, ?, ?)
                """,
                (title, author, year)
            )
            connection.commit()

        self.load_books()
        self.clear_form()
        self.table_status.setText(f'"{title}" was added.')

    # =====================================================
    # LOAD AND SEARCH BOOKS
    # =====================================================
    def load_books(self):
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, title, author, year
                FROM books
                ORDER BY id DESC
                """
            )
            rows = cursor.fetchall()

        self.table.setRowCount(0)

        for book in rows:
            row = self.table.rowCount()
            self.table.insertRow(row)

            for column, value in enumerate(book):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                if column in (0, 3):
                    item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(row, column, item)

        count = len(rows)
        self.count_badge.setText(
            f"{count} BOOK" if count == 1 else f"{count} BOOKS"
        )

        self.export_count.setText(
            f"{count} book{'s' if count != 1 else ''} ready to export"
        )

        self.filter_books(self.search_input.text())

    def filter_books(self, query):
        query = query.strip().lower()
        visible_count = 0

        for row in range(self.table.rowCount()):
            title_item = self.table.item(row, 1)
            author_item = self.table.item(row, 2)

            title = title_item.text().lower() if title_item else ""
            author = author_item.text().lower() if author_item else ""

            matches = query in title or query in author
            self.table.setRowHidden(row, not matches)

            if matches:
                visible_count += 1

        if query:
            self.table_status.setText(
                f"{visible_count} matching book(s)"
            )
        else:
            self.table_status.setText(
                f"{self.table.rowCount()} book(s) in your collection"
            )

    def clear_form(self):
        self.title_input.clear()
        self.author_input.clear()
        self.year_input.clear()
        self.title_input.setFocus()

    # =====================================================
    # SELECT BOOK
    # =====================================================
    def get_selected_book_id(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.information(
                self,
                "No Book Selected",
                "Please select a book first."
            )
            return None

        item = self.table.item(row, 0)

        if item is None:
            return None

        return int(item.text())

    # =====================================================
    # EDIT BOOK
    # =====================================================
    def edit_selected(self):
        book_id = self.get_selected_book_id()

        if book_id is not None:
            self.edit_book(self.table.currentRow(), 0)

    def edit_book(self, row, column):
        if row < 0:
            return

        id_item = self.table.item(row, 0)

        if id_item is None:
            return

        book_id = int(id_item.text())

        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT title, author, year
                FROM books
                WHERE id = ?
                """,
                (book_id,)
            )
            book = cursor.fetchone()

        if not book:
            return

        old_title, old_author, old_year = book

        new_title, ok = QInputDialog.getText(
            self,
            "Edit Book",
            "Book title:",
            text=old_title
        )
        if not ok:
            return

        new_title = new_title.strip()
        if not new_title:
            QMessageBox.warning(
                self, "Invalid Title", "Book title cannot be empty."
            )
            return

        new_author, ok = QInputDialog.getText(
            self,
            "Edit Book",
            "Author:",
            text=old_author
        )
        if not ok:
            return

        new_author = new_author.strip()
        if not new_author:
            QMessageBox.warning(
                self, "Invalid Author", "Author cannot be empty."
            )
            return

        new_year, ok = QInputDialog.getText(
            self,
            "Edit Book",
            "Year:",
            text=old_year
        )
        if not ok:
            return

        new_year = new_year.strip()
        if not new_year.isdigit() or len(new_year) != 4:
            QMessageBox.warning(
                self, "Invalid Year", "Enter a valid four-digit year."
            )
            return

        with sqlite3.connect(DB_PATH) as connection:
            connection.execute(
                """
                UPDATE books
                SET title = ?, author = ?, year = ?
                WHERE id = ?
                """,
                (new_title, new_author, new_year, book_id)
            )
            connection.commit()

        self.load_books()
        self.table_status.setText(f'"{new_title}" was updated.')

    # =====================================================
    # DELETE BOOK
    # =====================================================
    def delete_book(self):
        book_id = self.get_selected_book_id()

        if book_id is None:
            return

        row = self.table.currentRow()
        title_item = self.table.item(row, 1)
        title = title_item.text() if title_item else "this book"

        answer = QMessageBox.question(
            self,
            "Delete Book",
            f'Are you sure you want to delete "{title}"?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:
            return

        with sqlite3.connect(DB_PATH) as connection:
            connection.execute(
                "DELETE FROM books WHERE id = ?",
                (book_id,)
            )
            connection.commit()

        self.load_books()
        self.table_status.setText(f'"{title}" was deleted.')

    # =====================================================
    # EXPORT CSV
    # =====================================================
    def export_csv(self):
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, title, author, year
                FROM books
                ORDER BY id
                """
            )
            rows = cursor.fetchall()

        if not rows:
            QMessageBox.information(
                self,
                "Nothing to Export",
                "Your library is empty. Add some books first."
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Book Collection",
            "my_book_collection.csv",
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        if not file_path.lower().endswith(".csv"):
            file_path += ".csv"

        try:
            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["ID", "Book Title", "Author", "Year"]
                )
                writer.writerows(rows)

            QMessageBox.information(
                self,
                "Export Successful",
                f"Your collection was exported to:\n{file_path}"
            )

        except OSError as error:
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Could not export the file:\n{error}"
            )


# =========================================================
# RUN APPLICATION
# =========================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = BookManager()
    window.show()

    sys.exit(app.exec_())