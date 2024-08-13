#added automorphism counter

import tkinter as tk
from tkinter import simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph Editor")
        self.geometry("1000x600")

        self.graph = nx.Graph()
        self.nodes = []
        self.edges = []

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.mpl_connect("button_press_event", self.on_click)

        self.info_frame = tk.Frame(self)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.automorphisms_label = tk.Label(self.info_frame, text="Automorphisms: 0", font=("Helvetica", 16))
        self.automorphisms_label.pack(pady=20)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_click(self, event):
        if event.button == 3:  # Right-click
            self.show_context_menu(event)

    def show_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Create Node", command=lambda: self.create_node(event))
        if self.nodes:
            menu.add_command(label="Create Edge", command=lambda: self.create_edge())
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def create_node(self, event):
        node_id = simpledialog.askstring("Node ID", "Enter node ID:")
        if node_id:
            self.graph.add_node(node_id, pos=(event.x, event.y))
            self.nodes.append(node_id)
            self.update_automorphisms()
            self.draw_graph()

    def create_edge(self):
        if len(self.nodes) < 2:
            return
        node1 = simpledialog.askstring("Edge", "Enter first node ID:")
        node2 = simpledialog.askstring("Edge", "Enter second node ID:")
        if node1 in self.nodes and node2 in self.nodes:
            self.graph.add_edge(node1, node2)
            self.edges.append((node1, node2))
            self.update_automorphisms()
            self.draw_graph()

    def draw_graph(self):
        self.ax.clear()
        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray', ax=self.ax)
        self.canvas.draw()

    def update_automorphisms(self):
        from networkx.algorithms.isomorphism import GraphMatcher
        GM = GraphMatcher(self.graph, self.graph)
        automorphisms_count = sum(1 for _ in GM.isomorphisms_iter())
        self.automorphisms_label.config(text=f"Automorphisms: {automorphisms_count}")

    def on_close(self):
        self.destroy()
        self.quit()

if __name__ == "__main__":
    app = GraphEditor()
    app.mainloop()