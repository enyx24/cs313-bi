from flask import Blueprint, render_template, abort, request
from connectDB import connect_mysql

course_bp = Blueprint('course', __name__)
conn = connect_mysql()

@course_bp.route('/course/<cid>')
def course_detail(cid):
    try:
        cid_num = int(cid)
    except ValueError:
        abort(404)

    cursor = conn.cursor(dictionary=True)
    course = f"C_{cid_num}"

    # Danh sách người dùng
    cursor.execute("""
        SELECT u.uid, u.name 
        FROM user_course uc
        INNER JOIN user_info u ON u.uid = uc.uid
        WHERE uc.cid = %s
    """, (cid_num,))
    users = cursor.fetchall()

    # Lấy predict nếu có người dùng
    uid_list = [user['uid'] for user in users]
    predict_map = {}
    if uid_list:
        placeholders = ','.join(['%s'] * len(uid_list))
        cursor.execute(f"""
            SELECT uid, predict FROM user_predict
            WHERE uid IN ({placeholders})
        """, uid_list)
        predictions = cursor.fetchall()
        predict_map = {row['uid']: row['predict'] for row in predictions}
    # print(f"Predict map: {predict_map}")

    # Thêm predict vào từng user
    for user in users:
        user['predict'] = predict_map.get(user['uid'])

    # Lọc theo filter
    filter_val = request.args.get('filter')
    if filter_val:
        users = [u for u in users if u.get('predict') == int(filter_val)]
    print(f"Filtered users: {users}")
    print("filter_val:", filter_val)  

    count_predict = {0: 0, 1: 0, 2: 0, 'none': 0}
    for u in users:
        if u.get('predict') is None:
            count_predict['none'] += 1
        else:
            count_predict[int(u['predict'])] += 1

    return render_template(
        "course_detail.html",
        course=course,
        users=users,
        filter_val=filter_val,
        count_predict=count_predict
    )
