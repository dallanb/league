--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.20
-- Dumped by pg_dump version 9.6.20

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

ALTER TABLE ONLY public.member DROP CONSTRAINT member_status_fkey;
ALTER TABLE ONLY public.member DROP CONSTRAINT member_league_uuid_fkey;
ALTER TABLE ONLY public.league DROP CONSTRAINT league_status_fkey;
ALTER TABLE ONLY public.league DROP CONSTRAINT league_avatar_uuid_fkey;
DROP TRIGGER league_search_vector_trigger ON public.league;
DROP INDEX public.ix_league_search_vector;
ALTER TABLE ONLY public.member_status DROP CONSTRAINT member_status_pkey;
ALTER TABLE ONLY public.member DROP CONSTRAINT member_pkey;
ALTER TABLE ONLY public.member_materialized DROP CONSTRAINT member_materialized_pkey;
ALTER TABLE ONLY public.league_status DROP CONSTRAINT league_status_pkey;
ALTER TABLE ONLY public.league DROP CONSTRAINT league_pkey;
ALTER TABLE ONLY public.avatar DROP CONSTRAINT avatar_pkey;
DROP TABLE public.member_status;
DROP TABLE public.member_materialized;
DROP TABLE public.member;
DROP TABLE public.league_status;
DROP TABLE public.league;
DROP TABLE public.avatar;
DROP FUNCTION public.tsq_tokenize_character(state public.tsq_state);
DROP FUNCTION public.tsq_tokenize(search_query text);
DROP FUNCTION public.tsq_process_tokens(config regconfig, tokens text[]);
DROP FUNCTION public.tsq_process_tokens(tokens text[]);
DROP FUNCTION public.tsq_parse(config text, search_query text);
DROP FUNCTION public.tsq_parse(config regconfig, search_query text);
DROP FUNCTION public.tsq_parse(search_query text);
DROP FUNCTION public.tsq_append_current_token(state public.tsq_state);
DROP FUNCTION public.array_nremove(anyarray, anyelement, integer);
DROP TYPE public.tsq_state;
DROP TYPE public.memberstatusenum;
DROP TYPE public.leaguestatusenum;
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: league
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO league;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: league
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: leaguestatusenum; Type: TYPE; Schema: public; Owner: league
--

CREATE TYPE public.leaguestatusenum AS ENUM (
    'active',
    'inactive'
);


ALTER TYPE public.leaguestatusenum OWNER TO league;

--
-- Name: memberstatusenum; Type: TYPE; Schema: public; Owner: league
--

CREATE TYPE public.memberstatusenum AS ENUM (
    'invited',
    'pending',
    'active',
    'inactive'
);


ALTER TYPE public.memberstatusenum OWNER TO league;

--
-- Name: tsq_state; Type: TYPE; Schema: public; Owner: league
--

CREATE TYPE public.tsq_state AS (
	search_query text,
	parentheses_stack integer,
	skip_for integer,
	current_token text,
	current_index integer,
	current_char text,
	previous_char text,
	tokens text[]
);


ALTER TYPE public.tsq_state OWNER TO league;

--
-- Name: array_nremove(anyarray, anyelement, integer); Type: FUNCTION; Schema: public; Owner: league
--

CREATE FUNCTION public.array_nremove(anyarray, anyelement, integer) RETURNS anyarray
    LANGUAGE sql IMMUTABLE
    AS $_$
    WITH replaced_positions AS (
        SELECT UNNEST(
            CASE
            WHEN $2 IS NULL THEN
                '{}'::int[]
            WHEN $3 > 0 THEN
                (array_positions($1, $2))[1:$3]
            WHEN $3 < 0 THEN
                (array_positions($1, $2))[
                    (cardinality(array_positions($1, $2)) + $3 + 1):
                ]
            ELSE
                '{}'::int[]
            END
        ) AS position
    )
    SELECT COALESCE((
        SELECT array_agg(value)
        FROM unnest($1) WITH ORDINALITY AS t(value, index)
        WHERE index NOT IN (SELECT position FROM replaced_positions)
    ), $1[1:0]);
$_$;


ALTER FUNCTION public.array_nremove(anyarray, anyelement, integer) OWNER TO league;

--
-- Name: tsq_append_current_token(public.tsq_state); Type: FUNCTION; Schema: public; Owner: league
--

CREATE FUNCTION public.tsq_append_current_token(state public.tsq_state) RETURNS public.tsq_state
    LANGUAGE plpgsql IMMUTABLE
    AS $$
BEGIN
    IF state.current_token != '' THEN
        state.tokens := array_append(state.tokens, state.current_token);
        state.current_token := '';
    END IF;
    RETURN state;
END;
$$;


