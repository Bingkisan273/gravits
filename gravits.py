import tkinter as tk
from PIL import Image, ImageTk
import cv2
import random

# ==========================================
# WINDOW UTAMA
# ==========================================

root = tk.Tk()

root.title("GRAVITS")

window_width = 1000
window_height = 700

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2 + 50

root.geometry(
    f"{window_width}x{window_height}+{x}+{y}"
)

root.configure(bg="#728ab4")


# ==========================================
# VIDEO
# ==========================================

video = cv2.VideoCapture("new-gravits-video.mp4")

fps = video.get(cv2.CAP_PROP_FPS)

if fps <= 0:
    fps = 30

speed = 1.5

delay = int(1000 / (fps * speed))

video_label = tk.Label(
    root,
    bg="black"
)

# ==========================================
# PLAY VIDEO
# ==========================================

def play_video():

    ret, frame = video.read()

    if ret:

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frame = Image.fromarray(
            frame
        )

        frame = frame.resize(
            (1000, 700)
        )

        image = ImageTk.PhotoImage(
            frame
        )

        video_label.config(
            image=image
        )

        video_label.image = image

        root.after(
            delay,
            play_video
        )

    else:

        video.release()


# ==========================================
# DATA LIRIK
# ==========================================

# ==========================================
# DATA LIRIK
# ==========================================

lyrics = [

    {
        "text": "Mengejar bayangan kilau yang kau tinggalkan",
        "duration": 5300
    },

    {
        "text": "Sebagai memori yang takkan pergi",
        "duration": 6800
    },

    {
        "text": "Mimpi kan berganti dan takkan pernah berhenti",
        "duration": 6100
    },

    {
        "text": "Kan ku katakan sampai jumpa di lain hari",
        "duration": 8000
    }

]

# ==========================================
# WINDOW LIRIK
# ==========================================

lyric_window = None


def show_lyric(index):

    global lyric_window

    # Tutup window sebelumnya
    if lyric_window is not None:
        lyric_window.destroy()

    # ======================================
    # POSISI RANDOM
    # ======================================

    window_width = 600
    window_height = 250

    # Batas agar tidak terlalu dekat
    # dengan ujung layar
    margin_x = 180
    margin_y = 120

    x = random.randint(
        margin_x,
        screen_width - window_width - margin_x
    )

    y = random.randint(
        margin_y,
        screen_height - window_height - margin_y
    )

    # ======================================
    # WINDOW BARU
    # ======================================

    lyric_window = tk.Toplevel(root)

    lyric_window.title(
        f"memory_{index + 1}"
    )

    lyric_window.geometry(
        f"{window_width}x{window_height}+{x}+{y}"
    )

    lyric_window.configure(
        bg="#728ab4"
    )

    # Selalu di paling depan
    lyric_window.attributes(
        "-topmost",
        True
    )

    lyric_window.lift()

    jitter_lyric()

    add_jitter(
        lyric_window,
        x,
        y
    )

    # ======================================
    # LIRIK
    # ======================================

    text = tk.Label(
        lyric_window,

        text=lyrics[index]["text"],

        bg="#728ab4",

        fg="white",

        font=(
            "Comic Sans MS",
            24
        ),

        wraplength=540,

        justify="center"
    )

    text.pack(
        expand=True
    )

# ==========================================
# LYRIC JITTER
# ==========================================

def jitter_lyric():

    if lyric_window is not None:

        # Gerakan kecil dan patah-patah
        offset_x = random.choice(
            [-3, -2, -1, 0, 0, 0, 1, 2, 3]
        )

        offset_y = random.choice(
            [-2, -1, 0, 0, 0, 1, 2]
        )

        # Ambil posisi window sekarang
        current_x = lyric_window.winfo_x()
        current_y = lyric_window.winfo_y()

        lyric_window.geometry(
            f"+{current_x + offset_x}+{current_y + offset_y}"
        )

        # Ulangi setiap 80 ms
        root.after(
            80,
            jitter_lyric
        )

