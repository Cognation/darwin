import { create } from "zustand";

export const useZustandStore = create()((set) => ({

  messages : [],
  selectedProject : null,
  selectedProject_id : null,
  selected : "terminal",
  projectList : [],
  files : [],
  theme : "System",
  editor_expanded : true,
  setFiles : (prvfiles) => set({ files : prvfiles }),
  expandedNodes : {},
  selected_file : null,
  selected_file_language : "python",
  setMessages: (newchat) => set({ messages : newchat }),
  setselected: (newselected) => set({ selected : newselected }),
  setselectedProject : (prvproject) => set({ selectedProject : prvproject }),
  setprojectlist : (prvlist) => set({ projectList : prvlist }),
  setselectedProject_id : (id) => set({ selectedProject_id : id }),
  setExpandedNodes : (change) => set({ expandedNodes : change }),
  setTheme : (newtheme) => set({ theme : newtheme }),
  setEditor_expanded : (newwidth) => set({ editor_expanded : newwidth }),
  setselected_file : (newfile) => set({ selected_file : newfile }),
  setselected_file_language : (newlang) => set({ selected_file_language : newlang }),
}));
