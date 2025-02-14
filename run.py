import os
from app import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Usa el puerto de Railway o 5000 por defecto
    app.run(host="0.0.0.0", port=port, debug=True)
