import tkinter as tk
from tkinter import messagebox
import time
import threading

sample_text = (
    "Artificial Intelligence and Machine Learning are transforming industries by "
    "automating tasks, improving decision-making, and enhancing customer experiences. "
    "Python is one of the most popular programming languages used for developing AI applications."
)

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Tester")
        self.root.geometry("800x500")
        self.start_time = None
        self.time_limit = 60  # seconds
        self.timer_running = False

        # Display prompt text
        tk.Label(root, text="Type the text below:", font=("Arial", 14)).pack(pady=10)
        self.text_display = tk.Text(root, height=5, font=("Arial", 13), wrap="word")
        self.text_display.pack()
        self.text_display.insert("1.0", sample_text)
        self.text_display.config(state="disabled")

        # Typing entry area
        self.entry = tk.Text(root, height=6, font=("Arial", 13), wrap="word")
        self.entry.pack(pady=10)

        # Timer label
        self.timer_label = tk.Label(root, text="Time left: 60s", font=("Arial", 14), fg="blue")
        self.timer_label.pack()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.start_button = tk.Button(btn_frame, text="Start", width=10, command=self.start_test)
        self.start_button.pack(side="left", padx=10)

        self.submit_button = tk.Button(btn_frame, text="Submit", width=10, command=self.calculate_result, state="disabled")
        self.submit_button.pack(side="left", padx=10)

        self.restart_button = tk.Button(btn_frame, text="Restart", width=10, command=self.restart_test, state="disabled")
        self.restart_button.pack(side="left", padx=10)

    def start_test(self):
        self.entry.delete("1.0", tk.END)
        self.start_time = time.time()
        self.timer_running = True
        self.submit_button.config(state="normal")
        self.restart_button.config(state="disabled")
        threading.Thread(target=self.update_timer, daemon=True).start()
        messagebox.showinfo("Started", "Typing test started! You have 60 seconds.")

    def update_timer(self):
        for remaining in range(self.time_limit, -1, -1):
            if not self.timer_running:
                break
            self.timer_label.config(text=f"Time left: {remaining}s")
            time.sleep(1)
        if self.timer_running:
            self.calculate_result()

    def calculate_result(self):
        if not self.start_time:
            return
        self.timer_running = False
        self.submit_button.config(state="disabled")
        self.restart_button.config(state="normal")

        typed_text = self.entry.get("1.0", tk.END).strip()
        total_time = time.time() - self.start_time
        words = typed_text.split()
        wpm = (len(words) / total_time) * 60 if total_time > 0 else 0

        correct = sum(1 for i, w in enumerate(words) if i < len(sample_text.split()) and w == sample_text.split()[i])
        accuracy = (correct / len(sample_text.split())) * 100

        result = f"WPM: {wpm:.2f}\nAccuracy: {accuracy:.2f}%"
        messagebox.showinfo("Result", result)
        self.save_score(wpm, accuracy)

    def save_score(self, wpm, accuracy):
        with open("scores.txt", "a") as f:
            f.write(f"WPM: {wpm:.2f}, Accuracy: {accuracy:.2f}%\n")

    def restart_test(self):
        self.entry.delete("1.0", tk.END)
        self.timer_label.config(text=f"Time left: {self.time_limit}s")
        self.start_time = None
        self.submit_button.config(state="disabled")
        self.restart_button.config(state="disabled")
        self.timer_running = False

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
