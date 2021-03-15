type ButtonProps = {
  showAddTask: boolean;
  onClick: () => void;
};

const Button = ({ showAddTask, onClick }: ButtonProps) => {
  return (
    <button
      className={`btn ${showAddTask ? "btn-delete" : "btn-add"}`}
      onClick={onClick}
    >
      {`${showAddTask ? "Hide" : "Add"}`}
    </button>
  );
};

export default Button;