ALTER FUNCTION public.tsq_append_current_token(state public.tsq_state) OWNER TO league;

--
-- Name: tsq_parse(text); Type: FUNCTION; Schema: public; Owner: league
--

CREATE FUNCTION public.tsq_parse(search_query text) RETURNS tsquery
    LANGUAGE sql IMMUTABLE
    AS $$
    SELECT tsq_parse(get_current_ts_config(), search_query);
$$;


ALTER FUNCTION public.tsq_parse(search_query text) OWNER TO league;

--
-- Name: tsq_parse(regconfig, text); Type: FUNCTION; Schema: public; Owner: league
--

CREATE FUNCTION public.tsq_parse(config regconfig, search_query text) RETURNS tsquery
    LANGUAGE sql IMMUTABLE
    AS $$
    SELECT tsq_process_tokens(config, tsq_tokenize(search_query));
$$;


ALTER FUNCTION public.tsq_parse(config regconfig, search_query text) OWNER TO league;

--
-- Name: tsq_parse(text, text); Type: FUNCTION; Schema: public; Owner: league
--

CREATE FUNCTION public.tsq_parse(config text, search_query text) RETURNS tsquery
    LANGUAGE sql IMMUTABLE
    AS $$
    SELECT tsq_parse(config::regconfig, search_query);
$$;


ALTER FUNCTION public.tsq_parse(config text, search_query text) OWNER TO league;

--
-- Name: tsq_process_tokens(text[]); Type: FUNCTION; Schema: public; Owner: league
--

CREATE FUNCTION public.tsq_process_tokens(tokens text[]) RETURNS tsquery
    LANGUAGE sql IMMUTABLE
    AS $$
    SELECT tsq_process_tokens(get_current_ts_config(), tokens);
$$;


ALTER FUNCTION public.tsq_process_tokens(tokens text[]) OWNER TO league;

--
-- Name: tsq_process_tokens(regconfig, text[]); Type: FUNCTION; Schema: public; Owner: league
--

CREATE FUNCTION public.tsq_process_tokens(config regconfig, tokens text[]) RETURNS tsquery
    LANGUAGE plpgsql IMMUTABLE
    AS $$
DECLARE
    result_query text;
    previous_value text;
    value text;
BEGIN
    result_query := '';

    FOREACH value IN ARRAY tokens LOOP
        IF value = '"' THEN
            CONTINUE;
        END IF;

        IF value = 'or' THEN
            value := ' | ';
        END IF;

        IF left(value, 1) = '"' AND right(value, 1) = '"' THEN
            value := phraseto_tsquery(config, value);
        ELSIF value NOT IN ('(', ' | ', ')', '-') THEN
            value := quote_literal(value) || ':*';
        END IF;

        IF previous_value = '-' THEN
            IF value = '(' THEN
                value := '!' || value;
            ELSIF value = ' | ' THEN
                CONTINUE;
            ELSE
                value := '!(' || value || ')';
            END IF;
        END IF;

        SELECT
            CASE
                WHEN result_query = '' THEN value
                WHEN previous_value = ' | ' AND value = ' | ' THEN result_query
                WHEN previous_value = ' | ' THEN result_query || ' | ' || value
                WHEN previous_value IN ('!(', '(') OR value = ')' THEN result_query || value
                WHEN value != ' | ' THEN result_query || ' & ' || value
                ELSE result_query
            END
        INTO result_query;

        IF result_query = ' | ' THEN
            result_query := '';
        END IF;

        previous_value := value;
    END LOOP;

    RETURN to_tsquery(config, result_query);
END;
$$;


ALTER FUNCTION public.tsq_process_tokens(config regconfig, tokens text[]) OWNER TO league;

--
-- Name: tsq_tokenize(text); Type: FUNCTION; Schema: public; Owner: league
--

CREATE FUNCTION public.tsq_tokenize(search_query text) RETURNS text[]
    LANGUAGE plpgsql IMMUTABLE
    AS $$
DECLARE
    state tsq_state;
BEGIN
    SELECT
        search_query::text AS search_query,
        0::int AS parentheses_stack,
        0 AS skip_for,
        ''::text AS current_token,
        0 AS current_index,
        ''::text AS current_char,
        ''::text AS previous_char,
        '{}'::text[] AS tokens
    INTO state;

    state.search_query := lower(trim(
        regexp_replace(search_query, '""+', '""', 'g')
    ));

    FOR state.current_index IN (
        SELECT generate_series(1, length(state.search_query))
    ) LOOP
        state.current_char := substring(
            search_query FROM state.current_index FOR 1
        );

        IF state.skip_for > 0 THEN
            state.skip_for := state.skip_for - 1;
            CONTINUE;
        END IF;

        state := tsq_tokenize_character(state);
        state.previous_char := state.current_char;
    END LOOP;
    state := tsq_append_current_token(state);

    state.tokens := array_nremove(state.tokens, '(', -state.parentheses_stack);

    RETURN state.tokens;
