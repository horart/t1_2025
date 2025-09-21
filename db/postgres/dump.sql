--
-- PostgreSQL database dump
--

-- Dumped from database version 15.14
-- Dumped by pg_dump version 15.1

-- Started on 2025-09-21 09:35:47 UTC

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
-- TOC entry 218 (class 1259 OID 24577)
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
-- TOC entry 219 (class 1259 OID 24582)
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
-- TOC entry 3535 (class 0 OID 0)
-- Dependencies: 219
-- Name: achievements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.achievements_id_seq OWNED BY public.achievements.id;


--
-- TOC entry 220 (class 1259 OID 24583)
-- Name: blue_rating; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.blue_rating (
    id bigint NOT NULL,
    employee_id bigint NOT NULL,
    delta bigint NOT NULL,
    reason character varying NOT NULL,
    created_at timestamp with time zone
);


ALTER TABLE public.blue_rating OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 24588)
-- Name: blue_rating_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.blue_rating_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blue_rating_id_seq OWNER TO postgres;

--
-- TOC entry 3536 (class 0 OID 0)
-- Dependencies: 221
-- Name: blue_rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.blue_rating_id_seq OWNED BY public.blue_rating.id;


--
-- TOC entry 222 (class 1259 OID 24589)
-- Name: courses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.courses (
    id bigint NOT NULL,
    description character varying NOT NULL,
    name character varying NOT NULL,
    hardness bigint NOT NULL
);


ALTER TABLE public.courses OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 24594)
-- Name: courses_employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.courses_employees (
    id bigint NOT NULL,
    course_id bigint NOT NULL,
    employee_id bigint NOT NULL,
    course_started timestamp with time zone NOT NULL,
    course_completed timestamp with time zone
);


ALTER TABLE public.courses_employees OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 24597)
-- Name: courses_employees_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.courses_employees_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.courses_employees_id_seq OWNER TO postgres;

--
-- TOC entry 3537 (class 0 OID 0)
-- Dependencies: 224
-- Name: courses_employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.courses_employees_id_seq OWNED BY public.courses_employees.id;


--
-- TOC entry 225 (class 1259 OID 24598)
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
-- TOC entry 3538 (class 0 OID 0)
-- Dependencies: 225
-- Name: courses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.courses_id_seq OWNED BY public.courses.id;


--
-- TOC entry 226 (class 1259 OID 24599)
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id bigint NOT NULL,
    name character varying NOT NULL,
    employed_since timestamp with time zone NOT NULL,
    "position" character varying NOT NULL,
    rcoins bigint,
    bcoins bigint,
    last_review_date timestamp with time zone,
    grade_id bigint
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 24604)
-- Name: employees_achievements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees_achievements (
    id bigint NOT NULL,
    employee_id bigint,
    achievement_id bigint
);


ALTER TABLE public.employees_achievements OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 24607)
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
-- TOC entry 3539 (class 0 OID 0)
-- Dependencies: 228
-- Name: employees_achievements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_achievements_id_seq OWNED BY public.employees_achievements.id;


--
-- TOC entry 229 (class 1259 OID 24608)
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
-- TOC entry 3540 (class 0 OID 0)
-- Dependencies: 229
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- TOC entry 230 (class 1259 OID 24609)
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
-- TOC entry 231 (class 1259 OID 24614)
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
-- TOC entry 3541 (class 0 OID 0)
-- Dependencies: 231
-- Name: employees_projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_projects_id_seq OWNED BY public.employees_projects.id;


--
-- TOC entry 239 (class 1259 OID 24672)
-- Name: grades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.grades (
    id bigint NOT NULL,
    grade bigint,
    "position" character varying,
    grade_name character varying NOT NULL
);


ALTER TABLE public.grades OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 24671)
-- Name: grades_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.grades_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.grades_id_seq OWNER TO postgres;

--
-- TOC entry 3542 (class 0 OID 0)
-- Dependencies: 238
-- Name: grades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.grades_id_seq OWNED BY public.grades.id;


--
-- TOC entry 232 (class 1259 OID 24615)
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects (
    id bigint NOT NULL,
    name character varying NOT NULL,
    description character varying
);


