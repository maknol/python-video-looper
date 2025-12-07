import os
import random
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.FadeIn import FadeIn
from moviepy.video.fx.FadeOut import FadeOut
from moviepy.video.fx.Resize import Resize
from moviepy.video.fx.Loop import Loop

# === НАСТРОЙКИ ===
video_folder = r"H:\_Daytona\Нова папка"        # 📁 Папка с видеата
logo_path = r"C:\Users\tutra\Desktop\D6.png"     # 🖼️ Път към PNG логото
transition_duration = 1.5                        # ⏳ Продължителност на преходите (секунди)
logo_position = 'top-right'                      # 📌 Позиция: top-left, top-right, bottom-left, bottom-right
logo_scale = 0.15                                # 🔍 Размер на логото спрямо ширината
target_resolution = (1920, 1080)                 # 🖥️ Изходна резолюция

# === ПОЗИЦИЯ НА ЛОГОТО ===
def get_logo_position(clip, logo_clip, position):
    margin = 10
    if position == 'top-left':
        return (margin, margin)
    elif position == 'top-right':
        return (clip.w - logo_clip.w - margin, margin)
    elif position == 'bottom-left':
        return (margin, clip.h - logo_clip.h - margin)
    elif position == 'bottom-right':
        return (clip.w - logo_clip.w - margin, clip.h - logo_clip.h - margin)
    else:
        return ('center', 'center')

# === ПРОВЕРКА НА ПАПКАТА ===
if not os.path.exists(video_folder):
    print(f"❌ Папката не съществува: {video_folder}")
    exit()

# === ЗАРЕЖДАНЕ НА ВИДЕО ФАЙЛОВЕТЕ ===
video_files = [
    os.path.join(video_folder, f)
    for f in os.listdir(video_folder)
    if f.lower().endswith(('.mp4', '.mov', '.avi'))
]

if not video_files:
    print("❌ Няма видео файлове в папката.")
    exit()

random.shuffle(video_files)  # 🎲 Случаен ред

# === ЛОГО ===
logo = ImageClip(logo_path)

# === ГЕНЕРИРАНЕ НА КЛИПОВЕТЕ ===
final_clips = []
start_time = 0

for video_path in video_files:
    clip = VideoFileClip(video_path, audio=False)

    # 📏 Скалиране до 1920x1080
    clip = Resize(new_size=target_resolution).apply(clip)

    # ⬇️ Преходи
    clip = FadeIn(duration=transition_duration).apply(clip)
    clip = FadeOut(duration=transition_duration).apply(clip)

    # 🖼️ Добавяне на логото
    logo_resized = Resize(width=clip.w * logo_scale).apply(logo)
    logo_pos = get_logo_position(clip, logo_resized, logo_position)
    logo_clip = logo_resized.with_position(logo_pos).with_duration(clip.duration)

    # 🎬 Обединяване на видео + лого
    composed = CompositeVideoClip([clip, logo_clip], size=target_resolution).with_duration(clip.duration)

    # 🕒 Добавяне на стартово време
    composed = composed.with_start(start_time)
    start_time += clip.duration

    final_clips.append(composed)

# === ОБЕДИНЯВАНЕ НА ВСИЧКИ КЛИПОВЕ ===
full_slideshow = CompositeVideoClip(final_clips, size=target_resolution).with_duration(start_time)

# === ВЪЗПРОИЗВЕЖДАНЕ В БЕЗКРАЕН ЦИКЪЛ ===
print("▶️ Стартиране на безкрайно слайдшоу...")

while True:
    full_slideshow.preview(fps=30)
