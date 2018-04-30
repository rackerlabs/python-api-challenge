-- Create todo table
CREATE TABLE public.todo (
	id serial NOT NULL,
	title varchar NULL,
	status varchar NULL,
	CONSTRAINT todo_pk PRIMARY KEY (id)
)
WITH (
	OIDS=FALSE
);

CREATE SEQUENCE IF NOT EXISTS public.todo_id_seq
NO MINVALUE
NO MAXVALUE;
