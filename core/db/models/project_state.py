from copy import deepcopy
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, UniqueConstraint, delete, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.sql import func

from core.db.models import Base
from core.log import get_logger

if TYPE_CHECKING:
    from core.db.models import Branch, ExecLog, File, FileContent, LLMRequest, Specification, UserInput

log = get_logger(__name__)


class TaskStatus:
    """Status of a task."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEWED = "reviewed"
    DOCUMENTED = "documented"
    EPIC_UPDATED = "epic_updated"
    DONE = "done"
    SKIPPED = "skipped"


class ProjectState(Base):
    __tablename__ = "project_states"
    __table_args__ = (
        UniqueConstraint("prev_state_id"),
        UniqueConstraint("branch_id", "step_index"),
        {"sqlite_autoincrement": True},
    )

    # ID and parent FKs
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    branch_id: Mapped[UUID] = mapped_column(ForeignKey("branches.id", ondelete="CASCADE"))
    prev_state_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("project_states.id", ondelete="CASCADE"))
    specification_id: Mapped[int] = mapped_column(ForeignKey("specifications.id"))

    # Attributes
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    step_index: Mapped[int] = mapped_column(default=1, server_default="1")
    epics: Mapped[list[dict]] = mapped_column(default=list)
    tasks: Mapped[list[dict]] = mapped_column(default=list)
    steps: Mapped[list[dict]] = mapped_column(default=list)
    iterations: Mapped[list[dict]] = mapped_column(default=list)
    relevant_files: Mapped[list[str]] = mapped_column(default=list)
    modified_files: Mapped[dict] = mapped_column(default=dict)
    run_command: Mapped[Optional[str]] = mapped_column()
    action: Mapped[Optional[str]] = mapped_column()

    # Relationships
    branch: Mapped["Branch"] = relationship(back_populates="states", lazy="selectin")
    prev_state: Mapped[Optional["ProjectState"]] = relationship(
        back_populates="next_state",
        remote_side=[id],
        single_parent=True,
        lazy="raise",
        cascade="delete",
    )
    next_state: Mapped[Optional["ProjectState"]] = relationship(back_populates="prev_state", lazy="raise")
    files: Mapped[list["File"]] = relationship(
        back_populates="project_state",
        lazy="selectin",
        cascade="all,delete-orphan",
    )
    specification: Mapped["Specification"] = relationship(back_populates="project_states", lazy="selectin")
    llm_requests: Mapped[list["LLMRequest"]] = relationship(back_populates="project_state", cascade="all", lazy="raise")
    user_inputs: Mapped[list["UserInput"]] = relationship(back_populates="project_state", cascade="all", lazy="raise")
    exec_logs: Mapped[list["ExecLog"]] = relationship(back_populates="project_state", cascade="all", lazy="raise")

    @property
    def unfinished_steps(self) -> list[dict]:
        """
        Get the list of unfinished steps.

        :return: List of unfinished steps.
        """
        return [step for step in self.steps if not step.get("completed")]

    @property
    def current_step(self) -> Optional[dict]:
        """
        Get the current step.

        Current step is always the first step that's not finished yet.

        :return: The current step, or None if there are no more unfinished steps.
        """
        li = self.unfinished_steps
        return li[0] if li else None

    @property
    def unfinished_iterations(self) -> list[dict]:
        """
        Get the list of unfinished iterations.

        :return: List of unfinished iterations.
        """
        return [iteration for iteration in self.iterations if not iteration.get("completed")]

    @property
    def current_iteration(self) -> Optional[dict]:
        """
        Get the current iteration.

        Current iteration is always the first iteration that's not finished yet.

        :return: The current iteration, or None if there are no unfinished iterations.
        """
        li = self.unfinished_iterations
        return li[0] if li else None

    @property
    def unfinished_tasks(self) -> list[dict]:
        """
        Get the list of unfinished tasks.

        :return: List of unfinished tasks.
        """
        return [task for task in self.tasks if task.get("status") != TaskStatus.DONE]

    @property
    def current_task(self) -> Optional[dict]:
        """
        Get the current task.

        Current task is always the first task that's not finished yet.

        :return: The current task, or None if there are no unfinished tasks.
        """
        li = self.unfinished_tasks
        return li[0] if li else None

    @property
    def unfinished_epics(self) -> list[dict]:
        """
        Get the list of unfinished epics.

        :return: List of unfinished epics.
        """
        return [epic for epic in self.epics if not epic.get("completed")]

    @property
    def current_epic(self) -> Optional[dict]:
        """
        Get the current epic.

        Current epic is always the first epic that's not finished yet.

        :return: The current epic, or None if there are no unfinished epics.
        """
        li = self.unfinished_epics
        return li[0] if li else None

    @property
    def relevant_file_objects(self):
        """
        Get the relevant files with their content.

        :return: List of tuples with file path and content.
        """
        return [file for file in self.files if file.path in self.relevant_files]

    @staticmethod
    def create_initial_state(branch: "Branch") -> "ProjectState":
        """
        Create the initial project state for a new branch.

        This does *not* commit the new state to the database.

        No checks are made to ensure that the branch does not
        already have a state.

        :param branch: The branch to create the state for.
        :return: The new ProjectState object.
        """
        from core.db.models import Specification

        return ProjectState(
            branch=branch,
            specification=Specification(),
            step_index=1,
        )

    async def create_next_state(self) -> "ProjectState":
        """
        Create the next project state for the branch.

        This does NOT insert the new state and the associated objects (spec,
        files, ...) to the database.

        :param session: The SQLAlchemy session.
        :return: The new ProjectState object.
        """
        if not self.id:
            raise ValueError("Cannot create next state for unsaved state.")

        if "next_state" in self.__dict__:
            raise ValueError(f"Next state already exists for state with id={self.id}.")

        new_state = ProjectState(
            branch=self.branch,
            prev_state=self,
            step_index=self.step_index + 1,
            specification=self.specification,
            epics=deepcopy(self.epics),
            tasks=deepcopy(self.tasks),
            steps=deepcopy(self.steps),
            iterations=deepcopy(self.iterations),
            files=[],
            relevant_files=deepcopy(self.relevant_files),
            modified_files=deepcopy(self.modified_files),
            run_command=self.run_command,
        )

        session: AsyncSession = inspect(self).async_session
        session.add(new_state)

        # NOTE: we only need the await here because of the tests, in live, the
        # load_project() and commit() methods on StateManager make sure that
        # the the files are eagerly loaded.
        for file in await self.awaitable_attrs.files:
            clone = file.clone()
            new_state.files.append(clone)

        return new_state

    def complete_step(self):
        if not self.unfinished_steps:
            raise ValueError("There are no unfinished steps to complete")
        if "next_state" in self.__dict__:
            raise ValueError("Current state is read-only (already has a next state).")

        log.debug(f"Completing step {self.unfinished_steps[0]['type']}")
        self.unfinished_steps[0]["completed"] = True
        flag_modified(self, "steps")

    def complete_task(self):
        if not self.unfinished_tasks:
            raise ValueError("There are no unfinished tasks to complete")
        if "next_state" in self.__dict__:
            raise ValueError("Current state is read-only (already has a next state).")

        log.debug(f"Completing task {self.unfinished_tasks[0]['description']}")
        self.set_current_task_status(TaskStatus.DONE)
        self.steps = []
        self.iterations = []
        self.relevant_files = []
        self.modified_files = {}
        flag_modified(self, "tasks")

        if not self.unfinished_tasks and self.unfinished_epics:
            self.complete_epic()

    def complete_epic(self):
        if not self.unfinished_epics:
            raise ValueError("There are no unfinished epics to complete")
        if "next_state" in self.__dict__:
            raise ValueError("Current state is read-only (already has a next state).")

        log.debug(f"Completing epic {self.unfinished_epics[0]['name']}")
        self.unfinished_epics[0]["completed"] = True
        self.tasks = []
        flag_modified(self, "epics")

    def complete_iteration(self):
        if not self.unfinished_iterations:
            raise ValueError("There are no unfinished iterations to complete")
        if "next_state" in self.__dict__:
            raise ValueError("Current state is read-only (already has a next state).")

        log.debug(f"Completing iteration {self.unfinished_iterations[0]}")
        self.unfinished_iterations[0]["completed"] = True
        self.flag_iterations_as_modified()

    def flag_iterations_as_modified(self):
        """
        Flag the iterations field as having been modified

        Used by Agents that perform modifications within the mutable iterations field,
        to tell the database that it was modified and should get saved (as SQLalchemy
        can't detect changes in mutable fields by itself).
        """
        flag_modified(self, "iterations")

    def flag_tasks_as_modified(self):
        """
        Flag the tasks field as having been modified

        Used by Agents that perform modifications within the mutable tasks field,
        to tell the database that it was modified and should get saved (as SQLalchemy
        can't detect changes in mutable fields by itself).
        """
        flag_modified(self, "tasks")

    def set_current_task_status(self, status: str):
        """
        Set the status of the current task.

        :param status: The new status.
        """
        if not self.current_task:
            raise ValueError("There is no current task to set status for")
        if "next_state" in self.__dict__:
            raise ValueError("Current state is read-only (already has a next state).")

        self.current_task["status"] = status
        self.flag_tasks_as_modified()

    def get_file_by_path(self, path: str) -> Optional["File"]:
        """
        Get a file from the current project state, by the file path.

        :param path: The file path.
        :return: The file object, or None if not found.
        """
        for file in self.files:
            if file.path == path:
                return file

        return None

    def save_file(self, path: str, content: "FileContent", external: bool = False) -> "File":
        """
        Save a file to the project state.

        This either creates a new file pointing at the given content,
        or updates the content of an existing file. This method
        doesn't actually commit the file to the database, just attaches
        it to the project state.

        If the file was created by Pythagora (not externally by user or template import),
        mark it as relevant for the current task.

        :param path: The file path.
        :param content: The file content.
        :param external: Whether the file was added externally (e.g. by a user).
        :return: The (unsaved) file object.
        """
        from core.db.models import File

        if "next_state" in self.__dict__:
            raise ValueError("Current state is read-only (already has a next state).")

        file = self.get_file_by_path(path)
        if file:
            original_content = file.content.content
            file.content = content
        else:
            original_content = ""
            file = File(path=path, content=content)
            self.files.append(file)

        if path not in self.modified_files and not external:
            self.modified_files[path] = original_content
        if path not in self.relevant_files:
            self.relevant_files.append(path)

        return file

    async def delete_after(self):
        """
        Delete all states in the branch after this one.
        """

        session: AsyncSession = inspect(self).async_session

        log.debug(f"Deleting all project states in branch {self.branch_id} after {self.id}")
        await session.execute(
            delete(ProjectState).where(
                ProjectState.branch_id == self.branch_id,
                ProjectState.step_index > self.step_index,
            )
        )
