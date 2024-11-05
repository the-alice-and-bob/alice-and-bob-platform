import decouple
import sentry_sdk

from flask import Flask, request, jsonify

from alicebob.celery_app import app_celery

sentry_sdk.init(
    dsn=decouple.config('SENTRY_DSN'),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)


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


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
