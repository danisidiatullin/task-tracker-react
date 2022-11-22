import React, { useEffect, useState } from "react";

import Select from "react-select";

const TaskModal = ({ active, handleModal, token, id, setErrorMessage }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState(0);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");
  const [statuses, setStatuses] = useState([]);

  const getStatuses = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
    const response = await fetch("/api/task_statuses", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong. Couldn't load the statuses");
    } else {
      const data = await response.json();
      setStatuses(data);
    }
  };

  useEffect(() => {
    getStatuses();
  }, []);

  const statusOptions = statuses.map((text, index) => {
    return { value: text, label: text };
  });

  useEffect(() => {
    const getTask = async () => {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };
      const response = await fetch(`/api/tasks/${id}`, requestOptions);
      console.log(statusOptions);
      if (!response.ok) {
        setErrorMessage("Could not get the task");
      } else {
        const data = await response.json();
        setTitle(data.title);
        setDescription(data.description);
        setPriority(data.priority);
        setProgress(data.progress);
        setStatus(data.status);
      }
    };

    if (id) {
      getTask();
    }
  }, [id, token]);

  const cleanFormData = () => {
    setTitle("");
    setDescription("");
    setPriority(1);
    setProgress(0);
    setStatus("");
  };

  const handleCreateTask = async (e) => {
    e.preventDefault();
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({
        title: title,
        description: description,
        priority: priority,
        progress: progress,
        status: status,
      }),
    };
    const response = await fetch("/api/tasks", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong when creating task");
      if (response.status === 422) {
        console.log(requestOptions);
        console.log(response.json());
      }
    } else {
      cleanFormData();
      handleModal();
    }
  };

  const handleUpdateTask = async (e) => {
    e.preventDefault();
    const requestOptions = {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({
        title: title,
        description: description,
        priority: priority,
        progress: progress,
        status: status,
      }),
    };
    const response = await fetch(`/api/tasks/${id}`, requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong when updating task");
    } else {
      cleanFormData();
      handleModal();
    }
  };

  return (
    <div className={`modal ${active && "is-active"}`}>
      <div className="modal-background" onClick={handleModal}></div>
      <div className="modal-card">
        <header className="modal-card-head has-background-primary-light">
          <h1 className="modal-card-title">
            {id ? "Update Task" : "Create Task"}
          </h1>
        </header>
        <section className="modal-card-body">
          <form>
            <div className="field">
              <label className="label">Title</label>
              <div className="control">
                <input
                  type="text"
                  placeholder="Enter title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="input"
                  required
                />
              </div>
            </div>

            <div className="field">
              <label className="label">Description</label>
              <div className="control">
                <input
                  type="text"
                  placeholder="Enter description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="input"
                  required
                />
              </div>
            </div>

            <div className="field">
              <label className="label">Priority</label>
              <div className="control">
                <input
                  type="number"
                  placeholder="Enter priority"
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                  className="input"
                  min="1"
                  max="5"
                  required
                />
              </div>
            </div>

            <div className="field">
              <label className="label">Progress</label>
              <div className="control">
                <input
                  type="number"
                  placeholder="Enter title"
                  value={progress}
                  onChange={(e) => setProgress(e.target.value)}
                  className="input"
                  required
                />
              </div>
            </div>

            <div className="field">
              <label className="label">Status</label>
              <div className="control">
                <Select
                  options={statusOptions}
                  value={{
                    value: status,
                    label: status,
                  }}
                  onChange={(e) => setStatus(e.value)}
                />
              </div>
            </div>
          </form>
        </section>

        <footer className="modal-card-foot has-background-primary-light">
          {id ? (
            <button className="button is-info" onClick={handleUpdateTask}>
              Update
            </button>
          ) : (
            <button className="button is-primary" onClick={handleCreateTask}>
              Create
            </button>
          )}
          <button className="button" onClick={handleModal}>
            Cancel
          </button>
        </footer>
      </div>
    </div>
  );
};

export default TaskModal;
