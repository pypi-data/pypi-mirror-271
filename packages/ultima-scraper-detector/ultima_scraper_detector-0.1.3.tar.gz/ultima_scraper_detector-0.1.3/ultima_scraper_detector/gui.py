import mimetypes
import tkinter as tk
from pathlib import Path
from tkinter import NW, Canvas
from typing import Any

from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage


class Gui:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Image Viewer")

        canvas = Canvas(self.root, width=512, height=512)
        canvas.pack()
        self.canvas = canvas
        # self.root.mainloop()

    def image_to_canvas(self, tk_image: PhotoImage):
        # Convert image coordinates to canvas coordinates
        canvas_x = self.canvas.winfo_reqwidth()
        canvas_y = self.canvas.winfo_reqheight()
        scale_x = canvas_x / tk_image.width()
        scale_y = canvas_y / tk_image.height()
        return scale_x, scale_y

    def load_image(self, image_path: Path):
        photo_image = None
        mimetype = mimetypes.guess_type(image_path)[0]
        try:
            assert mimetype
        except Exception as _e:
            return photo_image
        if mimetype.startswith("image"):
            image = Image.open(image_path)
            photo_image = ImageTk.PhotoImage(image)
        return photo_image

    def resize_image(self, image_path: Path):
        image = Image.open(image_path)
        assert self.canvas
        canvas_w = self.canvas.winfo_reqwidth()
        canvas_h = self.canvas.winfo_reqheight()
        resized_image = image.resize((canvas_w, canvas_h), Image.Resampling.LANCZOS)
        new_image = ImageTk.PhotoImage(resized_image)
        return new_image

    def update_image(self, image_path: Path, details: list[dict[str, Any]]):
        tk_image = self.load_image(image_path)
        if not tk_image:
            return
        canvas = self.canvas
        resized_image = self.resize_image(image_path)
        assert self.canvas
        self.canvas.create_image(0, 0, anchor=NW, image=resized_image)  # type:ignore

        for detail in details:
            # Extract information from the details
            label = detail["class"]
            score = detail["score"]
            box = detail["box"]

            canvas_width = self.canvas.winfo_reqwidth()
            canvas_height = self.canvas.winfo_reqheight()
            image_width = tk_image.width()
            image_height = tk_image.height()
            x1, y1, width, height = box
            # Scale the coordinates based on the canvas size
            x1_scaled = (x1 / image_width) * canvas_width
            y1_scaled = (y1 / image_height) * canvas_height
            width_scaled = (width / image_width) * canvas_width
            height_scaled = (height / image_height) * canvas_height

            x2_scaled = x1_scaled + width_scaled
            y2_scaled = y1_scaled + height_scaled

            # Draw the rectangle
            canvas.create_rectangle(
                x1_scaled, y1_scaled, x2_scaled, y2_scaled, outline="red"
            )

            label_text = f"{label} ({score:.2f})"
            self.canvas.create_text(
                x1_scaled - 20,
                y1_scaled - 20,
                anchor=NW,
                text=label_text,
                fill="blue",
                font="ArialBold.ttf",
            )
        self.root.update_idletasks()
