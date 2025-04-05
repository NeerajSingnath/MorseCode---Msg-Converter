import tkinter as tk
from tkinter import ttk, messagebox

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', ' ': '/'
}

# Create reverse dictionary for morse to text conversion
REVERSE_MORSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

def text_to_morse(text):
    """Convert text to Morse code."""
    text = text.upper()
    morse_code = ' '.join(MORSE_CODE_DICT.get(char, '?') for char in text)
    return morse_code

def morse_to_text(morse):
    """Convert Morse code to text."""
    # Split morse code by space
    morse_words = morse.split(' / ')
    result = []
    
    for word in morse_words:
        chars = word.split(' ')
        word_result = ''
        for char in chars:
            if char:  # Skip empty strings
                word_result += REVERSE_MORSE_DICT.get(char, '?')
        result.append(word_result)
    
    return ' '.join(result)

def copy_to_clipboard(text):
    """Copy text to clipboard."""
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("Copied", "Text copied to clipboard!")

def convert():
    """Handle conversion based on selected mode."""
    input_text = input_field.get("1.0", "end-1c")
    if not input_text:
        messagebox.showwarning("Warning", "Please enter some text to convert!")
        return
    
    if mode_var.get() == "Text to Morse":
        result = text_to_morse(input_text)
    else:  # Morse to Text
        result = morse_to_text(input_text)
    
    output_field.delete("1.0", tk.END)
    output_field.insert("1.0", result)

def play_morse():
    """Play the Morse code sound."""
    morse_text = output_field.get("1.0", "end-1c")
    if not morse_text or mode_var.get() != "Text to Morse":
        messagebox.showwarning("Warning", "Please convert text to Morse code first!")
        return
    
    # Import needed only when function is called
    import winsound
    import time
    
    DOT_DURATION = 200  # milliseconds
    DASH_DURATION = DOT_DURATION * 3
    SYMBOL_PAUSE = DOT_DURATION
    LETTER_PAUSE = DOT_DURATION * 3
    WORD_PAUSE = DOT_DURATION * 7
    FREQUENCY = 800  # Hz
    
    try:
        for word in morse_text.split(' / '):
            for i, letter in enumerate(word.split(' ')):
                for symbol in letter:
                    if symbol == '.':
                        winsound.Beep(FREQUENCY, DOT_DURATION)
                    elif symbol == '-':
                        winsound.Beep(FREQUENCY, DASH_DURATION)
                    time.sleep(SYMBOL_PAUSE / 1000)
                
                # Pause between letters (except after the last letter)
                if i < len(word.split(' ')) - 1:
                    time.sleep(LETTER_PAUSE / 1000)
            
            # Pause between words
            time.sleep(WORD_PAUSE / 1000)
        
    except Exception as e:
        messagebox.showerror("Error", f"Could not play Morse code: {str(e)}")

def toggle_theme():
    """Toggle between light and dark theme."""
    current_bg = root.cget("background")
    if current_bg == "white" or current_bg == "SystemButtonFace":
        # Switch to dark theme
        root.configure(bg="#333333")
        main_frame.configure(bg="#333333")
        for child in main_frame.winfo_children():
            if isinstance(child, ttk.Label) or isinstance(child, ttk.Radiobutton):
                child.configure(background="#333333", foreground="white")
        
        style.configure("TButton", background="#555555", foreground="white")
        input_field.configure(bg="#444444", fg="white", insertbackground="white")
        output_field.configure(bg="#444444", fg="white", insertbackground="white")
        theme_button.configure(text="Light Theme")
    else:
        # Switch to light theme
        root.configure(bg="white")
        main_frame.configure(bg="white")
        for child in main_frame.winfo_children():
            if isinstance(child, ttk.Label) or isinstance(child, ttk.Radiobutton):
                child.configure(background="white", foreground="black")
        
        style.configure("TButton", background="#f0f0f0", foreground="black")
        input_field.configure(bg="white", fg="black", insertbackground="black")
        output_field.configure(bg="white", fg="black", insertbackground="black")
        theme_button.configure(text="Dark Theme")

def switch_mode():
    """Update the interface based on the selected mode."""
    if mode_var.get() == "Text to Morse":
        convert_button.configure(text="Convert to Morse")
        play_button.state(["!disabled"])  # Enable play button
    else:  # Morse to Text
        convert_button.configure(text="Convert to Text")
        play_button.state(["disabled"])  # Disable play button

# Set up the main window
root = tk.Tk()
root.title("Morse Code Converter")
root.geometry("600x500")
root.configure(bg="white")

# Create style for ttk widgets
style = ttk.Style()
style.configure("TButton", font=("Arial", 10))
style.configure("TLabel", font=("Arial", 12))
style.configure("TRadiobutton", font=("Arial", 10))

# Create main frame
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Mode selection (Text to Morse or Morse to Text)
mode_frame = ttk.Frame(main_frame)
mode_frame.pack(fill=tk.X, pady=10)

mode_var = tk.StringVar(value="Text to Morse")
mode_label = ttk.Label(mode_frame, text="Mode:")
mode_label.pack(side=tk.LEFT, padx=5)

text_to_morse_rb = ttk.Radiobutton(mode_frame, text="Text to Morse", variable=mode_var, 
                                   value="Text to Morse", command=switch_mode)
text_to_morse_rb.pack(side=tk.LEFT, padx=10)

morse_to_text_rb = ttk.Radiobutton(mode_frame, text="Morse to Text", variable=mode_var, 
                                  value="Morse to Text", command=switch_mode)
morse_to_text_rb.pack(side=tk.LEFT, padx=10)

# Input section
input_label = ttk.Label(main_frame, text="Input:")
input_label.pack(anchor=tk.W, pady=(10, 5))

input_field = tk.Text(main_frame, height=5, width=60, font=("Courier", 12))
input_field.pack(fill=tk.BOTH, expand=True, pady=5)

# Buttons section
button_frame = ttk.Frame(main_frame)
button_frame.pack(fill=tk.X, pady=10)

convert_button = ttk.Button(button_frame, text="Convert to Morse", command=convert)
convert_button.pack(side=tk.LEFT, padx=5)

play_button = ttk.Button(button_frame, text="Play Morse", command=play_morse)
play_button.pack(side=tk.LEFT, padx=5)

copy_button = ttk.Button(button_frame, text="Copy Result", 
                        command=lambda: copy_to_clipboard(output_field.get("1.0", "end-1c")))
copy_button.pack(side=tk.LEFT, padx=5)

clear_button = ttk.Button(button_frame, text="Clear All", 
                         command=lambda: [input_field.delete("1.0", tk.END), 
                                         output_field.delete("1.0", tk.END)])
clear_button.pack(side=tk.LEFT, padx=5)

theme_button = ttk.Button(button_frame, text="Dark Theme", command=toggle_theme)
theme_button.pack(side=tk.RIGHT, padx=5)

# Output section
output_label = ttk.Label(main_frame, text="Output:")
output_label.pack(anchor=tk.W, pady=(10, 5))

output_field = tk.Text(main_frame, height=5, width=60, font=("Courier", 12))
output_field.pack(fill=tk.BOTH, expand=True, pady=5)

# Status bar
status_bar = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Center the window
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    root.mainloop()