from flask import Flask, request, session, redirect, url_for, escape, render_template
from mailapi import db, app
import models


@app.route('/account/account/list', methods=['GET'])
def account_account_list():
    user_account, domain = get_current_account()

    if user_account is None or domain is None or user_account.rank_level != 1:
        return redirect(url_for('account_error_not_authorized'))

    return render_template('account_account_list.html', user_account=user_account, domain=domain)


@app.route('/account/account/create', methods=['POST'])
def account_account_create():
    user_account, domain = get_current_account()

    if user_account is None or domain is None or user_account.rank_level != 1:
        return redirect(url_for('account_error_not_authorized'))

    messages = []

    if 'account_name' not in request.form:
        messages.append('Kein Accountname angegeben')

    if 'account_password' not in request.form:
        messages.append('Kein Accountpasswort angegeben')

    if len(messages) > 0:
        return redirect(url_for('account_account_list', success=False, messages=messages))

    account = models.Account(domain=domain,
                             account_name=request.form['account_name'],
                             password_clear=request.form['account_password'],
                             rank=models.Rank.query.get(request.form['rank']))

    db.session.add(account)
    db.session.commit()

    return redirect(url_for('account_account_list', success=True))


@app.route('/account/account/delete/<int:account_id>', methods=['GET'])
def account_account_delete(account_id):
    user_account, domain = get_current_account()

    if user_account is None or domain is None or user_account.rank_level != 1:
        return redirect(url_for('account_error_not_authorized'))

    account = models.Account.query.filter(models.Account.id == account_id).first()

    if account.domain != domain or account.id == user_account.id:
        return redirect(url_for('account_error_not_authorized'))

    db.session.delete(account)
    db.session.commit()

    return redirect(url_for('account_account_list', success=True))


@app.route('/account/alias/list', methods=['GET'])
def account_alias_list():
    user_account, domain = get_current_account()

    if user_account is None or domain is None or user_account.rank_level != 1:
        return redirect(url_for('account_error_not_authorized'))

    return render_template('account_alias_list.html', user_account=user_account, domain=domain)


@app.route('/account/alias/create', methods=['POST'])
def account_alias_create():
    user_account, domain = get_current_account()

    if user_account is None or domain is None or user_account.rank_level != 1:
        return redirect(url_for('account_error_not_authorized'))

    messages = []

    if 'source' not in request.form and len(request.form['source']) == 0:
        messages.append('Kein Quelle angegeben')

    if 'destination' not in request.form and len(request.form['destination']) == 0:
        messages.append('Kein Ziel angegeben')

    if len(messages) > 0:
        return redirect(url_for('account_alias_list',
                                success=False,
                                messages=messages))

    alias = models.Alias(domain=domain,
                         source=request.form['source'],
                         destination=request.form['destination'])

    db.session.add(alias)
    db.session.commit()

    return redirect(url_for('account_alias_list', success=True))


@app.route('/account/alias/delete/<int:alias_id>', methods=['GET'])
def account_alias_delete(alias_id):
    user_account, domain = get_current_account()

    if user_account is None or domain is None or user_account.rank_level != 1:
        return redirect(url_for('account_error_not_authorized'))

    alias = models.Alias.query.filter(models.Alias.id == alias_id).first()

    if alias.domain != domain:
        return redirect(url_for('account_error_not_authorized'))

    db.session.delete(alias)
    db.session.commit()

    return redirect(url_for('account_alias_list', success=True))


@app.route('/account/error/not_authorized', methods=['GET'])
def account_error_not_authorized():
    user_account, domain = get_current_account()

    return render_template('account_error_not_authorized.html', user_account=user_account, domain=domain)


@app.route('/account/login', methods=['GET', 'POST'])
def account_login():
    if request.method == 'POST':

        email = request.form['email']

        valid, account_name, domain_name = get_account_domain_names(email)

        if valid:
            domain = models.Domain.query.filter(models.Domain.domain_name ==
                                                domain_name).first()

            account = models.Account.query.filter(models.Account.account_name ==
                                                  account_name and
                                                  models.Account.domain ==
                                                  domain).first()

        if account is not None and account.check_password(request.form['password']):
            session['email'] = request.form['email']
            session['is_admin'] = False
            return redirect(url_for('account_profile'))
        else:
            return redirect(url_for('index'))

    return render_template('account_login.html')


@app.route('/account/profile')
def account_profile():
    user_account, domain = get_current_account()

    if user_account is None or domain is None:
        return redirect(url_for('account_error_not_authorized'))

    return render_template('account_profile.html', user_account=user_account, domain=domain)


@app.route('/account/logout')
def account_logout():
    session.pop('email', None)
    return redirect(url_for('index'))


def get_current_account():
    if 'email' not in session:
        return redirect(url_for('index'))

    email = session['email']

    valid, account_name, domain_name = get_account_domain_names(email)

    if not valid:
        return redirect(url_for('index'))

    domain = models.Domain.query.filter(models.Domain.domain_name == domain_name).first()
    account = models.Account.query.filter(models.Account.account_name == account_name and
                                          models.Account.domain == domain).first()

    if account is None:
        return redirect(url_for('index'))

    return account, domain


def get_account_domain_names(email):
    if email.count('@') == 1:
        account_name, separator, domain_name = email.partition('@')

        return True, account_name, domain_name

    return False, None, None