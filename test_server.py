from flask import Flask, render_template, request, send_file, send_from_directory
import os
import random
from deep_translator import GoogleTranslator
import openai
import urllib.request
import requests
import shutil
import pandas as pd
import csv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images"

@app.route('/')
def home():
    # return '<button onclick="window.location.href=\'/text_to_image\'">Go to image</button>'
    return render_template('index.html')

@app.route("/main_page",methods = ['GET','POST'])
def text_To_Image():
    global path_to_save
    global path_to_save1
    global path_to_save2
  #lấy text từ client 
   
    text = request.args.get('text')
    
    if text:
        #Dịch văn bản 
        print("start translate text to english")
        translated_text = GoogleTranslator(source='auto', target='en').translate(text)
        Style_list = [' ','A digital illustration of with clockwork machines, 4k, detailed, trending in artstation, fantasy vivid colors',
                '| anime oil painting high resolution cottagecore ghibli inspired 4k',
                'mid century modern, indoor garden with fountain, retro,m vintage, designer furniture made of wood and plastic, concrete table, wood walls, indoor potted tree, large window, outdoor forest landscape, beautiful sunset, cinematic, concept art, sunstainable architecture, octane render, utopia, ethereal, cinematic light, -ar 16:9 -stylize 45000',
                'futuristic nighttime cyberpunk skyline landscape vista photography by Carr Clifton & Galen Rowell, 16K resolution, Landscape veduta photo by Dustin Lefevre & tdraw, 8k resolution, detailed landscape painting by Ivan Shishkin, DeviantArt, Flickr, rendered in Enscape, Miyazaki, Nausicaa Ghibli, Breath of The Wild, 4k detailed post processing, atmospheric, hyper realistic, 8k, epic composition, cinematic, artstation —ar 16:9',
                'The Legend of Zelda landscape atmospheric, hyper realistic, 8k, epic composition, cinematic, octane render, artstation landscape vista photography by Carr Clifton & Galen Rowell, 16K resolution, Landscape veduta photo by Dustin Lefevre & tdraw, 8k resolution, detailed landscape painting by Ivan Shishkin, DeviantArt, Flickr, rendered in Enscape, Miyazaki, Nausicaa Ghibli, Breath of The Wild, 4k detailed post processing, artstation, rendering by octane, unreal engine ']

        if 'Style1' in text:
            text = text.replace('Style1', "")#xoá chuỗi Style trong chuỗi văn bản 
            styles = Style_list[1] #thay đổi chuỗi Style ở đây
        elif 'Style2' in text:
            text = text.replace('Style2', "")
            styles = Style_list[2] #thay đổi chuỗi Style ở đây
        elif 'Style3' in text:
            text = text.replace('Style3', "")
            styles = Style_list[3] #thay đổi chuỗi Style ở đây
        elif 'Style4' in text:
            text = text.replace('Style4', "")
            styles = Style_list[4] #thay đổi chuỗi Style ở đây
        elif 'Style5' in text:
            text = text.replace('Style5', "")
            styles = Style_list[5] #thay đổi chuỗi Style ở đây
        elif text in text:
            styles = ' ' 
        
        
        #gửi translated_text vào model và chạy
        text_t_img = f"{translated_text},{styles}"
        print(text_t_img)
        #Nhập key dalle e 
        openai.api_key = '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'
        openai.Model.list()
        # Chạy model 
        response = openai.Image.create(prompt=text_t_img, n = 3, size= "1024x1024")
        print(response)
        image_url = response['data'][0]['url'] 
        image_url1 = response['data'][1]['url']
        image_url2 = response['data'][2]['url']
        
        #lưu ảnh#  
        ## tạo một tên ảnh ngẫu nhiên 
        sample_string = 'qwertyuiopasdfghj'
        random_name = ''.join((random.choice(sample_string)) for x in range(len(sample_string)))
        random_name1 = ''.join((random.choice(sample_string)) for x in range(len(sample_string)))
        random_name2 = ''.join((random.choice(sample_string)) for x in range(len(sample_string)))
        img_name = f"img_{random_name}.png"
        img_name1 = f"img_{random_name1}.png"
        img_name2 = f"img_{random_name2}.png"
        #tạo đường dẫn để lưu ảnh 
        path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        path_to_save1 = os.path.join(app.config['UPLOAD_FOLDER'], img_name1)
        path_to_save2 = os.path.join(app.config['UPLOAD_FOLDER'], img_name2)
        print(path_to_save) 
        print(path_to_save1)
        print(path_to_save2) 
        #lưu ảnh 
        urllib.request.urlretrieve(image_url,path_to_save)
        urllib.request.urlretrieve(image_url1,path_to_save1)
        urllib.request.urlretrieve(image_url2,path_to_save2)
        
        #lưu dữ liệu promt vào data theo mỗi tên ảnh
        with open('data/prompt_data.csv', 'a', newline='') as csvfile:
        # Create a CSV writer object
            writer = csv.writer(csvfile)

            # Write the data rows
            writer.writerow([img_name, translated_text])
            writer.writerow([img_name1, translated_text])
            writer.writerow([img_name2, translated_text])
            #lấy tên ảnh đã lưu
        # image_path = "img01.png"
        print("have text")
        return render_template("main_page.html", user_image = f'images/{img_name}', user_image1 = f'images/{img_name1}',
                            user_image2 = f'images/{img_name2}')
    else:
        return render_template("main_page.html")
    
