from flask import Flask, request, session, redirect, url_for, escape, render_template
from mailapi import db, app
import models


@app.route('/admin/dashboard')
def admin_dashboard():
    admin = get_current_admin()

    return render_template('admin_dashboard.html', admin=admin)


@app.route('/admin/apikey/list')
def admin_apikey_list():
    admin = get_current_admin()

    if admin is None:
        return redirect(url_for('index'))

    return render_template('admin_apikey_list.html', admin=admin)


@app.route('/admin/apikey/create', methods=['POST'])
def admin_apikey_create():
    admin = get_current_admin()

    if admin is None:
        return redirect(url_for('index'))

    description = None

    if 'description' in request.form:
        description = request.form['description']

    apikey = models.AdminApikey(admin.id, description)
    db.session.add(apikey)
    db.session.commit()

    return redirect(url_for('admin_apikey_list'))


@app.route('/admin/domain/list')
def admin_domain_list():
    admin = get_current_admin()

    domains = models.Domain.query.all()

    return render_template('admin_domain_list.html', admin=admin, domains=domains)


@app.route('/admin/domain/create', methods=['POST'])
def admin_domain_create():
    admin = get_current_admin()

    messages = []

    if 'domain_name' not in request.form:
        messages.append('Kein Domainname angegeben')

    if 'account_name' not in request.form:
        messages.append('Kein Accountname angegeben')

    if 'account_password' not in request.form:
        messages.append('Kein Accountpasswort angegeben')

    if len(messages) > 0:
        return redirect(url_for('admin_domain_list', success=False, messages=messages))

    domain = models.Domain(domain_name=request.form['domain_name'],
                           admin=admin)

    account = models.Account(domain=domain,
                             account_name=request.form['account_name'],
                             password_clear=request.form['account_password'],
                             rank=models.Rank.query.get(1))

    db.session.add(account)
    db.session.commit()

    return redirect(url_for('admin_domain_list', success=True))


@app.route('/admin/domain/<int:domain_id>', methods=['GET'])
def admin_domain_view(domain_id):
    admin = get_current_admin()

    domain = models.Domain.query.get(domain_id)

    view = 'accounts'
    if 'view' in request.values:
        view = request.values['view']

    return render_template('admin_domain_view.html', admin=admin, domain=domain, view=view)


@app.route('/admin/domain/<int:domain_id>/account/create', methods=['POST'])
def admin_account_create(domain_id):
    admin = get_current_admin()
    domain = models.Domain.query.get(domain_id)

    messages = []

    if 'account_name' not in request.form:
        messages.append('Kein Accountname angegeben')

    if 'account_password' not in request.form:
        messages.append('Kein Accountpasswort angegeben')

    if len(messages) > 0:
        return redirect(url_for('admin_domain_view', domain_id=domain_id, success=False, messages=messages))

    account = models.Account(domain=domain,
                             account_name=request.form['account_name'],
                             password_clear=request.form['account_password'],
                             rank=models.Rank.query.get(request.form['rank']))

    db.session.add(account)
    db.session.commit()

    return redirect(url_for('admin_domain_view', domain_id=domain_id, success=True))


@app.route('/admin/domain/<int:domain_id>/alias/create', methods=['POST'])
def admin_alias_create(domain_id):
    admin = get_current_admin()
    domain = models.Domain.query.get(domain_id)

    messages = []

    if 'source' not in request.form and len(request.form['source']) == 0:
        messages.append('Kein Quelle angegeben')

    if 'destination' not in request.form and len(request.form['destination']) == 0:
        messages.append('Kein Ziel angegeben')

    if len(messages) > 0:
        return redirect(url_for('admin_domain_view',
                                domain_id=domain_id,
                                success=False,
                                messages=messages,
                                view='aliases'))

    alias = models.Alias(domain=domain,
                         source=request.form['source'],
                         destination=request.form['destination'])

    db.session.add(alias)
    db.session.commit()

    return redirect(url_for('admin_domain_view', domain_id=domain_id, success=True, view='aliases'))


@app.route('/admin/admin/list')
def admin_admin_list():
    admin = get_current_admin()

    admins = models.Admin.query.all()

    return render_template('admin_admin_list.html', admin=admin, admins=admins)


@app.route('/admin/admin/create', methods=['POST'])
def admin_admin_create():
    admin = get_current_admin()

    messages = []

    if 'username' not in request.form and len(request.form['username']) == 0:
        messages.append('Kein Benutzername angegeben')

    if 'password' not in request.form and len(request.form['password']) == 0:
        messages.append('Kein Passwort angegeben')

    if len(messages) > 0:
        return redirect(url_for('admin_admin_list',
                                success=False,
                                messages=messages))

    new_admin = models.Admin(username=request.form['username'],
                             password_clear=request.form['password'])

    db.session.add(new_admin)
    db.session.commit()

    return redirect(url_for('admin_admin_list', success=True))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin = models.Admin.query.filter(models.Admin.username ==
                                          request.form['username']).first()

        if admin is not None and admin.check_password(request.form['password']):
            session['username'] = request.form['username']
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('index'))

    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('username', None)
    return redirect(url_for('index'))


def get_current_admin():
    if 'username' not in session:
        return redirect(url_for('index'))

    admin = models.Admin.query.filter(models.Admin.username == session['username']).first()

    if admin is None:
        return redirect(url_for('index'))

    return admin

