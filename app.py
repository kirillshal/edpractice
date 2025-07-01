import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import torch
import math


class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Processing App")

        # Проверка доступности PyTorch
        try:
            print(f"PyTorch version: {torch.__version__}")
            print(f"CUDA available: {torch.cuda.is_available()}")
        except Exception as e:
            messagebox.showerror("Error", f"PyTorch initialization error: {str(e)}")

        self.image = None
        self.original_image = None
        self.photo = None

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для кнопок загрузки
        load_frame = tk.Frame(self.root)
        load_frame.pack(pady=10)

        tk.Button(load_frame, text="Upload Image", command=self.upload_image).pack(side=tk.LEFT, padx=5)
        tk.Button(load_frame, text="Capture from Webcam", command=self.capture_from_webcam).pack(side=tk.LEFT, padx=5)

        # Фрейм для операций с изображением
        ops_frame = tk.Frame(self.root)
        ops_frame.pack(pady=10)

        # Каналы
        channel_frame = tk.Frame(ops_frame)
        channel_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(channel_frame, text="Color Channels:").pack()
        self.channel_var = tk.StringVar(value="red")
        tk.Radiobutton(channel_frame, text="Red", variable=self.channel_var, value="red").pack(anchor=tk.W)
        tk.Radiobutton(channel_frame, text="Green", variable=self.channel_var, value="green").pack(anchor=tk.W)
        tk.Radiobutton(channel_frame, text="Blue", variable=self.channel_var, value="blue").pack(anchor=tk.W)
        tk.Button(channel_frame, text="Show Channel", command=self.show_channel).pack(pady=5)

        # Обрезка
        crop_frame = tk.Frame(ops_frame)
        crop_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(crop_frame, text="Crop Image:").pack()
        tk.Button(crop_frame, text="Set Crop Area", command=self.set_crop_area).pack(pady=5)

        # Вращение
        rotate_frame = tk.Frame(ops_frame)
        rotate_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(rotate_frame, text="Rotate Image:").pack()
        tk.Button(rotate_frame, text="Rotate", command=self.rotate_image).pack(pady=5)

        # Рисование круга
        circle_frame = tk.Frame(ops_frame)
        circle_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(circle_frame, text="Draw Circle:").pack()
        tk.Button(circle_frame, text="Add Circle", command=self.draw_circle).pack(pady=5)

        # Кнопка сброса
        reset_frame = tk.Frame(self.root)
        reset_frame.pack(pady=10)
        tk.Button(reset_frame, text="Reset Image", command=self.reset_image).pack()

        # Canvas для отображения изображений
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])

        if not file_path:
            return

        try:
            self.image = cv2.imread(file_path)
            if self.image is None:
                raise ValueError("Failed to load image. Possibly unsupported format.")

            self.original_image = self.image.copy()
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(image_rgb)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def capture_from_webcam(self):
        try:
            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                raise RuntimeError("Unable to open webcam. Possible solutions:\n"
                                   "1. Check if webcam is connected properly\n"
                                   "2. Grant camera permissions to the application\n"
                                   "3. Try another USB port\n"
                                   "4. Restart the application")

            ret, frame = cap.read()
            cap.release()

            if not ret:
                raise RuntimeError("Failed to capture image from webcam")

            self.image = frame
            self.original_image = frame.copy()
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.display_image(image_rgb)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_image(self, image):
        image_pil = Image.fromarray(image)

        width, height = image_pil.size
        ratio = min(800 / width, 600 / height)
        new_size = (int(width * ratio), int(height * ratio))
        image_pil = image_pil.resize(new_size, Image.LANCZOS)

        self.photo = ImageTk.PhotoImage(image_pil)
        self.canvas.create_image(400, 300, image=self.photo)

    def show_channel(self):
        if self.image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return

        channel = self.channel_var.get()
        zeros = np.zeros_like(self.image[:, :, 0])

        if channel == "red":
            channel_image = cv2.merge([zeros, zeros, self.image[:, :, 2]])
        elif channel == "green":
            channel_image = cv2.merge([zeros, self.image[:, :, 1], zeros])
        elif channel == "blue":
            channel_image = cv2.merge([self.image[:, :, 0], zeros, zeros])
        else:
            raise ValueError("Invalid channel selected")

        channel_rgb = cv2.cvtColor(channel_image, cv2.COLOR_BGR2RGB)
        self.display_image(channel_rgb)

    def set_crop_area(self):
        if self.image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return

        try:
            x1 = simpledialog.askinteger("Crop", "Enter start X coordinate:", minvalue=0,
                                         maxvalue=self.image.shape[1] - 1)
            y1 = simpledialog.askinteger("Crop", "Enter start Y coordinate:", minvalue=0,
                                         maxvalue=self.image.shape[0] - 1)
            x2 = simpledialog.askinteger("Crop", "Enter end X coordinate:", minvalue=x1 + 1,
                                         maxvalue=self.image.shape[1])
            y2 = simpledialog.askinteger("Crop", "Enter end Y coordinate:", minvalue=y1 + 1,
                                         maxvalue=self.image.shape[0])

            if None in [x1, y1, x2, y2]:
                return

            self.image = self.image[y1:y2, x1:x2]
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(image_rgb)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to crop image: {str(e)}")

    def rotate_image(self):
        if self.image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return

        try:
            angle = simpledialog.askfloat("Rotate", "Enter rotation angle (degrees):")
            if angle is None:
                return

            (h, w) = self.image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            self.image = cv2.warpAffine(self.image, M, (w, h))

            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(image_rgb)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to rotate image: {str(e)}")

    def draw_circle(self):
        if self.image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return

        try:
            x = simpledialog.askinteger("Circle", "Enter center X coordinate:", minvalue=0,
                                        maxvalue=self.image.shape[1] - 1)
            y = simpledialog.askinteger("Circle", "Enter center Y coordinate:", minvalue=0,
                                        maxvalue=self.image.shape[0] - 1)
            radius = simpledialog.askinteger("Circle", "Enter radius:", minvalue=1,
                                             maxvalue=min(self.image.shape[0], self.image.shape[1]))

            if None in [x, y, radius]:
                return

            # Создаем копию изображения для рисования
            image_with_circle = self.image.copy()
            cv2.circle(image_with_circle, (x, y), radius, (0, 0, 255), 2)  # Красный круг

            image_rgb = cv2.cvtColor(image_with_circle, cv2.COLOR_BGR2RGB)
            self.display_image(image_rgb)

            # Обновляем основное изображение (без круга)
            self.image = image_with_circle.copy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to draw circle: {str(e)}")

    def reset_image(self):
        if self.original_image is not None:
            self.image = self.original_image.copy()
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(image_rgb)
        else:
            messagebox.showwarning("Warning", "No original image to reset to")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
