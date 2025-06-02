def get_stats_data(conn):
    cursor = conn.cursor()

    # Số lượng user
    cursor.execute('SELECT COUNT(*) FROM user_info')
    total_users = cursor.fetchone()[0]

    # Số lượng user được predict
    cursor.execute('SELECT COUNT(DISTINCT uid) FROM user_predict')
    predicted_users = cursor.fetchone()[0]

    # Tỉ lệ user được predict trên tổng user
    predict_rate = round((predicted_users / total_users) * 100, 2) if total_users else 0

    # Số lượng course (bảng course_info hoặc course_resource tùy bảng bạn dùng)
    cursor.execute('SELECT COUNT(DISTINCT cid) FROM course_resource')
    total_courses = cursor.fetchone()[0]

    # Số lượng comment
    cursor.execute('SELECT COUNT(*) FROM user_comment')
    total_comments = cursor.fetchone()[0]

    # Số lượng problem
    cursor.execute('SELECT COUNT(*) FROM exercise_problem')
    total_problems = cursor.fetchone()[0]

    # user_predict distribution
    cursor.execute('SELECT predict, COUNT(*) FROM user_predict GROUP BY predict')
    label_data = cursor.fetchall()
    labels = [str(row[0]) for row in label_data]
    label_counts = [row[1] for row in label_data]

    cursor.close()

    return {
        "total_users": total_users,
        "predicted_users": predicted_users,
        "predict_rate": predict_rate,
        "total_courses": total_courses,
        "total_comments": total_comments,
        "total_problems": total_problems,
        "labels": labels,
        "label_counts": label_counts,
    }
