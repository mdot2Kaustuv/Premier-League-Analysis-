from tkinter import *
import tkinter as tk
from tkinter import ttk

# main window
root = tk.Tk()
root.title("PREMIER LEAGUE ANALYSIS TOOL")
root.geometry("800x500")

# main container
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# title
title_label = tk.Label(
    main_frame, text="PREMIER LEAGUE ANALYSIS TOOL", font=("Helvetica", 20, "bold")
)
title_label.pack(pady=(0, 20))

# two-column layout player and club
content_frame = tk.Frame(main_frame)
content_frame.pack(fill=tk.BOTH, expand=True)

# Player column (left)
left_frame = tk.LabelFrame(
    content_frame, text="Player", font=("Helvetica", 12, "bold"), padx=10, pady=10
)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

# Add some content to left frame
left_label = tk.Label(
    left_frame, text="Player analysis will appear here", font=("Helvetica", 10)
)
left_label.pack(pady=20)

# table for players
player_table_frame = tk.Frame(left_frame)
player_table_frame.pack(fill=tk.BOTH, expand=True)

# treeview for players
player_columns = ("Name", "Club", "Goals")
player_tree = ttk.Treeview(
    player_table_frame, columns=player_columns, show="headings", height=8
)

for col in player_columns:
    player_tree.heading(col, text=col)
    player_tree.column(col, width=100)

# scrollbar for player table
player_scrollbar = ttk.Scrollbar(
    player_table_frame, orient=tk.VERTICAL, command=player_tree.yview
)
player_tree.configure(yscrollcommand=player_scrollbar.set)
player_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
player_tree.pack(fill=tk.BOTH, expand=True)

# Squad column (right)
right_frame = tk.LabelFrame(
    content_frame, text="Squad", font=("Helvetica", 12, "bold"), padx=10, pady=10
)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

# "View a club" section
view_club_frame = tk.Frame(right_frame)
view_club_frame.pack(fill=tk.X, pady=(0, 15))

view_club_label = tk.Label(view_club_frame, text="View a club:", font=("Helvetica", 10))
view_club_label.pack(side=tk.LEFT, padx=(0, 10))

# Club selector
club_selector = ttk.Combobox(
    view_club_frame,
    values=["Select Club"],
    state="readonly",
    width=20,
)
club_selector.pack(side=tk.LEFT)
club_selector.current(0)

# table for squads
squad_table_frame = tk.Frame(right_frame)
squad_table_frame.pack(fill=tk.BOTH, expand=True)

# Create Treeview for squads
squad_columns = ("Squad", "Points", "Wins")
squad_tree = ttk.Treeview(
    squad_table_frame, columns=squad_columns, show="headings", height=8
)

for col in squad_columns:
    squad_tree.heading(col, text=col)
    squad_tree.column(col, width=100)

# scrollbar for squad table
squad_scrollbar = ttk.Scrollbar(
    squad_table_frame, orient=tk.VERTICAL, command=squad_tree.yview
)
squad_tree.configure(yscrollcommand=squad_scrollbar.set)
squad_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
squad_tree.pack(fill=tk.BOTH, expand=True)

# Start the application
root.mainloop()
