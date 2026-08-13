from urllib.parse import urljoin, unquote, urlparse
import glob
import os
from datetime import datetime
import re
import tkinter as tk
import zipfile
from tkinter import messagebox
from bs4 import BeautifulSoup
import pandas as pd
import requests
from sqlalchemy import engine, text, text
import shutil
import backend.config as cfg


# Δημιουργία του παραθύρου
window = tk.Tk()
window.title("Vaseis Project")
window.minsize(width=900, height=500)
window.configure(bg="#468EB8")

width, height = 900, 500
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)
window.geometry(f"{width}x{height}+{x}+{y}")

label = tk.Label(text="Welcome to Vaseis Project", font=("Arial", 24, "bold"), bg="#468EB8", fg="white")
label.pack(pady=60)

frame = tk.Frame(window, bg="#468EB8")
frame.pack(pady=40)

# το content frame είναι αυτό που θα καθαρίζω και θα βάζω τα νέα widgets ανάλογα με τη ροή
content_frame = tk.Frame(window, bg="#468EB8")
content_frame.pack()


# ρυθμίζω τις μεταβλητές για τους φακέλους, το URL και τη βάση
TARGET_YEAR = str(datetime.now().year)
desktop = os.path.join(os.path.expanduser("~"), "Desktop") 
year_folder = os.path.join(desktop, "VaseisDownloads", str(TARGET_YEAR)) 
os.makedirs(year_folder, exist_ok=True)
BASE_URL = "https://www.minedu.gov.gr"
connection_string = f"mysql+pymysql://{cfg.DB_USER}:{cfg.DB_PASS}@{cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_NAME}"
engine = engine.create_engine(connection_string, echo=True)







# year_folder = ensure_folder(os.path.join(main_folder, str(datetime.now().year)))


# styling του κουμπιού με Canvas 
class Button(tk.Canvas):
    def __init__(self, parent, text, command=None,
                 width=200, height=70, radius=20,
                 bg="#469CF3", fg="white",
                 hover_bg="#339BF7", shadow=True):

        super().__init__(parent, width=width, height=height,
                         bg=parent["bg"], highlightthickness=0, cursor="hand2")

        self.command = command
        self.radius = radius
        self.bg_color = bg
        self.fg_color = fg
        self.hover_bg = hover_bg
        self.shadow = shadow
        self.width = width
        self.height = height

        self.draw_button(text)

        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def draw_button(self, text):
        self.delete("all")
        r = self.radius
        w = self.width
        h = self.height

        if self.shadow:
            self.create_rounded_rect(4, 4, w, h, r, fill="#333333", outline="")

        self.rect = self.create_rounded_rect(0, 0, w - 4, h - 4, r,
                                             fill=self.bg_color, outline=self.bg_color)

        self.text = self.create_text((w // 2) - 2, (h // 2) - 2,
                                     text=text, fill=self.fg_color,
                                     font=("Segoe UI", 14, "bold"))

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_click(self, event):
        if self.command:
            self.command()

    def on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_bg, outline=self.hover_bg)

    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color, outline=self.bg_color)


# καθαρίζω το content frame για να βάλω νέα widgets
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

# δημιουργία φακέλων για αποθήκευση αρχείων
def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


