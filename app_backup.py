from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EduPath AI Dashboard</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f5ff;
    color: #252b50;
}

header {
    background: linear-gradient(120deg, #4568dc, #8e54e9);
    color: white;
    padding: 30px 7%;
}

header h1 {
    margin: 0;
    font-size: 32px;
}

header p {
    margin-bottom: 0;
}

.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 0 20px;
}

.welcome {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 5px 20px #dfe1f5;
    margin-bottom: 25px;
}

.welcome h2 {
    margin-top: 0;
}

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 20px;
}

.card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    box-shadow: 0 5px 18px #e0e2f5;
    transition: transform 0.2s;
}

.card:hover {
    transform: translateY(-5px);
}

.icon {
    font-size: 35px;
}

.card h3 {
    margin-bottom: 8px;
}

.number {
    font-size: 28px;
    font-weight: bold;
    color: #6854df;
}

button {
    background: linear-gradient(120deg, #4568dc, #8e54e9);
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 15px;
}

button:hover {
    opacity: 0.85;
}

.progress-bg {
    height: 12px;
    background: #e7e8f5;
    border-radius: 10px;
    overflow: hidden;
}

.progress {
    height: 100%;
    width: 65%;
    background: linear-gradient(90deg, #4568dc, #8e54e9);
    border-radius: 10px;
}

.path {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 15px;
}

.path span {
    background: #eeebff;
    color: #6045c5;
    padding: 12px;
    border-radius: 10px;
    font-weight: bold;
}

footer {
    text-align: center;
    padding: 25px;
    color: #777;
}

@media (max-width: 500px) {
    header h1 {
        font-size: 25px;
    }
}
</style>
</head>

<body>

<header>
    <h1>🎓 EduPath AI</h1>
    <p>Your Smart Education Guide</p>
</header>

<div class="container">

    <section class="welcome">
        <h2>Welcome, Student! 👋</h2>
        <p>Your learning journey starts here. Keep learning and reach your goals!</p>
        <button onclick="alert('Welcome to EduPath AI!')">
            Explore Dashboard →
        </button>
    </section>

    <section class="cards">

        <div class="card">
            <div class="icon">⭐</div>
            <h3>Total Points</h3>
            <div class="number" id="points">60</div>
            <button onclick="addPoints()">Complete Task +10</button>
        </div>

        <div class="card">
            <div class="icon">📚</div>
            <h3>Learning Progress</h3>
            <p>Keep going! You're making progress.</p>
            <div class="progress-bg">
                <div class="progress"></div>
            </div>
            <p>65% completed</p>
        </div>

        <div class="card">
            <div class="icon">🏆</div>
            <h3>Achievements</h3>
            <div class="number">3</div>
            <p>Keep learning to earn more!</p>
        </div>

        <div class="card">
            <div class="icon">🎯</div>
            <h3>Opportunities</h3>
            <p>Explore workshops, hackathons and internships.</p>
            <button onclick="alert('Opportunities section coming soon!')">
                Explore
            </button>
        </div>

    </section>

    <section class="card" style="margin-top:25px">
        <h2>🛤️ My Learning Pathway</h2>
        <p>Follow these stages to build your skills.</p>

        <div class="path">
            <span>📖 Learn</span>
            <span>✍️ Practise</span>
            <span>🎤 Participate</span>
            <span>💡 Build Skills</span>
            <span>🎯 Goal</span>
        </div>
    </section>

    <section class="card" style="margin-top:25px">
        <h2>📅 Today's Tasks</h2>
        <p>☑ Learn a new concept</p>
        <p>☑ Practise Python programming</p>
        <p>☑ Explore a new opportunity</p>
    </section>

</div>

<footer>
    © 2026 EduPath AI | Learn • Practise • Grow 🚀
</footer>

<script>
function addPoints() {
    let pointsElement = document.getElementById("points");
    let points = Number(pointsElement.textContent);
    pointsElement.textContent = points + 10;
}
</script>

</body>
</html>
""")

if __name__ == "__main__":
    app.run(debug=True)