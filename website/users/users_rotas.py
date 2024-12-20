# user_routes.py
# aqui estão as rotas de um usuário comum (Não admin)
# esse usuário comum só tem acesso a home, detalhes e busca

from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from website import db, app
from website.adm.models import SPI

#pagina inicial de usuario
@app.route('/')
def home():
    per_page = 10
    page = request.args.get('page', type=int, default=1)
    specialissues = SPI.query.order_by(SPI.prazo.asc()).paginate(page=page, per_page=per_page)
    return render_template('users/users_home.html', title='Home para Usuários', specialissues=specialissues)

#detalhes das si 
@app.route('/detalhes/<int:id>', methods=['GET'])
def users_detalhes(id):
    
    spi = SPI.query.get(id)
    if spi:
        return render_template('users/users_detalhes.html', spi=spi, title='Detalhes da Special Issue')
    else:
        flash('Special Issue não encontrado', 'danger')
        return redirect(url_for('user.home'))

#busca de user
@app.route('/search', methods=['GET', 'POST'])
def users_search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search-box']
        session['search_value'] = search_value  # Armazena na sessão
        search = f"%{search_value}%"
        
        #a consulta para inclui tanto título quanto descrição -> like
        specialissues = SPI.query.filter(
            SPI.titulo.like(search) | SPI.detalhes.like(search)
        ).paginate(page=1, per_page=20)
        
        return render_template('users/users_busca.html', specialissues=specialissues, search_value=search_value)
    
    else:
        page = request.args.get('page', 1, type=int)
        per_page = 20

        search_value = session.get('search_value', '')  # Obtém da sessão
        if page == 1 and search_value:
            specialissues = SPI.query.filter(
                SPI.titulo.like(f"%{search_value}%") | SPI.detalhes.like(f"%{search_value}%")
            ).paginate(page=1, per_page=20)
        else:
            specialissues = SPI.query.paginate(page=page, per_page=per_page)

    return render_template('users/users_busca.html', specialissues=specialissues, search_value=search_value)
