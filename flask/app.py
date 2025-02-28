from flask import Flask, jsonify
from flask_cors import CORS
from connect import create_app  # 导入封装的 create_app()

app = create_app()
CORS(app)  # 允许 Vue 访问


if __name__ == '__main__':
    app.run(debug=True, port=5000)
