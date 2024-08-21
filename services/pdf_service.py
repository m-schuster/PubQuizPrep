import os
from fpdf import FPDF
from PIL import Image

class PDFService:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_font(family="DejaVuSansCondensed", fname='resources/ttf/DejaVuSansCondensed.ttf')
        self.pdf.add_font(family="DejaVuSansCondensed", style="B", fname='resources/ttf/DejaVuSansCondensed-Bold.ttf')
        self.pdf.set_left_margin(10)
        self.pdf.set_right_margin(10)
        self.pdf.set_top_margin(10)
        self.pdf.set_text_shaping(True)

    def add_news(self, news):
        FONT = "DejaVuSansCondensed"
        FONT_STYLE = "B"
        FONT_SIZE_TITLE = 16
        FONT_SIZE_TEXT = 12

        self.pdf.add_page()
        self.pdf.set_font(FONT, style=FONT_STYLE, size=FONT_SIZE_TITLE)
        self.pdf.multi_cell(0, 10, f"News der vergangenen Woche:")
        self.pdf.ln(5)
        self.pdf.set_font(FONT, size=FONT_SIZE_TEXT)
        self.pdf.multi_cell(0, 10, news)

    def add_summary(self, day, month, summary):
        FONT = "DejaVuSansCondensed"
        FONT_STYLE = "B"
        FONT_SIZE_TITLE = 16
        FONT_SIZE_TEXT = 12

        self.pdf.add_page()
        self.pdf.set_font(FONT, style=FONT_STYLE, size=FONT_SIZE_TITLE)
        self.pdf.multi_cell(0, 10, f"Zusammenfassung des {day}. {month}:")
        self.pdf.ln(5)
        self.pdf.set_font(FONT, size=FONT_SIZE_TEXT)
        self.pdf.multi_cell(0, 10, summary)

    def add_images(self, images, image_topic):
        FONT = "DejaVuSansCondensed"
        FONT_STYLE = "B"
        FONT_SIZE_TITLE = 16
        FONT_SIZE_TEXT = 12

        IMAGE_WIDTH = 55
        IMAGE_HEIGHT = 65
        SPACING_X = 10
        SPACING_Y = 20
        MARGIN_X = 10
        MARGIN_Y = 20
        IMAGES_PER_PAGE = 9
        IMAGES_PER_ROW = 3

        def _get_image_ratio(img_path):
            try:
                with Image.open(img_path) as img:
                    img_size = img.size
                    img_ratio = img_size[0] / img_size[1]
                    return img_ratio
            except Exception as e:
                print(f"An error occurred while getting image ratio: {e}")
                return None

        self.pdf.add_page()
        self.pdf.set_font(FONT, style=FONT_STYLE, size=FONT_SIZE_TITLE)
        self.pdf.multi_cell(0, 10, f"Bilderrunde: {image_topic}")

        for index, (title, img_path) in enumerate(images):
            if index % IMAGES_PER_PAGE == 0 and index != 0:
                self.pdf.add_page()

            img_ratio = _get_image_ratio(img_path)

            img_width = IMAGE_WIDTH if img_ratio > 0.8 else 0
            img_height = IMAGE_HEIGHT if img_ratio <= 0.8 else 0

            x = MARGIN_X + (index % IMAGES_PER_ROW) * (IMAGE_WIDTH + SPACING_X)
            y = MARGIN_Y + ((index % IMAGES_PER_PAGE) // IMAGES_PER_ROW) * (IMAGE_HEIGHT + SPACING_Y + 10)  # 10 for title height

            self.pdf.set_xy(x, y)
            self.pdf.set_font(FONT, size=FONT_SIZE_TEXT)
            self.pdf.cell(IMAGE_WIDTH, 10, title, border=0, align='C')
            try:
                self.pdf.image(img_path, x, y + 10, w=img_width, h=img_height)
            except Exception as e:
                print(f"An error occurred while adding image to PDF: {e}")

    def add_music_round(self, music_theme, songs, playlist_url, qr_code):
        FONT = "DejaVuSansCondensed"
        FONT_STYLE = "B"
        FONT_SIZE_TITLE = 16
        FONT_SIZE_TEXT = 12

        self.pdf.add_page()
        self.pdf.set_font(FONT, style=FONT_STYLE, size=FONT_SIZE_TITLE)
        self.pdf.multi_cell(0, 10, f"Musikrunde: {music_theme}")
        self.pdf.ln(5)
        self.pdf.set_font(FONT, size=FONT_SIZE_TEXT)
        self.pdf.multi_cell(0, 10, songs)
        self.pdf.ln(10)
        self.pdf.cell(0, 10, playlist_url, border=0, align='C')
        self.pdf.ln(10)
        self.pdf.image(qr_code, x=(self.pdf.w - 80) / 2, w=80, h=80)

    def save_pdf(self, day, month):
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        file_path = os.path.join(output_dir, f"pub_quiz_{day}_{month}.pdf")
        self.pdf.output(file_path)