ALTER TABLE public.projects OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 24620)
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
-- TOC entry 3543 (class 0 OID 0)
-- Dependencies: 233
-- Name: projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_id_seq OWNED BY public.projects.id;


--
-- TOC entry 234 (class 1259 OID 24625)
-- Name: red_rating; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.red_rating (
    id bigint NOT NULL,
    reason character varying,
    delta bigint NOT NULL,
    employee_id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.red_rating OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 24631)
-- Name: red_rating_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.red_rating_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.red_rating_id_seq OWNER TO postgres;

--
-- TOC entry 3544 (class 0 OID 0)
-- Dependencies: 235
-- Name: red_rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.red_rating_id_seq OWNED BY public.red_rating.id;


--
-- TOC entry 217 (class 1259 OID 16396)
-- Name: responders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.responders (
    id integer NOT NULL,
    employee_id integer NOT NULL,
    survey_id integer NOT NULL,
    answers_json json NOT NULL,
    quality integer NOT NULL
);


ALTER TABLE public.responders OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16395)
-- Name: responders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.responders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.responders_id_seq OWNER TO postgres;

--
-- TOC entry 3545 (class 0 OID 0)
-- Dependencies: 216
-- Name: responders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.responders_id_seq OWNED BY public.responders.id;


--
-- TOC entry 236 (class 1259 OID 24632)
-- Name: shop_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shop_items (
    id bigint NOT NULL,
    name character varying NOT NULL,
    description character varying,
    price_red_coins bigint NOT NULL,
    image_path character varying,
    category character varying,
    is_available boolean
);


ALTER TABLE public.shop_items OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 24637)
-- Name: shop_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shop_items_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shop_items_id_seq OWNER TO postgres;

--
-- TOC entry 3546 (class 0 OID 0)
-- Dependencies: 237
-- Name: shop_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shop_items_id_seq OWNED BY public.shop_items.id;


--
-- TOC entry 215 (class 1259 OID 16386)
-- Name: surveys; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.surveys (
    id bigint NOT NULL,
    content_json json NOT NULL,
    module character varying NOT NULL
);


ALTER TABLE public.surveys OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 16385)
-- Name: surveys_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.surveys_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.surveys_id_seq OWNER TO postgres;

--
-- TOC entry 3547 (class 0 OID 0)
-- Dependencies: 214
-- Name: surveys_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.surveys_id_seq OWNED BY public.surveys.id;


--
-- TOC entry 3322 (class 2604 OID 24638)
-- Name: achievements id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.achievements ALTER COLUMN id SET DEFAULT nextval('public.achievements_id_seq'::regclass);


--
-- TOC entry 3323 (class 2604 OID 24639)
-- Name: blue_rating id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blue_rating ALTER COLUMN id SET DEFAULT nextval('public.blue_rating_id_seq'::regclass);


--
-- TOC entry 3324 (class 2604 OID 24640)
-- Name: courses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses ALTER COLUMN id SET DEFAULT nextval('public.courses_id_seq'::regclass);


--
-- TOC entry 3325 (class 2604 OID 24641)
-- Name: courses_employees id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses_employees ALTER COLUMN id SET DEFAULT nextval('public.courses_employees_id_seq'::regclass);


--
-- TOC entry 3326 (class 2604 OID 24642)
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- TOC entry 3327 (class 2604 OID 24643)
-- Name: employees_achievements id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees_achievements ALTER COLUMN id SET DEFAULT nextval('public.employees_achievements_id_seq'::regclass);


--
-- TOC entry 3328 (class 2604 OID 24644)
-- Name: employees_projects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees_projects ALTER COLUMN id SET DEFAULT nextval('public.employees_projects_id_seq'::regclass);


--
-- TOC entry 3333 (class 2604 OID 24675)
-- Name: grades id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades ALTER COLUMN id SET DEFAULT nextval('public.grades_id_seq'::regclass);


--
-- TOC entry 3329 (class 2604 OID 24645)
-- Name: projects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects ALTER COLUMN id SET DEFAULT nextval('public.projects_id_seq'::regclass);


--
-- TOC entry 3330 (class 2604 OID 24647)
-- Name: red_rating id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.red_rating ALTER COLUMN id SET DEFAULT nextval('public.red_rating_id_seq'::regclass);


