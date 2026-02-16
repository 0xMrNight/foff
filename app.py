import io
import base64
from flask import Flask, render_template, request, redirect, url_for
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import os
import models
import simulation

app = Flask(__name__)
models.init_db()

@app.route("/")
def home():
    students = models.get_all_students()
    return render_template("home.html", students=students)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            models.add_student(
                request.form["name"],
                request.form["roll"],
                int(request.form["sleep_start"]),
                int(request.form["sleep_end"]),
                round(simulation.random.uniform(0.85, 1.2), 2)
            )
            return redirect(url_for('home'))
        except Exception as e:
            return f"Error: {e}"
    return render_template("register.html")

@app.route("/graph/<roll>")
def graph(roll):
    student = models.get_student_by_roll(roll)
    if not student: return "Student not found", 404

    # 1. Prepare Data
    _, name, _, capacity, s_start, s_end = student
    hours, scores = [], []
    for h in range(24):
        val = simulation.calculate_attention(h, capacity, s_start, s_end)
        if val is not None:
            hours.append(h)
            scores.append(val)

    plt.style.use('dark_background') # Makes the plot match the UI
    plt.figure(figsize=(10, 5), facecolor='#1e293b') 
    ax = plt.gca()
    ax.set_facecolor('#1e293b')

    plt.plot(hours, scores, marker='o', color='#38bdf8', linewidth=3, markersize=8, markerfacecolor='#ffffff')
    plt.fill_between(hours, scores, color='#38bdf8', alpha=0.2)

    # Grid and Spines styling
    ax.grid(color='#334155', linestyle='--', alpha=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor('#475569')

    plt.plot(hours, scores, marker='o', color='#007bff', linewidth=2)
    plt.fill_between(hours, scores, color='#007bff', alpha=0.1)
    plt.title(f"Attention Analytics: {name}")
    plt.xlabel("Hour of Day")
    plt.ylabel("Attention %")
    plt.ylim(0, 105)
    plt.grid(True, linestyle='--', alpha=0.6)

    # 3. Save to a Buffer (Memory) instead of Disk
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    
    # 4. Encode as Base64 string
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close() # Always close the figure to free memory

    return render_template("graph.html", name=name, plot_url=plot_data)

if __name__ == "__main__":
    app.run(debug=True)