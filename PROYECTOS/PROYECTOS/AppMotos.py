import sys, os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QScrollArea,
    QGridLayout, QFrame, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox, QDialog,
    QLineEdit, QTextEdit
)
from PySide6.QtGui import QPixmap, QPalette, QBrush, QFont
from PySide6.QtCore import Qt

MOTOS = {
    "Deportivas": [
        ("Yamaha R6", "Alta velocidad, diseño aerodinámico", "deportivas1.jpg", "Motor: 600cc\nPeso: 190kg\nConsumo: 17km/l"),
        ("Kawasaki ZX-6R", "Potencia en pista", "deportivas2.jpg", "Motor: 636cc\nPeso: 196kg\nConsumo: 16km/l"),
        ("Suzuki GSX-R600", "Estilo racing", "deportivas3.jpg", "Motor: 599cc\nPeso: 187kg\nConsumo: 18km/l"),
        ("Honda CBR600RR", "Precisión y control", "deportivas4.jpg", "Motor: 599cc\nPeso: 186kg\nConsumo: 19km/l"),
        ("Ducati Panigale V2", "Diseño italiano, alto rendimiento", "deportivas5.jpg", "Motor: 955cc\nPeso: 200kg\nConsumo: 15km/l"),
    ],
    "Enduro": [
        ("KTM 250 EXC", "Ideal para terrenos complicados", "enduro1.jpg", "Motor: 250cc\nPeso: 103kg\nConsumo: 30km/l"),
        ("Yamaha WR250F", "Alta tracción, suspensión superior", "enduro2.jpg", "Motor: 250cc\nPeso: 115kg\nConsumo: 28km/l"),
        ("Honda CRF250L", "Versátil y ágil", "enduro3.jpg", "Motor: 250cc\nPeso: 144kg\nConsumo: 26km/l"),
        ("Husqvarna TE 300", "Perfecta para obstáculos", "enduro4.jpg", "Motor: 293cc\nPeso: 111kg\nConsumo: 27km/l"),
        ("Beta RR 250", "Enduro profesional", "enduro5.jpg", "Motor: 250cc\nPeso: 108kg\nConsumo: 29km/l"),
    ],
    "Urbanas": [
        ("Yamaha FZ 2.0", "Ligera, ideal para ciudad", "urbanas1.jpg", "Motor: 149cc\nPeso: 135kg\nConsumo: 40km/l"),
        ("Bajaj Pulsar NS200", "Popular y confiable", "urbanas2.jpg", "Motor: 199cc\nPeso: 152kg\nConsumo: 35km/l"),
        ("Honda CB125F", "Eficiencia en cada trayecto", "urbanas3.jpg", "Motor: 125cc\nPeso: 128kg\nConsumo: 45km/l"),
        ("TVS Apache RTR 160", "Moderna y compacta", "urbanas4.jpg", "Motor: 159cc\nPeso: 140kg\nConsumo: 38km/l"),
        ("Suzuki Gixxer 155", "Estilo deportivo urbano", "urbanas5.jpg", "Motor: 155cc\nPeso: 141kg\nConsumo: 42km/l"),
    ]
}
IMG_FOLDER = "img"

# -------------------- Carrito Manager --------------------
class CarritoManager:
    _carrito = []

    @classmethod
    def agregar(cls, producto):
        cls._carrito.append(producto)

    @classmethod
    def eliminar(cls, indice):
        cls._carrito.pop(indice)

    @classmethod
    def obtener(cls):
        return cls._carrito.copy()

    @classmethod
    def total(cls):
        return sum(p[1] for p in cls._carrito)

    @classmethod
    def vaciar(cls):
        cls._carrito.clear()

# -------------------- Formulario de Compra --------------------
class FormularioDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finalizar Compra")
        self.setFixedSize(350, 300)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Nombre completo:"))
        self.nombre = QLineEdit()
        layout.addWidget(self.nombre)

        layout.addWidget(QLabel("Correo electrónico:"))
        self.correo = QLineEdit()
        layout.addWidget(self.correo)

        layout.addWidget(QLabel("Dirección de entrega:"))
        self.direccion = QTextEdit()
        layout.addWidget(self.direccion)

        btn = QPushButton("Confirmar compra")
        btn.clicked.connect(self.confirmar)
        layout.addWidget(btn)

    def confirmar(self):
        if not self.nombre.text() or not self.correo.text() or not self.direccion.toPlainText():
            QMessageBox.warning(self, "Campos incompletos", "Por favor, complete todos los campos.")
            return
        QMessageBox.information(self, "Compra exitosa", "¡Gracias por tu compra!")
        CarritoManager.vaciar()
        self.accept()

