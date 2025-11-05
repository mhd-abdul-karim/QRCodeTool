# 🧾 QRCode Tool – MHD Services

A modern **Windows desktop application** for generating stylish QR Codes with live preview, custom colors, and optional logo in the center — developed by **MHD Abdul Karim**.

---

## 🎨 Features

✅ **Customizable Colors** – Choose any fill and background colors.  
✅ **Logo Support** – Add your company or project logo at the center of the QR.  
✅ **Smart Logo Scaling** – Control the logo size (10–25% of QR).  
✅ **Live Preview** – Instantly see your QR code before saving.  
✅ **High Error Correction** – Uses `qrcode.constants.ERROR_CORRECT_H` for high reliability.  
✅ **Modern GUI** – Clean interface built with `Tkinter` and `Pillow`.  
✅ **Portable EXE Version** – Works on any Windows system, no installation required.  

---

## 🧠 Tech Stack

- **Language:** Python 3.11+  
- **Libraries:**  
  - `qrcode`  
  - `pillow (PIL)`  
  - `tkinter`  
- **Packaging:** PyInstaller (`.exe` generation)

---

## ⚙️ Run from Source

If you want to run or modify the source code manually:

```bash
git clone https://github.com/mhd-abdul-karim/QRCodeTool.git
cd QRCodeTool
pip install -r requirements.txt
python main.py
```

## 💾 Generate EXE (Developer Mode)

If you want to build your own .exe version:

```bash
pyinstaller --noconfirm --clean --onedir --noconsole ^
  --name QRCodeTool_MHD ^
  --icon assets\app_icon.ico ^
  --add-data "assets;assets" ^
  main.py
```

After build, the EXE will appear in:

```bash
dist/QRCodeTool_MHD/QRCodeTool_MHD.exe
```

## 📦 Folder Structure

```
QRCodeTool/
│
├── assets/                 # Icons and app images
├── main.py                 # Main source code
├── requirements.txt        # Python dependencies
├── .gitignore             # Ignore unnecessary files
└── README.md              # Project documentation
```

## 🚀 Download

⬇️ [Download Latest Version (Windows)](https://github.com/mhd-abdul-karim/QRCodeTool/releases)

---

## 🧑‍💻 Author

**MHD Abdul Karim**  
Software Engineer | AI & Automation Developer  
📍 Muscat, Oman  
🔗 [LinkedIn](https://www.linkedin.com/in/mhd-abdul-karim/)  
📧 [Contact Me](mailto:muhamadak.dev@gmail.com)

---

## 🪪 License

This project is currently unlicensed.  
If you plan to use or distribute it commercially, please contact the author.

---

## ⭐ Support

If you like this project, please consider giving it a ⭐ on GitHub — it helps a lot!
```
