CREATE OR REPLACE PROCEDURE public.loginUser(
    <p_nome pessoa.nome%type>,
    <p_password pessoa.nome%type>,
)

LANGUAGE 'plpgsql'
AS $BODY$
declare
    v_id pessoa.id%type;
    v_auth_token pessoa.authtoken%type;
    v_exp_date pessoa.timestamp%type;

    c1 cursor for select nome, password from pessoa where nome = p_nome and password = p_password;

    begin

    open c1;
    loop
        fetch c1 into v_id, v_exp_date;
	    exit when not found;

        -- AuthToken and stuff like that

        --Return AuthToken
    end loop;
    close c1;

    --Return Error
end;   

$BODY$;