# -------------------- Diálogo del Carrito --------------------
class CarritoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Carrito de Compras")
        self.setFixedSize(400, 400)

        self.layout = QVBoxLayout(self)
        self.actualizar_lista()

        btn_finalizar = QPushButton("Finalizar compra")
        btn_finalizar.clicked.connect(self.abrir_formulario)
        self.layout.addWidget(btn_finalizar)

    def actualizar_lista(self):
        for i in reversed(range(self.layout.count() - 1)):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        carrito = CarritoManager.obtener()
        for i, (nombre, precio) in enumerate(carrito):
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(f"{nombre} - ${precio:,}"))
            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.clicked.connect(lambda _, idx=i: self.eliminar_producto(idx))
            hbox.addWidget(btn_eliminar)
            frame = QWidget()
            frame.setLayout(hbox)
            self.layout.insertWidget(i, frame)

        total_lbl = QLabel(f"<b>Total: ${CarritoManager.total():,}</b>")
        total_lbl.setAlignment(Qt.AlignRight)
        self.layout.insertWidget(self.layout.count() - 1, total_lbl)

    def eliminar_producto(self, index):
        CarritoManager.eliminar(index)
        self.actualizar_lista()

    def abrir_formulario(self):
        form = FormularioDialog()
        form.exec()
        self.actualizar_lista()

# -------------------- Ventana de Detalle --------------------
class VentanaDetalle(QDialog):
    def __init__(self, nombre, descripcion, imagen, ficha, precio, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Detalle: {nombre}")
        self.setFixedSize(500, 600)
        self.setModal(True)
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout(self)

        lbl_nombre = QLabel(nombre)
        lbl_nombre.setFont(QFont("", 14, QFont.Bold))
        lbl_nombre.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_nombre)

        lbl_precio = QLabel(f"<span style='color: green; font-size: 14pt;'>${precio:,}</span>")
        lbl_precio.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_precio)

        lbl_img = QLabel()
        ruta = os.path.join(IMG_FOLDER, imagen)
        if os.path.exists(ruta):
            pix = QPixmap(ruta).scaled(400, 240, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            lbl_img.setPixmap(pix)
        else:
            lbl_img.setText("Imagen no disponible")
            lbl_img.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_img)

        layout.addWidget(QLabel(descripcion))

        layout.addWidget(QLabel("<b>Ficha técnica:</b>"))
        layout.addWidget(QLabel(ficha))

        btn_agregar = QPushButton("Agregar al carrito")
        btn_agregar.clicked.connect(lambda: self.agregar_al_carrito(nombre, precio))
        layout.addWidget(btn_agregar, alignment=Qt.AlignCenter)

    def agregar_al_carrito(self, nombre, precio):
        CarritoManager.agregar((nombre, precio))
        QMessageBox.information(self, "Agregado", f"{nombre} ha sido agregado al carrito.")

