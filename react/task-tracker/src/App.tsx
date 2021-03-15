import { useState, useEffect } from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import About from "./components/About";
import AddTask from "./components/AddTask";
import Footer from "./components/Footer";
import Header from "./components/Header";
import Tasks, { TaskPropsLesser, TaskProps } from "./components/Tasks";

function App() {
  const [showAddTask, setShowAddTask] = useState(false);
  const [tasks, setTasks] = useState(new Array<TaskProps>());

  const jsonServer = (route: string): string => {
    const domain = "http://localhost:5000";
    return domain + route;
  };

  useEffect(() => {
    const getTasks = async (): Promise<void> => {
      const tasksFromServer = await fetchTasks();
      setTasks(tasksFromServer);
    };

    getTasks();
  });

  const fetchTasks = async (): Promise<Array<TaskProps>> => {
    const res = await fetch(jsonServer("/tasks"));
    const data = await res.json();
    return data;
  };

  const fetchTask = async (id: number): Promise<TaskProps> => {
    const res = await fetch(jsonServer(`/tasks/${id}`));
    const data = await res.json();
    return data;
  };

  const toggleAddTask = (): void => {
    setShowAddTask(!showAddTask);
  };

  const addTask = async (task: TaskPropsLesser): Promise<void> => {
    const res = await fetch(jsonServer("/tasks"), {
      method: "POST",
      headers: { "Content-type": "application/json" },
      body: JSON.stringify(task),
    });
    const data = await res.json();
    setTasks([...tasks, data]);
  };

  const toggleReminder = async (id: number): Promise<void> => {
    const taskToToggle = await fetchTask(id);
    const updatedTask = { ...taskToToggle, reminder: !taskToToggle.reminder };

    const res = await fetch(jsonServer(`/tasks/${id}`), {
      method: "PUT",
      headers: { "Content-type": "application/json" },
      body: JSON.stringify(updatedTask),
    });
    const data = await res.json();

    setTasks(tasks.map((task) => (task.id !== id ? task : data)));
  };

  const deleteTask = async (id: number): Promise<void> => {
    await fetch(jsonServer(`/tasks/${id}`), { method: "DELETE" });
    setTasks(tasks.filter((task) => task.id !== id));
  };

  return (
    <Router>
      <div className="container">
        <Header showAddTask={showAddTask} onClick={toggleAddTask} />
        <Route
          path="/"
          exact
          render={(props) => (
            <>
              {showAddTask && <AddTask onSubmit={addTask} />}
              <Tasks
                tasks={tasks}
                onToggle={toggleReminder}
                onDelete={deleteTask}
              />
            </>
          )}
        />
        <Route path="/about" component={About} />
        <Footer />
      </div>
    </Router>
  );
}

export default App;
