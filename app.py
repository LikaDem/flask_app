from flask import Flask, render_template, request, redirect, url_for, jsonify
import os, json

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('hello.html')

upload_folder = 'static'
app.config['upload_folder'] = upload_folder

image_database =[]

@app.route('/upload_pics', methods=['GET', 'POST'])
def upload_pics():
    if request.method == 'POST':
        file = request.files.get("file")
        title = request.form.get('title')
        if file and title:
            filename = file.filename
            filepath = os.path.join(app.config['upload_folder'], filename)
            file.save(filepath)

            image_id = len(image_database) + 1
            image_data = {
                'filename': filename,
                'id': image_id,
                'title': title
            }
            image_database.append(image_data)

            response_json = json.dumps({'task': image_data}, ensure_ascii=False)
            return app.response_class(response_json, content_type='application/json')
        
        
    return render_template('upload.html')

@app.route('/pics', methods=['GET'])
def all_pics():
    response_data = {'database': image_database}
    response_json = json.dumps(response_data, ensure_ascii=False)
    return app.response_class(response_json, content_type='application/json')

@app.route('/pics/<int:pic_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_pic_by_id(pic_id):
    image = next((item for item in image_database if item['id'] == pic_id), None)
    if image is None:
        response_json = json.dumps({'error': 'Id not found'}, ensure_ascii=False)
        return app.response_class(response_json, content_type='application/json'), 404

    if request.method == 'PUT':
        new_data = request.form.get('new_data')
        if new_data:
            image['title'] = new_data
            response_json = json.dumps({'message': 'Image updated', 'updated_data': image}, ensure_ascii=False)
            return app.response_class(response_json, content_type='application/json')
        else:
            response_json = json.dumps({'error': 'No new data provided'}, ensure_ascii=False)
            return app.response_class(response_json, content_type='application/json'), 400

    if request.method == 'DELETE':
        image_database.remove(image)
        response_json = json.dumps({'message': 'Image deleted'}, ensure_ascii=False)
        return app.response_class(response_json, content_type='application/json')

    response_json = json.dumps(image, ensure_ascii=False)
    return app.response_class(response_json, content_type='application/json')

if __name__ == '__main__':
    app.run(debug=True)