# -------------------- Card de Producto --------------------
class CardProducto(QFrame):
    def __init__(self, nombre, descripcion, imagen, ficha):
        super().__init__()
        self.setObjectName("card")
        self.setFixedSize(220, 400)
        self.setStyleSheet("QFrame#card { border: 1px solid #ccc; border-radius: 8px; background: white; }")
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(8,8,8,8)
        vbox.setSpacing(6)

        img_label = QLabel()
        ruta = os.path.join(IMG_FOLDER, imagen)
        if os.path.exists(ruta):
            pix = QPixmap(ruta).scaled(200,120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            img_label.setPixmap(pix)
        else:
            img_label.setText("No Image")
            img_label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(img_label)

        precio = self.obtener_precio(nombre)

        name = QLabel(f"<b>{nombre}</b>")
        name.setFont(QFont("", 10))
        name.setAlignment(Qt.AlignCenter)

        precio_lbl = QLabel(f"<span style='color: green; font-size: 12pt;'>${precio:,}</span>")
        precio_lbl.setAlignment(Qt.AlignCenter)

        vbox.addWidget(name)
        vbox.addWidget(precio_lbl)
        vbox.addWidget(QLabel("<b>Ficha técnica:</b>"))
        ficha_lbl = QLabel(ficha)
        ficha_lbl.setWordWrap(True)
        vbox.addWidget(ficha_lbl)

        btn_detalle = QPushButton("Ver detalle")
        btn_detalle.clicked.connect(self.mostrar_detalle)
        vbox.addWidget(btn_detalle, alignment=Qt.AlignCenter)

        btn_agregar = QPushButton("Agregar al carrito")
        btn_agregar.clicked.connect(lambda: self.agregar_al_carrito(nombre, precio))
        vbox.addWidget(btn_agregar, alignment=Qt.AlignCenter)

        self._data = (nombre, descripcion, imagen, ficha, precio)

    def obtener_precio(self, nombre):
        precios = {
            "Yamaha R6": 54000000,
            "Kawasaki ZX-6R": 58000000,
            "Suzuki GSX-R600": 53000000,
            "Honda CBR600RR": 55000000,
            "Ducati Panigale V2": 72000000,
            "KTM 250 EXC": 48000000,
            "Yamaha WR250F": 46000000,
            "Honda CRF250L": 42000000,
            "Husqvarna TE 300": 50000000,
            "Beta RR 250": 47000000,
            "Yamaha FZ 2.0": 9500000,
            "Bajaj Pulsar NS200": 8700000,
            "Honda CB125F": 7300000,
            "TVS Apache RTR 160": 8200000,
            "Suzuki Gixxer 155": 9100000,
        }
        return precios.get(nombre, 0)

    def mostrar_detalle(self):
        nombre, descripcion, imagen, ficha, precio = self._data
        dialog = VentanaDetalle(nombre, descripcion, imagen, ficha, precio, parent=self.window())
        dialog.exec()

    def agregar_al_carrito(self, nombre, precio):
        CarritoManager.agregar((nombre, precio))
        QMessageBox.information(self, "Agregado", f"{nombre} ha sido agregado al carrito.")

# -------------------- Catálogo --------------------
class CatalogoWidget(QScrollArea):
    def __init__(self, categoria):
        super().__init__()
        self.setWidgetResizable(True)
        content = QWidget()
        self.setWidget(content)

        grid = QGridLayout(content)
        grid.setSpacing(15)
        productos = MOTOS.get(categoria, [])
        for idx, (n,d,img,f) in enumerate(productos):
            row, col = divmod(idx, 2)
            grid.addWidget(CardProducto(n,d,img,f), row, col)

# -------------------- Ventana Principal --------------------
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Motos - Catálogo")
        self.setFixedSize(600,600)

        top = QWidget()
        hbox = QHBoxLayout(top)
        self.combo = QComboBox()
        self.combo.addItems(list(MOTOS.keys()))
        btn = QPushButton("Cargar")
        btn.clicked.connect(self.cargar_catalogo)
        hbox.addWidget(QLabel("Categoría:"))
        hbox.addWidget(self.combo)
        hbox.addWidget(btn)

        btn_carrito = QPushButton("Ver Carrito")
        btn_carrito.clicked.connect(self.abrir_carrito)
        hbox.addWidget(btn_carrito)

        hbox.addStretch()

        self.central = QWidget()
        vmain = QVBoxLayout(self.central)
        vmain.addWidget(top)
        self.setCentralWidget(self.central)

        self.cargar_catalogo()

    def cargar_catalogo(self):
        if self.central.layout().count() > 1:
            old = self.central.layout().itemAt(1).widget()
            self.central.layout().removeWidget(old)
            old.deleteLater()
        cat = CatalogoWidget(self.combo.currentText())
        self.central.layout().addWidget(cat)

    def abrir_carrito(self):
        carrito = CarritoDialog()
        carrito.exec()

# -------------------- Pantalla de Inicio --------------------
class Inicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenido")
        self.setFixedSize(600,600)

        self.setAutoFillBackground(True)
        fondo = QPixmap("fondo.jpg")
        if not fondo.isNull():
            pal = self.palette()
            pal.setBrush(QPalette.Window, QBrush(fondo.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            self.setPalette(pal)

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(QLabel("Bienvenido al catálogo de Motos", alignment=Qt.AlignCenter))
        btn = QPushButton("Entrar")
        btn.setFixedSize(100,40)
        btn.clicked.connect(self.abrir_app)
        vbox.addSpacing(20)
        vbox.addWidget(btn, alignment=Qt.AlignCenter)

    def abrir_app(self):
        self.main = VentanaPrincipal()
        self.main.show()
        self.close()

# -------------------- Ejecución --------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    inicio = Inicio()
    inicio.show()
    sys.exit(app.exec())