@app.route('/download1')
def download_img1():
    img1 = path_to_save
    return send_file(img1,as_attachment=True)

@app.route('/download2')
def download_img2():
    img1 = path_to_save1
    return send_file(img1,as_attachment=True)

@app.route('/download3')
def download_img3():
    img1 = path_to_save2
    return send_file(img1,as_attachment=True)

@app.route('/addBM', methods=['POST'])
def get_img_bookmarks():
    # Lấy đường dẫn của hình ảnh từ request body
    image_path = request.form['image_path']
    print(image_path,"type:",type(image_path))
    n = 25
    image_name = image_path[-n:]
    print(image_name)

    # Tải hình ảnh từ đường dẫn
    response = requests.get(image_path, stream=True)
    # Mở file để ghi hình ảnh vào
    with open(f'Bookmarks/{image_name}', 'wb') as out_file:
        # Copy hình ảnh từ response vào file
        shutil.copyfileobj(response.raw, out_file)

    return 'Đã copy hình ảnh vào thư mục Bookmarks'


@app.route('/Bookmarks/<path:path>')
def send_image(path):
    return send_from_directory('Bookmarks', path)

@app.route('/bookmarks')
def show_bookmarks():
    #đọc file CSV xuất ra data
    df = pd.read_csv('data/prompt_data.csv')

    # chuyển data sang dạng mảng numpy
    array = df.values

    # lấy danh sách tên các file ảnh có trong thư mục bookmarks
    images = os.listdir('Bookmarks')

    return render_template('bookmarks.html', images=images, array = array)

@app.route('/static/images/<path:path>')
def send_image2(path):

    return send_from_directory('static/images', path)

@app.route('/images')
def show_images():
    #đọc file CSV xuất ra data
    df = pd.read_csv('data/prompt_data.csv')

    # chuyển data sang dạng mảng numpy
    array = df.values

    # lấy danh sách tên các file ảnh có trong thư mục bookmarks
    images = os.listdir('static/images')
    return render_template('images.html', images= images, array = array)


@app.route('/ranking')
def ranking():
    return render_template('ranking.html')

# @app.route('/bookmarks')
# def bookmarks():
#     return render_template('bookmarks.html')

@app.route('/Help&FAQ')
def Help_FAQ():
    return render_template('help&faq.html')




#start server 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 9999, debug = True)
