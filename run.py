import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # listen on all interfaces so container ports are exposed
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
