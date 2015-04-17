from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# API Endpoints
@app.route('/api/v1.0/admins', methods=['GET'])
def api_v1_0_admins_index():
    pass


@app.route('/api/v1.0/admins/<int:admin_id>', methods=['GET'])
def api_v1_0_admins_view(admin_id):
    pass


@app.route('/api/v1.0/admins/<int:admin_id>/apikeys/', methods=['GET'])
def api_v1_0_admins_apikeys_view(admin_id):
    pass


@app.route('/api/v1.0/admins/<int:admin_id>/apikeys/<int:admin_apikey_id>', methods=['GET'])
def api_v1_0_admins_apikeys_view(admin_id, admin_apikey_id):
    pass


@app.route('/api/v1.0/domains', methods=['GET'])
def api_v1_0_domains_index():
    pass


@app.route('/api/v1.0/domains', methods=['POST'])
def api_v1_0_domains_create():
    pass


@app.route('/api/v1.0/domains/<int:domain_id>', methods=['POST'])
def api_v1_0_domains_create(domain_id):
    pass



if __name__ == '__main__':
    app.run()