END;
$$;


ALTER FUNCTION public.tsq_tokenize(search_query text) OWNER TO league;

--
-- Name: tsq_tokenize_character(public.tsq_state); Type: FUNCTION; Schema: public; Owner: league
--

CREATE FUNCTION public.tsq_tokenize_character(state public.tsq_state) RETURNS public.tsq_state
    LANGUAGE plpgsql IMMUTABLE
    AS $$
BEGIN
    IF state.current_char = '(' THEN
        state.tokens := array_append(state.tokens, '(');
        state.parentheses_stack := state.parentheses_stack + 1;
        state := tsq_append_current_token(state);
    ELSIF state.current_char = ')' THEN
        IF (state.parentheses_stack > 0 AND state.current_token != '') THEN
            state := tsq_append_current_token(state);
            state.tokens := array_append(state.tokens, ')');
            state.parentheses_stack := state.parentheses_stack - 1;
        END IF;
    ELSIF state.current_char = '"' THEN
        state.skip_for := position('"' IN substring(
            state.search_query FROM state.current_index + 1
        ));

        IF state.skip_for > 1 THEN
            state.tokens = array_append(
                state.tokens,
                substring(
                    state.search_query
                    FROM state.current_index FOR state.skip_for + 1
                )
            );
        ELSIF state.skip_for = 0 THEN
            state.current_token := state.current_token || state.current_char;
        END IF;
    ELSIF (
        state.current_char = '-' AND
        (state.current_index = 1 OR state.previous_char = ' ')
    ) THEN
        state.tokens := array_append(state.tokens, '-');
    ELSIF state.current_char = ' ' THEN
        state := tsq_append_current_token(state);
    ELSE
        state.current_token = state.current_token || state.current_char;
    END IF;
    RETURN state;
END;
$$;


ALTER FUNCTION public.tsq_tokenize_character(state public.tsq_state) OWNER TO league;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: avatar; Type: TABLE; Schema: public; Owner: league
--

CREATE TABLE public.avatar (
    uuid uuid NOT NULL,
    ctime bigint,
    mtime bigint,
    s3_filename character varying NOT NULL
);


ALTER TABLE public.avatar OWNER TO league;

--
-- Name: league; Type: TABLE; Schema: public; Owner: league
--

CREATE TABLE public.league (
    uuid uuid NOT NULL,
    ctime bigint,
    mtime bigint,
    owner_uuid uuid NOT NULL,
    name character varying NOT NULL,
    search_vector tsvector,
    status public.leaguestatusenum NOT NULL,
    avatar_uuid uuid
);


ALTER TABLE public.league OWNER TO league;

--
-- Name: league_status; Type: TABLE; Schema: public; Owner: league
--

CREATE TABLE public.league_status (
    ctime bigint,
    mtime bigint,
    name public.leaguestatusenum NOT NULL
);


ALTER TABLE public.league_status OWNER TO league;

--
-- Name: member; Type: TABLE; Schema: public; Owner: league
--

CREATE TABLE public.member (
    uuid uuid NOT NULL,
    ctime bigint,
    mtime bigint,
    email character varying(255) NOT NULL,
    user_uuid uuid,
    status public.memberstatusenum NOT NULL,
    league_uuid uuid NOT NULL
);


ALTER TABLE public.member OWNER TO league;

--
-- Name: member_materialized; Type: TABLE; Schema: public; Owner: league
--

CREATE TABLE public.member_materialized (
    uuid uuid NOT NULL,
    ctime bigint,
    mtime bigint,
    display_name character varying,
    email character varying(255) NOT NULL,
    "user" uuid,
    member uuid,
    status character varying NOT NULL,
    league uuid NOT NULL,
    country character varying
);


ALTER TABLE public.member_materialized OWNER TO league;

--
-- Name: member_status; Type: TABLE; Schema: public; Owner: league
--

CREATE TABLE public.member_status (
    ctime bigint,
    mtime bigint,
    name public.memberstatusenum NOT NULL
);


ALTER TABLE public.member_status OWNER TO league;

--
-- Data for Name: avatar; Type: TABLE DATA; Schema: public; Owner: league
--

COPY public.avatar (uuid, ctime, mtime, s3_filename) FROM stdin;
a959ab24-eef8-4717-95f8-75c763183f71	1611448263690	\N	0d40ca41-7b62-4bb8-ac76-a9b53da85f0e.jpeg
\.


