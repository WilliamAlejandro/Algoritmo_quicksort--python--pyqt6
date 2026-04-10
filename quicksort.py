import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLineEdit, QLabel, QListWidget, QMessageBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quicksort")
        self.setMinimumSize(600, 700)

        self.inicio()

    def inicio(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        distribucion = QVBoxLayout()

        self.etiqueta_entrada = QLabel("Ingrese numeros separados por coma:")
        distribucion.addWidget(self.etiqueta_entrada)

        self.caja_entrada = QLineEdit()
        self.caja_entrada.setPlaceholderText("Ej: 5, 2, 8, 1, 9")
        distribucion.addWidget(self.caja_entrada)

        self.boton_ordenar = QPushButton("Ordenar")
        self.boton_ordenar.clicked.connect(self.ordenar)
        distribucion.addWidget(self.boton_ordenar)

        fila_original = QHBoxLayout()
        self.etiqueta_original = QLabel("Lista original:")
        fila_original.addWidget(self.etiqueta_original)
        fila_original.addStretch()
        self.boton_copiar_original = QPushButton("Copiar")
        self.boton_copiar_original.setFixedWidth(60)
        self.boton_copiar_original.clicked.connect(self.copiar_original)
        fila_original.addWidget(self.boton_copiar_original)
        distribucion.addLayout(fila_original)

        self.lista_original = QListWidget()
        self.lista_original.setMaximumHeight(100)
        distribucion.addWidget(self.lista_original)

        fila_ordenada = QHBoxLayout()
        self.etiqueta_ordenada = QLabel("Lista ordenada:")
        fila_ordenada.addWidget(self.etiqueta_ordenada)
        fila_ordenada.addStretch()
        self.boton_copiar_ordenada = QPushButton("Copiar")
        self.boton_copiar_ordenada.setFixedWidth(60)
        self.boton_copiar_ordenada.clicked.connect(self.copiar_ordenada)
        fila_ordenada.addWidget(self.boton_copiar_ordenada)
        distribucion.addLayout(fila_ordenada)

        self.lista_ordenada = QListWidget()
        self.lista_ordenada.setMaximumHeight(100)
        distribucion.addWidget(self.lista_ordenada)

        self.etiqueta_grafico = QLabel("Grafico:")
        distribucion.addWidget(self.etiqueta_grafico)

        self.figura = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figura)
        distribucion.addWidget(self.canvas)

        widget_central.setLayout(distribucion)

    def quicksort(self, numeros):
        if len(numeros) <= 1:
            return numeros
        pivote = numeros[0]
        menores = [x for x in numeros[1:] if x <= pivote]
        mayores = [x for x in numeros[1:] if x > pivote]
        return self.quicksort(menores) + [pivote] + self.quicksort(mayores)

    def ordenar(self):
        texto = self.caja_entrada.text().strip()
        if not texto:
            QMessageBox.warning(self, "Error", "Ingrese numeros")
            return

        try:
            numeros = [int(x.strip()) for x in texto.split(",")]
        except ValueError:
            QMessageBox.warning(self, "Error", "Solo se permiten numeros enteros")
            return

        self.lista_original.clear()
        self.lista_ordenada.clear()

        for numero in numeros:
            self.lista_original.addItem(str(numero))

        resultado = self.quicksort(numeros)

        for numero in resultado:
            self.lista_ordenada.addItem(str(numero))

        self.mostrar_grafico(numeros, resultado)

    def mostrar_grafico(self, original, ordenada):
        self.figura.clear()

        eje_antes = self.figura.add_subplot(121)
        eje_despues = self.figura.add_subplot(122)

        colores_original = ["#3498db"] * len(original)
        colores_ordenada = ["#2ecc71"] * len(ordenada)

        eje_antes.bar(range(len(original)), original, color=colores_original)
        eje_antes.set_yscale('log')
        eje_antes.yaxis.set_visible(False)
        eje_antes.set_title("Antes")
        eje_antes.set_xticks(range(len(original)))
        eje_antes.set_xticklabels([str(n) for n in original], rotation=45, ha="right")

        eje_despues.bar(range(len(ordenada)), ordenada, color=colores_ordenada)
        eje_despues.set_yscale('log')
        eje_despues.yaxis.set_visible(False)
        eje_despues.set_title("Despues")
        eje_despues.set_xticks(range(len(ordenada)))
        eje_despues.set_xticklabels([str(n) for n in ordenada], rotation=45, ha="right")

        self.figura.tight_layout()
        self.canvas.draw()

    def copiar_original(self):
        items = [self.lista_original.item(i).text() for i in range(self.lista_original.count())]
        if not items:
            return
        texto = ", ".join(items)
        QApplication.clipboard().setText(texto)

    def copiar_ordenada(self):
        items = [self.lista_ordenada.item(i).text() for i in range(self.lista_ordenada.count())]
        if not items:
            return
        texto = ", ".join(items)
        QApplication.clipboard().setText(texto)


if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(aplicacion.exec())
