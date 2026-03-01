from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():

    age = int(request.form['age'])
    weight = float(request.form['weight'])
    height = float(request.form['height']) / 100

    leafy = int(request.form['leafy'])
    fruits = int(request.form['fruits'])
    milk = int(request.form['milk'])
    eggs = int(request.form['eggs'])
    meat = int(request.form['meat'])
    pulses = int(request.form['pulses'])
    junk = int(request.form['junk'])
    sunlight = int(request.form['sunlight'])

    bmi = round(weight / (height ** 2), 2)

    iron_score = (leafy * 2) + (meat * 3) + (pulses * 2)
    iron_risk = "High" if iron_score < 10 else "Moderate" if iron_score < 18 else "Low"

    protein_score = (eggs * 2) + (meat * 3) + (pulses * 2) + (milk * 1.5)
    protein_risk = "High" if protein_score < 12 else "Moderate" if protein_score < 20 else "Low"

    calcium_risk = "High" if milk < 3 else "Low"
    vitamin_d_risk = "High" if sunlight < 15 else "Low"
    b12_risk = "High" if eggs == 0 and meat == 0 and milk == 0 else "Low"

    overall_score = min(100, int((iron_score + protein_score) * 2))

    return render_template(
        'result.html',
        bmi=bmi,
        iron=iron_risk,
        protein=protein_risk,
        calcium=calcium_risk,
        vitamin_d=vitamin_d_risk,
        b12=b12_risk,
        overall=overall_score
    )

if __name__ == '__main__':
    app.run(debug=True)