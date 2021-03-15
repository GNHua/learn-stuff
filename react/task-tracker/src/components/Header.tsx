import { useLocation } from "react-router";
import Button from "./Button";

type HeaderProps = {
  title: string;
  showAddTask: boolean;
  onClick: () => void;
};

const Header = ({ title, showAddTask, onClick }: HeaderProps) => {
  const location = useLocation();
  return (
    <div className="header">
      <h1>{title}</h1>
      {location.pathname === "/" && (
        <Button showAddTask={showAddTask} onClick={onClick} />
      )}
    </div>
  );
};

Header.defaultProps = {
  title: "Task Tracer",
};

export default Header;
