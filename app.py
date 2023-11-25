from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/course_registration'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    grade = db.Column(db.Integer, nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    instructor = db.Column(db.String(255), nullable=False)
    credits = db.Column(db.Integer, nullable=False)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrollment_date = db.Column(db.TIMESTAMP, nullable=False)
    grade = db.Column(db.Integer)

# 创建数据库表
db.create_all()

# 选课
@app.route('/enroll', methods=['POST'])
def enroll():
    data = request.get_json()

    student_id = data.get('student_id')
    course_id = data.get('course_id')

    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()

    return jsonify({'message': 'Enrollment successful'})

# 取消选课
@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()

    student_id = data.get('student_id')
    course_id = data.get('course_id')

    enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()

    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
        return jsonify({'message': 'Withdrawal successful'})
    else:
        return jsonify({'message': 'Enrollment not found'})

# 修改选课
@app.route('/modify_enrollment', methods=['POST'])
def modify_enrollment():
    data = request.get_json()

    student_id = data.get('student_id')
    course_id = data.get('course_id')
    new_grade = data.get('new_grade')

    enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()

    if enrollment:
        enrollment.grade = new_grade
        db.session.commit()
        return jsonify({'message': 'Enrollment modified successfully'})
    else:
        return jsonify({'message': 'Enrollment not found'})

# 查询选课
@app.route('/view_enrollment', methods=['GET'])
def view_enrollment():
    student_id = request.args.get('student_id')
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()

    enrollment_list = [{'course_id': e.course_id, 'grade': e.grade} for e in enrollments]

    return jsonify({'enrollments': enrollment_list})

if __name__ == '__main__':
    app.run(debug=True)