import { create } from "zustand";

export const useZustandStore = create()((set) => ({

  messages : [],
  selectedProject : null,
  selectedProject_id : null,
  selected : "terminal",
  projectList : [],
  setMessages: (newchat) => set({ messages : newchat }),
  setselected: (newselected) => set({ selected : newselected }),
  setselectedProject : (prvproject) => set({ selectedProject : prvproject }),
  setprojectlist : (prvlist) => set({ projectList : prvlist }),
  setselectedProject_id : (id) => set({ selectedProject_id : id }),
}));
