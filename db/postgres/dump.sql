--
-- PostgreSQL database dump
--

-- Dumped from database version 15.14
-- Dumped by pg_dump version 15.1

-- Started on 2025-09-20 16:28:01 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 221 (class 1259 OID 16436)
-- Name: achievements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.achievements (
    id bigint NOT NULL,
    name character varying NOT NULL,
    image_path character varying NOT NULL,
    description character varying
);


ALTER TABLE public.achievements OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16435)
-- Name: achievements_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.achievements_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.achievements_id_seq OWNER TO postgres;

--
-- TOC entry 3462 (class 0 OID 0)
-- Dependencies: 220
-- Name: achievements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.achievements_id_seq OWNED BY public.achievements.id;


--
-- TOC entry 225 (class 1259 OID 24628)
-- Name: courses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.courses (
    id bigint NOT NULL,
    description character varying NOT NULL,
    name character varying NOT NULL,
    "hardness (1-3)" bigint NOT NULL
);


ALTER TABLE public.courses OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 24627)
-- Name: courses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.courses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.courses_id_seq OWNER TO postgres;

--
-- TOC entry 3463 (class 0 OID 0)
-- Dependencies: 224
-- Name: courses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.courses_id_seq OWNED BY public.courses.id;


--
-- TOC entry 214 (class 1259 OID 16408)
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id bigint NOT NULL,
    name character varying NOT NULL,
    employed_since timestamp with time zone NOT NULL,
    "position" character varying NOT NULL
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16445)
-- Name: employees_achievements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees_achievements (
    id bigint NOT NULL,
    employee_id bigint,
    achievement_id bigint
);


ALTER TABLE public.employees_achievements OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16444)
-- Name: employees_achievements_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employees_achievements_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.employees_achievements_id_seq OWNER TO postgres;

--
-- TOC entry 3464 (class 0 OID 0)
-- Dependencies: 222
-- Name: employees_achievements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_achievements_id_seq OWNED BY public.employees_achievements.id;


--
-- TOC entry 215 (class 1259 OID 16413)
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employees_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.employees_id_seq OWNER TO postgres;

--
-- TOC entry 3465 (class 0 OID 0)
-- Dependencies: 215
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- TOC entry 216 (class 1259 OID 16414)
-- Name: employees_projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees_projects (
    id bigint NOT NULL,
    employee_id bigint NOT NULL,
    project_id bigint NOT NULL,
    job_start timestamp with time zone NOT NULL,
    job_end timestamp with time zone,
    "position" character varying NOT NULL
);


ALTER TABLE public.employees_projects OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16419)
-- Name: employees_projects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employees_projects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.employees_projects_id_seq OWNER TO postgres;

--
-- TOC entry 3466 (class 0 OID 0)
-- Dependencies: 217
-- Name: employees_projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_projects_id_seq OWNED BY public.employees_projects.id;


--
-- TOC entry 218 (class 1259 OID 16420)
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects (
    id bigint NOT NULL,
    name character varying NOT NULL,
    description character varying
);


ALTER TABLE public.projects OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16425)
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_id_seq OWNER TO postgres;

--
-- TOC entry 3467 (class 0 OID 0)
-- Dependencies: 219
-- Name: projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_id_seq OWNED BY public.projects.id;


--
-- TOC entry 3288 (class 2604 OID 16439)
-- Name: achievements id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.achievements ALTER COLUMN id SET DEFAULT nextval('public.achievements_id_seq'::regclass);


--
-- TOC entry 3290 (class 2604 OID 24631)
-- Name: courses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses ALTER COLUMN id SET DEFAULT nextval('public.courses_id_seq'::regclass);


--
-- TOC entry 3285 (class 2604 OID 16426)
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- TOC entry 3289 (class 2604 OID 16448)
-- Name: employees_achievements id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees_achievements ALTER COLUMN id SET DEFAULT nextval('public.employees_achievements_id_seq'::regclass);


--
-- TOC entry 3286 (class 2604 OID 16427)
-- Name: employees_projects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees_projects ALTER COLUMN id SET DEFAULT nextval('public.employees_projects_id_seq'::regclass);


--
-- TOC entry 3287 (class 2604 OID 16428)
-- Name: projects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects ALTER COLUMN id SET DEFAULT nextval('public.projects_id_seq'::regclass);


--
-- TOC entry 3452 (class 0 OID 16436)
-- Dependencies: 221
-- Data for Name: achievements; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.achievements VALUES (1, 'Best worker', '/images/best-employee.png', 'Award for best work');


--
-- TOC entry 3456 (class 0 OID 24628)
-- Dependencies: 225
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3445 (class 0 OID 16408)
-- Dependencies: 214
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.employees VALUES (2, 'Egor Kor', '2023-09-15 10:00:00+00', 'DeveloperBackend');
INSERT INTO public.employees VALUES (1, 'John Doe Updated', '2023-01-15 10:00:00+00', 'Lead Developer');


--
-- TOC entry 3454 (class 0 OID 16445)
-- Dependencies: 223
-- Data for Name: employees_achievements; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.employees_achievements VALUES (1, 1, 1);
INSERT INTO public.employees_achievements VALUES (2, 2, 1);


--
-- TOC entry 3447 (class 0 OID 16414)
-- Dependencies: 216
-- Data for Name: employees_projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.employees_projects VALUES (1, 2, 1, '2024-01-01 09:00:00+00', '2024-06-30 18:00:00+00', 'Project Manager');
INSERT INTO public.employees_projects VALUES (2, 1, 1, '2024-01-15 09:00:00+00', NULL, 'налитик');


--
-- TOC entry 3449 (class 0 OID 16420)
-- Dependencies: 218
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.projects VALUES (1, 'еб-сайт Updated', 'бновленный корпоративный сайт');


--
-- TOC entry 3468 (class 0 OID 0)
-- Dependencies: 220
-- Name: achievements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.achievements_id_seq', 1, true);


--
-- TOC entry 3469 (class 0 OID 0)
-- Dependencies: 224
-- Name: courses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.courses_id_seq', 1, false);


--
-- TOC entry 3470 (class 0 OID 0)
-- Dependencies: 222
-- Name: employees_achievements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_achievements_id_seq', 2, true);


--
-- TOC entry 3471 (class 0 OID 0)
-- Dependencies: 215
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_id_seq', 3, true);


--
-- TOC entry 3472 (class 0 OID 0)
-- Dependencies: 217
-- Name: employees_projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_projects_id_seq', 2, true);


--
-- TOC entry 3473 (class 0 OID 0)
-- Dependencies: 219
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_id_seq', 2, true);


--
-- TOC entry 3298 (class 2606 OID 16443)
-- Name: achievements achievements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.achievements
    ADD CONSTRAINT achievements_pkey PRIMARY KEY (id);


--
-- TOC entry 3302 (class 2606 OID 24635)
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (id);


--
-- TOC entry 3300 (class 2606 OID 16450)
-- Name: employees_achievements employees_achievements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees_achievements
    ADD CONSTRAINT employees_achievements_pkey PRIMARY KEY (id);


--
-- TOC entry 3292 (class 2606 OID 16430)
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- TOC entry 3294 (class 2606 OID 16432)
-- Name: employees_projects employees_projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees_projects
    ADD CONSTRAINT employees_projects_pkey PRIMARY KEY (id);


--
-- TOC entry 3296 (class 2606 OID 16434)
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


-- Completed on 2025-09-20 16:28:03 UTC

--
-- PostgreSQL database dump complete
--
