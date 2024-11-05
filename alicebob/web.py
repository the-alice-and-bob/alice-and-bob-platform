import decouple

from flask import Flask, request, jsonify

from alicebob.celery_app import app_celery

app = Flask(__name__)
app.config['SECRET_TOKEN'] = "ec752ee9a72048bba515a5304935e5cd206eada27e984596b82d18fa8489f5ec"
app.config['URL_TOKEN'] = decouple.config('URL_TOKEN')
app.config['DEBUG'] = decouple.config('DEBUG', default=False, cast=bool)


@app.route('/webhooks', methods=['POST'])
def webhooks():
    # Get Query Params
    token = request.args.get('token')

    if token != app.config['URL_TOKEN']:
        return jsonify({"error": "Invalid token"}), 401

    # Checks if the request is JSON
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.json

    app_celery.send_task('inoreader_distributor', args=(data,))

    return jsonify({"message": "Success"})


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
