type TaskPropsLesser = {
  text: string;
  time: string;
  reminder: boolean;
};

type TaskProps = TaskPropsLesser & { id: number };

type TasksProps = {
  tasks: Array<TaskProps>;
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
};

const Tasks = ({ tasks, onToggle, onDelete }: TasksProps) => {
  return (
    <>
      {tasks.map((task) => (
        <div
          key={task.id}
          className={`task ${task.reminder ? "reminder" : ""}`}
          onDoubleClick={() => onToggle(task.id)}
        >
          <div>
            <h3>{task.text}</h3>
            <p>{task.time}</p>
          </div>
          <strong className="delete-task" onClick={() => onDelete(task.id)}>
            &times;
          </strong>
        </div>
      ))}
    </>
  );
};

export default Tasks;
export type { TaskPropsLesser, TaskProps };
