import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# ================= COLORS & THEME =================
PRIMARY = "#22C55E"
DARK_BG = "#0B1120"
CARD_BG = "#070000"
TEXT_MUTED = "#9CA3AF"
NAV_BLUE = "#0A4EA3"

class PremierLeagueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Premier League Analysis")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        self.show_landing_page()
    
    def show_player_profile(self, player_name):
        profile_win = tk.Toplevel(self.root)
        profile_win.title(f"Player Profile - {player_name}")
        profile_win.geometry("400x500")
        profile_win.configure(bg=DARK_BG)

        # Profile Header
        tk.Label(profile_win, text=player_name, font=("Helvetica", 24, "bold"), 
                 bg=DARK_BG, fg=PRIMARY).pack(pady=20)

        try:
            df = pd.read_csv("players.csv")
            player_data = df[df['Player'] == player_name].iloc[0]
            
            # Display Stats 
            stats = [
                ("Team", player_data['Team']),
                ("Position", player_data['Position']),
                ("Goals", player_data['Goals']),
                ("Assists", player_data['Assists'])
            ]

            for label, value in stats:
                stat_frame = tk.Frame(profile_win, bg=DARK_BG)
                stat_frame.pack(fill="x", padx=40, pady=5)
                tk.Label(stat_frame, text=label, fg=TEXT_MUTED, bg=DARK_BG, font=("Helvetica", 12)).pack(side="left")
                tk.Label(stat_frame, text=value, fg="white", bg=DARK_BG, font=("Helvetica", 12, "bold")).pack(side="right")

        except Exception as e:
            tk.Label(profile_win, text="Profile data not found.", fg="red", bg=DARK_BG).pack()

        #close Button
        tk.Button(
            profile_win, 
            text="CLOSE PROFILE", 
            command=profile_win.destroy, 
            bg="#ffffff",         
            fg="black",           
            font=("Helvetica", 10, "bold"),
            padx=20, 
            pady=10,
            relief="flat",       
            cursor="hand2"        
        ).pack(pady=30)

    def show_team_members(self, team_name):
        squad_win = tk.Toplevel(self.root)
        squad_win.title(f"{team_name} - Squad Members")
        squad_win.geometry("700x600")
        squad_win.configure(bg="#0B1120")

        tk.Label(squad_win, text=f"{team_name} Official Squad", font=("Helvetica", 20, "bold"), 
                 bg="#0B1120", fg="#22C55E").pack(pady=(20, 10))

        # --- SEARCH SECTION ---
        search_frame = tk.Frame(squad_win, bg="#0B1120")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(search_frame, text="Search Player:", fg="white", bg="#0B1120").pack(side="left")
        
        # Use a StringVar to track typing in real-time
        search_var = tk.StringVar()
        search_ent = tk.Entry(search_frame, textvariable=search_var, font=("Helvetica", 12), 
                              bg="#1F2937", fg="white", insertbackground="white")
        search_ent.pack(side="left", padx=10, fill="x", expand=True)

        # --- TABLE SECTION ---
        cols = ("Player", "Position", "Goals", "Assists")
        tree = ttk.Treeview(squad_win, columns=cols, show="headings", height=15)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        tree.pack(fill="both", expand=True, padx=20, pady=10) 

        # --- CLICK TO OPEN PROFILE ---
        def on_player_click(event):
            selection = tree.selection()
            if selection:
                selected_item = selection[0]
                player_name = tree.item(selected_item)['values'][0]
                self.show_player_profile(player_name)

        tree.bind("<Double-1>", on_player_click)

        # --- FILTER & LOAD LOGIC ---
        def update_list(*args):
            search_term = search_var.get().lower()
            # Clear current table
            for item in tree.get_children():
                tree.delete(item)
            
            try:
                # IMPORTANT: Ensure your file is named 'players.csv'
                df = pd.read_csv("players.csv")
                
                # Filter by Team AND Search Term
                # Using .str.contains for flexible searching
                filtered_df = df[(df['Team'] == team_name) & 
                                 (df['Player'].str.lower().str.contains(search_term))]
                
                for _, row in filtered_df.iterrows():
                    tree.insert("", "end", values=(row['Player'], row['Position'], row['Goals'], row['Assists']))
            except Exception as e:
                print(f"Error loading players: {e}")

        # This tells Python: "Every time the text changes, run update_list"
        search_var.trace_add("write", update_list)

        # Run once at the start to show all players for the team
        update_list()
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_top_scorers(self, parent):
        # Container for the leaderboard
        container = tk.Frame(parent, bg="#102A43", padx=10, pady=10)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="🏆 Golden Boot Race", font=("Helvetica", 16, "bold"), 
                 bg="#102A43", fg="#22C55E").pack(pady=(0, 10))

        cols = ("Player", "Team", "G", "A")
        tree = ttk.Treeview(container, columns=cols, show="headings", height=5)
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=80, anchor="center")

        try:
            # Read the player data
            df = pd.read_csv("players.csv")
            # Sort by Goals, then Assists as a tie-breaker
            top_5 = df.sort_values(by=["Goals", "Assists"], ascending=False).head(5)
            
            for _, row in top_5.iterrows():
                tree.insert("", "end", values=(row['Player'], row['Team'], row['Goals'], row['Assists']))
        except Exception as e:
            tree.insert("", "end", values=("No Data", "-", "-", "-"))

        tree.pack(fill="both", expand=True)

    def create_table(self, parent):
        cols = ("Pos", "Team", "W", "D", "L", "Pts")
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=8)
        
        # Style the headers
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=70, anchor="center")

        try:
            # Load real data from CSV
            df = pd.read_csv("premier_league_data.csv")
            
            # Insert data from CSV into the table
            for index, row in df.iterrows():
                tree.insert("", "end", values=(
                    row['Pos'], 
                    row['Team'], 
                    row['W'], 
                    row['D'], 
                    row['L'], 
                    row['Pts']
                ))
        except FileNotFoundError:
            # Fallback if file isn't found
            tree.insert("", "end", values=("Error", "File Not Found", "-", "-", "-", "-"))

        tree.pack(fill="both", expand=True)

        def on_tree_select(event):
            selected_item = tree.selection()[0] # Get the selected row
            team_data = tree.item(selected_item)['values']
            team_name = team_data[1] # The team name is in the second column
            self.show_team_members(team_name)

        # Bind the click event to the table
        tree.bind("<Double-1>", on_tree_select) # Double-click to see members
        tree.pack(fill="both", expand=True)

    def plot_stats(self, parent):
        fig, ax = plt.subplots(figsize=(4, 3), facecolor="#102A43")
        ax.set_facecolor("#102A43")
        
        try:
            df = pd.read_csv("premier_league_data.csv")
            # Create a bar chart of Points per Team
            ax.bar(df['Team'], df['Pts'], color=PRIMARY)
            ax.set_title("Current Points Comparison", color="white", fontsize=10)
            ax.tick_params(axis='x', rotation=45, colors='white', labelsize=7)
            ax.tick_params(axis='y', colors='white', labelsize=8)
        except:
            ax.text(0.5, 0.5, "Data unavailable", color="white", ha='center')
        
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    # ================= ORIGINAL LANDING PAGE =================
    def show_landing_page(self):
        self.clear_screen()
        
        # Background Image
        try:
            bg_image = Image.open("background.png")
            bg_image = bg_image.resize((1000, 800))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            self.root.configure(bg=DARK_BG)
            tk.Label(self.root, text="[Background Image Missing]", fg="white", bg=DARK_BG).pack()

        # Title
        title = tk.Label(
            self.root, text="Premier League Analysis",
            font=("Helvetica", 36, "bold"), bg="#FDFBFA", fg="brown"
        )
        title.pack(pady=40)

        # Center Card
        frame = tk.Frame(self.root, bg=CARD_BG)
        frame.place(relx=0.5, rely=0.55, anchor="center", width=520, height=230)

        tk.Label(
            frame, text="Your Live Insights & Statistics",
            font=("Helvetica", 18), fg="white", bg=CARD_BG
        ).pack(pady=30)

        # Buttons (No Login - Just Start)
        tk.Button(
            frame, text="Start Analysis", command=self.show_dashboard,
            bg=PRIMARY, fg="black", font=("Helvetica", 16, "bold"),
            padx=25, pady=10, relief="flat", cursor="hand2"
        ).pack(pady=10)

        tk.Button(
            frame, text="Exit", command=self.root.quit,
            bg=PRIMARY, fg="black", font=("Helvetica", 16, "bold"),
            padx=25, pady=10, relief="flat", cursor="hand2"
        ).pack(pady=10)

    # ================= PROFESSIONAL DASHBOARD =================
    # ================= UPDATED DASHBOARD =================
    def show_dashboard(self):
        self.clear_screen()
        self.root.geometry("2500x1500")
        self.root.configure(bg="#020617")

        # Top Navbar
        navbar = tk.Frame(self.root, bg=NAV_BLUE, height=70)
        navbar.pack(fill="x")

        tk.Label(navbar, text="Premier League", fg="white", bg=NAV_BLUE, 
                 font=("Helvetica", 24, "bold")).pack(side="left", padx=30)

        # --- REFRESH BUTTON ---
        tk.Button(
            navbar, text="🔄 Refresh Data", command=self.refresh_dashboard,
            bg=PRIMARY, fg="black", font=("Helvetica", 10, "bold"),
            relief="flat", cursor="hand2", padx=15
        ).pack(side="right", padx=20)

        # Content Area
        self.main_content = tk.Frame(self.root, bg="#020617")
        self.main_content.pack(fill="both", expand=True, padx=30, pady=20)

        self.render_dashboard_elements()

    def render_dashboard_elements(self):
        """Uses weighted grids to ensure sections don't compress each other"""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Configure columns to have equal weight (1:1:1 ratio)
        self.main_content.columnconfigure(0, weight=1)
        self.main_content.columnconfigure(1, weight=1)
        self.main_content.columnconfigure(2, weight=1)
        self.main_content.rowconfigure(1, weight=1) # Let the middle row expand

        # --- Top KPIs (Span across all 3 columns) ---
        k_frame = tk.Frame(self.main_content, bg="#020617")
        k_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=10)
        
        self.create_kpi(k_frame, "Matches Played", "11,480").pack(side="left", padx=10, expand=True)
        self.create_kpi(k_frame, "Total Goals", "31,232").pack(side="left", padx=10, expand=True)
        self.create_kpi(k_frame, "Current Leader", "Arsenal").pack(side="left", padx=10, expand=True)

        # --- Column 1: Chart ---
        c1 = tk.Frame(self.main_content, bg="#102A43", highlightbackground=PRIMARY, highlightthickness=1)
        c1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.plot_stats(c1)
        
        # --- Column 2: Standings Table ---
        c2 = tk.Frame(self.main_content, bg="#102A43", highlightbackground=PRIMARY, highlightthickness=1)
        c2.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.create_table(c2)
        
        # --- Column 3: Golden Boot (Now with plenty of room!) ---
        c3 = tk.Frame(self.main_content, bg="#102A43", highlightbackground=PRIMARY, highlightthickness=1)
        c3.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
        self.create_top_scorers(c3)

    def create_top_scorers(self, parent):
        """Creates the Golden Boot leaderboard"""
        tk.Label(parent, text="🏆 Golden Boot", font=("Helvetica", 14, "bold"), 
                 bg="#102A43", fg="#22C55E").pack(pady=10)

        cols = ("Player", "Goals")
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=8)
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        try:
            df = pd.read_csv("players.csv")
            # Sort by Goals descending and take top 5
            top_5 = df.sort_values(by="Goals", ascending=False).head(8)
            
            for _, row in top_5.iterrows():
                tree.insert("", "end", values=(row['Player'], row['Goals']))
        except:
            tree.insert("", "end", values=("No Data", "-"))

        tree.pack(fill="both", expand=True, padx=5, pady=5)

    def refresh_dashboard(self):
        """Function called by the Refresh button"""
        print("Refreshing data from CSV...")
        self.render_dashboard_elements()

        # Back Button
        tk.Button(self.root, text="Return to Home", command=self.show_landing_page, 
                  bg=PRIMARY, font=("Helvetica", 10, "bold")).pack(side="bottom", pady=10)

    def create_kpi(self, parent, title, val):
        f = tk.Frame(parent, bg="#102A43", padx=20, pady=15, width=220, height=100)
        f.pack_propagate(False)
        tk.Label(f, text=title, bg="#102A43", fg=TEXT_MUTED).pack()
        tk.Label(f, text=val, bg="#102A43", fg=PRIMARY, font=("Helvetica", 20, "bold")).pack()
        return f

    def plot_stats(self, parent):
        fig, ax = plt.subplots(figsize=(4, 3), facecolor="#102A43")
        ax.set_facecolor("#102A43")
        ax.plot([1, 2, 3, 4, 5], [10, 15, 12, 18, 20], color=PRIMARY, marker='o')
        ax.set_title("Season Intensity Index", color="white", fontsize=10)
        ax.tick_params(colors='white', labelsize=8)
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_table(self, parent):
        cols = ("Pos", "Team", "W", "D", "L", "Pts")
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=8)
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=60, anchor="center")

        data = [(1, "Arsenal", 12, 2, 1, 38), (2, "Man City", 11, 3, 1, 36), (3, "Liverpool", 10, 4, 1, 34)]
        for item in data: tree.insert("", "end", values=item)
        
        tree.pack(fill="both", expand=True)
        
        def on_double_click(event):
            # Get the ID of the clicked row
            item_id = tree.selection()[0]
            # Get the values from that row
            item_values = tree.item(item_id, 'values')
            # Extract the team name (usually column 2 / index 1)
            selected_team = item_values[1]
            # Launch the squad window
            self.show_team_members(selected_team)

        # 2. Attach (Bind) the event to the treeview
        tree.bind("<Double-1>", on_double_click)
        
        tree.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = PremierLeagueApp(root)
    root.mainloop()