# κανω scraping τη σελίδα του υπουργείου για να βρω τα αρχεία, αν αποτύχει επιστρέφω False για να ξεκινήσει το URL search
def scrape_ministry_site():
    
    label.config(text="Searching...")
    MAIN_PAGE = f"{BASE_URL}/baseis-an" 
     

    # Βρίσκω το link της σελίδας αποτελεσμάτων
    try:
        resp = requests.get(MAIN_PAGE)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Conection error: {e}")
        label.config(text="Connection Error! Try another method.")
        #exit()
        return False

    soup = BeautifulSoup(resp.text, "html.parser")

    target_link = None

    # Ψάχνω τον τίτλο της ανακοίνωσης
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        
        # Τίτλος 2024
        if "Βάσεις" in text and "Στατιστικά" in text and TARGET_YEAR in text:
            target_link = a["href"]
            break 
        
        # Τίτλος 2025
        if "Σχετικά με τα αποτελέσματα εισαγωγής" in text and TARGET_YEAR in text:
            target_link = a["href"]
            break

    if not target_link:
        print(f"Could not find a link for the year {TARGET_YEAR}")
        return False
        #exit()

    full_page_url = urljoin(BASE_URL, target_link)
    print(f"Page URL: {full_page_url}")

    # Μπαίνω στη σελίδα με τα αποτελέσματα
    resp2 = requests.get(full_page_url)
    soup2 = BeautifulSoup(resp2.text, "html.parser")

    download_links = []

    for a in soup2.find_all("a", href=True):
        href = a['href']
        
        # Αποκωδικοποίηση URL για να διαβάζουμε σωστά τα Ελληνικά (π.χ. %CE%92%CE...)
        decoded_href = unquote(href)
        
        filename_lower = decoded_href.lower()
        
        # Έλεγχος αρχείου
        if filename_lower.endswith((".zip", ".xls", ".xlsx")):
            
            full_url = urljoin(BASE_URL, href)
            keep_file = False
            
            # Βάσεις ΓΕΛΕΠΑΛ
            if ("βάσεις" in filename_lower) and ("γελ" in filename_lower or "επαλ" in filename_lower):
                keep_file = True

            # Στατιστικά Προτιμήσεων ΓΕΛΕΠΑΛ
            # if ("στατιστικά" in filename_lower and "προτιμήσεων" in filename_lower) and ("γελ" in filename_lower or "επαλ" in filename_lower):
            #      keep_file = True
            if (
                ("στατισ" in filename_lower or "statist" in filename_lower) and
                ("προτιμ" in filename_lower or "protim" in filename_lower) and
                ("γελ" in filename_lower or "gel" in filename_lower or "επαλ" in filename_lower or "epal" in filename_lower)
            ):
                keep_file = True


            # Αν τα βρήκε τα βάζω στη λίστα
            if keep_file:
                if full_url not in download_links:
                    download_links.append(full_url)
                    print(f"Selected: {decoded_href.split('/')[-1]}")
                
    if not download_links:
        print("There are no files matching the criteria.")
        return False
        #exit()

    # Κατεβάζω τα αρχεία
    os.makedirs(year_folder, exist_ok=True)
    downloaded_files = []

    print(f"\n Start downloading {len(download_links)} files ---")

    for link in download_links:
        
            filename = os.path.basename(unquote(link))
            save_path = os.path.join(year_folder, filename)
            
            print(f"Downloading: {filename}")
            try:
                r = requests.get(link, stream=True)
                with open(save_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                downloaded_files.append(save_path)
            except Exception as e:
                print(f"Error downloading {filename}: {e}")
                return False
    # Unzip
    for file_path in downloaded_files:

        if file_path.endswith(".zip"):

            try:
                zip_name = os.path.basename(file_path).lower()

                # Επιλογή σωστού φακέλου
                if "βάσεις" in zip_name:
                    target_folder = os.path.join(year_folder, "Vaseis")
                elif "στατιστικά" in zip_name:
                    target_folder = os.path.join(year_folder, "Statistics")
                else:
                    target_folder = os.path.join(year_folder, "Other")
                os.makedirs(target_folder, exist_ok=True)

                # Προσωρινός φάκελος για unzip
                temp_folder = os.path.join(year_folder, "_temp_unzip")
                os.makedirs(temp_folder, exist_ok=True)

                # Unzip στο temp
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    zip_ref.extractall(temp_folder)

                # Μεταφορά ΟΛΩΝ των αρχείων από temp → target_folder
                for root, dirs, files in os.walk(temp_folder):
                    for f in files:
                        src = os.path.join(root, f)
                        dst = os.path.join(target_folder, f)
                        shutil.move(src, dst)

                # Καθαρισμός temp
                shutil.rmtree(temp_folder)

                print(f"Unzipped to: {target_folder}")

            except zipfile.BadZipFile:
                print(f"The file {os.path.basename(file_path)} is not a valid zip.")
                return False

    print("\n End of scraping.")
    process_statistics(year_folder)
    process_vaseis(year_folder)
    return True
    


# ζητάω από τον χρήστη να δώσει URL αν αποτύχει το scraping και ψαχνω τα αρχεία με URL search
def ask_for_url_from_user():
    

    clear_content()
    label.config(text="Auto-Scraping Failed \n Searching with URL")
    label.pack(pady=60)
    msg = tk.Label(content_frame, text="Give the URL where the files are located:",
                   font=("Arial", 16), bg="#468EB8", fg="white")
    msg.pack(pady=10)

    entry = tk.Entry(content_frame, width=70)
    entry.pack(ipady=10)

    def url_search():
        global link
        link = entry.get().strip()
        parsed = urlparse(link)
        
        
        # Έλεγχος: Πρέπει να έχει σχήμα (http/https) ΚΑΙ domain (π.χ. google.com)
        if parsed.scheme in ('http', 'https') and parsed.netloc:
        
            print(f"URL page: {link}")
            clear_content()
            label.config(text="Searching...")
            label.update_idletasks()
            
            # Μπαίνω στη σελίδα με τα αποτελέσματα
            resp2 = requests.get(link)
            soup2 = BeautifulSoup(resp2.text, "html.parser")

            download_links = []

            for a in soup2.find_all("a", href=True):
                href = a['href']
                
                # Αποκωδικοποίηση URL για να διαβάζουμε σωστά τα Ελληνικά (π.χ. %CE%92%CE...)
                decoded_href = unquote(href)
                
                filename_lower = decoded_href.lower()
                
                # Έλεγχος αρχείου
                if filename_lower.endswith((".zip", ".xls", ".xlsx")):
                    
                    full_url = urljoin(BASE_URL, href)
                    keep_file = False
                    
                    # Βάσεις ΓΕΛΕΠΑΛ
                    if ("βάσεις" in filename_lower) and ("γελ" in filename_lower or "επαλ" in filename_lower):
                        keep_file = True

                    # Στατιστικά Προτιμήσεων ΓΕΛΕΠΑΛ
                    # if ("στατιστικά" in filename_lower and "προτιμήσεων" in filename_lower) and ("γελ" in filename_lower or "επαλ" in filename_lower):
                    #      keep_file = True
                    if (
                        ("στατισ" in filename_lower or "statist" in filename_lower) and
                        ("προτιμ" in filename_lower or "protim" in filename_lower) and
                        ("γελ" in filename_lower or "gel" in filename_lower or "επαλ" in filename_lower or "epal" in filename_lower)
                    ):
                        keep_file = True


                    # Αν τα βρήκε τα βάζω στη λίστα
                    if keep_file:
                        if full_url not in download_links:
                            download_links.append(full_url)
                            print(f"Selected: {decoded_href.split('/')[-1]}")
                        
            if not download_links:
                print("There are no files matching the criteria.")
                ask_user_to_place_files(year_folder)
                #exit()

            # Κατεβάζω τα αρχεία
            os.makedirs(year_folder, exist_ok=True)
            downloaded_files = []

            print(f"\n Start downloading {len(download_links)} files ")

            for link in download_links:
                
                    filename = os.path.basename(unquote(link))
                    save_path = os.path.join(year_folder, filename)
                    
                    print(f"Downloading: {filename}")
                    try:
                        r = requests.get(link, stream=True)
                        with open(save_path, "wb") as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                        downloaded_files.append(save_path)
                    except Exception as e:
                        print(f"Error downloading {filename}: {e}")

            # Unzip
            for file_path in downloaded_files:

                if file_path.endswith(".zip"):

                    try:
                        zip_name = os.path.basename(file_path).lower()

                        # Επιλογή σωστού φακέλου
                        if "βάσεις" in zip_name:
                            target_folder = os.path.join(year_folder, "Vaseis")
                        elif "στατιστικά" in zip_name:
                            target_folder = os.path.join(year_folder, "Statistics")
                        else:
                            target_folder = os.path.join(year_folder, "Other")
                        os.makedirs(target_folder, exist_ok=True)

                        # Προσωρινός φάκελος για unzip
                        temp_folder = os.path.join(year_folder, "_temp_unzip")
                        os.makedirs(temp_folder, exist_ok=True)

                        # Unzip στο temp
                        with zipfile.ZipFile(file_path, "r") as zip_ref:
                            zip_ref.extractall(temp_folder)

                        # Μεταφορά ΟΛΩΝ των αρχείων από temp → target_folder
                        for root, dirs, files in os.walk(temp_folder):
                            for f in files:
                                src = os.path.join(root, f)
                                dst = os.path.join(target_folder, f)
                                shutil.move(src, dst)

                        # Καθαρισμός temp
                        shutil.rmtree(temp_folder)

                        print(f"Unzipped to: {target_folder}")

                    except zipfile.BadZipFile:
                        print(f"The file {os.path.basename(file_path)} is not a valid zip.")
                        return False

            print("\n End of URL search.")
            if not link:
                messagebox.showwarning("Warning", "You must give a URL.")
                return

            clear_content()
            label.config(text="URL saved")

            # Αν τα αρχεία βρέθηκαν και κατεβάστηκαν, προχωράω στην επεξεργασία, αλλιώς ζητάω από τον χρήστη να τα βάλει χειροκίνητα
            if downloaded_files:
                process_statistics(year_folder)
                process_vaseis(year_folder)
            else:
                ask_user_to_place_files(year_folder)
        else:
            label.config(text="Invalid URL! Try again.")

    btn = Button(content_frame, text="Submit", command=url_search,
        bg="#194775", hover_bg="#1558A0", radius=18)
    btn.pack(pady=20)


# ζητάω από τον χρήστη να βάλει τα αρχεία σε φάκελο αν αποτύχει το scraping και το url search
def ask_user_to_place_files(year_folder):
    clear_content()
    for widget in content_frame.winfo_children():
        widget.destroy()
    label.config(text="Url-Searching Failed \nSearching with Folder Path")
    msg = tk.Label(content_frame, text="Give the folder path where you placed the files:",
    font=("Arial", 16), bg="#468EB8", fg="white")
    msg.pack(pady=10)

    entry = tk.Entry(content_frame, width=70)
    entry.pack(ipady=10)

    def retry_check():
        find_excel_files(entry.get())

    btn = Button(content_frame, text="Submit", command=retry_check,
                 bg="#194775", hover_bg="#1558A0", radius=18)
    btn.pack(pady=20)


# ψαχνω Excel αρχεία στους φακέλους, αν δεν υπάρχουν δείχνω το label1 + Start που οδηγεί σε scraping 
def find_excel_files(year_folder=year_folder):
    global link
    
    clear_content()
    frame.pack_forget()
    content_frame.pack(expand=True, fill="both", pady=10)
    
    for widget in content_frame.winfo_children():
        widget.destroy()


    vaseis_folder = ensure_folder(
        os.path.join(year_folder, "Vaseis")
    )

    stats_folder = ensure_folder(
        os.path.join(year_folder, "Statistics")
    )

    vaseis_files = [
        f for f in os.listdir(vaseis_folder)
        if f.lower().endswith((".xls", ".xlsx", ".xlsm"))
    ]

    stats_files = [
        f for f in os.listdir(stats_folder)
        if f.lower().endswith((".xls", ".xlsx", ".xlsm"))
    ]

    # πρεπει να υπάρχουν αρχεία και στους δύο φακέλους
    if vaseis_files and stats_files:
        print("Excel files found. Processing...")
        process_statistics(year_folder)
        process_vaseis(year_folder)
        return

    # αν δεν βρέθηκαν αρχεία → δείξε label1 + Start
    label1 = tk.Label(
        content_frame,
        text="No Excel files found.\nPress Start to scrape the ministry site...",
        font=("Arial", 16, "bold"),
        bg="#468EB8",
        fg="white"
    )
    label1.pack(pady=(0, 20))


    # Το Start κουμπί ΤΩΡΑ ξεκινάει scraping
    start_button = Button(
        content_frame,
        text="Start",
        command=start_scraping,
        bg="#194775",
        hover_bg="#1558A0",
        radius=18
    )
    start_button.pack()


def start_scraping():
    
    for widget in frame.winfo_children():
        widget.destroy()
    clear_content()
    label.config(text="Scraping ministry site...")

    success = scrape_ministry_site() 
    if success: 
        print("Scraping completed successfully.") 
    else: 
        ask_for_url_from_user()



def process_statistics(save_folder):
    clear_content()
    for widget in content_frame.winfo_children():
        widget.destroy()
    # μετατροπή αρχείων statistics σε csv
    label.config(text="Processing data...")
    label.update_idletasks()

    folderstat = os.path.join(save_folder, "Statistics")

    # βρίσκω όλα τα Excel αρχεία (xls, xlsx) 
    files = [f for f in glob.glob(os.path.join(folderstat, "*.xls*")) if not os.path.basename(f).startswith("~$") ] 


    dfs = []

    for f in files:

        try:
            # διαβάζω το Excel από τη δεύτερη γραμμή
            df = pd.read_excel(f, header=1)

            # μετονομασία στηλών 
            rename_map = {
                "ΚΩΔΙΚΟΣ ΣΧΟΛΗΣ": "code",
                "ΣΧΟΛΗ": "name",
                "ΠΡΟΤΙΜΗΣΗ\n1η": "protimisi1",
                "ΠΡΟΤΙΜΗΣΗ\n2η": "protimisi2",
                "ΠΡΟΤΙΜΗΣΗ\n3η": "protimisi3",
                "ΠΡΟΤΙΜΗΣΗ\n4η": "protimisi4",
                "ΠΡΟΤΙΜΗΣΗ\n5η": "protimisi5",
                "ΠΡΟΤΙΜΗΣΗ\n6η": "protimisi6",
                "ΠΡΟΤΙΜΗΣΗ\n(Άλλη Σειρά)": "protimisi7"
            }
            df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

            df["year"] = str(TARGET_YEAR)

            # category 1 ή 0 βάσει του ονόματος αρχείου
            if "category" not in df.columns:
                title = os.path.basename(f).lower()
                if "επιτυχόντων" in title:
                    df["category"] = 1
                elif "υποψηφίων" in title:
                    df["category"] = 0
                else:
                    df["category"] = None

            # αν δεν υπάρχουν protimisi4/protimisi5/protimisi6 τις προσθέτω
            for col in ["protimisi4", "protimisi5", "protimisi6" ]:
                if col not in df.columns:
                    df[col] = 0


            try:
                first_row = pd.read_excel(f, header=None, nrows=1)
                header_text = str(first_row.iloc[0, 0]).strip()

                # αναζητώ είτε "ΕΠΙΛΟΓΗ 10% ΓΕΛ 2023", είτε "ΕΠΙΛΟΓΗ ΕΠΑΛ", είτε "ΕΠΙΛΟΓΗ ΓΕΛ"
                match = re.search(r"(?:10%\s+)?(ΓΕΛ|ΕΠΑΛ)(?:\s+\d{4})?", header_text)
                if match:
                    part = match.group(0)  #  "ΕΠΙΛΟΓΗ 10% ΓΕΛ 2023" ή "ΕΠΙΛΟΓΗ ΕΠΑΛ"
                    # βάζω "ΗΜΕΡΗΣΙΑ & ΕΣΠΕΡΙΝΑ" μετά από ΓΕΛ/ΕΠΑΛ
                    selection_value = re.sub(r"(ΓΕΛ|ΕΠΑΛ)", r"\1 ΗΜΕΡΗΣΙΑ & ΕΣΠΕΡΙΝΑ", part)
                else:
                    selection_value = None

                df["id"] = selection_value
            except Exception:
                df["id"] = None


            # κρατάω μόνο τις στήλες που χρειάζομαι
            wanted_cols = ["code","name", "protimisi1", "protimisi2", "protimisi3", "protimisi4", "protimisi5", "protimisi6", "protimisi7", "category", "year", "id"]
            df = df[[c for c in wanted_cols if c in df.columns]]

            dfs.append(df)

        except Exception as e:
            print("Error in", f, ":", e)
    # συγχωνεύω όλα τα DataFrames και αποθηκεύω σε CSV
    if dfs:
        full = pd.concat(dfs, ignore_index=True)
        output_file = os.path.join(folderstat, f"stats.{TARGET_YEAR}.csv")
        full.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"The file stats.{TARGET_YEAR}.csv was created with", len(full), "rows.")
    else:
        print("No Excel files were found for merging.")





    # Εισαγωγή statistics στην βάση

    df = pd.read_csv(os.path.join(folderstat, f"stats.{TARGET_YEAR}.csv"))


    # Μετατροπή από wide σε long format
    protimisi_cols = [c for c in df.columns if c.startswith("protimisi")]
    df_long = df.melt(
        id_vars=["code","id","category","year"],
        value_vars=protimisi_cols,
        var_name="protimisi",
        value_name="plithos"
    )

    # καθαρισμός: protimisi1 -> 1, protimisi2 -> 2, ..., protimisi_other -> 7
    df_long["protimisi"] = df_long["protimisi"].str.replace("protimisi","")
    df_long["protimisi"] = df_long["protimisi"].replace({"other":"7"})
    df_long["protimisi"] = df_long["protimisi"].astype(int)

    # αν category=0 και protimisi είναι 4,5,6 τότε κράτα μόνο όσες έχουν plithos > 0
    mask = ~((df_long["category"] == 0) & (df_long["protimisi"].isin([4,5,6])) & (df_long["plithos"] == 0))
    df_long = df_long[mask]


    # εισαγωγή στον πίνακα statistics
    with engine.begin() as conn:
        for _, row in df_long.iterrows():   # <-- Χρησιμοποιούμε df_long
            conn.execute(text("""
                INSERT IGNORE INTO statistics 
                (code, id, category, protimisi, plithos, year)
                VALUES (:code, :id, :category, :protimisi, :plithos, :year)
            """), row.to_dict())

    print("The data was inserted into the statistics table")







