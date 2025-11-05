# -*- coding: utf-8 -*-
"""
QRCode Tool - MHD, Services
A lightweight Tkinter GUI for generating QR codes with:
- Custom colors (fill/background)
- Optional centered logo (with white padding)
- Live preview
- Simple, modern-styled buttons with hover states
"""

import os
import sys
import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, ttk

# ---------- Utilities ----------
def resource_path(rel_path: str) -> str:
    """
    Resolve resource path for both normal runs and PyInstaller bundles.
    """
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)

# ---------- UI Colors ----------
PRIMARY_BG = "#0d6efd"
PRIMARY_BG_HOVER = "#0b5ed7"
PRIMARY_TX = "#ffffff"
APP_BG = "#f7f9fc"
CARD_BG = "#ffffff"
BORDER = "#e5e7eb"

PREVIEW_BG = "#6c757d"
PREVIEW_HOVER = "#5c636a"
SAVE_BG = "#16a34a"
SAVE_HOVER = "#12823d"

def make_btn(parent, text, command, width=24, bg=PRIMARY_BG, hover=None):
    """
    Create a unified, hoverable Tk button with consistent styling.
    """
    hover = hover or (PREVIEW_HOVER if bg == PREVIEW_BG else (SAVE_HOVER if bg == SAVE_BG else PRIMARY_BG_HOVER))
    btn = tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=PRIMARY_TX, activebackground=hover,
        activeforeground=PRIMARY_TX, relief="flat", bd=0,
        padx=12, pady=8, font=("Segoe UI", 10, "bold"),
        width=width, cursor="hand2", highlightthickness=0
    )
    def on_enter(e): btn.configure(bg=hover)
    def on_leave(e): btn.configure(bg=bg)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

def center_window(win, w=400, h=680):
    """
    Center the root window on screen.
    """
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ---------- QR Generation ----------
def generate_qr(preview=False):
    """
    Build a QR image from the current form settings.
    If preview=True, render into the preview area instead of saving.
    """
    data = entry.get().strip()
    if not data:
        messagebox.showwarning("Input required", "Please enter text or URL!")
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color=fill_color.get(),
        back_color=back_color.get()
    ).convert("RGB")

    # Optional centered logo with a thin white border for readability
    if logo_path.get():
        try:
            logo = Image.open(logo_path.get()).convert("RGBA")
            qr_w, qr_h = qr_img.size

            scale = logo_scale.get() / 100.0
            logo_size = int(qr_w * scale)
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

            border_pad = 10
            border = Image.new("RGBA", (logo_size + border_pad, logo_size + border_pad), (255, 255, 255, 255))
            border.paste(logo, (border_pad // 2, border_pad // 2), logo)

            pos = ((qr_w - border.size[0]) // 2, (qr_h - border.size[1]) // 2)
            qr_img.paste(border, pos, border)

        except Exception as e:
            messagebox.showerror("Logo Error", f"Failed to add logo: {e}")

    if preview:
        show_preview(qr_img)
        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        initialfile="qr_code.png",
        title="Save QR Code"
    )
    if filename:
        qr_img.save(filename)
        messagebox.showinfo("Success", f"QR Code saved as {filename}")

def choose_color(var):
    """
    Open a color picker and assign the chosen color to a Tk variable.
    """
    color_code = colorchooser.askcolor(title="Choose color")[1]
    if color_code:
        var.set(color_code)

def choose_logo():
    """
    Select a center logo image file (PNG/JPG).
    """
    path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg")],
        title="Choose QR center logo"
    )
    if path:
        logo_path.set(path)

def show_preview(img):
    """
    Render a resized thumbnail of the QR into the preview label.
    """
    preview_side = 260
    qr_w, qr_h = img.size
    ratio = preview_side / max(qr_w, qr_h)
    preview_img = img.resize((int(qr_w * ratio), int(qr_h * ratio)), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(preview_img)
    preview_label.config(image=img_tk, text="")
    preview_label.image = img_tk

# ---------- GUI ----------
root = tk.Tk()
root.title("QRCode Tool - MHD, Services")
root.configure(bg=APP_BG)
center_window(root, 400, 680)
root.minsize(380, 620)

# App icon (supports both .ico for Windows and .png for cross-platform)
ico_path = resource_path(os.path.join("assets", "app_icon.ico"))
png_path = resource_path(os.path.join("assets", "app_icon.png"))

if os.path.exists(ico_path):
    try: root.iconbitmap(ico_path)
    except: pass
if os.path.exists(png_path):
    try:
        _icon_img = tk.PhotoImage(file=png_path)
        root.iconphoto(True, _icon_img)
        root._app_icon_ref = _icon_img
    except: pass

# Card container
card = tk.Frame(root, bg=CARD_BG, bd=0, highlightthickness=1, highlightbackground=BORDER)
card.pack(padx=16, pady=16, fill="both", expand=True)

# Input
tk.Label(card, text="Enter text or URL:", bg=CARD_BG, fg="#111827", font=("Segoe UI", 10, "bold")).pack(pady=(16, 6))
entry = tk.Entry(card, width=40, font=("Segoe UI", 10))
entry.pack(padx=16, pady=(0, 12))

# State variables
fill_color = tk.StringVar(value="black")
back_color = tk.StringVar(value="white")
logo_path = tk.StringVar(value="")
logo_scale = tk.DoubleVar(value=25)

# Controls
btn_fill = make_btn(card, "Pick Fill Color", lambda: choose_color(fill_color))
btn_back = make_btn(card, "Pick Background Color", lambda: choose_color(back_color))
btn_logo = make_btn(card, "Choose Logo (optional)", choose_logo)

btn_fill.pack(pady=4)
btn_back.pack(pady=4)
btn_logo.pack(pady=4)

ttk.Separator(card, orient="horizontal").pack(fill="x", padx=16, pady=10)

tk.Label(card, text="Logo size (% of QR):", bg=CARD_BG, fg="#374151", font=("Segoe UI", 9)).pack(pady=(2, 4))
scale = ttk.Scale(
    card,
    from_=10,
    to=25,
    orient="horizontal",
    variable=logo_scale
)
scale.pack(fill="x", padx=32)

# Actions
btn_preview = make_btn(card, "Preview QR Code", lambda: generate_qr(preview=True), bg=PREVIEW_BG, hover=PREVIEW_HOVER)
btn_save = make_btn(card, "Save QR Code", generate_qr, bg=SAVE_BG, hover=SAVE_HOVER)

btn_preview.pack(pady=(12, 6))
btn_save.pack(pady=6)

# Preview area
preview_wrap = tk.Frame(card, bg=CARD_BG)
preview_wrap.pack(padx=12, pady=(6, 16), fill="both", expand=True)

preview_label = tk.Label(
    preview_wrap,
    text="QR Preview will appear here",
    bg=APP_BG, fg="#6b7280",
    font=("Segoe UI", 9),
    bd=1, relief="solid", padx=8, pady=8
)
preview_label.pack(expand=True, padx=4, pady=4, fill="both")

root.mainloop()
