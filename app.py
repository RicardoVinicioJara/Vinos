from flask import Flask, render_template, request

app = Flask(__name__)


def calcular_similitud_jaccard(valores_vino):

    def calculo_similitud(calidad, set_valores_vino):
        return {
            'calidad': calidad,
            'similitud': len(set_valores_vino.intersection(valores_vino)) /
                         len(set_valores_vino.union(valores_vino))
        }

    lista_calculada = []
    with open("winequality-red.csv", "r") as f:
        valores_vino_data = f.readline()
        while valores_vino_data:
            valores_vino_data = f.readline()
            propiedades_vino = valores_vino_data.split(";")
            calidad = propiedades_vino[-1:][0].replace("\n", "")
            lista_calculada.append(calculo_similitud(calidad, set(map(float, propiedades_vino[:-1]))))
    # Retorna las similitudes y su calidad
    return sorted(lista_calculada, key=lambda item: item['similitud'], reverse=True)


@app.route('/calcular', methods=['POST'])
def calcular_calidad():
    valores_vino = list(map(float, request.form.values()))
    return render_template("index.html", valores=valores_vino, lista=calcular_similitud_jaccard(valores_vino))


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.debug = True
    app.run()