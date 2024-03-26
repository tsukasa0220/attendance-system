import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import AttendanceDB, NameDB

# 学籍番号から名前探す関数
def number_to_name(data, namedb):
    for column in namedb:
        if data["number"] == column.number:
            return column.name, column.grade
    return f"不明なユーザ[{data["number"]}]", ""

# JSONファイル開く
with open('/app/data.json', 'r') as json_file:
    json_datas = json.load(json_file)

# SQLiteデータベースに接続
engine2 = create_engine('sqlite:///name.db')
engine1 = create_engine('sqlite:///attendance.db')

# SQLAlchemyセッションを作成
Session1 = sessionmaker(bind=engine1)
session1 = Session1()
Session2 = sessionmaker(bind=engine2)
session2 = Session2()

# NameDBからデータを取得
namedb = session2.query(NameDB).all()

# 学籍番号から名前と学年を探す関数
for json_data in json_datas:

    # myInfo = {名前, 学年}
    myInfo = number_to_name(json_data, namedb)

    # 文字列型から日時型に変換
    date_object = datetime.strptime(json_data["timestamp"], "%Y-%m-%d %H:%M:%S")

    # AttendanceDBに保存するための型を用意
    attendance = AttendanceDB(number=json_data["number"], name=myInfo[0], grade=myInfo[1], date=date_object)

    # AttendanceDBに追加(※ステージング)
    session1.add(attendance)

# 変更内容をデータベースに反映
session1.commit()

# セッションを閉じる
session1.close()
session2.close()