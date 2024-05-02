import time

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import DataTable
from textual.worker import Worker, get_current_worker

ROWS = [
    ("lane", "swimmer", "country", "time"),
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),
]


class TableApp(App):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*ROWS[0])
        self.add_rows()

    def add_rows(self):
        table = self.query_one(DataTable)
        table.add_rows(ROWS[1:5])
        self.update_table()
        
        
    @work(thread=True)
    def update_table(self):
        worker = get_current_worker()
        time.sleep(5)
        
        table = self.query_one(DataTable)
        if not worker.is_cancelled:
            self.call_from_thread(table.add_rows, ROWS[5:])

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        self.log(event)        

app = TableApp()
if __name__ == "__main__":
    app.run()
