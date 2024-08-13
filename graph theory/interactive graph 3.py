import tkinter as tk
from tkinter import simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle

class GraphEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph Editor")
        self.geometry("1000x600")

        self.graph = nx.Graph()
        self.nodes = []
        self.edges = []
        self.first_node_created = False

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Remove axis ticks and labels
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)

        self.info_frame = tk.Frame(self)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.automorphisms_label = tk.Label(self.info_frame, text="Automorphisms: 0", font=("Helvetica", 16))
        self.automorphisms_label.pack(pady=20)

        self.cursor_pos_label = tk.Label(self.info_frame, text="Cursor Position: (0, 0)", font=("Helvetica", 16))
        self.cursor_pos_label.pack(pady=20)

        self.create_graph_button = tk.Button(self, text="Create Graph", command=self.create_initial_node)
        self.create_graph_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_initial_node(self):
        self.create_graph_button.destroy()
        # Create the first node at the center, relying on the existing feature to delete it
        self.create_node_at_position(500, 300)

    def create_node_at_position(self, x, y):
        # Automatically generate an ID for the initial node
        node_id = "Initial Node"
        x_data, y_data = self.canvas_to_data(x, y)
        print(f"Screen coordinates: ({x}, {y}) -> Data coordinates: ({x_data}, {y_data})")
        self.graph.add_node(node_id, pos=(x_data, y_data))
        self.nodes.append(node_id)
        self.update_automorphisms()
        self.draw_graph()
        if not self.first_node_created:
            self.first_node_created = True
            self.delete_first_node(node_id)

    def on_click(self, event):
        if event.button == 1:  # Left-click
            self.show_context_menu(event, left_click=True)
        elif event.button == 3:  # Right-click
            self.show_context_menu(event, left_click=False)

    def show_context_menu(self, event, left_click):
        menu = tk.Menu(self, tearoff=0)
        if left_click:
            menu.add_command(label="Create Node", command=lambda: self.create_node(event))
            if self.nodes:
                menu.add_command(label="Create Edge", command=self.create_edge)
        else:
            menu.add_command(label="Delete Node", command=self.select_node_for_deletion)
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def select_node_for_deletion(self):
        node_id = simpledialog.askstring("Delete Node", "Enter node ID to delete:")
        if node_id in self.nodes:
            self.delete_node(node_id)

    def on_motion(self, event):
        if event.inaxes:
            x_data, y_data = self.canvas_to_data(event.x, event.y)
            self.cursor_pos_label.config(text=f"Cursor Position: ({int(x_data)}, {int(y_data)})")

    def create_node(self, event):
        node_id = simpledialog.askstring("Node ID", "Enter node ID:")
        if node_id:
            x_screen, y_screen = event.x, event.y
            x_data, y_data = self.canvas_to_data(x_screen, y_screen)
           
            self.graph.add_node(node_id, pos=(x_data, y_data))
            self.nodes.append(node_id)
            self.update_automorphisms()
            self.draw_graph()
            if not self.first_node_created:
                self.first_node_created = True
                self.delete_first_node(node_id)

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

    def delete_first_node(self, node_id):
        self.graph.remove_node(node_id)
        self.nodes.remove(node_id)
        self.update_automorphisms()
        self.draw_graph()

    def delete_node(self, node_id):
        self.graph.remove_node(node_id)
        self.nodes.remove(node_id)
        self.update_automorphisms()
        self.draw_graph()

    def draw_graph(self):
        self.ax.clear()
        # Remove axis ticks and labels
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        pos = nx.get_node_attributes(self.graph, 'pos')
        self.ax.set_xlim(0, self.canvas.get_width_height()[0])
        self.ax.set_ylim(self.canvas.get_width_height()[1], 0)  # Reverse the y-axis to match the canvas coordinates

        # Draw the black border
        self.ax.add_patch(Rectangle((0, 0), self.canvas.get_width_height()[0], self.canvas.get_width_height()[1], fill=None, edgecolor='black', linewidth=2))

        nx.draw(self.graph, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray', ax=self.ax)
        self.canvas.draw()  # Force redraw of the canvas

    def canvas_to_data(self, x, y):
        """Convert canvas coordinates to data coordinates."""
        trans = self.ax.transData.inverted()
        return trans.transform((x, y))

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
