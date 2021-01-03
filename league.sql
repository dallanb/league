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

ALTER TABLE ONLY public.member DROP CONSTRAINT member_league_uuid_fkey;
ALTER TABLE ONLY public.league DROP CONSTRAINT league_status_fkey;
ALTER TABLE ONLY public.league DROP CONSTRAINT league_avatar_uuid_fkey;
DROP TRIGGER league_search_vector_trigger ON public.league;
DROP INDEX public.ix_league_search_vector;
ALTER TABLE ONLY public.member DROP CONSTRAINT member_pkey;
ALTER TABLE ONLY public.league_status DROP CONSTRAINT league_status_pkey;
ALTER TABLE ONLY public.league DROP CONSTRAINT league_pkey;
ALTER TABLE ONLY public.avatar DROP CONSTRAINT avatar_pkey;
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
    user_uuid uuid NOT NULL,
    league_uuid uuid NOT NULL
);


ALTER TABLE public.member OWNER TO league;

--
-- Data for Name: avatar; Type: TABLE DATA; Schema: public; Owner: league
--

COPY public.avatar (uuid, ctime, mtime, s3_filename) FROM stdin;
55d3e2d9-ed57-4aa6-a8bc-0374c1391989	1609642309540	\N	a0c8dd0e-2119-48c0-8527-cffa36385241.jpeg
1df34ca9-dfcf-43c6-9b7e-47fb3ca10c2d	1609702292439	\N	19dec7a8-52c0-4f48-8ed3-ce478d052d11.jpeg
\.


--
-- Data for Name: league; Type: TABLE DATA; Schema: public; Owner: league
--

COPY public.league (uuid, ctime, mtime, owner_uuid, name, search_vector, status, avatar_uuid) FROM stdin;
a0c8dd0e-2119-48c0-8527-cffa36385241	1609642307303	1609642309568	4519d094-2235-48d9-be8c-e73e453c76f0	Duke Golf Club	'club':3 'duke':1 'golf':2	active	55d3e2d9-ed57-4aa6-a8bc-0374c1391989
19dec7a8-52c0-4f48-8ed3-ce478d052d11	1609702289588	1609702292521	4519d094-2235-48d9-be8c-e73e453c76f0	Galactic Golf Club	'club':3 'galact':1 'golf':2	active	1df34ca9-dfcf-43c6-9b7e-47fb3ca10c2d
\.


--
-- Data for Name: league_status; Type: TABLE DATA; Schema: public; Owner: league
--

COPY public.league_status (ctime, mtime, name) FROM stdin;
1609642194473	\N	active
1609642194473	\N	inactive
\.


--
-- Data for Name: member; Type: TABLE DATA; Schema: public; Owner: league
--

COPY public.member (uuid, ctime, mtime, user_uuid, league_uuid) FROM stdin;
167b0075-bb55-459f-9655-f474e680e229	1609642307590	\N	4519d094-2235-48d9-be8c-e73e453c76f0	a0c8dd0e-2119-48c0-8527-cffa36385241
12ae8bf2-0340-482c-84fa-42f2dda67c4c	1609701454485	\N	ea903223-00a7-479e-8604-e29c722e7595	a0c8dd0e-2119-48c0-8527-cffa36385241
6020f282-432c-4fc1-bdcf-c85105dce89a	1609702289815	\N	4519d094-2235-48d9-be8c-e73e453c76f0	19dec7a8-52c0-4f48-8ed3-ce478d052d11
60293042-ee0b-4500-afb0-ce2b34209b82	1609702319356	\N	ea903223-00a7-479e-8604-e29c722e7595	19dec7a8-52c0-4f48-8ed3-ce478d052d11
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
-- Name: member member_pkey; Type: CONSTRAINT; Schema: public; Owner: league
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT member_pkey PRIMARY KEY (uuid);


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
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: league
--

GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