# ==========================================
# TIMELINE LIRIK
# ==========================================

def start_lyrics(index=0):

    if index < len(lyrics):

        show_lyric(index)

        duration = lyrics[index]["duration"]

        root.after(
            duration,
            lambda: start_lyrics(index + 1)
        )

    else:

        if lyric_window is not None:
            lyric_window.destroy()

# ==========================================
# CLOUD WINDOWS
# ==========================================

cloud_windows = []

# ==========================================
# GLOBAL JITTER
# ==========================================

jitter_windows = []


def add_jitter(window, x, y):

    jitter_windows.append(
        {
            "window": window,
            "x": x,
            "y": y
        }
    )


def move_jitter_windows():

    for item in jitter_windows:

        window = item["window"]

        try:

            offset_x = random.choice(
                [-3, -2, -1, 0, 0, 0, 1, 2, 3]
            )

            offset_y = random.choice(
                [-2, -1, 0, 0, 0, 1, 2]
            )

            new_x = item["x"] + offset_x
            new_y = item["y"] + offset_y

            window.geometry(
                f"+{new_x}+{new_y}"
            )

        except tk.TclError:
            pass

    root.after(
        80,
        move_jitter_windows
    )


def create_cloud(x, y):

    cloud_window = tk.Toplevel(root)

    cloud_window.title(
        "cloud"
    )

    cloud_window.geometry(
        f"500x180+{x}+{y}"
    )

    cloud_window.configure(
        bg="#728ab4"
    )

    # Cloud berada di atas window utama
    cloud_window.transient(root)


    # --------------------------------------
    # GAMBAR CLOUD
    # --------------------------------------

    try:

        image = Image.open(
            "images/cloud.png"
        )

        image.thumbnail(
            (330, 150)
        )

        photo = ImageTk.PhotoImage(
            image
        )

        cloud_label = tk.Label(
            cloud_window,

            image=photo,

            bg="#728ab4"
        )

        cloud_label.image = photo

        cloud_label.pack(
            expand=True
        )

    except Exception as error:

        print(
            "Gagal membuka cloud.png:",
            error
        )


    # Simpan posisi asli
    cloud_windows.append(
        {
            "window": cloud_window,
            "x": x,
            "y": y
        }
    )

    add_jitter(
        cloud_window,
        x,
        y
    )

# ==========================================
# CLOUD JITTER / DOODLE
# ==========================================

def move_clouds():

    for cloud in cloud_windows:

        window = cloud["window"]

        # Gerakan kecil dan patah-patah
        offset_x = random.choice(
            [-4, -3, -2, 0, 0, 0, 2, 3, 4]
        )

        offset_y = random.choice(
            [-3, -2, -1, 0, 0, 1, 2, 3]
        )

        new_x = (
            cloud["x"]
            + offset_x
        )

        new_y = (
            cloud["y"]
            + offset_y
        )

        window.geometry(
            f"+{new_x}+{new_y}"
        )


    # Ulangi setiap 100 ms
    root.after(
        100,
        move_clouds
    )


# ==========================================
# START PROGRAM
# ==========================================

