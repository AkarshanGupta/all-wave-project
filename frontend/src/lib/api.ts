import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health check
export const checkHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

// API info
export const getApiInfo = async () => {
  const response = await api.get('/');
  return response.data;
};

// Projects
export interface Project {
  id?: number;
  name: string;
  description?: string;
  status?: string;
  priority?: number;  // 1-10 scale
  start_date?: string;
  deadline?: string;
  created_at?: string;
  updated_at?: string;
}

export const getProjects = async () => {
  const response = await api.get('/projects');
  return response.data;
};

export const createProject = async (project: Project) => {
  const response = await api.post('/projects', project);
  return response.data;
};

export const updateProject = async (id: number, project: Partial<Project>) => {
  const response = await api.put(`/projects/${id}`, project);
  return response.data;
};

export const deleteProject = async (id: number) => {
  const response = await api.delete(`/projects/${id}`);
  return response.data;
};

// Meetings
export interface Meeting {
  id?: number;
  project_id: number;
  title: string;
  raw_text: string;
  summary?: string;
  decisions?: string;
  open_questions?: string;
  date?: string;
  time?: string;
  duration?: number;
  attendees?: string[];
  status?: string;
  created_at?: string;
  updated_at?: string;
}

export const getMeetings = async () => {
  const response = await api.get('/meetings');
  return response.data;
};

export const createMeeting = async (meeting: Meeting) => {
  const response = await api.post('/meetings', meeting);
  return response.data;
};

export const updateMeeting = async (id: number, meeting: Partial<Meeting>) => {
  const response = await api.put(`/meetings/${id}`, meeting);
  return response.data;
};

export const deleteMeeting = async (id: number) => {
  const response = await api.delete(`/meetings/${id}`);
  return response.data;
};

// Risks
export interface Risk {
  id?: number;
  project_id: number;
  title: string;
  description: string;
  category: string;
  probability: number;
  impact: number;
  severity: string;
  risk_score?: number;
  trend?: string;
  mitigation_plan?: string;
  status?: string;
  approval_status?: string;
  approved_by?: string;
  created_at?: string;
  updated_at?: string;
}

export const getRisks = async () => {
  const response = await api.get('/risks');
  return response.data;
};

export const createRisk = async (risk: Risk) => {
  const response = await api.post('/risks', risk);
  return response.data;
};

export const updateRisk = async (id: number, risk: Partial<Risk>) => {
  const response = await api.put(`/risks/${id}`, risk);
  return response.data;
};

export const deleteRisk = async (id: number) => {
  const response = await api.delete(`/risks/${id}`);
  return response.data;
};

export const analyzeProjectDocumentation = async (projectId: number) => {
  const response = await api.post(`/risks/analyze-project/${projectId}`);
  return response.data;
};

// Resources
export interface ResourceSkill {
  id?: number;
  skill_name: string;
  proficiency_level: number; // 1-5
}

export interface Resource {
  id?: number;
  project_id?: number;
  name: string;
  role: string;
  capacity_hours: number;
  availability_hours: number;
  department?: string;
  location?: string;
  skills?: ResourceSkill[];
  created_at?: string;
  updated_at?: string;
}

export const getResources = async () => {
  const response = await api.get('/resources');
  return response.data;
};

export const createResource = async (resource: Resource) => {
  const response = await api.post('/resources', resource);
  return response.data;
};

export const updateResource = async (id: number, resource: Partial<Resource>) => {
  const response = await api.put(`/resources/${id}`, resource);
  return response.data;
};

export const deleteResource = async (id: number) => {
  const response = await api.delete(`/resources/${id}`);
  return response.data;
};

// Allocations
export interface Allocation {
  id?: string;
  resource_id: string | number;
  project_id: string | number;
  allocated_hours: number;
  start_date?: string;
  end_date?: string;
}

export const getAllocations = async () => {
  const response = await api.get('/allocations');
  return response.data;
};

export const createAllocation = async (allocation: Allocation) => {
  const response = await api.post('/allocations', allocation);
  return response.data;
};

// Status Reports
export interface StatusReport {
  id?: string;
  project_id: string | number;
  executive_summary: string;
  risks_summary?: string;
  meetings_summary?: string;
  resources_summary?: string;
}

export const getStatusReports = async () => {
  const response = await api.get('/status');
  return response.data;
};

export const createStatusReport = async (report: StatusReport) => {
  const response = await api.post('/status', report);
  return response.data;
};

export const updateStatusReport = async (id: string, report: Partial<StatusReport>) => {
  const response = await api.put(`/status/${id}`, report);
  return response.data;
};

export const deleteStatusReport = async (id: string) => {
  const response = await api.delete(`/status/${id}`);
  return response.data;
};

export default api;
