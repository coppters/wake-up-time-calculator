from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

def calculate_wakeup_times(sleep_cycles=5, cycle_duration=90):
    """Calculate wake-up times for fresh wake-ups based on sleep cycles."""
    
    current_time = datetime.datetime.now()
    wakeup_times = []
    
    for i in range(1, sleep_cycles + 1):
        total_sleep_minutes = i * cycle_duration + 15  # 15 minutes to fall asleep
        wakeup_time = current_time + datetime.timedelta(minutes=total_sleep_minutes)
        wakeup_times.append(wakeup_time.strftime("%I:%M %p"))
    
    return wakeup_times

def calculate_bedtime(wakeup_time, sleep_cycles=6, cycle_duration=90):
    """Calculate the time to go to bed in order to wake up at the specified time."""
    
    wakeup_time_obj = datetime.datetime.strptime(wakeup_time, "%I:%M %p")
    current_date = datetime.datetime.now().date()
    wakeup_time_with_date = datetime.datetime.combine(current_date, wakeup_time_obj.time())
    
    if wakeup_time_with_date < datetime.datetime.now():
        wakeup_time_with_date += datetime.timedelta(days=1)
    
    bedtimes = []
    
    for i in range(1, sleep_cycles + 1):
        total_sleep_minutes = i * cycle_duration + 15  # 15 minutes to fall asleep
        bedtime = wakeup_time_with_date - datetime.timedelta(minutes=total_sleep_minutes)
        if i in [5, 6]:  # Mark suggested bedtimes for 5 and 6 cycles
            bedtimes.append(f"{bedtime.strftime('%I:%M %p')} (Suggested for {i} cycles)")
        else:
            bedtimes.append(bedtime.strftime("%I:%M %p"))
    
    return bedtimes

def suggest_good_sleep_cycle():
    """Suggest the optimal sleep times for 5-6 complete sleep cycles."""
    
    current_time = datetime.datetime.now()
    sleep_cycles = [5, 6]  # Good sleep cycles
    suggested_wakeup_times = []
    
    for cycles in sleep_cycles:
        total_sleep_minutes = cycles * 90 + 15  # Each cycle is 90 minutes + 15 minutes to fall asleep
        wakeup_time = current_time + datetime.timedelta(minutes=total_sleep_minutes)
        suggested_wakeup_times.append(f"{wakeup_time.strftime('%I:%M %p')} (Suggested for {cycles} cycles)")
    
    return suggested_wakeup_times

@app.route("/", methods=["GET", "POST"])
def home():
    wakeup_times = []
    bedtimes = []
    suggested_wakeup_times = []
    if request.method == "POST":
        if 'calculate_wakeup' in request.form:
            sleep_cycles = int(request.form.get("sleep_cycles", 5))
            wakeup_times = calculate_wakeup_times(sleep_cycles=sleep_cycles)
        if 'calculate_bedtime' in request.form:
            desired_wakeup_time = request.form.get("wakeup_time")
            bedtimes = calculate_bedtime(desired_wakeup_time, sleep_cycles=6)  # Ensure it calculates for 6 cycles too
    
    suggested_wakeup_times = suggest_good_sleep_cycle()
    
    return render_template("index.html", wakeup_times=wakeup_times, bedtimes=bedtimes, suggested_wakeup_times=suggested_wakeup_times)

if __name__ == "__main__":
    app.run(debug=True)
