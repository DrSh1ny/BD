CREATE OR REPLACE FUNCTION loginUser(p_nome pessoa.nome%type,p_password pessoa.nome%type) returns Pessoa.auth_token%type
LANGUAGE 'plpgsql'
AS $BODY$
declare
	c1 cursor(p_nome pessoa.nome%type,p_password pessoa.nome%type) for
		select *
		from pessoa
		where nome=p_nome and password=p_password
		for update;
	resPessoa pessoa%rowtype;
	authToken pessoa.auth_token%type;
	expiration pessoa.exp_date%type;
	aux varchar;
begin
	--check if email already exists
	if(p_nome='' or p_password='') then
		return -2;
	end if;

	open c1(p_nome,p_password);
	fetch c1 into resPessoa;

	if(found) then
		select substr(md5(random()::text), 0, 50) into aux;
		update pessoa
		set auth_token=aux, exp_date=current_timestamp + (60 * interval '1 minute')
		where current of c1;
		return aux;
	else
		return -1;
	end if;
end;   
$BODY$;