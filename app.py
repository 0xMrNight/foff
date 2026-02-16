import io
import base64
from flask import Flask, render_template, request, redirect, url_for
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import os
import models
import simulation
from datetime import datetime


app = Flask(__name__)
models.init_db()

@app.route("/")
def home():
    all_data = models.get_all_student_details()
    current_hour = datetime.now().hour
    leaderboard = []

    for name, roll, cap, s_start, s_end in all_data:
        score = simulation.calculate_attention(current_hour, cap, s_start, s_end)
        # If score is None, student is sleeping (0 focus)
        focus_val = score if score is not None else 0
        leaderboard.append({
            'name': name,
            'roll': roll,
            'score': focus_val,
            'is_sleeping': score is None
        })

    # Sort by score descending
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
    
    # We still need the basic list for the main table
    students = models.get_all_students()
    
    return render_template("home.html", students=students, leaderboard=leaderboard[:5], hour=current_hour)

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
    # 1. Fetch data from DB
    student = models.get_student_by_roll(roll)
    if not student:
        return "Student not found", 404

    # Unpack DB record (id, name, roll, capacity, sleep_start, sleep_end)
    _, name, _, capacity, s_start, s_end = student
    
    # 2. Generate simulation data and find the peak
    hours, scores = [], []
    best_hour = None
    max_score = -1

    for h in range(24):
        val = simulation.calculate_attention(h, capacity, s_start, s_end)
        if val is not None:
            hours.append(h)
            scores.append(val)
            # Logic to find the highest focus hour
            if val > max_score:
                max_score = val
                best_hour = h

    # 3. Format the "Best Time" for the UI (e.g., 14 -> 2:00 PM)
    if best_hour is not None:
        time_suffix = "AM" if best_hour < 12 else "PM"
        display_hour = best_hour if 1 <= best_hour <= 12 else abs(best_hour - 12)
        if display_hour == 0: display_hour = 12
        best_time_str = f"{display_hour}:00 {time_suffix}"
    else:
        best_time_str = "N/A"

    # 4. Generate the Plot with Dark Mode styling
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#161b22')
    ax.set_facecolor('#161b22')

    # Plotting the focus line
    plt.plot(hours, scores, color='#00d4ff', linewidth=3, marker='o', 
             markerfacecolor='#ffffff', markersize=6, label='Attention Level')
    
    # Fill the area under the curve
    plt.fill_between(hours, scores, color='#00d4ff', alpha=0.15)

    # Customize Axes and Grid
    plt.title(f"Focus Forecast: {name}", fontsize=16, pad=20, color='#ffffff')
    plt.xlabel("Hour of Day (24h Format)", color='#8b949e')
    plt.ylabel("Attention Percentage", color='#8b949e')
    plt.ylim(0, 105)
    plt.xticks(range(0, 24, 2))
    plt.grid(color='#30363d', linestyle='--', alpha=0.5)
    
    # Remove plot borders (spines) for a cleaner look
    for spine in ax.spines.values():
        spine.set_visible(False)

    # 5. Convert plot to Base64 string (In-Memory)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)  # Crucial to prevent memory leaks

    # 6. Render the updated graph.html with all variables
    return render_template("graph.html", 
                           name=name, 
                           plot_url=plot_data, 
                           best_time=best_time_str, 
                           peak_score=round(max_score, 1))

if __name__ == "__main__":
    app.run(debug=True)