def start_program():

    # Hapus tampilan awal
    title.destroy()
    start_button.destroy()


    # ======================================
    # TAMPILKAN VIDEO
    # ======================================

    video_label.pack(
        fill="both",
        expand=True
    )

    play_video()


    # ======================================
    # POSISI LAYAR
    # ======================================

    root.update_idletasks()

    video_x = root.winfo_x()
    video_y = root.winfo_y()


    # ======================================
    # DISC
    # ======================================

    create_disc()


    # ======================================
    # OBJECTS
    # ======================================

    # TAPE
    create_object(
        "images/tape.png",
        screen_width - 400 - 30,
        (screen_height // 2) + 250,
        width=400,
        height=220,
        image_width=360,
        image_height=190
    )

    # EARPHONE
    create_object(
        "images/earphone.png",
        20,
        (screen_height // 2) - 245,
        width=400,
        height=300,
        image_width=360,
        image_height=270
    )

    # CAM
    create_object(
        "images/cam.png",
        20,
        (screen_height // 2) + 155,
        width=400,
        height=300,
        image_width=360,
        image_height=270
    )

    # ======================================
    # CLOUD
    # ======================================

    cloud_width = 500
    cloud_height = 180


    # Cloud 1
    create_cloud(
        0,
        video_y - 230
    )


    # Cloud 2
    create_cloud(
        (screen_width // 2) - (cloud_width // 2),
        video_y - 230
    )


    # Cloud 3
    create_cloud(
        screen_width - cloud_width,
        video_y - 230
    )


    # Mulai efek jitter cloud
    move_clouds()

    move_jitter_windows()

    # ======================================
    # LIRIK
    # ======================================

    root.after(
        5000,
        start_lyrics
    )

# ==========================================
# DISC WINDOW
# ==========================================

def create_disc():

    disc_window = tk.Toplevel(root)

    disc_window.title("disc")

    # Ukuran window disc
    disc_width = 400
    disc_height = 400

    # Ukuran layar
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = screen_width - disc_width - 30

    # Posisi vertikal
    y = (screen_height - disc_height) // 2

    disc_window.geometry(
        f"{disc_width}x{disc_height}+{x}+{y}"
    )

    add_jitter(
        disc_window,
        x,
        y
    )

    disc_window.configure(
        bg="#728ab4"
    )

    # Tetap di atas window video
    disc_window.attributes(
        "-topmost",
        True
    )


    # ======================================
    # GAMBAR
    # ======================================

    try:

        image = Image.open(
            "images/disc.png"
        ).convert("RGBA")

        image = image.resize(
            (400, 400)
        )

        photo = ImageTk.PhotoImage(
            image
        )

        label = tk.Label(
            disc_window,

            image=photo,

            bg="#728ab4"
        )

        label.image = photo

        label.pack(
            fill="both",
            expand=True
        )


        # ==================================
        # ROTASI
        # ==================================

        def rotate():

            nonlocal image

            rotate.angle += 3

            if rotate.angle >= 360:
                rotate.angle = 0

            rotated = image.rotate(
                rotate.angle,
                resample=Image.Resampling.BICUBIC,
                expand=False
            )

            new_photo = ImageTk.PhotoImage(
                rotated
            )

            label.config(
                image=new_photo
            )

            label.image = new_photo

            root.after(
                30,
                rotate
            )


        rotate.angle = 0

        rotate()

    except Exception as error:

        print(
            "Gagal membuka disc.png:",
            error
        )

# ==========================================
# OBJECT WINDOWS
# ==========================================

object_windows = []

def create_object(
    image_path,
    x,
    y,
    width=250,
    height=180,
    image_width=230,
    image_height=150
):

    window = tk.Toplevel(root)

    window.title(
        "object"
    )

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )

    window.configure(
        bg="#728ab4"
    )

    window.attributes(
        "-topmost",
        True
    )

    try:

        image = Image.open(
            image_path
        )

        image.thumbnail(
            (image_width, image_height)
        )

        photo = ImageTk.PhotoImage(
            image
        )

        label = tk.Label(
            window,

            image=photo,

            bg="#728ab4"
        )

        label.image = photo

        label.pack(
            expand=True
        )

        object_windows.append(
            window
        )

        add_jitter(
            window,
            x,
            y
        )

    except Exception as error:

        print(
            "Gagal membuka:",
            image_path,
            error
        )

# ==========================================
# START SCREEN
# ==========================================

title = tk.Label(
    root,

    text="GRAVITS",

    font=(
        "Comic Sans MS",
        42,
        "bold"
    ),

    fg="white",

    bg="#728ab4"
)

title.pack(
    pady=220
)


start_button = tk.Button(
    root,

    text="START",

    font=(
        "Arial",
        16
    ),

    command=start_program,

    width=12,

    height=1
)

start_button.pack()


# ==========================================
# RUN
# ==========================================

root.mainloop()