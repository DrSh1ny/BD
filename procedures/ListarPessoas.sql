CREATE OR REPLACE FUNCTION listUsers() 
    RETURNS TABLE (
        id Pessoa.id%type,
        nome Pessoa.nome%type,
		email Pessoa.email%type
) 
LANGUAGE plpgsql
AS $BODY$
declare
begin
	return query select 
	pessoa.id,pessoa.nome,pessoa.email 
	from Pessoa;
end;
$BODY$;