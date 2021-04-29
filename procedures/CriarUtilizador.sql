CREATE OR REPLACE PROCEDURE public.registerUser(
    <p_nome pessoa.nome%type>,
    <p_email pessoa.email%type>
    <p_password pessoa.nome%type>,
)

LANGUAGE 'plpgsql'
AS $BODY$
declare
    v_auth_token pessoa.authtoken%type;
    v_exp_date pessoa.timestamp%type;
begin
	-- AuthToken and stuff like that

    -- Insert
	insert into pessoa(nome, email, password, authtoken, timestamp) values (p_nome, p_email, p_password, v_auth_token, v_exp_date);


    --ReturnUserId
end;

$BODY$;