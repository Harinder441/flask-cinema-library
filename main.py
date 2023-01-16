from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from movieForm import AddMovie,RateMovie
from movieApi import get_movie_list,get_movie

db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies-collection.db"
db.init_app(app)
Bootstrap(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    review = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)

#to create model need to run only one time
with app.app_context():
    # db.create_all()
    pass

#home page list all movies ranked in desc order according to ratings given
@app.route("/")
def home():
    all_movies=Movie.query.order_by(Movie.rating.asc()).all()
    rank = len(all_movies)
    for movie in all_movies:
        movie.ranking = rank
        rank-=1

    db.session.commit()

    return render_template("index.html", movies=all_movies)

#add movies by searching title on moviedatabase api then selecting right movies to add
@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovie()
    if request.method == "POST":
        data = request.form

        movies = get_movie_list(query= data['title'])
        return render_template("select.html", movies=movies)
    return render_template("add.html", form=form)


@app.route("/add_movie")
def add_movie():
    id_ = int(request.args.get("id_"))
    data = get_movie(id_=id_)
    new_movie = Movie(
        id =id_,
        title= data['title'],
        year=int(data['release_date'][:4]),
        description=data['overview'],
        img_url='https://image.tmdb.org/t/p/w500'+data['backdrop_path'],
        rating= 0,
        ranking = 0,
        review = ' ',
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(app.url_for('update', id_=id_))


#delete perticularmovie by id
@app.route("/delete/<int:id_>")
def delete(id_):
    movie_to_delete = Movie.query.get(id_)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(app.url_for("home"))

# update rating and review of movie by id
@app.route("/update/<int:id_>", methods=["POST", "GET"])
def update(id_):
    movie_to_edit = Movie.query.get(id_)
    form = RateMovie()
    if request.method == "POST":
        movie_to_edit.rating = request.form['rating']
        if request.form['review']:
            movie_to_edit.review = request.form['review']
        db.session.commit()
        return redirect(app.url_for("home"))
    return render_template("edit.html",movie = movie_to_edit, form =form)



if __name__ == '__main__':
    app.run(debug=True)
