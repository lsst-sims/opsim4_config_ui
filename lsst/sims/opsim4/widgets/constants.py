"""The CSS definition for the application.
"""
CSS = """
        QGroupBox {
            border: 1px solid gray;
            border-radius: 3px;
            margin-top: 0.5em;
            font-size: 16px;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center; /* position at the top center */
            padding: 0 3px;
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #D0D0D0, stop: 1 #F0F0F0);
        }

        QMenu {
            font-size: 16px;
        }

        QMenuBar {
            font-size: 16px;
        }

        QCheckBox {
            font-size: 16px;
        }

        QToolTip {
            font-size: 16px;
        }

        QLabel {
            font-size: 16px;
        }

        QRadioButton {
            font-size: 16px;
        }

        QComboBox {
            font-size: 16px;
        }

        QPushButton {
            font-size: 16px;
        }

        QPlainTextEdit {
            font-size: 16px;
        }

        QWizard::title {
            font-size: 16px;
        }

        QLineEdit {
            font-size: 16px;
            background: white;
            border: 2px solid gray;
            border-radius: 6px;
        }

        QLineEdit[readOnly="true"] {
            font-size: 16px;
            background: #f0f0f0;
        }

        QTabWidget::pane { /* The tab widget frame */
            border-top: 2px solid #C2C7CB;
        }

        QTabWidget::tab-bar {
            left: 5px; /* move to the right by 5px */
        }

        QTabBar::tab {
            font-size: 16px;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
            border: 2px solid #C4C4C3;
            border-bottom-color: #C2C7CB; /* same as the pane color */
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            padding: 2px;
            min-width: 15ex;
        }

        QTabBar::tab:selected, QTabBar::tab:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                        stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
        }

        QTabBar::tab:selected {
            border-color: #9B9B9B;
            border-bottom-color: #C2C7CB; /* same as pane color */
        }

        QTabBar::tab:!selected {
            margin-top: 2px; /* make non-selected tabs look smaller */
        }

        /* make use of negative margins for overlapping tabs */
        QTabBar::tab:selected {
            /* expand/overlap to the left and right by 4px */
            margin-left: -4px;
            margin-right: -4px;
        }

        QTabBar::tab:first:selected {
            margin-left: 0; /* the first selected tab has nothing to overlap with on the left */
        }

        QTabBar::tab:last:selected {
            margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
        }

        QTabBar::tab:only-one {
            margin: 0; /* if there is only one tab, we don't want overlapping margins */
        }
      """
