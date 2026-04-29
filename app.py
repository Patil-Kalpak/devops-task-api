from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
app = Flask(__name__)

# Hardcoded users for the application
USERS = [
    "Alice Johnson",
    "Bob Smith", 
    "Charlie Davis",
    "Diana Martinez",
    "Ethan Brown"
]

# Priority levels
PRIORITIES = ["Low", "Medium", "High", "Cr	itical"]

# In-memory task storage
tasks = []
task_id = 1

@app.route("/health")
def health():
    return {"status": "ok"}
@app.route("/")
def home():
    """Render the main application page"""
    return render_template("index.html", users=USERS, priorities=PRIORITIES)


@app.route("/users", methods=["GET"])
def get_users():
    """Return list of hardcoded users"""
    return jsonify(USERS)


@app.route("/add", methods=["POST"])
def add_task():
    """Add a new task with validation"""
    global task_id
    
    try:
        data = request.get_json()
        
        # Validation
        if not data.get("task") or not data.get("task").strip():
            return jsonify({"error": "Task description is required"}), 400
        
        if not data.get("user") or data.get("user") not in USERS:
            return jsonify({"error": "Valid user is required"}), 400
        
        priority = data.get("priority", "Medium")
        if priority not in PRIORITIES:
            priority = "Medium"
        
        task = {
            "id": task_id,
            "task": data.get("task").strip(),
            "user": data.get("user"),
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        tasks.append(task)
        task_id += 1
        
        return jsonify({"message": "Task added successfully", "task": task}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Get all tasks with optional filtering"""
    user = request.args.get("user")
    status = request.args.get("status")
    priority = request.args.get("priority")
    
    filtered = tasks.copy()
    
    if user:
        filtered = [t for t in filtered if t["user"] == user]
    if status:
        filtered = [t for t in filtered if t["status"] == status]
    if priority:
        filtered = [t for t in filtered if t["priority"] == priority]
    
    # Sort by ID descending (newest first)
    filtered.sort(key=lambda x: x["id"], reverse=True)
    
    return jsonify(filtered)


@app.route("/complete/<int:id>", methods=["PUT"])
def complete_task(id):
    """Mark a task as completed"""
    for task in tasks:
        if task["id"] == id:
            task["status"] = "completed"
            task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return jsonify({"message": "Task marked as completed", "task": task})
    
    return jsonify({"error": "Task not found"}), 404


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_task(id):
    """Delete a task by ID"""
    global tasks
    
    for i, task in enumerate(tasks):
        if task["id"] == id:
            deleted_task = tasks.pop(i)
            return jsonify({"message": "Task deleted successfully", "task": deleted_task})
    
    return jsonify({"error": "Task not found"}), 404


@app.route("/stats", methods=["GET"])
def stats():
    """Get statistics for tasks"""
    user = request.args.get("user")
    
    filtered = tasks.copy()
    if user:
       filtered = [t for t in filtered if t["user"] == user]
    
    total = len(filtered)
    completed = len([t for t in filtered if t["status"] == "completed"])
    pending = total - completed
    
    # Priority breakdown
    priority_stats = {
        "Critical": len([t for t in filtered if t["priority"] == "Critical"]),
        "High": len([t for t in filtered if t["priority"] == "High"]),
        "Medium": len([t for t in filtered if t["priority"] == "Medium"]),
        "Low": len([t for t in filtered if t["priority"] == "Low"])
    }
    
    return jsonify({
        "total": total,
        "completed": completed,
        "pending": pending,
        "priority_breakdown": priority_stats
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