--
-- TOC entry 3321 (class 2604 OID 16399)
-- Name: responders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.responders ALTER COLUMN id SET DEFAULT nextval('public.responders_id_seq'::regclass);


--
-- TOC entry 3332 (class 2604 OID 24648)
-- Name: shop_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_items ALTER COLUMN id SET DEFAULT nextval('public.shop_items_id_seq'::regclass);


--
-- TOC entry 3320 (class 2604 OID 16389)
-- Name: surveys id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveys ALTER COLUMN id SET DEFAULT nextval('public.surveys_id_seq'::regclass);


--
-- TOC entry 3508 (class 0 OID 24577)
-- Dependencies: 218
-- Data for Name: achievements; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.achievements VALUES (1, 'Best worker', '/images/best-employee.png', 'Award for best work');


--
-- TOC entry 3510 (class 0 OID 24583)
-- Dependencies: 220
-- Data for Name: blue_rating; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.blue_rating VALUES (2, 1, 25, 'тличная работа', NULL);
INSERT INTO public.blue_rating VALUES (3, 1, 25, 'тличная работа', '2025-09-20 23:50:27.225678+00');
INSERT INTO public.blue_rating VALUES (4, 1, 50, 'авершил сложный проект', '2025-09-21 00:06:14.227851+00');


--
-- TOC entry 3512 (class 0 OID 24589)
-- Dependencies: 222
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.courses VALUES (1, 'Advanced Python description', 'Python Advanced', 2);


--
-- TOC entry 3513 (class 0 OID 24594)
-- Dependencies: 223
-- Data for Name: courses_employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.courses_employees VALUES (1, 1, 1, '2025-09-20 17:26:57.967585+00', '2025-09-20 17:30:18.497413+00');


--
-- TOC entry 3516 (class 0 OID 24599)
-- Dependencies: 226
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.employees VALUES (4, 'овый Сотрудник', '2024-01-20 09:00:00+00', 'жуниор', NULL, NULL, NULL, NULL);
INSERT INTO public.employees VALUES (2, 'Egor Kor', '2023-09-15 10:00:00+00', 'DeveloperBackend', 1100, NULL, NULL, NULL);
INSERT INTO public.employees VALUES (1, 'John Doe Updated', '2023-01-15 10:00:00+00', 'Lead Developer', 750, NULL, '2025-09-21 09:31:01.062391+00', NULL);


--
-- TOC entry 3517 (class 0 OID 24604)
-- Dependencies: 227
-- Data for Name: employees_achievements; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.employees_achievements VALUES (1, 1, 1);
INSERT INTO public.employees_achievements VALUES (2, 2, 1);


--
-- TOC entry 3520 (class 0 OID 24609)
-- Dependencies: 230
-- Data for Name: employees_projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.employees_projects VALUES (1, 2, 1, '2024-01-01 09:00:00+00', '2024-06-30 18:00:00+00', 'Project Manager');
INSERT INTO public.employees_projects VALUES (2, 1, 1, '2024-01-15 09:00:00+00', NULL, 'налитик');
INSERT INTO public.employees_projects VALUES (3, 1, 3, '2024-01-15 09:00:00+00', NULL, 'Tester Project History');


--
-- TOC entry 3529 (class 0 OID 24672)
-- Dependencies: 239
-- Data for Name: grades; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.grades VALUES (1, 1, 'Developer', 'Junior Developer');


--
-- TOC entry 3522 (class 0 OID 24615)
-- Dependencies: 232
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.projects VALUES (1, 'еб-сайт Updated', 'бновленный корпоративный сайт');
INSERT INTO public.projects VALUES (3, 'Тестовый проект', 'ля теста');


--
-- TOC entry 3524 (class 0 OID 24625)
-- Dependencies: 234
-- Data for Name: red_rating; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3507 (class 0 OID 16396)
-- Dependencies: 217
-- Data for Name: responders; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3526 (class 0 OID 24632)
-- Dependencies: 236
-- Data for Name: shop_items; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3505 (class 0 OID 16386)
-- Dependencies: 215
-- Data for Name: surveys; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3548 (class 0 OID 0)
-- Dependencies: 219
-- Name: achievements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.achievements_id_seq', 1, true);


--
-- TOC entry 3549 (class 0 OID 0)
-- Dependencies: 221
-- Name: blue_rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.blue_rating_id_seq', 4, true);


