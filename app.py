from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy.exc import IntegrityError

from sql_alchemy import banco


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class HotelModel (banco.Model):
    __tablename__ = 'hoteis'
    hotel_id = banco.Column(banco.Integer, primary_key=True, autoincrement=True)
    nome = banco.Column(banco.String(80), nullable=False)
    estrela = banco.Column(banco.String(4), nullable=False)
    diaria = banco.Column(banco.String(10), nullable=False)
    cidade = banco.Column(banco.String(80), nullable=False)
    endereco = banco.Column(banco.String(100), nullable=False)
    numero = banco.Column(banco.Integer, nullable=False)
    cnpj = banco.Column(banco.String(18), unique=True)

    def __init__(self, nome, estrela, diaria, cidade, endereco, numero, cnpj):
        self.nome = nome
        self.estrela = estrela
        self.diaria = diaria
        self.cidade = cidade
        self.endereco = endereco
        self.numero = numero
        self.cnpj = cnpj

@app.route("/")
def init():
    return render_template("index.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")


@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        estrela = request.form.get("estrela")
        diaria = request.form.get("diaria")
        cidade = request.form.get("cidade")
        endereco = request.form.get("endereco")
        numero = request.form.get("numero")
        cnpj = request.form.get("cnpj")
        try:
            if nome and estrela and diaria and cidade and endereco and numero and cnpj:
                hotel = HotelModel(nome, estrela, diaria, cidade, endereco, numero, cnpj)
                banco.session.add(hotel)
                banco.session.commit()
            return redirect(url_for("index"))
        except IntegrityError:
            banco.session.rollback()
            return render_template('cadastro.html', mensagem='o CNPJ já esta cadastrado')



@app.route("/lista")
def lista():
    hotel = HotelModel.query.all()
    return render_template("lista.html", hotel=hotel)


@app.route("/excluir/<int:id>")
def excluir(id):
    hotels = HotelModel.query.filter_by(hotel_id=id).first()

    banco.session.delete(hotels)
    banco.session.commit()
    try:
        hotel = HotelModel.query.all()
        return render_template("lista.html", hotel=hotel)
    except:

        return {"Message": "tivemos um problema para excluir o hotel"}


@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    hotel = HotelModel.query.filter_by(hotel_id=id).first()

    if request.method == "POST":
        nome = request.form.get("nome")
        estrela = request.form.get("estrela")
        diaria = request.form.get("diaria")
        cidade = request.form.get("cidade")
        endereco = request.form.get("endereco")
        numero = request.form.get("numero")

        if nome and estrela and diaria and cidade and endereco and numero:
            hotel.nome = nome
            hotel.estrela = estrela
            hotel.diaria = diaria
            hotel.cidade = cidade
            hotel.endereco = endereco
            hotel.numero = numero

            banco.session.commit()
            return redirect(url_for("lista"))
    return render_template("atualizar.html", hotel=hotel)


@app.before_first_request
def cria_banco():
   banco.create_all()


if __name__ == '__main__':
    banco.init_app(app)
    app.run(debug=True)
