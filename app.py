from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

def calculate_wakeup_times(sleep_cycles=5, cycle_duration=90):
    """Calculate wake-up times based on sleep cycles."""
    current_time = datetime.datetime.now()
    return [
        (current_time + datetime.timedelta(minutes=(i * cycle_duration + 15))).strftime("%H:%M")
        for i in range(1, sleep_cycles + 1)
    ]

def calculate_bedtime(wakeup_time, sleep_cycles=6, cycle_duration=90):
    """Calculate bedtimes to wake up at the specified time."""
    wakeup_time_obj = datetime.datetime.strptime(wakeup_time, "%H:%M")
    current_date = datetime.datetime.now().date()
    wakeup_time_with_date = datetime.datetime.combine(current_date, wakeup_time_obj.time())

    if wakeup_time_with_date < datetime.datetime.now():
        wakeup_time_with_date += datetime.timedelta(days=1)

    return [
        f"{(wakeup_time_with_date - datetime.timedelta(minutes=(i * cycle_duration + 15))).strftime('%H:%M')} (Suggested for {i} cycles)" 
        if i in [5, 6] else (wakeup_time_with_date - datetime.timedelta(minutes=(i * cycle_duration + 15))).strftime("%H:%M")
        for i in range(1, sleep_cycles + 1)
    ]

def suggest_good_sleep_cycle():
    """Suggest optimal sleep times for 5-6 complete sleep cycles."""
    current_time = datetime.datetime.now()
    return [
        f"{(current_time + datetime.timedelta(minutes=(cycles * 90 + 15))).strftime('%H:%M')} (Suggested for {cycles} cycles)"
        for cycles in [5, 6]
    ]

@app.route("/", methods=["GET", "POST"])
def home():
    wakeup_times = []
    bedtimes = []
    suggested_wakeup_times = suggest_good_sleep_cycle()
    
    if request.method == "POST":
        if 'calculate_wakeup' in request.form:
            sleep_cycles = int(request.form.get("sleep_cycles", 5))
            wakeup_times = calculate_wakeup_times(sleep_cycles=sleep_cycles)
        elif 'calculate_bedtime' in request.form:
            desired_wakeup_time = request.form.get("wakeup_time")
            try:
                bedtimes = calculate_bedtime(desired_wakeup_time, sleep_cycles=6)
            except ValueError:
                bedtimes = ["Invalid time format. Please use HH:MM."]
    
    return render_template("index.html", wakeup_times=wakeup_times, bedtimes=bedtimes, suggested_wakeup_times=suggested_wakeup_times)

if __name__ == "__main__":
    app.run(debug=True)