--
-- TOC entry 3550 (class 0 OID 0)
-- Dependencies: 224
-- Name: courses_employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.courses_employees_id_seq', 1, true);


--
-- TOC entry 3551 (class 0 OID 0)
-- Dependencies: 225
-- Name: courses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.courses_id_seq', 2, true);


--
-- TOC entry 3552 (class 0 OID 0)
-- Dependencies: 228
-- Name: employees_achievements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_achievements_id_seq', 2, true);


--
-- TOC entry 3553 (class 0 OID 0)
-- Dependencies: 229
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_id_seq', 4, true);


--
-- TOC entry 3554 (class 0 OID 0)
-- Dependencies: 231
-- Name: employees_projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_projects_id_seq', 3, true);


--
-- TOC entry 3555 (class 0 OID 0)
-- Dependencies: 238
-- Name: grades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.grades_id_seq', 1, true);


--
-- TOC entry 3556 (class 0 OID 0)
-- Dependencies: 233
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_id_seq', 3, true);


--
-- TOC entry 3557 (class 0 OID 0)
-- Dependencies: 235
-- Name: red_rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.red_rating_id_seq', 1, false);


--
-- TOC entry 3558 (class 0 OID 0)
-- Dependencies: 216
-- Name: responders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.responders_id_seq', 1, false);


--
-- TOC entry 3559 (class 0 OID 0)
-- Dependencies: 237
-- Name: shop_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.shop_items_id_seq', 1, false);


--
-- TOC entry 3560 (class 0 OID 0)
-- Dependencies: 214
-- Name: surveys_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.surveys_id_seq', 1, false);


--
-- TOC entry 3341 (class 2606 OID 24650)
-- Name: achievements achievements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.achievements
    ADD CONSTRAINT achievements_pkey PRIMARY KEY (id);


--
-- TOC entry 3357 (class 2606 OID 24652)
-- Name: red_rating blue_rating_pk_1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.red_rating
    ADD CONSTRAINT blue_rating_pk_1 PRIMARY KEY (id);


--
-- TOC entry 3343 (class 2606 OID 24654)
-- Name: blue_rating blue_rating_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blue_rating
    ADD CONSTRAINT blue_rating_pkey PRIMARY KEY (id);


--
-- TOC entry 3347 (class 2606 OID 24656)
-- Name: courses_employees courses_employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses_employees
    ADD CONSTRAINT courses_employees_pkey PRIMARY KEY (id);


--
-- TOC entry 3345 (class 2606 OID 24658)
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (id);


--
-- TOC entry 3351 (class 2606 OID 24660)
-- Name: employees_achievements employees_achievements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees_achievements
    ADD CONSTRAINT employees_achievements_pkey PRIMARY KEY (id);


--
-- TOC entry 3349 (class 2606 OID 24662)
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- TOC entry 3353 (class 2606 OID 24664)
-- Name: employees_projects employees_projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees_projects
    ADD CONSTRAINT employees_projects_pkey PRIMARY KEY (id);


--
-- TOC entry 3361 (class 2606 OID 24679)
-- Name: grades grades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades
    ADD CONSTRAINT grades_pkey PRIMARY KEY (id);


--
-- TOC entry 3355 (class 2606 OID 24666)
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- TOC entry 3339 (class 2606 OID 16403)
-- Name: responders responders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.responders
    ADD CONSTRAINT responders_pkey PRIMARY KEY (id);


--
-- TOC entry 3359 (class 2606 OID 24670)
-- Name: shop_items shop_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_items
    ADD CONSTRAINT shop_items_pkey PRIMARY KEY (id);


--
-- TOC entry 3336 (class 2606 OID 16393)
-- Name: surveys surveys_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveys
    ADD CONSTRAINT surveys_pkey PRIMARY KEY (id);


--
-- TOC entry 3337 (class 1259 OID 16404)
-- Name: ix_responders_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_responders_id ON public.responders USING btree (id);


--
-- TOC entry 3334 (class 1259 OID 16394)
-- Name: ix_surveys_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_surveys_id ON public.surveys USING btree (id);


-- Completed on 2025-09-21 09:35:49 UTC

--
-- PostgreSQL database dump complete
--

