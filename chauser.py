import tkinter as tk
import random
from tkinter import messagebox

class ModifiedNumberedGrid:
    def __init__(self, master):
        self.master = master
        self.master.title("CHAUSER GAME")
        
        # Set grid dimensions
        self.GRID_SIZE = 19
        self.CELL_SIZE = 30  # Size of each cell
        
        # Calculate the size of the merged boxes
        self.MERGED_BOX_WIDTH = 8 * self.CELL_SIZE
        self.MERGED_BOX_HEIGHT = 8 * self.CELL_SIZE
        
        # Calculate center box dimensions (3x3)
        self.CENTER_BOX_SIZE = 3 * self.CELL_SIZE
        
        # Adjust canvas size to accommodate the merged boxes
        self.canvas_width = self.GRID_SIZE * self.CELL_SIZE
        self.canvas_height = self.GRID_SIZE * self.CELL_SIZE
        
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(padx=20, pady=20)

        # Button to roll the dice
        self.roll_button = tk.Button(master, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack(pady=10)

        # Button for rules
        self.rules_button = tk.Button(master, text="Rules", command=self.show_rules)
        self.rules_button.pack(pady=10)

        # Label to display the dice result
        self.result_label = tk.Label(master, text="", font=('Arial', 14))
        self.result_label.pack(pady=10)

        self.tokens = []  # List to store token IDs
        self.selected_token = None  # Track the currently selected token
        self.dice_total = 0  # Variable to store the total of the dice rolls
        self.draw_grid()

    def show_rules(self):
        messagebox.showinfo("Game Rules", """→Games can last anything from 30 mins to hours and hours. 
                            →Technically, a game can never end depending on the players. 
                            →This is possible if players keepdoing 'Alkhee' ghaats.
                            →It is an individual game played between a maximum of four player 
                            →The center column on each arm of the cross is the 'home column' for each player's men after they cross the flower motif. 
                            →The starting point for each player is the flower motif on the column to the left of his home column. 
                            →If two of your pieces land on the same square, they became a 'super piece' and move together. 
                            →The same goes for 3 and 4 pieces .
                            →An extra turn is granted by playing a 6, 12, 10 or '8' (25 square move). 
                            →There are 8 safe squares (called Cheere).""")

    def draw_grid(self):
        # Draw Box1 (top-left corner) - Red
        self.canvas.create_rectangle(0, 0, self.MERGED_BOX_WIDTH, self.MERGED_BOX_HEIGHT, 
                                     outline='black', fill='red', width=2)
        self.draw_crowns(0, 0)

        # Draw Box2 (top-right corner) - Blue
        self.canvas.create_rectangle(11 * self.CELL_SIZE, 0, self.canvas_width, self.MERGED_BOX_HEIGHT, 
                                     outline='black', fill='blue', width=2)
        self.draw_crowns(11 * self.CELL_SIZE, 0)

        # Draw Box3 (bottom-left corner) - Green
        self.canvas.create_rectangle(0, 11 * self.CELL_SIZE, self.MERGED_BOX_WIDTH, self.canvas_height, 
                                     outline='black', fill='green', width=2)
        self.draw_crowns(0, 11 * self.CELL_SIZE)

        # Draw Box4 (bottom-right corner) - Yellow
        self.canvas.create_rectangle(11 * self.CELL_SIZE, 11 * self.CELL_SIZE, self.canvas_width, self.canvas_height, 
                                     outline='black', fill='yellow', width=2)
        self.draw_crowns(11 * self.CELL_SIZE, 11 * self.CELL_SIZE)

        # Draw Center Box (3x3)
        center_x = (self.GRID_SIZE // 2 - 1 ) * self.CELL_SIZE
        center_y = (self.GRID_SIZE // 2 - 1) * self.CELL_SIZE
        self.canvas.create_rectangle(center_x, center_y, 
                                   center_x + self.CENTER_BOX_SIZE, 
                                   center_y + self.CENTER_BOX_SIZE,
                                   outline='black', fill='orange', width=2)
        self.canvas.create_text(center_x + self.CENTER_BOX_SIZE / 2, 
                              center_y + self.CENTER_BOX_SIZE / 2,
                              text="*-*", font=('Arial', 14, 'bold'))

        # Start numbering from a specific number
        start_number = 100
        cell_number = start_number
        
        # List of cell numbers to draw diagonal lines
        diagonal_cells = [111, 109, 107, 127, 142, 159, 184, 188, 186, 136, 153, 168]

        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                # Calculate position
                x1 = col * self.CELL_SIZE
                y1 = row * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                
                # Skip the merged areas (Box1, Box2, Box3, Box4, and Center Box)
                if (col < 8 and row < 8) or (col >= 11 and row < 8) or (col < 8 and row >= 11) or (col >= 11 and row >= 11) or \
                   (8 <= col <= 10 and 8 <= row <= 10):
                    continue
                
                # Change the color of the first 8 boxes in the middle row (row index 9) to red if row == 9 and col < 8:
                fill_color = 'red' if row == 9 and col < 8 else \
                             'yellow' if row == 9 and col >= 11 else \
                             'blue' if col == 9 and row < 8 else \
                             'green' if col == 9 and row >= 11 else \
                             'white' if (row + col) % 2 == 0 else 'lightblue'
                
                # Draw rectangle for each cell
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill=fill_color)
                
                # Draw diagonal lines for specified cells
                if cell_number in diagonal_cells:
                    self.canvas.create_line(x1, y1, x2, y2, fill='black', width=2)  # Top-left to bottom-right
                    self.canvas.create_line(x2, y1, x1, y2, fill='black', width=2)  # Top-right to bottom-left
                
                # Add overlapping hearts to box number 122, centered
                if cell_number == 122:
                    for _ in range(4):  # Create 4 hearts
                        token_id = self.canvas.create_text(x1 + self.CELL_SIZE / 2, 
                                            y1 + self.CELL_SIZE / 2, 
                                            text="💙", font=('Arial', 14))  # Centered
                        self.tokens.append(token_id)  # Store token ID for movement
                        self.canvas.tag_bind(token_id, '<Button-1>', self.on_token_click)  # Bind click event to each token
                if cell_number == 173:
                    for _ in range(4):  # Create 4 green hearts
                        token_id = self.canvas.create_text(x1 + self.CELL_SIZE / 2, 
                                            y1 + self.CELL_SIZE / 2, 
                                            text="💚", font=('Arial', 14))  # Centered
                        self.tokens.append(token_id)  # Store token ID for movement
                        self.canvas.tag_bind(token_id, '<Button-1>', self.on_token_click)  # Bind click event to each token

                if cell_number == 147:
                    for _ in range(4):  # Create 4 red hearts
                        token_id = self.canvas.create_text(x1 + self.CELL_SIZE / 2, 
                                            y1 + self.CELL_SIZE / 2, 
                                            text="❤️", font=('Arial', 14))  # Centered
                        self.tokens.append(token_id)  # Store token ID for movement
                        self.canvas.tag_bind(token_id, '<Button-1>', self.on_token_click)  # Bind click event to each token

                if cell_number == 148:
                    for _ in range(4):  # Create 4 yellow hearts
                        token_id = self.canvas.create_text(x1 + self.CELL_SIZE /  2, 
                                            y1 + self.CELL_SIZE / 2, 
                                            text="💛", font=('Arial', 14))  # Centered
                        self.tokens.append(token_id)  # Store token ID for movement
                        self.canvas.tag_bind(token_id, '<Button-1>', self.on_token_click)  # Bind click event to each token
            
                cell_number += 1

    def draw_crowns(self, start_x, start_y):
        # Calculate positions for the crowns in each box, adjusted for centering and moving up
        crown_positions = [
            (start_x + self.CELL_SIZE * 2.5, start_y + self.CELL_SIZE * 2.0),  # Adjusted y-coordinate
            (start_x + self.CELL_SIZE * 5.5, start_y + self.CELL_SIZE * 2.0),  # Adjusted y-coordinate
            (start_x + self.CELL_SIZE * 2.5, start_y + self.CELL_SIZE * 5.0),  # Adjusted y-coordinate
            (start_x + self.CELL_SIZE * 5.5, start_y + self.CELL_SIZE * 5.0)   # Adjusted y-coordinate
        ]
        
        for pos in crown_positions:
            self.canvas.create_text(pos[0], pos[1], text="♚", font=('Arial', 90, 'bold'), fill='white')  # Size remains 90

    def on_token_click(self, event):
        self.selected_token = self.canvas.find_closest(event.x, event.y)[0]  # Get the token ID that was clicked
        self.master.bind('<Key>', self.move_token)  # Bind key events to move the selected token

    def move_token(self, event):
        if self.selected_token is not None:
            move_distance = self.dice_total * self.CELL_SIZE  # Calculate the move distance based on dice total
            if event.keysym == "Up":
                self.canvas.move(self.selected_token, 0, -move_distance)  # Move up
            elif event.keysym == "Down":
                self.canvas.move(self.selected_token, 0, move_distance)  # Move down
            elif event.keysym == "Left":
                self.canvas.move(self.selected_token, -move_distance, 0)  # Move left
            elif event.keysym == "Right":
                self.canvas.move(self.selected_token, move_distance, 0)  # Move right

    def roll_dice(self):
        """Roll two dice and display the result."""
        die1, die2 = random.choice([1,3,4,6]), random.choice([1,3,4,6])  # Standard dice roll
        self.dice_total = die1 + die2  # Store the total of the dice rolls
        self.result_label.config(text=f"Die 1: {die1}, Die 2: {die2}, Total: {self.dice_total}")

if __name__ == "__main__":
    root = tk.Tk()
    grid = ModifiedNumberedGrid(root)
    root.mainloop()