def process_vaseis(save_folder):

    foldervas = os.path.join(save_folder, "Vaseis")

    # βρίσκω όλα τα Excel αρχεία (xls, xlsx)
    files = [f for f in glob.glob(os.path.join(foldervas, "*.xls*")) if not os.path.basename(f).startswith("~$")]

    print("Found files:", files)

    dfs = []

    for f in files:
        try:
            # διαβάζω το Excel από τη δεύτερη γραμμή
            df = pd.read_excel(f, header=1)

            # μετονομασία στηλών 
            rename_map = {
                "ΚΩΔΙΚΟΣ ΣΧΟΛΗΣ": "code",
                "ΙΔΡΥΜΑ": "institution",
                "ΟΝΟΜΑ ΣΧΟΛΗΣ": "title",
                "ΕΙΔΟΣ ΘΕΣΗΣ": "cat_title",
                "ΑΡΧΙΚΕΣ ΘΕΣΕΙΣ": "positions",
                "ΕΠΙΣΤΗΜΟΝΙΚΑ ΠΕΔΙΑ": "field",
                "ΒΑΘΜΟΣ ΠΡΩΤΟΥ": "vasiprotou",
                "ΒΑΘΜΟΣ ΤΕΛΕΥΤΑΙΟΥ": "vasitel"
            }
            df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

            # στήλη code πρεπει να είναι αριθμητική
            if "code" in df.columns:
                df["code"] = pd.to_numeric(df["code"], errors="coerce")
                df = df.dropna(subset=["code"])
                df["code"] = df["code"].astype(int)

            df["year"] = str(TARGET_YEAR)

            # προσθέτω στήλες που λείπουν
            if "field" not in df.columns:
                df["field"] = None


            for col in ["admissions", "minimumBase"]:
                if col not in df.columns:
                    df[col] = None

            # παίρνω το title από την πρώτη γραμμή του αρχείου 
            try:
                first_row = pd.read_excel(f, header=None, nrows=1)
                header_text = str(first_row.iloc[0, 0]).strip()

                # Προσδιορισμός του title βάσει του header_text
                if "ΕΠΙΛΟΓΗ" in header_text:
                    after_choice = header_text.split("ΕΠΙΛΟΓΗ", 1)[1].strip()
                    main_part = after_choice.split("--")[0].strip()
                    # βρίσκω το έτος (4 ψηφία) και προσθέτουμε "-ΗΜΕΡΗΣΙΑ"
                    title_value = re.sub(r"(\d{4})", r"\1 ΗΜΕΡΗΣΙΑ", main_part)
                else:
                    title_value = header_text if header_text else None

                df["title"] = title_value
            except Exception:
                df["title"] = None

            # κρατάω μόνο τις στήλες που χρειάζομαι
            wanted_cols = ["code","institution", "title", "cat_title", "positions", "admissions", "field", "year", "vasiprotou", "vasitel", "minimumBase"]
            df = df[[c for c in wanted_cols if c in df.columns]]

            dfs.append(df)

        except Exception as e:
            print("Error in", f, ":", e)

    # Συγχωνεύω όλα τα DataFrames και αποθηκεύω σε CSV
    if dfs:
        full = pd.concat(dfs, ignore_index=True)

        full['title'] = full['title'].str.replace("-", " ", regex=False)

        output_file = os.path.join(foldervas, f"vaseis.{TARGET_YEAR}.csv")
        full.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"The file vaseis.{TARGET_YEAR}.csv was created with", len(full), "rows.")
    else:
        print("No Excel files were found for merging.")





    # Εισαγωγή vaseis στην βάση

    df = pd.read_csv(os.path.join(foldervas, f"vaseis.{TARGET_YEAR}.csv"))
    # διαγραφή της στήλης institution αν υπάρχει
    if "institution" in df.columns:
        df = df.drop(columns=["institution"])
    # στήλη code πρεπει να είναι αριθμητική
    df['code'] = pd.to_numeric(df['code'], errors='coerce')
    df = df.dropna(subset=['code'])   
    df['code'] = df['code'].astype(int)
    # αλλαγή NaN με 0 σε vasiprotou και vasitel
    df['vasiprotou'] = df['vasiprotou'].fillna(0).astype(int)
    df['vasitel'] = df['vasitel'].fillna(0).astype(int)
    # όλα τα NaN σε None για να γίνουν NULL στη MySQL
    df = df.where(pd.notnull(df), None)
    # παιρνω τα δεδομένα από τους πίνακες 
    exam_titles = pd.read_sql("SELECT title FROM examtype", engine)
    dept_codes = pd.read_sql("SELECT code FROM dept", engine)
    specialcat_titles = pd.read_sql("SELECT title FROM specialcat", engine)
    # ποιες τιμές λείπουν
    missing_titles = df[~df['title'].isin(exam_titles['title'])]['title'].dropna().unique()
    missing_codes = df[~df['code'].isin(dept_codes['code'])]['code']
    missing_cat_titles = df[~df['cat_title'].isin(specialcat_titles['title'])]['cat_title'].dropna().unique()
    print("Missing from examtype:", len(missing_titles))
    print("Missing from dept:", len(missing_codes))
    print("Missing from specialcat:", len(missing_cat_titles))
    # αποθήκευση των missing values
    pd.DataFrame(missing_titles, columns=["title"]).to_csv("missing_examtype.csv", index=False)
    pd.DataFrame(missing_codes, columns=["code"]).to_csv("missing_dept.csv", index=False)
    pd.DataFrame(missing_cat_titles, columns=["cat_title"]).to_csv("missing_specialcat.csv", index=False)
    print("The following files were created: missing_examtype.csv, missing_dept.csv, missing_specialcat.csv")
    # εισαγωγή των missing values
    with engine.begin() as conn:
        for t in missing_titles:
            conn.execute(text("INSERT IGNORE INTO examtype (title) VALUES (:title)"), {"title": t})
        for c in missing_codes:
            conn.execute(text("INSERT IGNORE INTO dept (code) VALUES (:code)"), {"code": int(c)})
        for ct in missing_cat_titles:
            conn.execute(text("INSERT IGNORE INTO specialcat (title) VALUES (:cat_title)"), {"cat_title": ct})

    print("The tables examtype, dept, specialcat were updated with the new values")
    # όλα τα NaN σε None για να γίνουν NULL στη MySQL
    df = df.where(pd.notnull(df), None)
    # καποιες στήλες να γίνουν 0 αντί για NULL
    df['vasiprotou'] = df['vasiprotou'].fillna(0).astype(int)
    df['vasitel'] = df['vasitel'].fillna(0).astype(int)
    df['admissions'] = df['admissions'].fillna(0).astype(int)
    df['minimumBase'] = df['minimumBase'].fillna(0).astype(int)
    # εισαγωγή με IGNORE για να αγνοεί διπλότυπα
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT IGNORE INTO base 
                (code, title, cat_title, positions, admissions, field, year, vasiprotou, vasitel, minimumBase)
                VALUES (:code, :title, :cat_title, :positions, :admissions, :field, :year, :vasiprotou, :vasitel, :minimumBase)
            """), row.to_dict())

    print("The data was inserted into the base table")
    
    
    label.config(text="Search Complete! \n Statistics and Vaseis imported to Database")
    update_ml_datasets()
    





def update_ml_datasets():
    clear_content()
    for widget in content_frame.winfo_children():
        widget.destroy()
    print("\nΞεκινά η δημιουργία των 4 Machine Learning Datasets...")
    label.config(text="Creating ML Datasets...\nPlease wait.")
    window.update_idletasks() # Ανανεώνει το γραφικό περιβάλλον
    
    # Το Query που τραβάει όλα τα έτη δυναμικά (μέχρι και το 2026+)
    query = """
    SELECT b.code, b.year, b.vasitel, b.field, u.title AS university,
           (SELECT ROUND(SUM(s.protimisi * s.plithos) / NULLIF(SUM(s.plithos), 0))
            FROM statistics s WHERE s.code = b.code AND s.category = 1) AS avg_pref_success
    FROM base b
    JOIN dept d ON b.code = d.code
    JOIN university u ON d.uni_id = u.id
    WHERE
        (b.year = 2013 AND b.cat_title LIKE '90%% ΓΕΝΙΚΗ%%ΣΕΙΡΑ%%') OR
        (b.year IN (2014, 2015) AND b.cat_title = '90%% ΓΕΛ/ΕΠΑΛΒ ΓΕΝ.ΣΕΙΡΑ ΗΜ.') OR
        (b.year = 2016 AND b.cat_title = 'ΓΕΛ ΓΕΝ.ΣΕΙΡΑ ΗΜ. (ΝΕΟ)') OR
        (b.year >= 2017 AND b.year != 2020 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.') OR
        (b.year = 2020 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ. (ΝΕΟ)')
    """
    
    # Χρησιμοποιεί το "engine" που έχεις ήδη ορίσει στην αρχή του αρχείου σου!
    df_raw = pd.read_sql(query, engine)

    # Pandas Pivot - Δημιουργία στηλών ετών
    df_pivot = df_raw.pivot_table(index=['code', 'university'], columns='year', values='vasitel', aggfunc='max').reset_index()
    df_meta = df_raw[['code', 'field', 'avg_pref_success']].groupby('code').max().reset_index()
    df_full = pd.merge(df_pivot, df_meta, on='code')

    # Μετονομασία στηλών (π.χ. 2026 -> base_2026)
    years = [col for col in df_full.columns if isinstance(col, int)]
    df_full = df_full.rename(columns={year: f'base_{year}' for year in years})
    max_year = max(years)

    # ΠΡΟΣΟΧΗ: Βάλε το ακριβές μονοπάτι για τον φάκελο datasets του site σου
    data_dir = r"C:\xampp\htdocs\VASEIS-APP\datasets" 
    os.makedirs(data_dir, exist_ok=True)

    # Dataset 1: 2013 έως Σήμερα
    cols_ds1 = ['code', 'field', 'university', 'avg_pref_success'] + [f'base_{y}' for y in range(min(years), max_year + 1)]
    df_ds1 = df_full[[c for c in cols_ds1 if c in df_full.columns]].dropna()
    df_ds1.to_csv(os.path.join(data_dir, 'dataset1.from2013.csv'), index=False)

    # Dataset 2: 2019 έως Σήμερα
    cols_ds2 = ['code', 'field', 'university', 'avg_pref_success'] + [f'base_{y}' for y in range(2019, max_year + 1)]
    df_ds2 = df_full[[c for c in cols_ds2 if c in df_full.columns]].dropna()
    df_ds2.to_csv(os.path.join(data_dir, 'dataset2.from2019.csv'), index=False)

    # Dataset 3: Διαφορές από 2013
    df_ds3 = df_full.copy()
    diff_cols_3 = []
    for y in range(min(years) + 1, max_year + 1):
        col_name = f'diff_{str(y)[-2:]}_{str(y-1)[-2:]}'
        df_ds3[col_name] = df_ds3[f'base_{y}'] - df_ds3[f'base_{y-1}']
        diff_cols_3.append(col_name)
    df_ds3[['code', 'field', 'university', 'avg_pref_success'] + diff_cols_3].dropna().to_csv(os.path.join(data_dir, 'dataset3.difsfrom2013.csv'), index=False)

    # Dataset 4: Διαφορές από 2019
    df_ds4 = df_full.copy()
    diff_cols_4 = []
    for y in range(2020, max_year + 1):
        col_name = f'diff_{str(y)[-2:]}_{str(y-1)[-2:]}'
        df_ds4[col_name] = df_ds4[f'base_{y}'] - df_ds4[f'base_{y-1}']
        diff_cols_4.append(col_name)
    df_ds4[['code', 'field', 'university', 'avg_pref_success'] + diff_cols_4].dropna().to_csv(os.path.join(data_dir, 'dataset4.difsfrom2019.csv'), index=False)

    print(f"Επιτυχία! Τα αρχεία του K-Means ανανεώθηκαν με βάση το {max_year}.")

    label.config(text="All Done!\n Datasets are Replaced!")






find_excel_files()


window.mainloop()
