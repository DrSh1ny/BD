create or replace function listUsers ()
	returns table (
		id Pessoa.id%type,
		nome Pessoa.nome%type,
		email Pessoa.email%type
	) 
	language plpgsql
as $$
begin
	return query 
		select
			pessoa.id,pessoa.nome,pessoa.email
		from
			pessoa;
end;
$$