--
-- Data for Name: league; Type: TABLE DATA; Schema: public; Owner: league
--

COPY public.league (uuid, ctime, mtime, owner_uuid, name, search_vector, status, avatar_uuid) FROM stdin;
0d40ca41-7b62-4bb8-ac76-a9b53da85f0e	1611448262520	1611448263754	4f003f91-20f3-459f-b4de-e17a05d837b8	Duke Golf Club	'club':3 'duke':1 'golf':2	active	a959ab24-eef8-4717-95f8-75c763183f71
\.


--
-- Data for Name: league_status; Type: TABLE DATA; Schema: public; Owner: league
--

COPY public.league_status (ctime, mtime, name) FROM stdin;
1611448129440	\N	active
1611448129440	\N	inactive
\.


--
-- Data for Name: member; Type: TABLE DATA; Schema: public; Owner: league
--

COPY public.member (uuid, ctime, mtime, email, user_uuid, status, league_uuid) FROM stdin;
e82501b9-cfaa-4091-bc1f-653ed1d8cfe8	1611448262607	\N	dallan.bhatti@techtapir.com	4f003f91-20f3-459f-b4de-e17a05d837b8	active	0d40ca41-7b62-4bb8-ac76-a9b53da85f0e
\.


--
-- Data for Name: member_materialized; Type: TABLE DATA; Schema: public; Owner: league
--

COPY public.member_materialized (uuid, ctime, mtime, display_name, email, "user", member, status, league, country) FROM stdin;
e82501b9-cfaa-4091-bc1f-653ed1d8cfe8	1611448262630	\N	Dallan Bhatti	dallan.bhatti@techtapir.com	4f003f91-20f3-459f-b4de-e17a05d837b8	68bb0f90-044c-4636-bccd-e895da313a9c	active	0d40ca41-7b62-4bb8-ac76-a9b53da85f0e	CA
\.


--
-- Data for Name: member_status; Type: TABLE DATA; Schema: public; Owner: league
--

COPY public.member_status (ctime, mtime, name) FROM stdin;
1611448129455	\N	invited
1611448129455	\N	pending
1611448129455	\N	active
1611448129455	\N	inactive
\.


--
-- Name: avatar avatar_pkey; Type: CONSTRAINT; Schema: public; Owner: league
--

ALTER TABLE ONLY public.avatar
    ADD CONSTRAINT avatar_pkey PRIMARY KEY (uuid);


--
-- Name: league league_pkey; Type: CONSTRAINT; Schema: public; Owner: league
--

ALTER TABLE ONLY public.league
    ADD CONSTRAINT league_pkey PRIMARY KEY (uuid);


--
-- Name: league_status league_status_pkey; Type: CONSTRAINT; Schema: public; Owner: league
--

ALTER TABLE ONLY public.league_status
    ADD CONSTRAINT league_status_pkey PRIMARY KEY (name);


--
-- Name: member_materialized member_materialized_pkey; Type: CONSTRAINT; Schema: public; Owner: league
--

ALTER TABLE ONLY public.member_materialized
    ADD CONSTRAINT member_materialized_pkey PRIMARY KEY (uuid);


--
-- Name: member member_pkey; Type: CONSTRAINT; Schema: public; Owner: league
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT member_pkey PRIMARY KEY (uuid);


--
-- Name: member_status member_status_pkey; Type: CONSTRAINT; Schema: public; Owner: league
--

ALTER TABLE ONLY public.member_status
    ADD CONSTRAINT member_status_pkey PRIMARY KEY (name);


--
-- Name: ix_league_search_vector; Type: INDEX; Schema: public; Owner: league
--

CREATE INDEX ix_league_search_vector ON public.league USING gin (search_vector);


--
-- Name: league league_search_vector_trigger; Type: TRIGGER; Schema: public; Owner: league
--

CREATE TRIGGER league_search_vector_trigger BEFORE INSERT OR UPDATE ON public.league FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger('search_vector', 'pg_catalog.english', 'name');


--
-- Name: league league_avatar_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: league
--

ALTER TABLE ONLY public.league
    ADD CONSTRAINT league_avatar_uuid_fkey FOREIGN KEY (avatar_uuid) REFERENCES public.avatar(uuid);


--
-- Name: league league_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: league
--

ALTER TABLE ONLY public.league
    ADD CONSTRAINT league_status_fkey FOREIGN KEY (status) REFERENCES public.league_status(name);


--
-- Name: member member_league_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: league
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT member_league_uuid_fkey FOREIGN KEY (league_uuid) REFERENCES public.league(uuid);


--
-- Name: member member_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: league
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT member_status_fkey FOREIGN KEY (status) REFERENCES public.member_status(name);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: league
--

GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

