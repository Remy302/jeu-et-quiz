import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import time

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("700x500")
        self.root.config(bg="#f0f0f0")
        
        # Game variables
        self.score = 0
        self.current_question = 0
        self.time_left = 20  # seconds per question
        self.timer_running = False
        self.questions = []
        
        # Sample questions (in real app, load from file)
        self.load_questions()
        
        # Create frames
        self.create_frames()
        
        # Start with welcome screen
        self.show_welcome_screen()
    
    def load_questions(self):
        # In a real app, load from JSON file
        # For demonstration, we'll create a list directly
        self.questions = [
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "correct": 1
            },
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct": 2
            },
            {
                "question": "Which language is Python named after?",
                "options": ["A snake", "A comedy group", "A programming language", "A scientist"],
                "correct": 1
            },
            {
                "question": "What is the largest mammal on Earth?",
                "options": ["Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
                "correct": 1
            },
            {
                "question": "Who wrote 'Romeo and Juliet'?",
                "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                "correct": 1
            }
        ]
        # Shuffle questions
        random.shuffle(self.questions)
        
    def create_frames(self):
        # Welcome Frame
        self.welcome_frame = tk.Frame(self.root, bg="#f0f0f0")
        
        # Quiz Frame
        self.quiz_frame = tk.Frame(self.root, bg="#f0f0f0")
        
        # Result Frame
        self.result_frame = tk.Frame(self.root, bg="#f0f0f0")
    
    def show_welcome_screen(self):
        # Hide other frames
        self.quiz_frame.pack_forget()
        self.result_frame.pack_forget()
        
        # Configure welcome frame
        self.welcome_frame.pack(fill="both", expand=True)
        
        # Clear previous widgets
        for widget in self.welcome_frame.winfo_children():
            widget.destroy()
        
        # Add welcome widgets
        title_label = tk.Label(
            self.welcome_frame, 
            text="Welcome to Quiz Game!", 
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=50)
        
        desc_label = tk.Label(
            self.welcome_frame,
            text="Test your knowledge with this fun quiz game!\nYou'll have 20 seconds to answer each question.",
            font=("Arial", 12),
            bg="#f0f0f0",
            justify="center"
        )
        desc_label.pack(pady=20)
        
        start_button = tk.Button(
            self.welcome_frame,
            text="Start Quiz",
            font=("Arial", 14),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            command=self.start_quiz
        )
        start_button.pack(pady=30)
        
        # Add options for difficulty (not implemented yet)
        difficulty_frame = tk.Frame(self.welcome_frame, bg="#f0f0f0")
        difficulty_frame.pack(pady=20)
        
        tk.Label(
            difficulty_frame,
            text="Difficulty:",
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=10)
        
        difficulty = ttk.Combobox(
            difficulty_frame,
            values=["Easy", "Medium", "Hard"],
            state="readonly",
            width=10
        )
        difficulty.current(1)  # Default medium
        difficulty.pack(side=tk.LEFT)
    
    def start_quiz(self):
        # Reset game variables
        self.score = 0
        self.current_question = 0
        
        # Hide welcome frame and show quiz frame
        self.welcome_frame.pack_forget()
        self.quiz_frame.pack(fill="both", expand=True)
        
        # Load first question
        self.load_question()
    
    def load_question(self):
        # Clear previous widgets
        for widget in self.quiz_frame.winfo_children():
            widget.destroy()
        
        if self.current_question < len(self.questions):
            # Get current question data
            question_data = self.questions[self.current_question]
            
            # Progress indicator
            progress_text = f"Question {self.current_question + 1} of {len(self.questions)}"
            progress_label = tk.Label(
                self.quiz_frame,
                text=progress_text,
                font=("Arial", 10),
                bg="#f0f0f0"
            )
            progress_label.pack(anchor="w", padx=20, pady=10)
            
            # Score display
            score_label = tk.Label(
                self.quiz_frame,
                text=f"Score: {self.score}",
                font=("Arial", 10),
                bg="#f0f0f0"
            )
            score_label.pack(anchor="e", padx=20, pady=10)
            
            # Timer display
            self.time_left = 20
            self.timer_label = tk.Label(
                self.quiz_frame,
                text=f"Time: {self.time_left}s",
                font=("Arial", 12),
                bg="#f0f0f0",
                fg="#FF5722"
            )
            self.timer_label.pack(pady=5)
            
            # Question display
            question_label = tk.Label(
                self.quiz_frame,
                text=question_data["question"],
                font=("Arial", 16, "bold"),
                bg="#f0f0f0",
                wraplength=600,
                justify="center"
            )
            question_label.pack(pady=20)
            
            # Option buttons
            self.option_var = tk.IntVar()
            option_frame = tk.Frame(self.quiz_frame, bg="#f0f0f0")
            option_frame.pack(pady=20, fill="both", expand=True)
            
            for i, option in enumerate(question_data["options"]):
                option_btn = tk.Radiobutton(
                    option_frame,
                    text=option,
                    variable=self.option_var,
                    value=i,
                    font=("Arial", 12),
                    bg="#f0f0f0",
                    padx=20,
                    pady=5,
                    indicator=0,
                    selectcolor="#90CAF9",
                    width=40
                )
                option_btn.pack(pady=5)
            
            # Submit button
            submit_btn = tk.Button(
                self.quiz_frame,
                text="Submit Answer",
                font=("Arial", 12),
                bg="#2196F3",
                fg="white",
                padx=20,
                pady=10,
                command=self.check_answer
            )
            submit_btn.pack(pady=20)
            
            # Start the timer
            self.start_timer()
        else:
            # No more questions, show results
            self.show_results()
    
    def start_timer(self):
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time: {self.time_left}s")
            self.root.after(1000, self.update_timer)
        elif self.timer_running and self.time_left <= 0:
            self.timer_running = False
            messagebox.showinfo("Time's up!", "You ran out of time!")
            self.next_question()
    
    def check_answer(self):
        self.timer_running = False  # Stop the timer
        
        user_answer = self.option_var.get()
        correct_answer = self.questions[self.current_question]["correct"]
        
        if user_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct!", "Your answer is correct!")
        else:
            correct_option = self.questions[self.current_question]["options"][correct_answer]
            messagebox.showinfo("Incorrect", f"The correct answer is: {correct_option}")
        
        self.next_question()
    
    def next_question(self):
        self.current_question += 1
        self.load_question()
    
    def show_results(self):
        # Hide quiz frame
        self.quiz_frame.pack_forget()
        
        # Show result frame
        self.result_frame.pack(fill="both", expand=True)
        
        # Clear previous widgets
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Calculate percentage
        percentage = (self.score / len(self.questions)) * 100
        
        # Determine message based on score
        if percentage >= 80:
            message = "Excellent! You're a quiz master!"
            color = "#4CAF50"  # Green
        elif percentage >= 60:
            message = "Good job! You did well!"
            color = "#2196F3"  # Blue
        elif percentage >= 40:
            message = "Not bad, but you can do better!"
            color = "#FF9800"  # Orange
        else:
            message = "You need more practice!"
            color = "#F44336"  # Red
        
        # Results title
        title_label = tk.Label(
            self.result_frame,
            text="Quiz Results",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=30)
        
        # Score display
        score_label = tk.Label(
            self.result_frame,
            text=f"Your Score: {self.score}/{len(self.questions)} ({percentage:.1f}%)",
            font=("Arial", 16),
            bg="#f0f0f0"
        )
        score_label.pack(pady=20)
        
        # Performance message
        message_label = tk.Label(
            self.result_frame,
            text=message,
            font=("Arial", 14),
            fg=color,
            bg="#f0f0f0"
        )
        message_label.pack(pady=20)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.result_frame, bg="#f0f0f0")
        buttons_frame.pack(pady=30)
        
        # Play again button
        play_again_btn = tk.Button(
            buttons_frame,
            text="Play Again",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            command=self.start_quiz
        )
        play_again_btn.pack(side=tk.LEFT, padx=10)
        
        # Back to main menu button
        main_menu_btn = tk.Button(
            buttons_frame,
            text="Main Menu",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
            command=self.show_welcome_screen
        )
        main_menu_btn.pack(side=tk.LEFT, padx=10)
        
        # Exit button
        exit_btn = tk.Button(
            buttons_frame,
            text="Exit",
            font=("Arial", 12),
            bg="#F44336",
            fg="white",
            padx=20,
            pady=10,
            command=self.root.destroy
        )
        exit_btn.pack(side=tk.LEFT, padx=10)

# Main function to run the app
def main():
    root = tk.Tk()
    app = QuizGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()