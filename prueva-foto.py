import tkinter as tk
from tkinter import filedialog
import google.generativeai as genai

# Configura tu clave API de Gemini
API_KEY = 'AIzaSyAhRae2tesr51ZghpECc5AqU4bZon9cuQg'
genai.configure(api_key=API_KEY)

class GeminiImageAnalyzer:
    def __init__(self, master):
        self.master = master
        master.title("Analizador de Imágenes con Gemini")
        
        # Botón para cargar imagen
        self.upload_btn = tk.Button(master, text="Subir Imagen", command=self.upload_image)
        self.upload_btn.pack(pady=20)
        
        # Área de texto para mostrar resultados
        self.result_text = tk.Text(master, height=15, width=50)
        self.result_text.pack(pady=10)
        
        # Modelo Gemini
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def upload_image(self):
        # Abrir selector de archivos
        file_path = filedialog.askopenfilename(
            filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            try:
                # Limpiar resultado anterior
                self.result_text.delete(1.0, tk.END)
                
                # Subir y analizar imagen
                uploaded_file = genai.upload_file(file_path)
                response = self.model.generate_content([
                    "Describe en detalle lo que ves en esta imagen.", 
                    uploaded_file
                ])
                
                # Mostrar resultado
                self.result_text.insert(tk.END, response.text)
            
            except Exception as e:
                self.result_text.insert(tk.END, f"Error: {str(e)}")

# Crear ventana
root = tk.Tk()
root.geometry("400x500")
app = GeminiImageAnalyzer(root)
root.mainloop()