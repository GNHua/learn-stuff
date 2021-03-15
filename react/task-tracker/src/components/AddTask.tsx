import { useState, FormEvent } from "react";
import { TaskPropsLesser } from "./Tasks";

type AddTaskProps = {
  onSubmit: (task: TaskPropsLesser) => void;
};

const AddTask = ({ onSubmit }: AddTaskProps) => {
  const [text, setText] = useState("");
  const [time, setTime] = useState("");
  const [reminder, setReminder] = useState(false);

  const handleSubmit = (e: FormEvent<HTMLFormElement>): void => {
    e.preventDefault();

    onSubmit({
      text: text,
      time: time,
      reminder: reminder,
    });

    setText("");
    setTime("");
    setReminder(false);
  };

  return (
    <form className="add-task" onSubmit={handleSubmit}>
      <div className="form-control">
        <label>Task</label>
        <input
          type="text"
          placeholder="Add Task"
          value={text}
          onChange={(e): void => setText(e.target.value)}
        />
      </div>
      <div className="form-control">
        <label>Day & Time</label>
        <input
          type="text"
          placeholder="Add Day & Time"
          value={time}
          onChange={(e): void => setTime(e.target.value)}
        />
      </div>
      <div className="form-control-check">
        <label>Set Reminder</label>
        <input
          type="checkbox"
          checked={reminder}
          onChange={(e) => setReminder(e.currentTarget.checked)}
        />
      </div>
      <input type="submit" value="Save Task" className="btn btn-block" />
    </form>
  );
};

export default AddTask;
