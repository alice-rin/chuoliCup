import configparser
import time
import os
from flask import Flask, render_template, request, jsonify
import pandas as pd

from Chromosome import *
from ScenarioGenerator import *

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def parse_txt_to_dataframe(file_path):
    try:
        # 尝试不同分隔符
        separators = [',', '\t', ';', '|', ' ']
        for sep in separators:
            try:
                # 读取前100行检测分隔符和结构
                df = pd.read_csv(file_path, sep=sep, nrows=100, encoding='utf-8')

                # 如果成功读取且列数大于1
                if len(df.columns) > 1:
                    # 读取全文
                    full_df = pd.read_csv(file_path, sep=sep, encoding='utf-8')
                    return full_df
            except Exception:
                continue
        # 如果无法识别分隔符,按行读取
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # 创建简单的DataFrame
        df = pd.DataFrame({'原始内容': lines})
        return df

    except Exception as e:
        return pd.DataFrame({'错误': [str(e)]})


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '未选择文件'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    # 保存文件
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    # 解析文件
    df = parse_txt_to_dataframe(filename)
    df['序号'] = range(1, len(df) + 1)
    cols = df.columns.tolist()
    cols = ['序号'] + [col for col in cols if col != '序号']
    df = df[cols]

    # 转换为HTML表格
    table_html = df.to_html(
        classes='table table-striped table-bordered table-hover',
        justify='center',
        index=False
    )

    data = {
        'filename': filename,
        'table_html': table_html,
        'headers': df.columns.tolist(),
        'rows': df.values.tolist(),
        'total_rows': len(df),
        'total_columns': len(df.columns)
    }

    return jsonify({'success': True, 'data': data})

if __name__ == "__main__":
    con = configparser.ConfigParser()
    con.read("./config.ini", encoding="utf-8")

    host_session = con.items("host")
    host_session_dict = dict(host_session)
    host_url = host_session_dict["host_url"]
    port = int(host_session_dict["port"])
    app.run(port=port, host=host_url, debug=True)

if __name__ == "__main__":
    start_time = time.time()

    temp_scenario_generator = ScenarioGenerator()
    temp_scenario_generator.createScenario()

    temp_chromosome = Chromosome(temp_scenario_generator.red_side_list, temp_scenario_generator.blue_side_list)
    temp_chromosome.generate_chromosome_random()
    temp_chromosome.print_chromosome()

    temp_evaluator = ChromosomeEvaluator(temp_chromosome)
    temp_evaluator.print_evaluate_result()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"耗时: {elapsed_time:.6f}秒")
    input("...")
