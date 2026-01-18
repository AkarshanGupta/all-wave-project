-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.action_items (
  id integer NOT NULL DEFAULT nextval('action_items_id_seq'::regclass),
  meeting_id integer NOT NULL,
  description text NOT NULL,
  assignee character varying,
  due_date timestamp with time zone,
  status character varying,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone,
  CONSTRAINT action_items_pkey PRIMARY KEY (id),
  CONSTRAINT action_items_meeting_id_fkey FOREIGN KEY (meeting_id) REFERENCES public.meetings(id)
);
CREATE TABLE public.alembic_version (
  version_num character varying NOT NULL,
  CONSTRAINT alembic_version_pkey PRIMARY KEY (version_num)
);
CREATE TABLE public.allocations (
  id integer NOT NULL DEFAULT nextval('allocations_id_seq'::regclass),
  resource_id integer NOT NULL,
  project_id integer NOT NULL,
  allocated_hours numeric NOT NULL,
  start_date timestamp with time zone,
  end_date timestamp with time zone,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone,
  CONSTRAINT allocations_pkey PRIMARY KEY (id),
  CONSTRAINT allocations_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id),
  CONSTRAINT allocations_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES public.resources(id)
);
CREATE TABLE public.meetings (
  id integer NOT NULL DEFAULT nextval('meetings_id_seq'::regclass),
  project_id integer NOT NULL,
  title character varying NOT NULL,
  raw_text text NOT NULL,
  summary text,
  decisions text,
  open_questions text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone,
  CONSTRAINT meetings_pkey PRIMARY KEY (id),
  CONSTRAINT meetings_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id)
);
CREATE TABLE public.projects (
  id integer NOT NULL DEFAULT nextval('projects_id_seq'::regclass),
  name character varying NOT NULL,
  description text,
  status character varying,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone,
  CONSTRAINT projects_pkey PRIMARY KEY (id)
);
CREATE TABLE public.resources (
  id integer NOT NULL DEFAULT nextval('resources_id_seq'::regclass),
  project_id integer,
  name character varying NOT NULL,
  role character varying NOT NULL,
  capacity_hours numeric NOT NULL,
  availability_hours numeric NOT NULL,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone,
  CONSTRAINT resources_pkey PRIMARY KEY (id),
  CONSTRAINT resources_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id)
);
CREATE TABLE public.risks (
  id integer NOT NULL DEFAULT nextval('risks_id_seq'::regclass),
  project_id integer NOT NULL,
  title character varying NOT NULL,
  description text NOT NULL,
  category character varying NOT NULL,
  probability integer NOT NULL,
  impact integer NOT NULL,
  severity character varying NOT NULL,
  mitigation_plan text,
  status character varying,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone,
  CONSTRAINT risks_pkey PRIMARY KEY (id),
  CONSTRAINT risks_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id)
);
CREATE TABLE public.status_reports (
  id integer NOT NULL DEFAULT nextval('status_reports_id_seq'::regclass),
  project_id integer NOT NULL,
  executive_summary text NOT NULL,
  risks_summary text,
  meetings_summary text,
  resources_summary text,
  generated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT status_reports_pkey PRIMARY KEY (id),
  CONSTRAINT status_reports_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id)
);