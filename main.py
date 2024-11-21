import os
import shutil
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.aiff import AIFF

ver="0.0.1"

source_folder_entry=None
source_format_entry=None
target_folder_entry=None
target_format_entry=None

def select_folder(entry_widget):
    folder = filedialog.askdirectory()
    if folder:
        entry_widget.delete(0, "end")
        entry_widget.insert(0, folder)

def copy_tags(source_file, target_file, source_format):
    if source_format == "mp3":
        source_tags = EasyID3(source_file)
        target_audio = MP3(target_file, ID3=EasyID3)
    elif source_format == "flac":
        source_tags = FLAC(source_file)
        target_audio = FLAC(target_file)
    elif source_format == "wav":
        source_tags = WAVE(source_file)
        target_audio = WAVE(target_file)
    elif source_format == "aiff":
        source_tags = AIFF(source_file)
        target_audio = AIFF(target_file)
    else:
        return
    for key, value in source_tags.items():
        target_audio[key] = value
    target_audio.save()

def convert_files():
    global source_folder_entry, source_format_entry, target_folder_entry, target_format_entry
    source_folder = source_folder_entry.get()
    source_format = source_format_entry.get().lower()
    target_folder = target_folder_entry.get()
    target_format = target_format_entry.get().lower()
    if not (source_folder and source_format and target_folder and target_format):
        messagebox.showerror("Error!", "Please select a folder and a format")
        return
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for filename in os.listdir(source_folder):
        if filename.endswith(f".{source_format}"):
            source_path = os.path.join(source_folder, filename)
            target_path = os.path.join(target_folder, os.path.splitext(filename)[0] + f".{target_format}")
            try:
                shutil.copy2(source_path, target_path)
                copy_tags(source_path, target_path, source_format)
            except Exception as e:
                messagebox.showerror(
                    "Error!", f"Error with file {filename}:\n{e}")
                continue
    messagebox.showinfo("Done", "All files have been converted!")

def main():
    global source_folder_entry, source_format_entry, target_folder_entry, target_format_entry
    root = Tk()
    root.title("Soupoconverter")
    root.resizable(False, False)
    Label(root, text="Input folder:").grid(row=0, column=0, sticky="w")
    source_folder_entry = Entry(root, width=40)
    source_folder_entry.grid(row=0, column=1)
    Button(root, text="Choose", command=lambda: select_folder(source_folder_entry)).grid(row=0, column=2)
    Label(root, text="Input files format:").grid(row=1, column=0, sticky="w")
    source_format_entry = Entry(root, width=40)
    source_format_entry.grid(row=1, column=1)
    Label(root, text="Output folder:").grid(row=2, column=0, sticky="w")
    target_folder_entry = Entry(root, width=40)
    target_folder_entry.grid(row=2, column=1)
    Button(root, text="Choose", command=lambda: select_folder(target_folder_entry)).grid(row=2, column=2)
    Label(root, text="Converted files format:").grid(row=3, column=0, sticky="w")
    target_format_entry = Entry(root, width=40)
    target_format_entry.grid(row=3, column=1)
    Button(root, text="Convert", command=convert_files).grid(row=4, column=0, columnspan=3)
    root.mainloop()

if __name__ == "__main__":
    main()