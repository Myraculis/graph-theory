import tkinter as tk
from tkinter import simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph Editor")
        self.geometry("800x600")

        self.graph = nx.Graph()
        self.nodes = []
        self.edges = []
        self.dragging_node = None

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.canvas.mpl_connect("button_press_event", self.on_click)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_click(self, event):
        if event.button == 3:  # Right-click
            self.show_context_menu(event)
        elif event.button == 1:  # Left-click
            self.create_node(event)

    def show_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Create Node", command=lambda: self.create_node(event))
        if self.nodes:
            menu.add_command(label="Create Edge", command=lambda: self.create_edge())
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def create_node(self, event):
        node_id = simpledialog.askstring("Node ID", "Enter node ID:")
        if node_id:
            # Convert screen coordinates to data coordinates
            x_screen, y_screen = event.x, event.y
            x_data, y_data = self.canvas_to_data(x_screen, y_screen)
            print(f"Screen coordinates: ({x_screen}, {y_screen}) -> Data coordinates: ({x_data}, {y_data})")
            self.graph.add_node(node_id, pos=(x_data, y_data))
            self.nodes.append(node_id)
            self.draw_graph()

    def create_edge(self):
        if len(self.nodes) < 2:
            return
        node1 = simpledialog.askstring("Edge", "Enter first node ID:")
        node2 = simpledialog.askstring("Edge", "Enter second node ID:")
        if node1 in self.nodes and node2 in self.nodes:
            self.graph.add_edge(node1, node2)
            self.edges.append((node1, node2))
            self.draw_graph()

    def draw_graph(self):
        self.ax.clear()
        pos = nx.get_node_attributes(self.graph, 'pos')
        print(f"Drawing graph with positions: {pos}")
        # Ensure that the axes limits are set to the full range of the canvas
        self.ax.set_xlim(0, self.canvas.get_width_height()[0])
        self.ax.set_ylim(self.canvas.get_width_height()[1], 0)  # Reverse the y-axis to match the canvas coordinates
        nx.draw(self.graph, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray', ax=self.ax)
        self.canvas.draw()

    def canvas_to_data(self, x, y):
        """Convert canvas coordinates to data coordinates."""
        trans = self.ax.transData.inverted()
        return trans.transform((x, y))

    def on_close(self):
        self.destroy()
        self.quit()

if __name__ == "__main__":
    app = GraphEditor()
    app.mainloop()
