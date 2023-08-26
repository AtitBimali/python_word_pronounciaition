import tkinter as tk
from tkinter import filedialog,messagebox
from gtts import gTTS
import os
import threading  # Import the threading module

class PronunciationDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pronunciation Downloader")

        self.output_dir = "pronunciations"
        os.makedirs(self.output_dir, exist_ok=True)

        self.label = tk.Label(root, text="Enter words (separated by newline):")
        self.label.pack()

        self.textbox = tk.Text(root, height=10, width=30)
        self.textbox.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_download)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_download)
        self.stop_button.pack()

        self.clear_button = tk.Button(root, text="Clear Pronunciations", command=self.clear_pronunciations)
        self.clear_button.pack()

        self.downloading = False  # Flag to indicate downloading status
        self.download_thread = None  # Thread for downloading

    def download_pronunciation(self, word):
        tts = gTTS(text=word, lang='en')
        output_file = os.path.join(self.output_dir, f'{word}.mp3')
        tts.save(output_file)
        print(f"Pronunciation for '{word}' saved as '{output_file}'")

    def download_loop(self):
        self.downloading = True
        words = self.textbox.get("1.0", "end-1c").split("\n")
        for word in words:
            if not self.downloading:
                break
            self.download_pronunciation(word)
        self.downloading = False
        messagebox.showinfo("Finished", "Pronunciation downloading finished!")

    def start_download(self):
        if not self.downloading:
            self.download_thread = threading.Thread(target=self.download_loop)
            self.download_thread.start()

    def stop_download(self):
        if self.downloading:
            self.downloading = False
            self.download_thread.join()  # Wait for the download thread to finish

    def clear_pronunciations(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear pronunciations?")
        if confirm:
            for file_name in os.listdir(self.output_dir):
                file_path = os.path.join(self.output_dir, file_name)
                os.remove(file_path)
            print("Pronunciations directory cleared.")
            messagebox.showinfo("Cleared", "Pronunciation folder cleared!")



if __name__ == "__main__":
    root = tk.Tk()
    app = PronunciationDownloaderApp(root)
    root.mainloop()
