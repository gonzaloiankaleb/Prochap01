import os
import customtkinter as ctk
from tkinter import messagebox, filedialog
import re
import webbrowser
from fpdf import FPDF
from PyPDF2 import PdfMerger
from urllib.parse import quote

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def validar_correo(correo):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(patron, correo)

def seleccionar_imagen():
    return filedialog.askopenfilename(title="Selecciona la imagen de la placa", 
                                      filetypes=[("Archivos de imagen", "*.jpg *.png")])

def seleccionar_pdf():
    return filedialog.askopenfilename(title="Selecciona el PDF del proveedor", 
                                      filetypes=[("Archivos PDF", "*.pdf")])

def generar_pdf_chapa(ruta_imagen, ruta_pdf, ruta_guardado):
    try:
        if not ruta_imagen or not ruta_pdf or not os.path.exists(ruta_imagen) or not os.path.exists(ruta_pdf):
            raise FileNotFoundError("Archivos de imagen o PDF no encontrados.")

        pdf = FPDF()
        pdf.add_page()
        pdf.image(ruta_imagen, x=10, y=8, w=190)

        pdf.add_page()
        pdf.output(ruta_guardado)

        merger = PdfMerger()
        merger.append(ruta_guardado)
        merger.append(ruta_pdf)
        merger.write(ruta_guardado)
        merger.close()

        messagebox.showinfo("PDF Generado", f"PDF generado: {ruta_guardado}")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el PDF: {str(e)}")
        return False

def abrir_cliente_correo(destinatario, ruta_pdf):
    try:
        if not os.path.exists(ruta_pdf):
            raise FileNotFoundError("El archivo PDF no existe.")

        # Asunto y cuerpo del correo
        asunto = quote("Especificación de la placa")
        cuerpo = quote("Estimado cliente,\nAdjunto encontrará el archivo PDF con la especificación de la placa junto con la especificación del proveedoren formato PDF.")

        # Preparar el enlace mailto con la estructura
        mailto_link = f"mailto:{destinatario}?subject={asunto}&body={cuerpo}"

        # Abrir el cliente de correo predeterminado con el archivo adjunto
        webbrowser.open(mailto_link)

        messagebox.showinfo("Cliente de correo abierto", "El cliente de correo predeterminado se ha abierto con la información precargada.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el cliente de correo: {str(e)}")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Prochap")
        self.geometry("500x500")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)

        self.label_correo = ctk.CTkLabel(self.frame, text="Correo del Cliente:")
        self.label_correo.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.entrada_correo = ctk.CTkEntry(self.frame)
        self.entrada_correo.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.ruta_imagen = ctk.StringVar()
        self.ruta_pdf = ctk.StringVar()

        self.imagen_cargada = ctk.BooleanVar(value=False)
        self.pdf_cargado = ctk.BooleanVar(value=False)

        self.btn_seleccionar_imagen = ctk.CTkButton(self.frame, text="Seleccionar Imagen", command=self.seleccionar_imagen_wrapper)
        self.btn_seleccionar_imagen.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.check_imagen = ctk.CTkCheckBox(self.frame, text="Imagen cargada", variable=self.imagen_cargada, state="disabled")
        self.check_imagen.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        self.btn_seleccionar_pdf = ctk.CTkButton(self.frame, text="Seleccionar PDF", command=self.seleccionar_pdf_wrapper)
        self.btn_seleccionar_pdf.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.check_pdf = ctk.CTkCheckBox(self.frame, text="PDF cargado", variable=self.pdf_cargado, state="disabled")
        self.check_pdf.grid(row=5, column=0, padx=20, pady=10, sticky="w")

        self.btn_generar = ctk.CTkButton(self.frame, text="Generar PDF", command=self.generar_pdf)
        self.btn_generar.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        self.btn_enviar = ctk.CTkButton(self.frame, text="Abrir correo con PDF", command=self.abrir_correo)
        self.btn_enviar.grid(row=7, column=0, padx=20, pady=10, sticky="ew")

    def seleccionar_imagen_wrapper(self):
        ruta = seleccionar_imagen()
        if ruta:
            self.ruta_imagen.set(ruta)
            self.imagen_cargada.set(True)

    def seleccionar_pdf_wrapper(self):
        ruta = seleccionar_pdf()
        if ruta:
            self.ruta_pdf.set(ruta)
            self.pdf_cargado.set(True)

    def generar_pdf(self):
        if not self.ruta_imagen.get() or not self.ruta_pdf.get():
            messagebox.showerror("Error", "Por favor, selecciona tanto la imagen como el PDF.")
            return
        
        ruta_guardado = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                                     filetypes=[("PDF files", "*.pdf")], 
                                                     title="Guardar PDF como")
        if ruta_guardado:
            if generar_pdf_chapa(self.ruta_imagen.get(), self.ruta_pdf.get(), ruta_guardado):
                self.pdf_cargado.set(True)
                self.ruta_pdf.set(ruta_guardado)

    def abrir_correo(self):
        correo = self.entrada_correo.get().strip()
        if not correo:
            messagebox.showerror("Error", "Por favor, ingrese un correo electrónico.")
            return
        if not validar_correo(correo):
            messagebox.showerror("Error", "Por favor, ingrese un correo electrónico válido.")
            return
        abrir_cliente_correo(correo, self.ruta_pdf.get())

if __name__ == "__main__":
    app = App()
    app.mainloop()
