import configparser
import io
import time
import os
from urllib.parse import quote

from flask import Flask, render_template, request, jsonify, Response
from datetime import datetime

from GA_Algorithm import *
from ScenarioGenerator import *

app =  Flask(__name__)
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

    scenario_generator = ScenarioGenerator()
    scenario_generator.create_from_file(df)

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

@app.route('/calculate', methods=['GET'])
def fire_planning():
    start_time = time.time()
    scenario_generator = ScenarioGenerator()
    temp_ga_algorithm = GA_Algorithm()
    temp_ga_algorithm.setup(scenario_generator, 100, 100)
    temp_ga_algorithm.initialize_chromosome()
    temp_ga_algorithm.loop()

    best_chromosome = temp_ga_algorithm.best_chromosome

    temp_evaluator = temp_ga_algorithm.chromosome_evaluator
    temp_evaluator.setupChromosome(best_chromosome)
    temp_evaluator.evaluate()
    temp_evaluator.print_evaluate_result()

    end_time = time.time()
    elapsed_time = end_time - start_time

    df = best_chromosome.create_plan_df()
    data = {
        'total_damage': temp_evaluator.total_damage,
        'total_coat': temp_evaluator.total_cost,
        'total_time': format(temp_evaluator.total_time, '.2f'),
        'missile_num': temp_evaluator.total_missile_number,
        'headers': df.columns.tolist(),
        'rows': df.values.tolist(),
        'total_rows': len(df),
        'cal_time': elapsed_time
    }
    return jsonify({'success': True, 'data': data})

@app.route('/export', methods=['GET'])
def export_csv():
    """导出CSV文件接口"""
    plan_data = None
    try:
        ga_algorithm = GA_Algorithm()
        best_chromosome = ga_algorithm.best_chromosome
        plan_data = best_chromosome.create_plan_df()

        if plan_data is None or plan_data.empty:
            return jsonify({
                'success': False,
                'message': '没有可导出的计算结果，请先完成计算'
            }), 400

        output = io.StringIO()
        plan_data.to_csv(output, index=False, encoding='utf-8')
        csv_data = output.getvalue()
        output.close()

        # 创建响应对象
        response = Response(
            csv_data,
            mimetype='text/csv; charset=utf-8',
        )
        filename = "火力规划方案_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
        encoded_filename = quote(filename, safe='')  # 对文件名进行URL编码
        rfc5987_filename = f"UTF-8''{encoded_filename}"
        response.headers['Content-Disposition'] = f"attachment; filename*=utf-8''{rfc5987_filename}"

        return response

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'导出失败: {str(e)}'
        }), 500

if __name__ == "__main__":
    con = configparser.ConfigParser()
    con.read("./config.ini", encoding="utf-8")

    host_session = con.items("host")
    host_session_dict = dict(host_session)
    host_url = host_session_dict["host_url"]
    port = int(host_session_dict["port"])
    app.run(port=port, host=host_url, debug=True)
