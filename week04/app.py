from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


# 주문 정보 DB에 저장하기
@app.route('/order', methods=['POST'])
def write_order():
    # 주문 정보 변수 생성
    name = request.form['name']
    qty = request.form['qty']
    address = request.form['address']
    phone = request.form['phone']

    # db에 저장하기
    db.myshoporder.insert_one({
        'name': name,
        'qty': qty,
        'address': address,
        'phone': phone
    })

    return jsonify({'result': 'success'})


# 주문자 리스트 화면에 보여주기
@app.route('/order', methods=['GET'])
def read_order():
    orders = list(db.myshoporder.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
