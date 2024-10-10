from flask import Flask, jsonify, request
from multiprocessing import Pool, cpu_count
import time

app = Flask(__name__)

current_pi = 3.0

def calculate_pi_part(start, steps, num_processes):
    pi_part = 0.0
    for i in range(start, steps, num_processes):
        pi_part += (-1)**i / (2*i + 1)
    return pi_part * 4

def run_pi_calculation(cpu_percentage):
    global current_pi
    total_steps = 1000000
    num_cpus = cpu_count()
    pool_size = num_cpus if cpu_percentage == 100 else num_cpus // 2

    with Pool(processes=pool_size) as pool:
        results = pool.starmap(calculate_pi_part, [(i, total_steps, pool_size) for i in range(pool_size)])
        current_pi = sum(results)

@app.route('/calculate-pi', methods=['GET'])
def calculate_pi():
    duration = int(request.args.get('duration'))
    cpu_percentage = int(request.args.get('cpu'))

    run_pi_calculation(cpu_percentage)

    return jsonify({"pi": current_pi})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
