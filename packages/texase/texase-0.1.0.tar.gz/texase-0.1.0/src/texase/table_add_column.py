import time

import numpy as np
from textual.app import App, ComposeResult
from textual.coordinate import Coordinate
from textual.widgets import DataTable

ROWS = [f"header{i}" for i in range(5)]
ROWS = [ROWS] + [[f"row{i}c{j}" for j in range(5)] for i in range(10000)]
ROWS = np.asarray(ROWS)

class TableApp(App):
    BINDINGS = [('a', 'add_column', 'Add Column'),
                ('b', 'add_column_brute_force', 'Add Column Brute Force')]
    
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*ROWS[0, :-1])
        self.add_rows()

    def add_rows(self) -> None:
        table = self.query_one(DataTable)
        table.add_rows(ROWS[1:, :-1])
        
    def action_add_column(self) -> None:
        table = self.query_one(DataTable)
        col_key = table.add_column(ROWS[0, -1])
        col_index = table.get_column_index(col_key)
        values = ROWS[1:, -1]
        for i, val in enumerate(values[:-1]):
            table.update_cell_at(Coordinate(i, col_index), val)
        table._updated_cells.clear()
        table.update_cell_at(
            Coordinate(len(values) - 1, col_index),
            values[-1],
            update_width=True,
        )
        
    def action_add_column_brute_force(self) -> None:
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns(*ROWS[0, :])
        table.add_rows(ROWS[1:, :])

app = TableApp()
if __name__ == "__main__":
    app.run()
